# Teleoperation

Start with [VR](6-vr_teleop.md) or a [game controller](9-joystick_teleop.md). The other pages cover isomorphic teleop, DexCap, Wuji gloves, Vive Tracker, and related assists. Drag teaching (拖动遥操作) is not implemented.

VR, a foot pedal, or an exoskeleton report the current mode on `teleop/mode_state`. A game controller or the keyboard report it on `teleop_mode`. How to subscribe, and how that differs from the change event: {ref}`teleop-mode-status`.

```{toctree}
:maxdepth: 1

6-vr_teleop
9-joystick_teleop
7-isomorphic_teleop
7-drag_teleop
8-dexcap_teleop
```
