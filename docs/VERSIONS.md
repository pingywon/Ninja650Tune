# Version history and naming

The ordering below follows the relationships recorded in the project. A file date or version label alone does not prove that two files are identical. Original and public-copy hashes are in the manifest.

## SmoothOperator

| Stage | Preserved location | Relationship and status |
| --- | --- | --- |
| SmoothOP v1.0.0 original | `archive/so-v1.0.0-original/` | 1,828-byte container, including a Target AFR table; 111 fuel changes versus its baseline. Superseded container. |
| SmoothOP v1.0.0 corrected | `archive/so-v1.0.0-corrected/` | 1,648-byte no-AutoTune map. All 440 fuel values match the original; ignition unchanged. The included baseline is still the earlier 1,828-byte file. |
| SO v1.0 Known Good | `maps/smooth-operator/SO_v1.0_KNOWN_GOOD.pvm` | Same fuel values as corrected v1.0.0; different notes and file hash. Source package calls this the accepted rollback. |
| SO v1.3 Test | `maps/smooth-operator/SO_v1.3_TEST.pvm` | Exactly 25 +1 fuel-point changes versus SO v1.0. Ignition unchanged. Latest recovered SO experiment. |

SO v1.3 changes affect 15/20% TPS between 3,250–5,500 RPM and 40/60% TPS around 5,750–6,250 RPM. These are table changes, not evidence of a measured improvement. The exact cells are in [SO_v1.3_vs_v1.0.csv](../data/SO_v1.3_vs_v1.0.csv).

No separate SO v1.1 or v1.2 binary was recovered. No placeholders or invented versions are supplied.

## RiceCrispy: two different meanings of v1.0

| Identity | Base | Recovered fuel changes | Status |
| --- | --- | --- | --- |
| Early RC v1.0 | SO v1.0 | 40 cells, 0/2% TPS, 3,000–8,000 RPM | Superseded experiment in `archive/rice-crispy-legacy/` |
| RC v1.1 AGGRESSIVE TEST | Project no-AutoTune baseline | 67 cells, 0/2/5% TPS, 2,500–8,250 RPM | Recovered July 21 device capture, retained under its visible-note identity |
| Later RC v1.0 Test alias | Aggressive branch, renamed in the later conversation | Recorded as the same 67-cell stock-based design | Exact August 15 field-kit binary is missing |

The 67-cell aggressive map is **not** an incremental addition to SO v1.0. Compared directly with SO v1.0 it has 178 changed cells: the 111 SO-specific changes are absent, and 67 different baseline cells are modified. Its pointed fuel axes, descriptor block, and ignition table match the baseline; unreferenced gaps in the container differ. See [RC_aggressive_vs_baseline.csv](../data/RC_aggressive_vs_baseline.csv).

No RC map is recorded as accepted known good. Older source documents retain their historical “CURRENT” labels inside the archive; this page and the root manifest describe the reconciled state.

## Switch convention

The later explicit project assignment supersedes any older assignment:

| Physical label on this project | Intended map position | Family |
| --- | --- | --- |
| OUT | Map 1 | SmoothOperator |
| IN | Map 2 | RiceCrispy |

These physical labels require verification against the actual configured input and retrieved contents. No `FIELD_LOAD` aliases are supplied that could silently substitute an older RC map for the missing later release.

## Baselines and captures

The original 1,828-byte baseline and the forked 1,648-byte no-AutoTune baseline have different hashes and table containers, but their 440 fuel values agree. Their “stock” labels refer to this project; the tables contain nonzero adjustments.

`PCV_RETRIEVED_STANDINGMOD1.pvm`, older loose maps, and 23 dated software backups are retained for comparison. Backup filenames preserve capture timestamps; their selection as Map 1 or Map 2 at capture time has not been independently established. A filename suffix such as `_x2` is not treated as proof of a switch assignment.
