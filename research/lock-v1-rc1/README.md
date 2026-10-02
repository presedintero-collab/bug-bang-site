# LOCK v1 RC1 — TwistPhysics public release

Public page: https://twistphysics.org/lock-v1-rc1.html

The reproducibility ZIP is stored in this repository as six base64 parts:
- zip.part01.b64
- zip.part02.b64
- zip.part03.b64
- zip.part04.b64
- zip.part05.b64
- zip.part06.b64

The public page fetches the six parts, concatenates them in order, decodes them locally in the browser, and downloads:

LOCK_KLIPPER_RC1_PUBLIC_2026-10-02.zip

Expected package:
- Size: 23046 bytes
- SHA-256: 7beb1092226941b3e7ccae732e90e8ec09b237a849486d8699a4f2d955e3e4a3
- Base64 length: 30728 characters

Pinned Klipper commit:
https://github.com/Klipper3d/klipper/commit/461c4e3722c3a897fba1c6b3f0780a5315043842

Published controlled result:
- LOCK_TRACE median wall time: 3817.9 ns/move
- VERIFY_EVERY_MOVE median: 4536.1 ns/move
- reduction vs strict per-move verify: 15.83%
- 12/12 paired rounds favored LOCK_TRACE
- 6240/6240 masked compensating fault pairs detected by exact trace evidence
- 320/320 declared single input-delta faults detected
- LOCK_TRACE remained 22.77% slower than RAW_SUBSET

Scope: controlled source-derived offline subset; not full Klipper daemon, MCU, physical printer, safety certification, or final LOCK v1 freeze.
