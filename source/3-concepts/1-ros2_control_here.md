# ros2_control in This Stack

This page explains how FiveAges Sim uses the ROS 2 control framework.

## Overview

The stack uses `ros2_control` as its hardware abstraction layer:

:::{code-block} none
Controllers (MPC, teleop)
        ↓
Controller Manager
        ↓
Hardware Interfaces (plugins)
        ↓
Physical/Simulated Hardware
:::

## Key Components

### Controller Manager

The Controller Manager loads, configures, and executes controllers. In this stack:

- Controllers are spawned via launch files
- Multiple controllers can run simultaneously
- Controller switching is handled by the manager

### Hardware Interfaces

Hardware interfaces bridge controllers to actual hardware:

| Interface Type | Plugin | Example |
|----------------|--------|---------|
| Mock | `mock_components/GenericSystem` | Testing without hardware |
| Gazebo | `gz_ros2_control/GazeboSimSystem` | Gazebo simulation |
| Isaac | Topic-based interface | Isaac Sim bridge |
| Real | Vendor-specific plugins | CAN, TCP, serial |

### Controllers

The main controllers in this stack:

| Controller | Purpose |
|------------|---------|
| `ocs2_arm_controller` | MPC-based arm motion |
| `adaptive_gripper_controller` | Gripper position/force control |
| `arms_teleop_controller` | End-effector target tracking |
| `target_manager_controller` | Target pose management |

## The `hardware:=` Parameter

Launch files use the `hardware` parameter to select the interface:

```bash
# Mock - no hardware, instant response
ros2 launch ocs2_arm_controller demo.launch.py hardware:=mock

# Gazebo - physics simulation
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz

# Isaac - Isaac Sim bridge
ros2 launch ocs2_arm_controller demo.launch.py hardware:=isaac

# Real hardware (robot-specific)
ros2 launch ocs2_arm_controller demo.launch.py hardware:=real
```

## Configuration Flow

1. **URDF/xacro** defines the robot model and includes ros2_control tags
2. **ros2_control xacro** specifies hardware interfaces per `hardware:=` value
3. **Controller config YAML** defines controller parameters
4. **Launch file** spawns controller manager and controllers

Example xacro snippet:

```xml
<ros2_control name="ArmSystem" type="system">
  <xacro:if value="${hardware_type == 'mock'}">
    <hardware>
      <plugin>mock_components/GenericSystem</plugin>
    </hardware>
  </xacro:if>
  
  <joint name="joint_1">
    <command_interface name="position"/>
    <state_interface name="position"/>
    <state_interface name="velocity"/>
  </joint>
</ros2_control>
```

## Command and State Interfaces

### Command Interfaces

What controllers can command:

| Interface | Description |
|-----------|-------------|
| `position` | Joint position (radians) |
| `velocity` | Joint velocity (rad/s) |
| `effort` | Joint torque (Nm) |

### State Interfaces

What controllers can read:

| Interface | Description |
|-----------|-------------|
| `position` | Current joint position |
| `velocity` | Current joint velocity |
| `effort` | Current joint effort/torque |

## Controller Lifecycle

Controllers follow the ROS 2 lifecycle:

1. **Unconfigured** — Initial state
2. **Inactive** — Configured but not running
3. **Active** — Running and commanding hardware
4. **Finalized** — Shutdown

Typical commands:

```bash
# List controllers
ros2 control list_controllers

# Switch controllers
ros2 control switch_controllers --activate new_controller --deactivate old_controller

# Check hardware interfaces
ros2 control list_hardware_interfaces
```

## MPC Controller Specifics

The OCS2 arm controller uses Model Predictive Control:

- **Prediction horizon:** Looks ahead to plan smooth trajectories
- **Constraints:** Respects joint limits, velocity limits
- **Real-time:** Runs at control loop frequency

Key topics:

| Topic | Direction | Purpose |
|-------|-----------|---------|
| `/target_pose` | Subscribe | Cartesian target |
| `/target_joint_positions` | Subscribe | Joint space target |
| `/joint_states` | Publish | Current state |
| `/mpc_solution` | Publish | Planned trajectory |

## Best Practices

1. **Always test with mock first** — Verify behavior before simulation/real
2. **Check hardware interfaces** — Use `ros2 control list_hardware_interfaces`
3. **Monitor controller state** — Use `ros2 control list_controllers`
4. **Use appropriate QoS** — Match publisher/subscriber QoS settings
