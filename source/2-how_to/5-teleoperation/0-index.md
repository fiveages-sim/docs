# Teleoperation

FaSim offers several ways to teleoperate a robot. Each way matches its own hardware. Open the page for the hardware you have.

| Way | Hardware | Start here |
|-----|----------|------------|
| VR | Headset (Pico or Meta Quest), with controllers or optical hand tracking | [VR Teleoperation](6-vr_teleop.md) |
| Game controller | Joystick / gamepad | [Joystick teleop](9-joystick_teleop.md) |
| Isomorphic | HighTorque Panthera HT master arm and follower | [Isomorphic Teleop](7-isomorphic_teleop.md) |
| DexCap (internal) | Exoskeleton and gloves | [DexCap Teleoperation](8-dexcap_teleop.md) |
| Wuji gloves (internal) | Gloves, with an optional Vive Tracker for the arms | [wuji_glove_teleop](../../4-reference/teleop/5-wuji_glove.md) |
| Vive Tracker (internal) | SteamVR Vive Tracker | [vive_tracker_teleop](../../4-reference/teleop/6-vive_tracker.md) |
| Foot pedal | USB pedal (SayoDevice CM6K), used beside another method | [Foot pedal](9-joystick_teleop.md#foot-pedal-assist-only) |

Message names and fields are on {ref}`Teleop topics and data <teleop-topics-and-data>`.

```{toctree}
:maxdepth: 1

6-vr_teleop
9-joystick_teleop
7-isomorphic_teleop
8-dexcap_teleop
```
