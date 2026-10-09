# Classical algorithm engineer

For engineers who keep their own vision, planning, or visual-servoing stack and need a stable Python / ROS 2 interface to the robot.

## 1. Workspace and a moving robot

1. [Install Environment](../1-getting_started/2-install_environment.md) — Ubuntu 24.04, ROS 2 Jazzy.
2. [open-deploy-ws Setup](../1-getting_started/3-open_deploy_ws.md) or a lean-branch how-to if you are on a single public robot.
3. [Run Mock Demo](../2-how_to/1-basic_operations/1-run_mock_demo.md) — confirm FSM / motion before hardware.
4. [Switch Robot](../2-how_to/1-basic_operations/2-switch_robot.md) — `robot:=` key and end-effector `type` / `left_type` / `right_type`.

## 2. Install the Python interface

1. [fa-py-libraries](../4-reference/python_apps/2-fa_py_libraries.md) — `./init.sh all` (Python 3.12).
2. [Python Interface](../2-how_to/3-programming/5-python_interface.md) — `ROS2RobotInterface`, handlers, read state.
3. [ros2_robot_interface](../4-reference/python_apps/1-ros2_robot_interface.md) — API names used on those pages.

Entry is the fa-py-libraries env, not `pip install ros2-robot-interface` on system Python.

## 3. Hook your own vision or servoing

This site does **not** document a vision-guided or visual-servoing pipeline (no camera calibration how-to, no servo gain list).

Use the interface as the robot side of **your** loop:

- Cartesian: `left_arm_handler.send_target_stamped` / `get_pose` on [ros2_robot_interface](../4-reference/python_apps/1-ros2_robot_interface.md)
- Joints: `left_arm_handler.send_joint_positions` / `get_joint_state`
- Blocking MoveL / MoveJ: `execute_movel_action` / `execute_joint_trajectory_action` (Action, not the topic rows)
- FSM: [FSM and Topics](../3-concepts/4-fsm_and_topics.md) (`/fsm_command` is `std_msgs/Int32`; WBC `/mode_command` needs 全身)

Camera plugins under [lerobot_ros2](../4-reference/python_apps/4-lerobot_ros2.md) (`lerobot_camera_ros2`) are for **dataset recording**, not a visual-servo controller.

## 4. Optional: see the robot while you debug

[ros2-viser](../4-reference/python_apps/3-ros2_viser.md) — `./run.sh viser` after the stack is up.

## Related

- [Controllers](../4-reference/controllers/0-index.md)
- [Use Basic Joint Controller](../2-how_to/4-controllers/11-basic_joint.md)
- [Configure ROS 2 controller parameters](../2-how_to/4-controllers/12-ros2_parameters.md)
