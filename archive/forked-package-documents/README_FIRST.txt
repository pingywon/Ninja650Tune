Ninja 650 Power Commander V — Forked Tune Package
====================================================

Motorcycle:
2020 Kawasaki Ninja 650 KRT
Yoshimura full exhaust with muffler
DB killer removed
DNA air filter
Stock O2 sensor retained
Power Commander V
No AutoTune

BRANCH STATUS
-------------
SmoothOperator:
- SO v1.0 KNOWN GOOD: accepted rollback map.
- SO v1.3 TEST: current SmoothOperator experiment.

RiceCrispy:
- RC v1.0 TEST: first sound-focused experiment.
- No RiceCrispy map is known good yet.

STOCK:
- One shared no-AutoTune stock baseline.

RC v1.0 DESIGN
--------------
RC v1.0 is forked directly from SO v1.0 Known Good.

Only the 0% and 2% TPS fuel columns were changed.
The active test range is approximately 3000-8000 RPM.
All 5-100% TPS fuel values remain identical to SO v1.0.
Ignition remains identical to SO v1.0 and stock.
No Target AFR or AutoTune table is included.
Visible flame is not a tuning objective and is a rollback condition.

RECOMMENDED LAPTOP TEST SET
---------------------------
1. STOCK baseline
2. SO v1.0 Known Good
3. RC v1.0 Test

Do not operate the laptop while riding.
Stop safely before changing maps.
Open each file in Dynojet PCV software before sending it.
Do not send a map if the software reports an AutoTune/Target AFR conflict.

INITIAL RC TEST
---------------
Warm the motorcycle fully on SO v1.0 Known Good.
Establish its normal deceleration sound.
Stop safely and load RC v1.0.
Test closed-throttle deceleration progressively around:
- 4000 RPM
- 5000 RPM
- 6000 RPM
- 7000 RPM

Begin with ordinary roll-off. Do not start with repeated redline roll-offs.

ROLL BACK TO SO v1.0 FOR
------------------------
- Violent cannon-like bangs
- Visible flames
- Persistent raw-fuel smell
- Misfire or unstable idle
- Bogging or hesitation when reopening the throttle
- Check-engine light
- Abnormal exhaust or bodywork heat
- Smoke from the muffler or packing

REPORT BACK
-----------
For each RPM range, report:
- No change
- Deeper burble
- Repeated crackle
- Sharp pop
- Too aggressive

Also report throttle reopening, idle, fuel smell, heat, warning lights,
and whether RC changes normal riding behavior.
