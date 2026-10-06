# ocs2_arm_controller

MPC-based arm controller for the FiveAges Sim stack.

**Repository:** [fiveages-sim/arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control)

## Purpose

`ocs2_arm_controller` provides:
- End-effector pose tracking
- Joint position control
- Smooth trajectory generation
- Multiple hardware backend support

## Installation

Included in `arms_ros2_control` package:

```bash
colcon build --packages-up-to ocs2_arm_controller
```

## Usage

### Basic Launch

```bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=mock
```

### With Parameters

```bash
ros2 launch ocs2_arm_controller demo.launch.py \
  robot:=dobot_cr5 \
  hardware:=mock \
  gripper:=dh_ag95 \
  rviz:=true
```

## Launch Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `robot` | Robot names | `dobot_cr5` | Robot model |
| `hardware` | `mock`, `gz`, `isaac`, etc. | varies | Hardware type |
| `gripper` | Gripper names | none | Attached gripper |
| `rviz` | `true`, `false` | `true` | Launch RViz |

## Topics

### Subscribed

| Topic | Type | Description |
|-------|------|-------------|
| `/target_pose` | `PoseStamped` | Cartesian target |
| `/target_joint_positions` | `JointState` | Joint targets |

### Published

| Topic | Type | Description |
|-------|------|-------------|
| `/joint_states` | `JointState` | Current state |
| `/mpc_solution` | Custom | MPC trajectory |
| `/ee_pose` | `PoseStamped` | End-effector pose |

## Configuration

### OCS2 Config

Located in description packages:

```yaml
# config/ocs2_arm_config.yaml
arm:
  dof: 6
  joint_names: [joint_1, joint_2, joint_3, joint_4, joint_5, joint_6]

mpc:
  dt: 0.01
  horizon: 1.0

task:
  targetTrackingWeight: [100, 100, 100, 10, 10, 10]
  inputWeight: [1, 1, 1, 1, 1, 1]
```

### Controller Config

```yaml
ocs2_arm_controller:
  ros__parameters:
    joints:
      - joint_1
      - joint_2
      - joint_3
      - joint_4
      - joint_5
      - joint_6
    
    command_interfaces:
      - position
    
    state_interfaces:
      - position
      - velocity
```

## Python Interface

```python
from geometry_msgs.msg import PoseStamped
import rclpy

rclpy.init()
node = rclpy.create_node('target_sender')
pub = node.create_publisher(PoseStamped, '/target_pose', 10)

target = PoseStamped()
target.header.frame_id = 'base_link'
target.pose.position.x = 0.3
target.pose.position.y = 0.0
target.pose.position.z = 0.4
target.pose.orientation.w = 1.0

pub.publish(target)
```

## Modes

### Cartesian Mode

Target end-effector pose:

```bash
ros2 topic pub /target_pose geometry_msgs/msg/PoseStamped \
  "{header: {frame_id: 'base_link'}, pose: {position: {x: 0.3, y: 0, z: 0.4}, orientation: {w: 1}}}" --once
```

### Joint Mode

Target joint positions:

```bash
ros2 topic pub /target_joint_positions sensor_msgs/msg/JointState \
  "{position: [0, -0.5, 0.5, 0, 0.5, 0]}" --once
```

## Debugging

### Check Controller Status

```bash
ros2 control list_controllers
```

### Monitor MPC

```bash
ros2 topic echo /mpc_solution
```

### Visualize Trajectory

RViz displays:
- Current robot state
- Target marker
- Planned trajectory (if published)

## Related

- [ocs2_ros2](1-ocs2_ros2.md)
- [Gripper and Teleop Plugins](6-gripper_teleop_plugins.md)
