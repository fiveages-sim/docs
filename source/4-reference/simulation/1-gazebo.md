# Gazebo Harmonic

Physics simulation with Gazebo.

## Installation

```bash
sudo apt install ros-jazzy-gz-*
```

## Usage

### Launch

```bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz
```

### Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `hardware` | `gz` | Use Gazebo backend |
| `world` | World file path | Custom world |
| `headless` | `true/false` | No GUI |

## Features

### Physics

- Rigid body dynamics
- Contact simulation
- Joint dynamics

### Sensors

- Camera simulation
- Depth sensors
- Force-torque

## Worlds

Default world includes ground plane. Custom worlds:

```bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz world:=custom.sdf
```

## Integration

### ros2_control Bridge

`gz_ros2_control` bridges Gazebo physics to ROS 2:

```xml
<ros2_control name="GazeboSystem" type="system">
  <hardware>
    <plugin>gz_ros2_control/GazeboSimSystem</plugin>
  </hardware>
</ros2_control>
```

### Topics

Gazebo publishes ROS 2 topics:
- `/joint_states` — Joint feedback
- `/clock` — Simulation time
- Sensor topics as configured

## Debugging

### Check Gazebo Status

```bash
gz topic -l
```

### View Simulation

```bash
gz gui
```

### Slow Simulation

If simulation runs slow:
1. Reduce world complexity
2. Use headless mode
3. Check GPU acceleration

## Related

- [Isaac Sim](2-fasim_isaac.md)
- [ros2_control here](../../3-concepts/1-ros2_control_here.md)
