# Binary provenance and version audit

Audit date: 2026-10-09. This audit compares recovered source bytes with the published archive, checks the observed PVM structure, and reconciles version labels. It does not establish measured AFR, engine behavior, controller compatibility, or tune suitability. No fuel, ignition, axis, or controller-setting bytes were changed for publication.

## Source-to-public verification

All **54 artifacts** in [`manifest.json`](../manifest.json) were independently compared with their recovered local sources:

| Published artifacts | Count | Result |
| --- | ---: | --- |
| Standalone PVM files | 35 | Source hashes resolve; exact metadata-cleanup comparison passes; active tables and axes are preserved. |
| Historical text, CSV, and JSON documents | 17 | Byte-identical to recovered source documents. |
| Repacked source ZIP files | 2 | Original members retained; six enclosed PVM files receive the same metadata cleanup; all other original members remain byte-identical. |

Thirty standalone PVM copies had unused notes-buffer residue removed; five were already clean. The cleanup changed **1,647 bytes in total across the 35 standalone PVM files**. This total counts separate archived copies separately and excludes the six PVM copies inside the repacked ZIPs.

For every standalone PVM, the manifest records its published hash, original source hash, file size, notes offset, cleanup start, and exact changed byte offsets. The independently recomputed changed-offset lists match every manifest entry. All 35 files preserve their original size and every byte through the visible notes' first NUL terminator. Every active descriptor, axis, and table array remains byte-identical to its own source.

The original files remain private. Published `.public.zip` archives contain a `PUBLIC_METADATA_CLEANUP.txt` explanation and their original archive hash. Their embedded historical checksum documents still describe the original bytes; use the repository manifest for the published copies' hashes. Source-to-public checks also compared every enclosed PVM against its original ZIP member, verified archive CRCs, and scanned standalone files and decompressed ZIP members for the recovered local paths, device serial, and HID identifiers. No such markers remain in the published artifacts.

## What metadata cleanup does

In this recovered file family, a UInt32 little-endian field at offset `0x10` points to a final 256-byte notes buffer. The importer requires `notes_offset + 256 == file_size`, locates the first NUL within that buffer, and replaces only subsequent bytes with zero. Visible notes, their terminator, the header, and all preceding data remain unchanged.

This removes incidental data left after the intentional notes, including device identifiers and local backup-path residue. Public copies have new hashes where bytes changed. They are explicitly documented derivatives of recovered sources, not byte-identical originals or newly tuned calibrations. Binary comparison proves which bytes were preserved; Dynojet software open/read-back validation remains a separate step.

## Confirmed fuel differences

Fuel comparisons use the pointed 440-byte fuel array and the verified 44-by-10 axes. For these files, `displayed_fuel_value = stored_byte - 100`. All 440 decoded cells of corrected SO v1.0.0 match its supplied full-fuel CSV.

| Candidate | Comparison baseline | Changed fuel cells | Finding |
| --- | --- | ---: | --- |
| SO v1.0 | Project stock baseline | 111 | Changes are +1 or +2. |
| SO v1.3 test | SO v1.0 | 25 | Every change is +1. |
| Earlier RC v1.0, now archived as superseded | SO v1.0 | 40 | Exactly matches all 40 rows in its supplied change CSV; only 0% and 2% TPS differ. |
| Recovered RC v1.1 aggressive test | Project stock baseline | 67 | Only 0%, 2%, and 5% TPS differ; matches the later documented stock-based design. |
| Recovered RC v1.1 aggressive test | SO v1.0 | 178 | The 111 SO changes are absent and the 67 RC changes occupy different TPS columns. |

All five comparisons have byte-identical active ignition arrays. The original 1,828-byte SO v1.0.0 and corrected 1,648-byte SO v1.0.0 have identical fuel arrays despite different file containers. The later SO v1.0 known-good file also has that same fuel array. The no-AutoTune project stock file preserves the original project's stock fuel array.

SO v1.3's 25 changes relative to SO v1.0 are:

| TPS | RPM range | Cells | Delta |
| ---: | --- | ---: | ---: |
| 15% | 3,250–5,500 | 10 | +1 |
| 20% | 3,500–5,500 | 9 | +1 |
| 40% | 5,750–6,250 | 3 | +1 |
| 60% | 5,750–6,250 | 3 | +1 |

The recovered stock-based RC candidate's 67 changes are:

| TPS | RPM range | Cells | Delta versus project stock |
| ---: | --- | ---: | --- |
| 0% | 2,500–8,250 | 24 | +4 through +35 |
| 2% | 2,750–8,000 | 22 | +3 through +18 |
| 5% | 3,000–8,000 | 21 | +2 through +9 |

These are descriptions of recovered files, not recommended adjustments.

## Version reconciliation and missing evidence

The recovered fork package's manifest and four original PVM checksums are internally consistent. Its RC v1.0 is the earlier **40-cell SO-based experiment**. The later conversation superseded that experiment, retained SO v1.3, and normalized the stock-based RC design to **RC v1.0**.

The July 21 backup retains its original visible title, **RiceCrispy v1.1 AGGRESSIVE TEST**, and verifies the later design's 67 stock-based changes. The repository keeps that recovered title in the filename and manifest provenance. It does not claim that this backup is byte-identical to the later renamed field-kit map.

The two August 15 field-kit ZIPs listed in the manifest were not recovered. Their reported hashes are preserved as missing-source evidence. The recovered SO v1.3 is a 1,648-byte file from the earlier fork package; the exact later field-kit binary remains unverified. The repository therefore distinguishes recovered artifacts from the latest documented targets.

Both original and corrected SO v1.0.0 packages pass all seven checks in their original checksum manifests. The corrected package still contains a 1,828-byte stock baseline with the earlier extra target AFR descriptor; its archive status must not be confused with the separate 1,648-byte no-AutoTune baseline.

The source labels **stock** and **known good** describe project history. The project stock file contains nonzero fuel corrections; this audit does not establish it as an OEM calibration or a zero map. No recovered project record establishes a known-good RC map.

## Observed PVM layouts

Offsets below are zero-based hexadecimal byte offsets. These observations apply to the recovered repository files, not to PVM files generally. Thirty-five standalone files fall into three layouts:

| Bytes | Files | Descriptors | TPS block | RPM block | Fuel values | Ignition values | Extra target AFR values | Notes |
| ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| 1,648 | 28 | 4 | `0x78` | `0x13c` | `0x200` | `0x3b8` | absent | `0x570` |
| 1,828 | 3 | 5 | `0x88` | `0xa0` | `0xfc` | `0x2b4` | `0x46c` | `0x624` |
| 2,104 | 4 | 5 | `0x88` | `0x14c` | `0x210` | `0x3c8` | `0x580` | `0x738` |

Each TPS block is 24 bytes, each RPM block is 92 bytes, and each values array is 440 bytes. Notes occupy the final 256 bytes in each layout. The shared first 16 header bytes are:

```text
02 00 00 00 27 02 00 00 30 00 00 00 00 01 00 00
```

The descriptor count is a UInt32 little-endian value at `0x30`; the list begins at `0x38`. Each 16-byte descriptor contains a four-byte identifier and three UInt32 little-endian pointers: TPS, RPM, and values. Masking pointers with `0x7fffffff` removes the high-bit flag used by the recovered layouts. Fuel descriptors `c1403fd0` and `c1403fd1` share one array. Ignition descriptors `c1413fd6` and `c1413fd7` share another. The five-descriptor layouts also contain `c14a3f7c`, identified by the source documentation as target AFR.

TPS blocks begin `0a c5 00 00`, followed by ten UInt16 little-endian values that decode, after division by 10, to `0, 2, 5, 10, 15, 20, 40, 60, 80, 100` percent. RPM blocks begin `2c 1c 00 00`, followed by 44 UInt16 little-endian values from 250 through 11,000 RPM in increments of 250. Fuel arrays are row-major by RPM, then TPS.

Some gaps between pointed blocks contain old, unreferenced axis or data remnants. In the recovered 67-cell RC source, 178 bytes before its fuel array differ from the fork stock file, all in unreferenced gaps. Its header/descriptors, pointed TPS and RPM axes, and pointed ignition array are byte-identical to that stock file. The audit consequently compares active blocks separately and does not claim that every non-fuel byte is equal between different source maps.

## Read-only tooling check

[`tools/pcv.py`](../tools/pcv.py) verified all 54 manifest artifacts successfully. Independent calls to its fuel comparison function returned exactly **111, 25, 40, 67, and 178** changed cells for the five comparisons above, with ignition equality in every case. The tool also reported every SO v1.3 delta as +1.

The inspector checks the recognized header, notes boundaries, descriptor identifiers and bounds, shared cylinder tables, and expected axes before interpreting fuel values. It does not edit a PVM or communicate with a controller. Packaging and checksums establish file integrity; they do not establish successful loading or engine validation.
