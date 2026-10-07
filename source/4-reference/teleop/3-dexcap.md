# DexCap System

DexCap glove teleoperation system.

```{admonition} Access Required
:class: warning

DexCap components require private repository access.
```

## Components

| Component | Repository | Purpose |
|-----------|------------|---------|
| dexcap-ros2-control | Private | V4 driver |
| dexcap_teleop_ws | Private | Workspace |
| teleop-joint-mapper | Private | Joint mapping |

## dexcap-ros2-control

### Purpose

ROS 2 driver for DexCap V4 gloves:
- Sensor reading
- Calibration
- Joint angle output

### Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/dexcap/joint_states` | `JointState` | Glove joint angles |
| `/dexcap/hand_pose` | `PoseStamped` | Hand position |
| `/dexcap/calibration_status` | `Bool` | Calibration state |

### Usage

```bash
ros2 launch dexcap_ros2_control driver.launch.py
```

First connection with safety:

```bash
ros2 launch dexcap_ros2_control driver.launch.py publish_command:=false
```

## dexcap_teleop_ws

Deployment workspace for DexCap teleoperation.

### Setup

Follow the **private workspace README** for its init / setup scripts. This page does not invent `conda create -n dexcap`, `deploy/deploy_fw.sh`, or `deploy/setup_env.bash`.

## Related

- [DexCap Teleop How-To](../../2-how_to/5-teleoperation/8-dexcap_teleop.md)
- [teleop-joint-mapper](4-teleop_joint_mapper.md)
