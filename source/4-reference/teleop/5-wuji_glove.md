# wuji_glove_teleop

Wuji glove teleoperation with optional Vive tracking.

```{admonition} Access Required
:class: warning

This package requires private repository access.
```

**Repository:** wuji_glove_teleop (private)

## Purpose

Teleop using Wuji gloves:
- Hand joint tracking
- Optional arm tracking via Vive
- Hand2 hand control

## Components

| Component | Purpose |
|-----------|---------|
| Glove driver | Read glove sensors |
| Retargeting | Map to robot hand |
| Vive integration | Arm position (optional) |

## Usage

### Glove Only

```bash
ros2 launch wuji_glove_teleop glove.launch.py
```

### With Vive Arm Tracking

```bash
ros2 launch wuji_glove_teleop full_teleop.launch.py
```

## Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/wuji/hand_joints` | `JointState` | Glove joint angles |
| `/wuji/target_hand` | `JointState` | Robot hand targets |

## Configuration

Complex gating logic for:
- Grasp detection
- Motion filtering
- Safety limits

See repository documentation for detailed configuration.

## Related

- [wuji-ros2-control](7-wuji_hand_hi.md)
- [Vive Tracker](6-vive_tracker.md)
