# Controllers Reference

ROS 2 controllers in [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control).

## 分体控制 vs 全身控制

| Mode | Chinese | Controllers | Launch |
|------|---------|-------------|--------|
| **Split** | 分体控制 | Arm MPC: [ocs2_arm_controller](2-ocs2_arm_controller.md). Body / head / hands: [basic_joint_controller](7-basic_joint_controller.md) | `ocs2_arm_controller` `split_body.launch.py` (`launch_mode` `split_body`) |
| **Whole-body** | 全身控制 | Unified [ocs2_wbc_controller](3-ocs2_wbc.md) (`ocs2_wheel_humanoid`) | `ocs2_arm_controller` `full_body.launch.py` (`launch_mode` `full_body`) |

Concepts: [分体控制 vs 全身控制](../../3-concepts/7-split_vs_wbc.md). How-to: [Use basic_joint_controller](../../2-how_to/11-basic_joint.md). `/fsm_command` is `std_msgs/Int32` — [FSM and Topics](../../3-concepts/4-fsm_and_topics.md). End-effectors on OCS2 launches: `type` / `left_type` / `right_type` from [robot_common_launch](../descriptions/2-common.md).

## In This Section

```{toctree}
:maxdepth: 1

7-basic_joint_controller
1-ocs2_ros2
2-ocs2_arm_controller
3-ocs2_wbc
4-ocs2_humanoid
5-lina_planning
6-gripper_teleop_plugins
```

## Quick Reference

| Controller | Purpose | Visibility |
|------------|---------|------------|
| [basic_joint_controller](7-basic_joint_controller.md) | Joint FSM (Home / Hold / MoveJ); body/head/hands in split-body | Public |
| [ocs2_ros2](1-ocs2_ros2.md) | MPC library | External |
| [ocs2_arm_controller](2-ocs2_arm_controller.md) | Arm MPC; 分体控制 with basic_joint | Public |
| [ocs2-wbc-controller](3-ocs2_wbc.md) | 全身控制 (whole-body MPC) | Private |
| [ocs2-humanoid](4-ocs2_humanoid.md) | `ocs2_wheel_humanoid` library | Private |
| [lina_planning](5-lina_planning.md) | Trajectory primitives | Private |
| [Plugins](6-gripper_teleop_plugins.md) | Gripper, teleop | Public |
