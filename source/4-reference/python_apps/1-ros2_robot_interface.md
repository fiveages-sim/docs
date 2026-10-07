# ros2_robot_interface

High-level Python API for robot control.

**Repository:** [fiveages-sim/ros2_robot_interface](https://github.com/fiveages-sim/ros2_robot_interface)

## Purpose

Simplifies robot control from Python:
- Connection management
- Motion commands
- State queries
- Gripper control

## Installation

Install through **fa-py-libraries** (Python 3.12 env). That repo’s `./init.sh all` installs `ros2_robot_interface` among the other submodules.

:::{code-block} bash
git clone https://github.com/fiveages-sim/fa-py-libraries.git
cd fa-py-libraries
./init.sh all
:::

Datagen / motion-queue path: from a **lerobot_ros2** checkout, `./init.sh all-motion` (or `./init.sh all`) installs the same package as `submodules/ros2_robot_interface`.

:::{admonition} Manual fallback
:class: note

Standalone clone of `ros2_robot_interface` and `pip install -e .` (inside a project venv; `--no-deps` on uv so `rclpy` is not fetched from PyPI) is only for package development outside those umbrellas. Do not treat `pip install ros2-robot-interface` on system Python as the stack entry.
:::

## Quick Start

```python
from ros2_robot_interface import RobotInterface

robot = RobotInterface()
robot.connect()

# Move joints
robot.move_j([0.0, -0.5, 0.5, 0.0, 0.5, 0.0])

# Move Cartesian
robot.move_l([0.3, 0.0, 0.4], [1.0, 0.0, 0.0, 0.0])

# Gripper
robot.gripper_open()
robot.gripper_close()
```

## API Reference

### Connection

```python
robot = RobotInterface()
robot.connect()
robot.disconnect()
robot.is_connected()  # -> bool
```

### Motion

```python
# Joint space
robot.move_j(positions: List[float], duration: float = None)

# Cartesian
robot.move_l(
    position: List[float],  # [x, y, z]
    orientation: List[float],  # [qw, qx, qy, qz]
    duration: float = None
)

# Check motion state
robot.is_moving()  # -> bool
robot.wait_for_motion()
```

### State

```python
# Joint state
robot.get_joint_positions()  # -> List[float]
robot.get_joint_velocities()  # -> List[float]

# Cartesian
robot.get_ee_pose()  # -> Pose
```

### Gripper

```python
robot.gripper_open()
robot.gripper_close()
robot.gripper_move(position: float)  # 0.0-1.0
robot.get_gripper_position()  # -> float
```

### FSM

Controller FSM on `/fsm_command` is **`std_msgs/Int32`**. Do not send invented strings such as `stand` / `walk`. See [FSM and Topics](../../3-concepts/4-fsm_and_topics.md).

## Async Interface

```python
from ros2_robot_interface import AsyncRobotInterface
import asyncio

async def main():
    robot = AsyncRobotInterface()
    await robot.connect()
    await robot.move_j_async([0.0, -0.5, 0.5, 0.0, 0.5, 0.0])

asyncio.run(main())
```

## Configuration

```python
robot = RobotInterface(
    node_name='my_controller',
    namespace='robot1',
    domain_id=42
)
```

## Related

- [Python Interface How-To](../../2-how_to/3-programming/5-python_interface.md)
- [fa-py-libraries](2-fa_py_libraries.md)
