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
| `/teleop/left_ee_pose` | `PoseStamped` | Left arm target |
| `/teleop/right_ee_pose` | `PoseStamped` | Right arm target |

## Configuration

```yaml
vive_tracker_teleop:
  ros__parameters:
    left_tracker_id: LHR-xxx
    right_tracker_id: LHR-yyy
    
    transform_offset:
      position: [0.0, 0.0, 0.1]
      orientation: [0.0, 0.0, 0.0, 1.0]
```

## Setup

1. Configure SteamVR
2. Pair trackers
3. Calibrate offset to robot base

## Related

- [wuji_glove_teleop](5-wuji_glove.md)
- [VR Teleop How-To](../../2-how_to/6-vr_teleop.md)
