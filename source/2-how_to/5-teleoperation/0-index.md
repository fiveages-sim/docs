# Teleoperation

Start with [VR](6-vr_teleop.md) or a [game controller](9-joystick_teleop.md). The other pages cover isomorphic teleop, DexCap, Wuji gloves, Vive Tracker, and related assists.

VR, a foot pedal, or an exoskeleton report the current mode on `teleop/mode_state`. A game controller or the keyboard report it on `teleop_mode`. How to subscribe, and how that differs from the change event: {ref}`teleop-mode-status`. Poses, sticks, and triggers that VR publishes: [VR published topics](../../3-concepts/4-fsm_and_topics.md#vr-published-topics).

```{toctree}
:maxdepth: 1

6-vr_teleop
9-joystick_teleop
7-isomorphic_teleop
8-dexcap_teleop
```
