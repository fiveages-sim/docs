# Controllers Reference

ROS 2 controllers in [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control).

## 分体控制 vs 全身控制

| Mode | Chinese | Controllers | Launch |
|------|---------|-------------|--------|
| **Split Body** | 分体控制 | Arm MPC: [OCS2 Arm Controller](2-ocs2_arm_controller.md). Body / head / dexterous hands: [Basic Joint Controller](7-basic_joint_controller.md) | `ocs2_arm_controller` `split_body.launch.py` (`launch_mode` `split_body`) |
| **Full Body** | 全身控制 | Unified [OCS2 WBC Controller](3-ocs2_wbc.md) (`ocs2_wbc_controller`, `ocs2_wheel_humanoid`) | `ocs2_arm_controller` `full_body.launch.py` (`launch_mode` `full_body`) |

Concepts: [分体控制 vs 全身控制](../../3-concepts/7-split_vs_wbc.md). How-to: [Use Basic Joint Controller](../../2-how_to/4-controllers/11-basic_joint.md). `/fsm_command` is `std_msgs/Int32`; Action / Service types and WBC body/head topics: [FSM and Topics](../../3-concepts/4-fsm_and_topics.md). Msg / srv / action definitions: [`arms_ros2_control_msgs` README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_ros2_control_msgs/README.md). End-effectors on OCS2 launches: `type` / `left_type` / `right_type` from [robot_common_launch](../descriptions/2-common.md).

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
8-ros2_parameters
```

## Quick Reference

| Controller | Purpose | Visibility |
|------------|---------|------------|
| [Basic Joint Controller](7-basic_joint_controller.md) | Joint FSM (HOME / HOLD / MOVEJ); body/head/dexterous hands in 分体控制 | Public |
| [ocs2_ros2](1-ocs2_ros2.md) | MPC library | External |
| [OCS2 Arm Controller](2-ocs2_arm_controller.md) | Arm MPC; 分体控制 with Basic Joint Controller | Public |
| [OCS2 WBC Controller](3-ocs2_wbc.md) | 全身控制 (`ocs2_wbc_controller`) | Private |
| [ocs2-humanoid](4-ocs2_humanoid.md) | `ocs2_wheel_humanoid` library | Private |
| [lina_planning](5-lina_planning.md) | Trajectory primitives | Private |
| [Plugins](6-gripper_teleop_plugins.md) | Adaptive Gripper Controller (`adaptive_gripper_controller`; three channels + force feedback); `arms_target_manager` Cartesian topics | Public |
| [ROS 2 parameters](8-ros2_parameters.md) | Per-controller param tables; startup vs runtime | Public |
