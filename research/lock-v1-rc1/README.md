# LOCK v1 RC1 — public evaluation area

Public research page: https://twistphysics.org/lock-v1-rc1.html

The complete RC1 workbench is not distributed from this directory.

This public area retains:
- the published benchmark summary;
- declared scope and limitations;
- source provenance;
- the historical RC1 package identity for verification of previously obtained copies.

A reduced evaluation demo will be added after review.

Historical RC1 package SHA-256:
`7beb1092226941b3e7ccae732e90e8ec09b237a849486d8699a4f2d955e3e4a3`

Pinned Klipper source commit:
`461c4e3722c3a897fba1c6b3f0780a5315043842`

Published controlled results:
- LOCK_TRACE median wall time: 3817.9 ns/move
- VERIFY_EVERY_MOVE median: 4536.1 ns/move
- reduction vs strict per-move verify: 15.83%
- 12/12 paired rounds favored LOCK_TRACE
- 6240/6240 masked compensating fault pairs detected in the declared test class
- 320/320 declared single input-delta faults detected
- LOCK_TRACE remained 22.77% slower than RAW_SUBSET

Scope: controlled source-derived offline subset; not full Klipper daemon, MCU, physical printer, safety certification, or final LOCK v1 freeze.
