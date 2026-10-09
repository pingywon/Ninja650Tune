# Ninja650Tune

A preserved Power Commander V tuning project for a **2020 Kawasaki Ninja 650 KRT**: SmoothOperator for driveability experiments and RiceCrispy for historical deceleration-sound experiments. Includes recovered `.pvm` maps, original change records, device backups, a version history, and tools to inspect, compare, verify, and package the collection.

**Permanent project switch convention: OUT → Map 1 → SmoothOperator. IN → Map 2 → RiceCrispy.** Confirm both positions against the connected controller before applying these physical labels.

## Start here

1. Read the [map status and version history](docs/VERSIONS.md).
2. Check the [recorded motorcycle setup](#recorded-setup) against the actual bike.
3. Follow the [backup, review, and loading guide](docs/LOADING.md).
4. Identify the exact file by its hash in [manifest.json](manifest.json), and record checks in a [session log](templates/SESSION.md).

Download the cumulative archive from [Releases](https://github.com/pingywon/Ninja650Tune/releases). Each archive includes **every recovered version**, including superseded experiments. It is an archive of the project, not an instruction to load every file.

## Recovered maps

| Map | Status | Verified binary relationship |
| --- | --- | --- |
| [SO v1.0 Known Good](maps/smooth-operator/SO_v1.0_KNOWN_GOOD.pvm) | Owner-accepted historical rollback | 111 fuel cells differ from the project baseline |
| [SO v1.3 Test](maps/smooth-operator/SO_v1.3_TEST.pvm) | Experimental; latest recovered SO | Exactly 25 cells change by +1 versus SO v1.0 |
| [RC v1.1 Aggressive Test](maps/rice-crispy/RC_v1.1_AGGRESSIVE_TEST_RECOVERED.pvm) | Historical experiment; no accepted RC rollback | 67 cells differ from baseline, at 0/2/5% TPS |
| [Early RC v1.0](archive/rice-crispy-legacy/RC_v1.0_40_CELL_SUPERSEDED.pvm) | Superseded; retained for history | 40 changes from SO v1.0, at 0/2% TPS |
| [Baseline collection](maps/baselines) | Original project labels retained | Includes the no-AutoTune baseline and a PCV-retrieved reference |

The later project conversation **renamed the aggressive RC branch to RC v1.0**. That name also appears on the older, different 40-cell experiment. This repository keeps the recovered aggressive file's original **v1.1** label and explains the alias in the version history. Its 67-cell table matches the recorded design, but the exact later release binary has not been recovered.

The two August 15, 2026 cumulative ZIPs mentioned in the conversation remain missing. This collection does not claim to be either ZIP. Recovered SO files use the 1,648-byte no-AutoTune container; the missing PCV field kit was described as containing 1,828-byte files.

**Validation state:** hashes, source comparisons, decoded fuel changes, and archive integrity are checked. The public files still require opening in official Dynojet software and verification on the intended controller. “Known Good” records the owner's historical acceptance; it does not establish compatibility or measured air/fuel results for another bike.

## Recorded setup

Recovered project documentation describes:

- 2020 Kawasaki Ninja 650 KRT Edition.
- Dynojet Power Commander V, project-recorded part number **17-083**.
- Yoshimura full exhaust, muffler installed, DB killer removed.
- DNA replacement air filter; factory O2 sensor retained.
- No AutoTune and no recorded dyno or wideband AFR measurements.

These are source records, not a fresh inspection of the motorcycle. The project's “stock baseline” already contains nonzero fuel corrections; **it is not an OEM ECU image or a zero-correction map**. Hardware captures and unclassified files stay in the archive until their role is established.

## Tools

Python 3.10 or newer; no additional packages. Commands run from the repository root:

```sh
python tools/pcv.py verify
python tools/pcv.py inspect maps/smooth-operator/SO_v1.3_TEST.pvm
python tools/pcv.py diff maps/smooth-operator/SO_v1.0_KNOWN_GOOD.pvm maps/smooth-operator/SO_v1.3_TEST.pvm
python tools/pcv.py build
python -m unittest discover -s tests -v
```

`diff --csv path.csv` exports changed cells. `build` verifies the collection, then creates a cumulative ZIP and checksum in `dist/`. The package includes all recovered maps, their archived documents, and a checksum list for every packaged file. Build output is reproducible for identical repository contents.

These tools read the recovered 44 RPM × 10 TPS PVM family. They do not edit calibrations, convert unrelated formats, flash a device, or determine an engine's resulting mixture. See [binary audit](docs/BINARY_AUDIT.md) for what was actually checked.

## Preservation and privacy

All original source files remain untouched on the source machine. Published PVM copies have unused residue **after the visible notes' first NUL terminator** cleared inside the final 256-byte notes field. Some originals retained local backup paths or device identifiers there. The public files keep their original length, visible notes, active tables, axes, and configuration bytes. Their new hashes and exact changed offsets are recorded in the manifest.

Recovered source ZIPs were repacked with the same metadata cleanup and a notice. Embedded historical checksum documents describe the original source bytes; use the repository manifest for public copies. Read [provenance](docs/PROVENANCE.md) before comparing hashes.

## Repository guide

| Location | Contents |
| --- | --- |
| `maps/` | Identified recovered map families and reference baselines |
| `archive/` | Older versions, source documentation, metadata-cleaned source ZIPs, and every recovered device capture |
| `data/` | CSV comparisons generated from the published PVM tables |
| `docs/` | Version history, source boundaries, binary audit, and handling guide |
| `templates/` | Blank validation and observation record |
| `tools/`, `tests/` | Read-only inspection, integrity checks, and cumulative packaging |

Future releases should preserve every previous version, record exact hashes and parent maps, and promote a test map only after documented review and results. See [contributing](CONTRIBUTING.md). Original repository code and documentation use the scoped [MIT license](LICENSE); recovered third-party materials retain their existing rights.

Independent project; not affiliated with Dynojet, Kawasaki, Yoshimura, or DNA.
