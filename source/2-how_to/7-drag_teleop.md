# Drag Teleoperation

Manually guide the robot through motions using the drag teaching controller.

## Prerequisites

- Robot with compliant/teach mode support
- HT Panthera or similar robot with drag teaching
- Workspace built with drag_teleop_controller

## Overview

Drag teleoperation enables:
- Gravity compensation mode
- Recording trajectories while manually guiding
- Playback of recorded motions

## Setup

### 1. Build Controller

```bash
cd ~/open-deploy-ws
colcon build --packages-up-to drag_teleop_controller
source install/setup.bash
```

### 2. Launch

```bash
ros2 launch drag_teleop_controller drag_teleop.launch.py robot:=ht_panthera
```

## Usage

### Enter Teach Mode

```bash
ros2 service call /enter_teach_mode std_srvs/srv/Trigger
```

The robot enters gravity compensation — you can now physically guide it.

### Record Trajectory

```bash
# Start recording
ros2 service call /start_recording std_srvs/srv/Trigger

# Move the robot manually...

# Stop recording
ros2 service call /stop_recording std_srvs/srv/Trigger
```

### Playback

```bash
ros2 service call /playback std_srvs/srv/Trigger
```

### Exit Teach Mode

```bash
ros2 service call /exit_teach_mode std_srvs/srv/Trigger
```

## Safety

```{admonition} Physical Interaction
:class: warning

During drag teaching:
1. Keep emergency stop accessible
2. Move the robot slowly and smoothly
3. Avoid joint limits
4. Be aware of pinch points
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `gravity_compensation` | `true` | Enable gravity compensation |
| `recording_rate` | `100` | Recording sample rate (Hz) |
| `playback_speed` | `1.0` | Trajectory playback speed |

## Master-Slave Mode

For robots with master and slave arms (bilateral teleoperation):

```bash
ros2 launch drag_teleop_controller master_slave.launch.py \
  master_robot:=ht_panthera_master \
  slave_robot:=ht_panthera_slave
```

The slave arm mirrors the master arm's motion in real-time.

## Verification

1. Robot enters compliant state when teach mode activated
2. Trajectory is recorded (check `/recorded_trajectory` topic)
3. Playback reproduces the guided motion

## Troubleshooting

### Robot doesn't go compliant

- Verify hardware supports teach mode
- Check hardware interface configuration
- Ensure motor drivers are in correct mode

### Recording empty

- Verify `/joint_states` is publishing
- Check recording service completed successfully

### Playback jerky

- Reduce playback speed
- Check trajectory smoothness
- Verify controller gains

## Supported Robots

| Robot | Drag Support |
|-------|-------------|
| HT Panthera | Full |
| Dobot CR5 | Limited (external button) |
| ARX | Via SDK commands |

```{admonition} TODO
:class: warning

Complete list of drag-capable robots and their specific procedures.
```
