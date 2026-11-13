# DexCap System

DexCap V4 exoskeleton and glove teleoperation system.

```{admonition} Access Required
:class: warning

DexCap components require private repository access.
```

## Components

| Component | Repository | Purpose |
|-----------|------------|---------|
| dexcap-ros2-control | Private | V4 exoskeleton and glove driver |
| dexcap_teleop_ws | Private | Workspace |
| teleop-joint-mapper | Private | Joint mapping |

## dexcap-ros2-control

### Purpose

ROS 2 driver for the DexCap V4 exoskeleton and gloves:
- Waist, arm, and glove joint publication
- Calibration
- Mapper launches for grippers and LinkerHand O6

### Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/dexcap/waist` | `JointState` | Waist joints |
| `/dexcap/left_arm` | `JointState` | Left arm joints |
| `/dexcap/right_arm` | `JointState` | Right arm joints |
| `/dexcap/left_hand` | `JointState` | Left glove, 21 joints |
| `/dexcap/right_hand` | `JointState` | Right glove, 21 joints |

### Usage

```bash
ros2 launch dexcap_ros2_control dexcap_driver.launch.py
```

Optional `start_upper_body`, `start_left_hand`, and `start_right_hand` flags are in the private package README. `publish_command` is not a current launch argument.

## dexcap_teleop_ws

Deployment workspace for DexCap teleoperation.

### Setup

Follow the **private workspace README** for its init / setup scripts.

## Related

- [DexCap Teleop How-To](../../2-how_to/5-teleoperation/8-dexcap_teleop.md)
- [teleop-joint-mapper](4-teleop_joint_mapper.md)
