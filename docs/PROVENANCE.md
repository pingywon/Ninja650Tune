# Provenance and published bytes

This public collection was assembled on October 9, 2026 from local project packages, their extracted files, loose project maps, and 23 Power Commander software backups. Recent project-conversation excerpts supplied the later switch convention, RC naming change, and missing archive names. Private conversations, full device paths, and unrelated personal files are not included.

## Recovered package sources

| Original source | Original archive SHA-256 |
| --- | --- |
| `Ninja650_Forked_SO_v1.3_RC_v1.0_package.zip` | `2837ddaf004e8bf3fbdae8bbd64b75969f4ad2af60224927259a831fdac4856d` |
| `Ninja650_SO_v1.0.0_CORRECTED.zip` | `2204b259cb24613dccc54a4e6b012068ff6296757cc32e72a4a98d4d3f414206` |

The original SmoothOP v1.0.0 package was recovered as an extracted directory. All of its available files are preserved in the corresponding archive directory.

## Metadata cleanup

Each recovered PVM in this family ends with a fixed 256-byte notes buffer. Bytes beyond the visible note's first NUL terminator sometimes contained stale local paths, device serials, or HID identifiers. Public copies zero those unused bytes. They retain the visible note, its terminator, the file length, and every byte before and including that terminator.

The manifest records each published file's SHA-256 and size. For PVMs, `metadata_cleanup` additionally records the original `source_sha256`, the note and residue offsets, and every changed byte offset. An empty offset list means the public copy is byte-identical to its source. The cleanup does not generate or revise fuel values.

Source-package ZIPs are therefore named `.public.zip`. Their map members receive the same cleanup, and each ZIP has an explanatory notice. Original manifests, READMEs, and validation claims inside them retain their original bytes as historical evidence. **Those historical hashes apply to original PVMs, not metadata-cleaned copies.** The root manifest supplies the public hashes. Software import and device validation of the public derivatives are still pending.

## Missing source releases

The later conversation records these releases, but neither exact archive was recovered:

| Filename | Recorded SHA-256 | Recorded distinction |
| --- | --- | --- |
| `Ninja650Tune_FIELD_KIT_2026-08-15_SO_v1.3_RC_v1.0.zip` | `2178361ea644bd9e2b7bd269b7a4dccf20135642ec01e6954f40e3a3f605eb85` | Described as documentation/change records, with binary restoration still required |
| `Ninja650Tune_PCV_FIELD_KIT_2026-08-15_SO_v1.3_RC_v1.0.zip` | `decc2dacdf24968e2672775a35ca9f010ccad0776c5b319c781f9bc50b473af4` | Described as actual 1,828-byte PVMs built from the supplied baseline |

The recovered aggressive RC has the same 67-cell count and RPM/TPS envelope described later, which supports its branch identity. It does not prove byte identity with the later renamed release. The historical RC name stays visible until that release is recovered and compared.

## Evidence levels

- **Recomputed here:** public hashes, ZIP integrity, source-to-public metadata-only differences, decoded tables, CSV comparisons, and automated tool checks.
- **Historical source statement:** motorcycle configuration, SO known-good acceptance, experiment intent, and earlier software-validation claims.
- **Pending:** official-software import of the public copies, actual switch readback, current hardware state, AFR/dyno results, and exact missing-release recovery.

No new calibration was created for this repository. New work consists of recovery, metadata cleanup, reconciliation, documentation, comparison data, and audit/packaging tools.
