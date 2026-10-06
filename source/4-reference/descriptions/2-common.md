# robot-descriptions-common

Shared components: grippers, hands, sensors, and launch utilities.

**Repository:** [fiveages-sim/robot-descriptions-common](https://github.com/fiveages-sim/robot-descriptions-common)

## Purpose

Provides reusable components that can be attached to any robot arm:
- Grippers (parallel, adaptive)
- Dexterous hands
- Sensors (cameras, force-torque)
- Common launch utilities

## Components

### Grippers

| Gripper | Package | Type |
|---------|---------|------|
| DH AG95 | `dh_ag95_description` | Parallel adaptive |
| DH PGC | `dh_pgc_description` | Parallel |
| Inspire RH56 | `inspire_rh56_description` | Dexterous hand |
| Robotiq 2F-85 | `robotiq_2f85_description` | Parallel adaptive |

### Hands

| Hand | Package | DOF |
|------|---------|-----|
| Inspire RH56 | `inspire_rh56_description` | 6 |
| LinkerHand | `linkerhand_description` | Multi-finger |

### Sensors

| Sensor | Package | Type |
|--------|---------|------|
| RealSense D435 | `realsense_description` | RGB-D camera |
| Force-Torque | `ft_sensor_description` | F/T sensor |

## Usage

### In URDF/Xacro

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
  
  <!-- Include gripper -->
  <xacro:include filename="$(find dh_ag95_description)/urdf/dh_ag95.urdf.xacro"/>
  
  <!-- Attach to arm -->
  <xacro:dh_ag95 parent="arm_tool0" prefix="gripper_">
    <origin xyz="0 0 0" rpy="0 0 0"/>
  </xacro:dh_ag95>
  
</robot>
```

### Launch Parameter

```bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=dobot_cr5 gripper:=dh_ag95
```

## robot_common_launch

Utility launch files and helpers:

| Launch | Purpose |
|--------|---------|
| `display.launch.py` | RViz visualization |
| `spawn_robot.launch.py` | Gazebo spawning |

## Debian Package

Available as Debian package:

```bash
sudo apt install ros-jazzy-robot-descriptions-common
```

## Package Structure

```
robot-descriptions-common/
├── dh_ag95_description/
│   ├── urdf/
│   │   └── dh_ag95.urdf.xacro
│   ├── meshes/
│   │   ├── visual/
│   │   └── collision/
│   └── config/
├── inspire_rh56_description/
├── robot_common_launch/
└── ...
```

## Adding Components

1. Create description package following standard layout
2. Include ros2_control configuration
3. Add to common repository
4. Update documentation

## Related

- [robot_descriptions](1-robot_descriptions.md)
- [Brand packages](3-brand_public.md)
