# Python Interface

Control robots programmatically using the Python interface.

## Prerequisites

- ROS 2 Jazzy installed
- Robot demo running (mock, Gazebo, or real)
- **Python 3.12** (ROS 2 Jazzy)

## Install fa-py-libraries

```bash
cd ~/
git clone https://github.com/fiveages-sim/fa-py-libraries.git
cd fa-py-libraries
./init.sh all    # Python 3.12 env
```

Or install ros2_robot_interface directly:

```bash
pip install ros2-robot-interface
```

## Basic Usage

### Connect to Robot

```python
from ros2_robot_interface import RobotInterface

# Initialize
robot = RobotInterface()
robot.connect()

# Check connection
print(f"Connected: {robot.is_connected()}")
```

### Move Robot

```python
# Move to joint position (radians)
robot.move_j([0.0, -0.5, 0.5, 0.0, 0.5, 0.0])

# Move to Cartesian pose
robot.move_l([0.3, 0.0, 0.4], [1.0, 0.0, 0.0, 0.0])  # [x,y,z], [qw,qx,qy,qz]
```

### Gripper Control

```python
# Open gripper
robot.gripper_open()

# Close gripper
robot.gripper_close()

# Set position (0.0 = closed, 1.0 = open)
robot.gripper_move(0.5)
```

### Read State

```python
# Joint positions
joints = robot.get_joint_positions()
print(f"Joints: {joints}")

# End-effector pose
pose = robot.get_ee_pose()
print(f"EE pose: {pose}")
```

## Example: Pick and Place

```python
from ros2_robot_interface import RobotInterface
import time

robot = RobotInterface()
robot.connect()

# Move to home
robot.move_j([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
time.sleep(1)

# Move above pick location
robot.move_l([0.3, 0.1, 0.3], [1.0, 0.0, 0.0, 0.0])
time.sleep(0.5)

# Move down to pick
robot.move_l([0.3, 0.1, 0.15], [1.0, 0.0, 0.0, 0.0])
time.sleep(0.5)

# Close gripper
robot.gripper_close()
time.sleep(0.5)

# Lift
robot.move_l([0.3, 0.1, 0.3], [1.0, 0.0, 0.0, 0.0])
time.sleep(0.5)

# Move to place
robot.move_l([0.3, -0.1, 0.3], [1.0, 0.0, 0.0, 0.0])
time.sleep(0.5)

# Lower
robot.move_l([0.3, -0.1, 0.15], [1.0, 0.0, 0.0, 0.0])
time.sleep(0.5)

# Release
robot.gripper_open()
time.sleep(0.5)

# Return home
robot.move_j([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
```

## With Viser Visualization

Launch Viser from **fa-py-libraries** (`./run.sh viser`). That is the primary entry; do not start it from lerobot_ros2 or treat `pip install ros2-viser` as the product launcher.

```bash
cd ~/fa-py-libraries
./run.sh viser
```

`ros2_viser` is a library dependency of that command. Embedding `ROS2ViserVisualizer` in your own script is covered on [ros2-viser](../4-reference/python_apps/3-ros2_viser.md).

## FSM Commands

For whole-body control or complex motions:

```python
# Send FSM command
robot.send_fsm_command("stand")
robot.send_fsm_command("walk")

# Mode commands
robot.send_mode_command("arm_teleop")
```

See [FSM and Topics](../3-concepts/4-fsm_and_topics.md) for available commands.

## Async Interface

For non-blocking operations:

```python
import asyncio
from ros2_robot_interface import AsyncRobotInterface

async def main():
    robot = AsyncRobotInterface()
    await robot.connect()
    
    # Non-blocking motion
    await robot.move_j_async([0.0, -0.5, 0.5, 0.0, 0.5, 0.0])
    
    # Do other things while moving
    while robot.is_moving():
        print("Moving...")
        await asyncio.sleep(0.1)
    
    print("Done!")

asyncio.run(main())
```

## Verification

```python
# Test script
from ros2_robot_interface import RobotInterface

robot = RobotInterface()
robot.connect()

# Read current state
print(f"Joints: {robot.get_joint_positions()}")
print(f"EE Pose: {robot.get_ee_pose()}")

# Small motion test
current = robot.get_joint_positions()
current[0] += 0.1  # Small rotation of first joint
robot.move_j(current)
```

## Troubleshooting

### Connection fails

- Ensure robot demo is running
- Check ROS 2 domain ID matches
- Verify topics are publishing: `ros2 topic list`

### Motion commands ignored

- Check controller is in correct mode
- Verify target is within joint limits
- Check for collision detection blocks

### Import error

```bash
cd ~/fa-py-libraries
./init.sh all
# or, inside that env:
pip install -e ~/fa-py-libraries
# or
pip install ros2-robot-interface
```
