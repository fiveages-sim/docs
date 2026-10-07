# Python Interface

Control robots programmatically using the Python interface.

## Prerequisites

- ROS 2 Jazzy installed
- Robot demo running (mock, Gazebo, or real)
- **Python 3.12** (ROS 2 Jazzy)

## Install fa-py-libraries

:::{code-block} bash
cd ~/
git clone https://github.com/fiveages-sim/fa-py-libraries.git
cd fa-py-libraries
./init.sh all    # Python 3.12 env; installs ros2_robot_interface
:::

`./init.sh all` initializes submodules, creates the env, and installs the Python packages. Then use `./run.sh` (or `./run.sh viser`) for launchers.

:::{admonition} Manual fallback
:class: note

`pip install ros2-robot-interface` on system Python is not the documented entry. If you must install the package alone, do it inside the fa-py-libraries env after `./init.sh env 3.12`.
:::

## Basic Usage

### Connect to Robot

:::{code-block} python
from ros2_robot_interface import RobotInterface

# Initialize
robot = RobotInterface()
robot.connect()

# Check connection
print(f"Connected: {robot.is_connected()}")
:::

### Move Robot

:::{code-block} python
# Move to joint position (radians)
robot.move_j([0.0, -0.5, 0.5, 0.0, 0.5, 0.0])

# Move to Cartesian pose
robot.move_l([0.3, 0.0, 0.4], [1.0, 0.0, 0.0, 0.0])  # [x,y,z], [qw,qx,qy,qz]
:::

### Gripper Control

:::{code-block} python
# Open gripper
robot.gripper_open()

# Close gripper
robot.gripper_close()

# Set position (0.0 = closed, 1.0 = open)
robot.gripper_move(0.5)
:::

### Read State

:::{code-block} python
# Joint positions
joints = robot.get_joint_positions()
print(f"Joints: {joints}")

# End-effector pose
pose = robot.get_ee_pose()
print(f"EE pose: {pose}")
:::

## Example: Pick and Place

:::{code-block} python
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
:::

## With Viser Visualization

Launch Viser from **fa-py-libraries** (`./run.sh viser`). That is the primary entry; do not start it from lerobot_ros2 or treat `pip install ros2-viser` as the product launcher.

:::{code-block} bash
cd ~/fa-py-libraries
./run.sh viser
:::

`ros2_viser` is a library dependency of that command. Embedding `ROS2ViserVisualizer` in your own script is covered on [ros2-viser](../../4-reference/python_apps/3-ros2_viser.md).

## FSM Commands

`/fsm_command` is **`std_msgs/Int32`** (not strings such as `stand` / `walk`). Values and legal transitions depend on the running controller. See [FSM and Topics](../../3-concepts/4-fsm_and_topics.md).

## Async Interface

For non-blocking operations:

:::{code-block} python
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
:::

## Verification

:::{code-block} python
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
:::

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

:::{code-block} bash
cd ~/fa-py-libraries
./init.sh all
:::
