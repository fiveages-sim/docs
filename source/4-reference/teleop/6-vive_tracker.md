# vive_tracker_teleop

Vive tracker to end-effector pose bridge.

```{admonition} Access Required
:class: warning

This package requires private repository access.
```

**Repository:** vive_tracker_teleop (private)

## Purpose

Maps Vive tracker poses to arm end-effector targets:
- Tracker position → EE position
- Tracker orientation → EE orientation
- Configurable offset

## Topics

### Published

| Topic | Type | Description |
|-------|------|-------------|
| `/teleop/left_ee_pose` | `geometry_msgs/Pose` | Left absolute end-effector pose |
| `/teleop/right_ee_pose` | `geometry_msgs/Pose` | Right absolute end-effector pose |

`tracker_openvr` publishes these two poses. A side with no tracker publishes an identity pose while any live side is enabled. Headset pose, sticks, and triggers are on {ref}`the teleop pose stream <teleop-pose-stream>`.

## Configuration

Copy `trackers.example.yaml` to `trackers.yaml` and fill each tracker serial. That example sets `publish_rate_hz` to 120, plus `wrist_C_rpy_deg`, `wrist_offset`, and `room_yaw_deg`. The package README lists the fields.

## Setup

1. Configure SteamVR
2. Pair trackers
3. Calibrate offset to robot base

## Related

- [wuji_glove_teleop](5-wuji_glove.md)
- [VR Teleop How-To](../../2-how_to/5-teleoperation/6-vr_teleop.md)
