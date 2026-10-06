# drag_teleop_controller

Drag teaching controller for manual robot guidance.

**Repository:** [fiveages-sim/drag_teleop_controller](https://github.com/fiveages-sim/drag_teleop_controller)

## Purpose

Enables manual robot guidance:
- Gravity compensation mode
- Trajectory recording
- Playback

## Supported Robots

| Robot | Support Level |
|-------|---------------|
| HT Panthera | Full |
| Other compliant arms | Partial |

## Usage

### Launch

```bash
ros2 launch drag_teleop_controller drag_teleop.launch.py robot:=ht_panthera
```

### Services

| Service | Type | Description |
|---------|------|-------------|
| `/enter_teach_mode` | `Trigger` | Enable gravity compensation |
| `/exit_teach_mode` | `Trigger` | Return to normal mode |
| `/start_recording` | `Trigger` | Begin recording |
| `/stop_recording` | `Trigger` | End recording |
| `/playback` | `Trigger` | Play recorded trajectory |

### Workflow

```bash
# Enter teach mode
ros2 service call /enter_teach_mode std_srvs/srv/Trigger

# Record trajectory (manually guide robot)
ros2 service call /start_recording std_srvs/srv/Trigger
# ... move robot ...
ros2 service call /stop_recording std_srvs/srv/Trigger

# Playback
ros2 service call /playback std_srvs/srv/Trigger

# Exit
ros2 service call /exit_teach_mode std_srvs/srv/Trigger
```

## Topics

| Topic | Type | Direction | Description |
|-------|------|-----------|-------------|
| `/recorded_trajectory` | `JointTrajectory` | Publish | Recorded path |
| `/joint_states` | `JointState` | Subscribe | Current state |

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `gravity_compensation` | `true` | Enable during teach |
| `recording_rate` | `100` | Sample rate (Hz) |
| `playback_speed` | `1.0` | Playback multiplier |

## Related

- [Drag Teleop How-To](../../2-how_to/7-drag_teleop.md)
