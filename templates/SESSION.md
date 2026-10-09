# Map verification session

Copy this template for a session. Leave unknown values marked `unknown`; distinguish planned actions from completed checks. Keep private device identifiers, registration details, and personal locations out of a public copy.

## Session and setup

| Field | Record |
| --- | --- |
| Date and timezone | |
| Purpose / question being checked | |
| Repository commit | |
| Motorcycle model and year | |
| Engine / ECU changes | |
| Exhaust and intake configuration | |
| Fuel used | |
| Controller model and part number | |
| Firmware version | |
| Dynojet software and version | |
| Throttle system | |
| Auto Tune / ignition / other modules | |
| Enabled features and configured switch input | |
| Setup differences or unresolved unknowns | |

## Files and backups

Record exact repository paths for candidates. Device backups and raw logs may be kept locally; record a shareable reference rather than a private absolute path.

| Role | File / reference | SHA-256 | Evidence / status |
| --- | --- | --- | --- |
| Pre-change device map backup | | | |
| Pre-change configuration record | | | |
| Second backup copy | | | |
| Reviewed Map 1 candidate | | | |
| Reviewed Map 2 candidate | | | |
| Retrieved Map 1 after transfer | | | |
| Retrieved Map 2 after transfer | | | |
| Post-change configuration record | | | |

## Software inspection

| Check | Result / evidence |
| --- | --- |
| Manifest hash match for each candidate | |
| File import success or exact error | |
| Visible map notes | |
| Map positions present | |
| Table types, modules, cylinder and gear groups | |
| RPM / throttle axes | |
| Differences from the pre-change backup | |
| Candidate setup matches actual machine | |
| Remaining compatibility questions | |

## Actual switch behavior

Project intent: **OUT → Map 1 → SmoothOperator; IN → Map 2 → RiceCrispy.** Fill in observed results independently. A match is pending until checked on the connected device.

| Physical position | Observed software selection | Retrieved map / hash | Table contents checked | Matches intent? |
| --- | --- | --- | --- | --- |
| OUT | | | | |
| IN | | | | |

- Configured purpose of switch (two maps / Auto Tune learning / other):
- Observed electrical state, if measured:
- Device configuration evidence:
- Label corrections needed:

## Transfer and readback

| Item | Result / evidence |
| --- | --- |
| Transfer attempted? Date and time | |
| Destination position(s) confirmed | |
| Software transfer result | |
| Full contents retrieved again | |
| Tables and configuration compared | |
| Byte differences explained, if any | |
| Switch positions checked again | |
| TPS observation and engine state | |
| Other unresolved differences | |

## Observations and measurements

Describe only the conditions actually observed; no particular riding test is required by this template.

| Time / condition | Map position and file | Observation or measurement | Instrument / log reference | Interpretation / uncertainty |
| --- | --- | --- | --- | --- |
| | | | | |

## Rollback and disposition

| Item | Record |
| --- | --- |
| Verified pre-change rollback reference | |
| Reason for rollback, if applicable | |
| Contents and configuration restored | |
| Readback and physical switch verification | |
| Final installed state | |
| Session outcome (pending / validated within stated scope / reverted) | |
| Scope of validation and remaining unknowns | |
| Follow-up evidence needed | |

A completed import, transfer, or readback establishes only the check documented here. Record engine calibration evidence separately; avoid changing an archive label into a performance or compatibility claim.
