# Drag teaching is not implemented

This stack does **not** implement drag teaching (拖动遥操作): no physical drag-to-teach path, no trajectory record/playback, and no `enter_teach_mode` API.

**Implemented** teleop for **HighTorque Panthera HT** is master–slave **isomorphic teleop** (同构遥操作). On the `panthera-ht` branch that is `./teleop_start.sh` — see [HighTorque Panthera HT](12-panthera_ht.md). The package is still named [`drag_teleop_controller`](https://github.com/fiveages-sim/drag_teleop_controller); follow [Isomorphic Teleop](7-isomorphic_teleop.md).
