NINJA 650 POWER COMMANDER V — SMOOTHOP v1.0.0
=================================================

Bike configuration used for this map
------------------------------------
2020 Kawasaki Ninja 650 KRT Edition
Dynojet Power Commander V, model 17-083
Yoshimura full exhaust with muffler installed
DB killer removed
DNA replacement air filter
Factory narrowband O2 sensor retained
No AutoTune and no dyno/AFR measurement

FILES
-----
00_STOCK_BASELINE_2020_NINJA650_PCV5.pvm
  Untouched locked rollback map. Do not edit this copy.

01_SmoothOP_v1.0.0_TEST.pvm
  First conservative SmoothOP test map.

SmoothOP_v1.0.0_change_log.csv
  Every changed RPM/TPS cell, including stock and new values.

SmoothOP_v1.0.0_delta_from_stock.csv
  Matrix showing only the amount added to the stock baseline.

SmoothOP_v1.0.0_full_fuel_table.csv
  Complete resulting fuel table for auditing.

WHAT V1 CHANGES
---------------
1. Leaves 0%, 2%, 5%, 10% and 15% TPS completely stock.
2. Adds +1 fuel point at 20-100% TPS from 3000-6500 RPM.
3. Adds a tapered +1 at 40-100% TPS at 6750-7000 RPM.
4. Reduces selected high-RPM negative corrections by +1.
5. At 100% TPS only, cells that were -7 or leaner receive +2 instead of +1.
6. No fuel cell is reduced relative to the locked stock baseline.
7. Maximum change in any fuel cell is +2 percentage points.
8. Ignition table is byte-for-byte unchanged.
9. Target AFR table is byte-for-byte unchanged and is inactive without AutoTune.

VALIDATION BEFORE SENDING TO THE PCV
------------------------------------
1. Open 00_STOCK_BASELINE... in Dynojet PCV software and confirm it displays normally.
2. Open 01_SmoothOP_v1.0.0_TEST.pvm.
3. Confirm the Notes identify SmoothOP v1.0.0.
4. Confirm ignition and target-AFR tables match stock.
5. Review the CSV change log before using Send Map.
6. Keep the stock file open and immediately available for rollback.

FIRST TEST — DO NOT SKIP STEPS
------------------------------
1. Start with the engine fully cold and the stock map still loaded.
2. Check oil level, coolant level, intake boots, exhaust joints and O2 connection.
3. Load SmoothOP v1.0.0 with the engine OFF and ignition ON, following Dynojet's procedure.
4. Start the bike and let it warm normally. Do not repeatedly rev a cold engine.
5. Confirm stable idle, no warning light, no misfire, no fuel leak and no strong raw-fuel odor.
6. Perform a short low-load ride first. Avoid full throttle.
7. If normal, test steady 3000-6000 RPM roll-ons at approximately 20%, 40% and 60% throttle.
8. Only after those tests are normal, perform one brief higher-load roll-on in a safe closed-course environment.
9. Stop and return to stock immediately for a check-engine light, persistent misfire, severe bogging, abnormal heat, fuel smell, black smoke, detonation/pinging, or any behavior that concerns you.

FEEDBACK NEEDED FOR v1.0.1
--------------------------
Report separately for cold start, warm idle, steady cruise, 3000-4500 roll-on,
4500-6500 roll-on, 6500+ pull, engine braking, popping, fuel smell, heat,
and any warning light. Describe throttle position as light/moderate/heavy where possible.

IMPORTANT LIMITATION
--------------------
This is a conservative experimental road-test map, not a measured AFR tune. Without a
wideband sensor, AutoTune or dyno, exact mixture and maximum-power safety cannot be
verified. The locked stock map is included for immediate rollback.

Changed fuel cells: 111
Stock baseline SHA-256: d6259388eb1a35981cd1caea08f447816f7a3a1eb7317ddce65d0133a87d17dc
SmoothOP v1.0.0 SHA-256: dcedd77b8084de559a96247807839552e8d4a7ada34af6d76a3a4452181c2993
