# Check, back up, and verify maps

The recovered files are an archive of this project's development. **Dynojet software import, controller transfer, device readback, and engine calibration have not been verified for this release.** This guide describes the evidence to collect before treating a recovered file as a field-ready map.

## Identify the candidate

Read the [README](../README.md) and [manifest](../manifest.json) first. Keep these distinctions intact:

- `SO_v1.3_TEST.pvm` is a recovered test file. It is not the missing August 15 field-kit binary.
- `SO_v1.0_KNOWN_GOOD.pvm` retains an owner's historical acceptance label. That label is not current software or hardware validation.
- `RC_v1.1_AGGRESSIVE_TEST_RECOVERED.pvm` is the recovered 67-cell historical candidate. Its identity as the later renamed RC v1.0 field-kit file is unverified.
- The earlier 40-cell RC v1.0 is superseded. Its version number does not identify the later aggressive RC v1.0.

There are no field-load aliases in this repository. Use exact paths and hashes in every session record. The published files have only unused bytes in their final notes buffer cleared after the first NUL terminator; the manifest records those changes and the original source hashes. This metadata cleanup still requires a Dynojet import check.

Record the actual motorcycle's model year and installed parts, controller part number, firmware, and enabled features. A recovered filename or conversation description does not verify the machine in front of you.

## Know what a map contains

Power Core maps contain tables that can belong to different map positions. Record each table's position, module, cylinder grouping, and gear grouping. [Dynojet: Working With Maps](https://docs.dynojet.com/Support/SoftwareHelpFiles/PowerCoreHelp/en-US/2.3.0/C3Tuning/C3Tuning/C3Tuning/Working_With_Maps.htm)

The PCV guide identifies `.pvm` as the PCV map format. Fuel cells are percentage adjustments: positive values add fuel; negative values remove it. They are not target AFRs or measurements of the resulting mixture. Dynojet recommends measured air/fuel data when making fuel-curve changes. [Dynojet: PCV User Guide, page 1](https://www.dynojet.com/amfile/file/download/file/5/product/2908/)

C3 can open several formats, including PCV `.pvm` and PCIII `.djm`. Successful import does not establish controller or motorcycle compatibility. Renaming the extension is not a conversion. [Dynojet: To Open a Map File](https://docs.dynojet.com/support/softwarehelpfiles/powercorehelp/en-us/2.3.0/c3tuning/c3tuning/c3tuning/To_Open_a_Map_File.htm)

## Preserve the existing device state

Use a copy of the [session template](../templates/SESSION.md). The following is this project's verification workflow; menu names differ between legacy PCV software and C3.

1. Connect with the correct Dynojet software and identify the device. Record its configuration before changing anything.
2. Retrieve the existing device contents and save an untouched local backup. Preserve both map positions, relevant auxiliary tables, and configuration records. Keep a second backup outside the editing folder.
3. Calculate the candidate file's SHA-256 hash and compare it with the manifest. Open the candidate in Dynojet software; record success or the exact error and inspect all tables, axes, notes, and positions.
4. Resolve any mismatch between the candidate's documented setup and the actual machine. Record unknowns as unknowns.
5. If a transfer is intended after those checks, confirm the destination position and send the reviewed file. Retrieve the device contents again, inspect the tables and position assignments, and save the retrieved copy.
6. Compare table contents and configuration with the reviewed candidate. A byte hash may differ if the software rewrites a container; record and explain differences rather than assuming that transfer failed or succeeded.

Dynojet's legacy procedure connects by USB, opens the file, checks successful opening, and uses Send Map. Its Auto Tune guide uses Get Map to retrieve tables from the PCV. Hashes and readback comparison are additional project checks. [Dynojet: PCV User Guide, page 1](https://www.dynojet.com/amfile/file/download/file/5/product/2908/), [Dynojet: Auto Tune Dual Channel Guide, page 4](https://www.dynojet.com/amfile/file/download/file/14/category/71/)

## Verify the physical switch

The permanent project convention is:

| Physical position | Intended device position | Family |
| --- | --- | --- |
| OUT | Map 1 | SmoothOperator |
| IN | Map 2 | RiceCrispy |

**This assignment needs confirmation on the connected controller.** Observe the selected map in each physical position and retrieve its contents. Record what the device actually reports before applying or relying on labels.

In C3, Dynojet documents Home → Configure → Map Switch, enabling the feature, selecting the wired input, and using Send to apply the configuration. Tables are sent to their respective map positions. [Dynojet: To Configure Map Switch](https://docs.dynojet.com/Support/SoftwareHelpFiles/PowerCoreHelp/en-US/3.0.0/C3Tuning/C3Tuning/C3Tuning/To_Configure_Map_Switch.htm)

The accessory input accepts an open/close switch and wire polarity is not significant. Auto Tune can instead use the switch to choose base-map operation or learning mode, so confirm its configured purpose. Physical OUT/IN labels do not establish electrical state. [Dynojet: PCV Input Accessory Guide, page 2](https://www.dynojet.com/amfile/file/download/file/4941/product/135636/)

## Check TPS and keep a rollback record

Dynojet specifies 0% software TPS with the engine warmed up and idling. Use its applicable procedure if recalibration is needed; fly-by-wire motorcycles have a distinct requirement. Confirm the actual throttle system before following calibration instructions. [Dynojet: PCV User Guide, page 2](https://www.dynojet.com/amfile/file/download/file/5/product/2908/)

Record observations and measurements without promoting them into unmeasured performance claims. If a mismatch or unexpected behavior remains, retain the evidence and use the verified pre-change backup and configuration as the rollback reference. Restore the intended positions and verify them by readback; a historical `KNOWN_GOOD` filename is not a substitute for the actual device backup.

Get software, firmware, and the application-specific installation guide from [Dynojet's official PCV/PC6 downloads](https://www.dynojet.com/downloads/power-commander-v/). Record versions used. Sources checked October 9, 2026; manuals and software are linked, not redistributed.
