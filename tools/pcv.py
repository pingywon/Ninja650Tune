#!/usr/bin/env python3
"""Read-only auditing and reproducible packaging for this recovered PVM family.

No command edits a PVM or sends data to a controller. Python 3.10+, stdlib only.
The inferred layout is restricted to this repository's 44 x 10 map family.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import struct
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MAGIC = bytes.fromhex('02000000270200003000000000010000')
TPS = [0, 2, 5, 10, 15, 20, 40, 60, 80, 100]
RPM = list(range(250, 11001, 250))


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def confined(root, relative):
    part = PurePosixPath(relative)
    if part.is_absolute() or '..' in part.parts or '\\' in relative or ':' in relative:
        raise ValueError(f'Unsafe relative path: {relative}')
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes repository: {relative}')
    return path


def read_pvm(path):
    return read_pvm_bytes(Path(path).read_bytes())


def read_pvm_bytes(data):
    if data[:16] != MAGIC or len(data) < 0x38:
        raise ValueError('Unsupported PVM header; use Dynojet software for this file')
    notes = struct.unpack_from('<I', data, 0x10)[0]
    if notes + 256 != len(data):
        raise ValueError('Unsupported notes field layout')
    count = struct.unpack_from('<I', data, 0x30)[0]
    if count not in (4, 5) or 0x38 + 16 * count > notes:
        raise ValueError('Unsupported descriptor count')
    descriptors = {}
    for index in range(count):
        offset = 0x38 + 16 * index
        identifier = data[offset:offset+4].hex()
        pointers = tuple(v & 0x7fffffff for v in struct.unpack_from('<III', data, offset+4))
        if identifier in descriptors:
            raise ValueError('Duplicate table descriptor')
        descriptors[identifier] = pointers
    expected = {'c1403fd0', 'c1403fd1', 'c1413fd6', 'c1413fd7'}
    if set(descriptors) not in (expected, expected | {'c14a3f7c'}):
        raise ValueError('Unsupported table identifiers')
    if descriptors['c1403fd0'] != descriptors['c1403fd1'] or descriptors['c1413fd6'] != descriptors['c1413fd7']:
        raise ValueError('Separate cylinder tables are unsupported')
    tables = {}
    for name, identifier in [('fuel', 'c1403fd0'), ('ignition', 'c1413fd6'), ('target_afr', 'c14a3f7c')]:
        if identifier not in descriptors:
            continue
        tps_at, rpm_at, values_at = descriptors[identifier]
        for start, length in [(tps_at, 24), (rpm_at, 92), (values_at, 440)]:
            if start < 0x38 + 16 * count or start + length > notes:
                raise ValueError('Table pointer lies outside the supported data region')
        if data[tps_at:tps_at+4] != bytes.fromhex('0ac50000') or data[rpm_at:rpm_at+4] != bytes.fromhex('2c1c0000'):
            raise ValueError('Unsupported axis encoding')
        tps = [v / 10 for v in struct.unpack_from('<10H', data, tps_at+4)]
        rpm = list(struct.unpack_from('<44H', data, rpm_at+4))
        if tps != TPS or rpm != RPM:
            raise ValueError('Unsupported RPM/TPS axes; no guessed interpretation performed')
        tables[name] = data[values_at:values_at+440]
    # Fuel values in these files are stored as adjustment + 100, one byte per cell.
    fuel = [value - 100 for value in tables['fuel']]
    residue_start = data.find(b'\0', notes, notes+256)
    if residue_start < 0:
        raise ValueError('Unterminated notes field')
    return dict(data=data, tables=tables, fuel=fuel, notes_offset=notes,
                residue_clean=not any(data[residue_start+1:]), descriptors=descriptors)


def inspect_map(path):
    pvm = read_pvm(path)
    return dict(file=Path(path).name, bytes=len(pvm['data']), sha256=sha256(pvm['data']),
                rpm_rows=44, tps_columns=TPS, fuel_min=min(pvm['fuel']), fuel_max=max(pvm['fuel']),
                table_names=list(pvm['tables']), unused_notes_bytes_zero=pvm['residue_clean'],
                validation='binary inspection only; Dynojet software/device validation remains separate')


def compare(base, candidate):
    left, right = read_pvm(base), read_pvm(candidate)
    changes = []
    for index, (old, new) in enumerate(zip(left['fuel'], right['fuel'])):
        if old != new:
            changes.append(dict(rpm=RPM[index//10], tps_percent=TPS[index%10],
                                base_value=old, candidate_value=new, delta=new-old))
    other_tables = {name: left['tables'].get(name) == right['tables'].get(name)
                    for name in sorted((left['tables'].keys() | right['tables'].keys()) - {'fuel'})}
    return dict(base_sha256=sha256(left['data']), candidate_sha256=sha256(right['data']),
                changed_fuel_cells=len(changes), nonfuel_tables_equal=other_tables, changes=changes)


def verify(root):
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    errors, recorded = [], set()
    for artifact in manifest['artifacts']:
        relative = artifact['path']
        if relative in recorded:
            errors.append(f'Duplicate manifest path: {relative}')
        recorded.add(relative)
        try:
            path = confined(root, relative)
            data = path.read_bytes()
            if len(data) != artifact['bytes'] or sha256(data) != artifact['sha256']:
                errors.append(f'Size/checksum mismatch: {relative}')
            if path.suffix == '.pvm' and not read_pvm(path)['residue_clean']:
                errors.append(f'Uncleared notes-buffer residue: {relative}')
            if path.suffix == '.zip':
                with zipfile.ZipFile(io.BytesIO(data)) as archive:
                    if archive.testzip() is not None:
                        errors.append(f'ZIP CRC failure: {relative}')
                    for member in archive.infolist():
                        if not member.is_dir():
                            confined(root, member.filename)
                            if member.filename.endswith('.pvm') and not read_pvm_bytes(archive.read(member))['residue_clean']:
                                errors.append(f'Uncleared notes-buffer residue in ZIP: {relative}:{member.filename}')
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
            errors.append(f'{relative}: {exc}')
    for folder in ['maps', 'archive']:
        for path in (root / folder).rglob('*'):
            if path.is_file() and path.relative_to(root).as_posix() not in recorded:
                errors.append(f'Unrecorded artifact: {path.relative_to(root).as_posix()}')
    if errors:
        raise ValueError('\n'.join(errors))
    return dict(verified_artifacts=len(recorded), result='PASS',
                scope='published hashes, supported PVM structure, notes residue and archive integrity; not engine validation')


def package_files(root):
    return sorted(path for path in root.rglob('*') if path.is_file()
                  and not any(part in {'.git', '__pycache__', 'dist', '.pytest_cache'} for part in path.relative_to(root).parts)
                  and path.suffix not in {'.pyc', '.zip.tmp'})


def build(root, output):
    verify(root)
    files = package_files(root)
    if output.resolve().is_relative_to(root.resolve()) and output.parent != root / 'dist':
        raise ValueError('Build inside repository only under dist/, or choose an external destination')
    output.parent.mkdir(parents=True, exist_ok=True)
    sums = ''.join(f'{sha256(path.read_bytes())}  {path.relative_to(root).as_posix()}\n' for path in files)
    with zipfile.ZipFile(output, 'w') as archive:
        for path in files:
            member = zipfile.ZipInfo(path.relative_to(root).as_posix(), (2026,10,9,0,0,0))
            member.compress_type = zipfile.ZIP_DEFLATED
            member.external_attr = 0o100644 << 16
            archive.writestr(member, path.read_bytes())
        member = zipfile.ZipInfo('PACKAGE_SHA256SUMS.txt', (2026,10,9,0,0,0))
        member.compress_type = zipfile.ZIP_DEFLATED
        member.external_attr = 0o100644 << 16
        archive.writestr(member, sums)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError('Built ZIP failed CRC check')
        for path in files:
            if archive.read(path.relative_to(root).as_posix()) != path.read_bytes():
                raise ValueError('Built ZIP content mismatch')
    digest = sha256(output.read_bytes())
    output.with_suffix('.zip.sha256').write_text(f'{digest}  {output.name}\n', encoding='utf-8')
    return dict(file=str(output), files=len(files)+1, bytes=output.stat().st_size, sha256=digest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('verify', help='Verify repository assets against manifest.json')
    inspect = sub.add_parser('inspect', help='Inspect supported PVM tables without exposing notes')
    inspect.add_argument('file', type=Path)
    diff = sub.add_parser('diff', help='Compare decoded fuel cells and other table bytes')
    diff.add_argument('base', type=Path)
    diff.add_argument('candidate', type=Path)
    diff.add_argument('--csv', type=Path)
    package = sub.add_parser('build', help='Create cumulative reproducible ZIP containing all recovered versions')
    package.add_argument('--output', type=Path, default=ROOT / 'dist' / 'Ninja650Tune_Archive_2026-10-09.zip')
    args = parser.parse_args()
    try:
        if args.command == 'verify': result = verify(ROOT)
        elif args.command == 'inspect': result = inspect_map(args.file)
        elif args.command == 'build': result = build(ROOT, args.output)
        else:
            result = compare(args.base, args.candidate)
            if args.csv:
                args.csv.parent.mkdir(parents=True, exist_ok=True)
                with args.csv.open('w', newline='', encoding='utf-8') as output:
                    writer = csv.DictWriter(output, fieldnames=['rpm','tps_percent','base_value','candidate_value','delta'], lineterminator='\n')
                    writer.writeheader()
                    writer.writerows(result['changes'])
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, KeyError, struct.error) as exc:
        parser.exit(1, f'ERROR: {exc}\n')


if __name__ == '__main__':
    main()
