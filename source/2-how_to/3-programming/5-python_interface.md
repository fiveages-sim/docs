# Python Interface

Control robots from Python with `ROS2RobotInterface`.

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

## Connect, read, command

Classes: `ROS2RobotInterface` and `ROS2RobotInterfaceConfig`. The README “Basic Example” (config, `connect()`, `get_joint_state()`, `left_arm_handler`) is on [ros2_robot_interface](../../4-reference/python_apps/1-ros2_robot_interface.md).

:::{code-block} python
from geometry_msgs.msg import Pose
from ros2_robot_interface import (
    FSM_HOLD,
    ROS2RobotInterface,
    ROS2RobotInterfaceConfig,
)

config = ROS2RobotInterfaceConfig(
    joint_states_topic="/joint_states",
    end_effector_pose_topic="/left_current_pose",
    end_effector_target_topic="/left_target",
)
interface = ROS2RobotInterface(config)
interface.connect()

joint_state = interface.get_joint_state()
if joint_state:
    print(joint_state["positions"])

pose = interface.left_arm_handler.get_pose()

target = Pose()
target.position.x = 0.5
target.position.z = 0.3
target.orientation.w = 1.0
interface.left_arm_handler.send_target(target)

# Stroke in hardware units (not a 0–1 percent)
interface.left_gripper_handler.send_joint_positions(0.01)

interface.send_fsm_command(FSM_HOLD)
interface.disconnect()
:::

`right_arm_handler` / `right_gripper_handler` exist in dual-arm mode after `connect()` sees `/right_current_pose`. Cartesian vs joint vs gripper topics (including `*/twist`, `*/relative`, `target_percent`, and waist `waist_*`), plus `execute_*_action` and `execute_path`: [ros2_robot_interface](../../4-reference/python_apps/1-ros2_robot_interface.md) (Topic / Action / Service ↔ API map).

## With Viser visualization

Launch Viser from **fa-py-libraries** (`./run.sh viser`). That is the primary entry; do not start it from lerobot_ros2 or treat `pip install ros2-viser` as the product launcher.

:::{code-block} bash
cd ~/fa-py-libraries
./run.sh viser
:::

`ros2_viser` is a library dependency of that command. Embedding `ROS2ViserVisualizer` in your own script is covered on [ros2-viser](../../4-reference/python_apps/3-ros2_viser.md).

## FSM commands

`/fsm_command` is **`std_msgs/Int32`** (not strings such as `stand` / `walk`). Send integers with `send_fsm_command` (`1` HOME, `2` HOLD, `3` OCS2, `4` MOVEJ, `5` COMPLIANCE). Values and legal transitions depend on the running controller. See [FSM and Topics](../../3-concepts/4-fsm_and_topics.md).

WBC body / arm / base strings go to `/mode_command` via `send_mode_command`, which is a different topic from `/fsm_command`. That path needs `ocs2_wbc_controller` and 全身 launch/config — default mock / 分体 demos do not imply it.

Parameterized MoveL / MoveC / MoveJ wait for a result with `execute_movel_action`, `execute_movec_action_*`, and `execute_joint_trajectory_action`. Dual-arm Cartesian path uses the `execute_path` **service** (not the deprecated `/target_path` topic).

## Full method list

Method signatures, arrival checks, and actions: [API_REFERENCE.md](https://github.com/fiveages-sim/ros2_robot_interface/blob/main/API_REFERENCE.md).

## Troubleshooting

### Connection fails

- Ensure the robot demo is running
- Check ROS 2 domain ID matches
- Verify topics are publishing: `ros2 topic list`
- `get_joint_state()` / `get_pose()` return `None` until the first message; command methods raise `ROS2NotConnectedError` if you never called `connect()`

### Motion commands ignored

- Check the controller FSM (`get_fsm_state()` / `ros2 topic echo /fsm_state`)
- Pose targets need OCS2; joint targets need MOVEJ (the interface can switch these for you)
- Verify the target is within joint limits

### Import error

:::{code-block} bash
cd ~/fa-py-libraries
./init.sh all
:::
