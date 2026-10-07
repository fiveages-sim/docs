# Gripper and Teleop Plugins

Controller plugins for grippers and teleoperation.

**Repository:** [fiveages-sim/arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control)

## adaptive_gripper_controller

Position and force control for adaptive grippers.

### Usage

The launch stack does **not** take `gripper:=`. Attach an end-effector with `type` / `left_type` / `right_type` (and optional `robot_profile` / `use_profile_eef`) from [robot_common_launch](../descriptions/2-common.md). Hands and grippers that this controller can load are spawned from those EEF keys, not a separate `gripper` argument.

### Topics

| Topic | Type | Direction | Description |
|-------|------|-----------|-------------|
| `/gripper/command` | `Float64` | Subscribe | Position command (0-1) |
| `/gripper/state` | `Float64` | Publish | Current position |

### Commands

```bash
# Open gripper
ros2 topic pub /gripper/command std_msgs/msg/Float64 "{data: 1.0}" --once

# Close gripper
ros2 topic pub /gripper/command std_msgs/msg/Float64 "{data: 0.0}" --once

# Half open
ros2 topic pub /gripper/command std_msgs/msg/Float64 "{data: 0.5}" --once
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `max_effort` | float | Maximum grip force |
| `default_position` | float | Default position on start |

## arms_teleop_controller

End-effector target management for teleoperation.

### Purpose

Bridges teleop inputs to arm controller:
- Smooths target updates
- Applies workspace limits
- Handles frame transformations

### Topics

| Topic | Type | Direction | Description |
|-------|------|-----------|-------------|
| `/teleop/ee_pose` | `PoseStamped` | Subscribe | Teleop input |
| `/target_pose` | `PoseStamped` | Publish | Smoothed target |

### Configuration

```yaml
arms_teleop_controller:
  ros__parameters:
    input_topic: /teleop/ee_pose
    output_topic: /target_pose
    smoothing_factor: 0.8
    workspace_limits:
      x: [-0.5, 0.5]
      y: [-0.5, 0.5]
      z: [0.0, 0.8]
```

## target_manager_controller

Target pose queue management.

### Purpose

Manages sequences of target poses:
- Queue-based target execution
- Waypoint following
- Action interface

### Actions

| Action | Type | Description |
|--------|------|-------------|
| `/execute_targets` | Custom | Execute target sequence |

### Usage

```python
# Send target sequence
targets = [pose1, pose2, pose3]
action_client.send_goal(targets)
```

## Plugin Loading

Plugins are loaded via controller configuration:

```yaml
controller_manager:
  ros__parameters:
    update_rate: 100
    
    gripper_controller:
      type: adaptive_gripper_controller/AdaptiveGripperController

    teleop_controller:
      type: arms_teleop_controller/ArmsTeleopController
```

## Custom Plugins

To create custom plugins, follow the ros2_control plugin pattern:

1. Inherit from `controller_interface::ControllerInterface`
2. Implement lifecycle methods
3. Register with pluginlib
4. Add to controller configuration

## Related

- [ocs2_arm_controller](2-ocs2_arm_controller.md)
- [ros2_control here](../../3-concepts/1-ros2_control_here.md)
