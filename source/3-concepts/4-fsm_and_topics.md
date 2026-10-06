# FSM and Topics

This page explains the finite state machine (FSM) architecture and topic contracts used for robot control.

## Overview

The control stack uses FSM patterns for:
- Mode switching (arm control, teleop, walking)
- Safety state management
- Coordinated multi-system behavior

## FSM Topics

### Command Topics

| Topic | Type | Purpose |
|-------|------|---------|
| `/fsm_command` | `std_msgs/String` | High-level state commands |
| `/mode_command` | `std_msgs/Int32` | Numeric mode selection |

### State Topics

| Topic | Type | Purpose |
|-------|------|---------|
| `/fsm_state` | `std_msgs/String` | Current FSM state |
| `/mode_state` | `std_msgs/Int32` | Current mode |

## Common FSM States

### Arm Controller States

| State | Description |
|-------|-------------|
| `idle` | No active control |
| `position_control` | Joint position control |
| `cartesian_control` | End-effector pose control |
| `teleop` | Teleoperation mode |

### Humanoid States (WBC)

| State | Description |
|-------|-------------|
| `stand` | Standing position |
| `walk` | Walking mode |
| `arm_teleop` | Arm teleoperation |
| `full_body_teleop` | Full body control |

## Mode Commands

Mode commands are typically numeric:

```python
# Example mode definitions
MODE_IDLE = 0
MODE_POSITION = 1
MODE_CARTESIAN = 2
MODE_TELEOP = 3
```

Send mode command:

```bash
ros2 topic pub /mode_command std_msgs/msg/Int32 "{data: 2}" --once
```

## Target Topics

### End-Effector Targets

| Topic | Type | Description |
|-------|------|-------------|
| `/target_pose` | `PoseStamped` | Single arm EE target |
| `/left_target_pose` | `PoseStamped` | Left arm target |
| `/right_target_pose` | `PoseStamped` | Right arm target |

### Joint Targets

| Topic | Type | Description |
|-------|------|-------------|
| `/target_joint_positions` | `JointState` | Joint position targets |

### Teleop Targets

| Topic | Type | Description |
|-------|------|-------------|
| `/teleop/left_ee_pose` | `PoseStamped` | Left teleop input |
| `/teleop/right_ee_pose` | `PoseStamped` | Right teleop input |
| `/teleop/head_pose` | `PoseStamped` | Head tracking input |

## Topic Contracts

### Target Pose Contract

Publishers (teleop, planners) must:
- Use consistent frame_id (typically `base_link`)
- Publish at consistent rate (10-100 Hz typical)
- Include valid orientation quaternion

```python
from geometry_msgs.msg import PoseStamped

target = PoseStamped()
target.header.frame_id = "base_link"
target.header.stamp = self.get_clock().now().to_msg()
target.pose.position.x = 0.3
target.pose.position.y = 0.0
target.pose.position.z = 0.4
target.pose.orientation.w = 1.0  # Valid quaternion!
```

### Joint State Contract

Publishers must:
- Include all joint names
- Match joint order to URDF
- Provide positions at minimum (velocity/effort optional)

```python
from sensor_msgs.msg import JointState

js = JointState()
js.header.stamp = self.get_clock().now().to_msg()
js.name = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
js.position = [0.0, -0.5, 0.5, 0.0, 0.5, 0.0]
```

## State Transitions

### Safe Transitions

:::{code-block} none
idle → position_control → cartesian_control → teleop
  ↑                                              ↓
  ←←←←←←←←←← (any state) ←←←←←←←←←←←←←←←←←←←←←←←
:::

### Sending Transitions

```bash
# Enter teleop mode
ros2 topic pub /fsm_command std_msgs/msg/String "{data: 'teleop'}" --once

# Return to idle
ros2 topic pub /fsm_command std_msgs/msg/String "{data: 'idle'}" --once
```

## QoS Settings

Recommended QoS for control topics:

| Topic Type | Reliability | Durability | History |
|------------|------------|------------|---------|
| Commands | Reliable | Volatile | Keep last 1 |
| State | Reliable | Transient local | Keep last 1 |
| Targets | Best effort | Volatile | Keep last 1 |
| Joint states | Best effort | Volatile | Keep last 1 |

## Debugging

### Monitor FSM State

```bash
ros2 topic echo /fsm_state
ros2 topic echo /mode_state
```

### Check Topic Flow

```bash
# List all topics
ros2 topic list

# Check publishing rate
ros2 topic hz /target_pose

# Inspect message
ros2 topic echo /target_pose --once
```

### Verify Connections

```bash
ros2 topic info /target_pose
```

## Integration Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
from geometry_msgs.msg import PoseStamped

class ControlClient(Node):
    def __init__(self):
        super().__init__('control_client')
        
        self.fsm_pub = self.create_publisher(String, '/fsm_command', 10)
        self.mode_pub = self.create_publisher(Int32, '/mode_command', 10)
        self.target_pub = self.create_publisher(PoseStamped, '/target_pose', 10)
        
        self.fsm_sub = self.create_subscription(
            String, '/fsm_state', self.fsm_callback, 10)
    
    def set_teleop_mode(self):
        msg = String()
        msg.data = 'teleop'
        self.fsm_pub.publish(msg)
    
    def send_target(self, x, y, z):
        target = PoseStamped()
        target.header.frame_id = 'base_link'
        target.header.stamp = self.get_clock().now().to_msg()
        target.pose.position.x = x
        target.pose.position.y = y
        target.pose.position.z = z
        target.pose.orientation.w = 1.0
        self.target_pub.publish(target)
    
    def fsm_callback(self, msg):
        self.get_logger().info(f'FSM state: {msg.data}')
```
