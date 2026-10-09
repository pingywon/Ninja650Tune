import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('pcv', ROOT / 'tools' / 'pcv.py')
pcv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pcv)
BASE = ROOT / 'maps/baselines/STOCK_NO_AUTOTUNE.pvm'
SO = ROOT / 'maps/smooth-operator/SO_v1.0_KNOWN_GOOD.pvm'


class RecoveredEvidenceTests(unittest.TestCase):
    def test_complete_so_table_agrees_with_original_source_csv(self):
        source = ROOT / 'archive/so-v1.0.0-corrected/SmoothOP_v1.0.0_full_fuel_table.csv'
        with source.open(newline='', encoding='utf-8') as handle:
            rows = list(csv.reader(handle))[1:]
        expected = [int(value) for row in rows for value in row[1:]]
        self.assertEqual(len(expected), 440)
        self.assertEqual(pcv.read_pvm(SO)['fuel'], expected)
        original = ROOT / 'archive/so-v1.0.0-original/01_SmoothOP_v1.0.0_TEST.pvm'
        corrected = ROOT / 'archive/so-v1.0.0-corrected/01_SmoothOP_v1.0.0_TEST.pvm'
        self.assertEqual(pcv.read_pvm(original)['fuel'], expected)
        self.assertEqual(pcv.read_pvm(corrected)['fuel'], expected)

    def test_so_v13_exactly_25_positive_one_changes(self):
        diff = pcv.compare(SO, ROOT / 'maps/smooth-operator/SO_v1.3_TEST.pvm')
        self.assertEqual(diff['changed_fuel_cells'], 25)
        self.assertEqual({change['delta'] for change in diff['changes']}, {1})
        self.assertEqual(diff['nonfuel_tables_equal'], {'ignition': True})

    def test_rc_legacy_binary_agrees_with_all_40_source_rows(self):
        candidate = ROOT / 'archive/rice-crispy-legacy/RC_v1.0_40_CELL_SUPERSEDED.pvm'
        source = ROOT / 'archive/forked-package-documents/DOCUMENTATION/RC_v1.0_changes_from_SO_v1.0.csv'
        with source.open(newline='', encoding='utf-8') as handle:
            expected = {(int(row['rpm']), int(row['tps_percent']), int(row['delta'])) for row in csv.DictReader(handle)}
        diff = pcv.compare(SO, candidate)
        actual = {(row['rpm'], row['tps_percent'], row['delta']) for row in diff['changes']}
        self.assertEqual(len(expected), 40)
        self.assertEqual(actual, expected)

    def test_rc_aggressive_is_stock_based_not_so_based(self):
        candidate = ROOT / 'maps/rice-crispy/RC_v1.1_AGGRESSIVE_TEST_RECOVERED.pvm'
        diff = pcv.compare(BASE, candidate)
        self.assertEqual(diff['changed_fuel_cells'], 67)
        self.assertEqual({row['tps_percent'] for row in diff['changes']}, {0, 2, 5})
        self.assertEqual(min(row['rpm'] for row in diff['changes']), 2500)
        self.assertEqual(max(row['rpm'] for row in diff['changes']), 8250)
        self.assertEqual(diff['nonfuel_tables_equal'], {'ignition': True})
        self.assertEqual(pcv.compare(SO, candidate)['changed_fuel_cells'], 178)
        self.assertEqual(pcv.compare(BASE, SO)['changed_fuel_cells'], 111)

    def test_all_recorded_artifacts_verify(self):
        self.assertEqual(pcv.verify(ROOT)['result'], 'PASS')


class IntegrityTests(unittest.TestCase):
    def test_truncated_file_and_invalid_pointer_are_rejected(self):
        raw = BASE.read_bytes()
        with self.assertRaises(ValueError):
            pcv.read_pvm_bytes(raw[:100])
        malformed = bytearray(raw)
        struct.pack_into('<I', malformed, 0x44, 0x7fffffff)
        with self.assertRaises(ValueError):
            pcv.read_pvm_bytes(malformed)

    def test_manifest_detects_changed_file_and_unsafe_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'maps').mkdir()
            content = BASE.read_bytes()
            asset = root / 'maps/map.pvm'
            asset.write_bytes(content)
            manifest = {'artifacts': [dict(path='maps/map.pvm', bytes=len(content), sha256=hashlib.sha256(content).hexdigest())]}
            (root / 'manifest.json').write_text(json.dumps(manifest))
            pcv.verify(root)
            corrupted = bytearray(content)
            corrupted[0x200] += 1
            asset.write_bytes(corrupted)
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                pcv.verify(root)
            manifest['artifacts'][0]['path'] = '../escape.pvm'
            (root / 'manifest.json').write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'Unsafe relative path'):
                pcv.verify(root)

    def test_nested_zip_metadata_residue_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'archive').mkdir()
            raw = bytearray(BASE.read_bytes())
            raw[-1] = 65
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w') as archive:
                archive.writestr('map.pvm', raw)
            data = buffer.getvalue()
            (root / 'archive/bad.zip').write_bytes(data)
            manifest = {'artifacts': [dict(path='archive/bad.zip', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())]}
            (root / 'manifest.json').write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'notes-buffer residue in ZIP'):
                pcv.verify(root)

    def test_cumulative_build_reproducible_and_includes_all_versions(self):
        with tempfile.TemporaryDirectory() as temp:
            one, two = Path(temp) / 'one.zip', Path(temp) / 'two.zip'
            pcv.build(ROOT, one)
            pcv.build(ROOT, two)
            self.assertEqual(one.read_bytes(), two.read_bytes())
            manifest = json.loads((ROOT / 'manifest.json').read_text())
            with zipfile.ZipFile(one) as archive:
                for artifact in manifest['artifacts']:
                    self.assertEqual(archive.read(artifact['path']), (ROOT / artifact['path']).read_bytes())
                self.assertIn('PACKAGE_SHA256SUMS.txt', archive.namelist())
                self.assertFalse(any(name.startswith(('.git/', 'dist/')) for name in archive.namelist()))


if __name__ == '__main__':
    unittest.main()
