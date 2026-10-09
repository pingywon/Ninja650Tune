NINJA 650 POWER COMMANDER V — SMOOTHOP v1.0.0 (CORRECTED FILE)
==================================================================

This replaces the earlier SmoothOP v1.0.0 file. The version remains v1.0.0 because
the fuel tune itself has not changed. The file container was rebuilt from the map
retrieved from the installed Power Commander V so it contains no Target AFR table.

BIKE CONFIGURATION
------------------
2020 Kawasaki Ninja 650 KRT Edition
Power Commander V 17-083
Yoshimura full exhaust with muffler installed
DB killer removed
DNA air filter
Factory O2 sensor retained

FILES
-----
00_STOCK_BASELINE_2020_NINJA650_PCV5.pvm
  Locked untouched stock baseline and rollback map.

01_SmoothOP_v1.0.0_TEST.pvm
  Corrected SmoothOP v1.0.0 map. Use this file instead of the earlier v1.0.0.

CORRECTION MADE
---------------
- Removed the complete 440-cell Target AFR table by rebuilding the map in the
  PCV-retrieved file structure.
- Table-descriptor count is 4, matching the file retrieved from the installed PCV.
- Target-AFR descriptor is absent.
- SmoothOP fuel values are identical to the earlier v1.0.0.
- All 111 SmoothOP fuel-cell changes remain identical.
- Ignition table remains byte-for-byte stock.
- No version-number change was made.

BEFORE SENDING TO THE BIKE
--------------------------
1. Delete or clearly retire the earlier SmoothOP v1.0.0 file.
2. Open this corrected file in PCV software.
3. Confirm the warning no longer appears.
4. Confirm the fuel table displays correctly.
5. Confirm ignition is unchanged.
6. Keep the included stock baseline available for immediate rollback.

DO NOT LOAD THE FILE if PCV software still warns about incompatible tables or shows
a malformed map. Report the exact warning before proceeding.

TESTING
-------
Use the same staged test procedure previously supplied: warm-up and idle check,
gentle low-load ride, moderate 3,000-6,500 RPM roll-ons, then a brief higher-load
test only after all earlier checks are normal. Restore stock for a warning light,
persistent misfire, severe bogging, pinging, abnormal heat, black smoke, or a
strong raw-fuel smell.
