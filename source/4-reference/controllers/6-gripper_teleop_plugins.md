# Gripper and Teleop Plugins

Controller plugins for grippers and teleoperation.

**Repository:** [fiveages-sim/arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control)

## adaptive_gripper_controller

Listed in the [arms_ros2_control README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/README.md). The launch stack does **not** take `gripper:=`. Attach an end-effector with `type` / `left_type` / `right_type` (and optional `robot_profile` / `use_profile_eef`) from [robot_common_launch](../descriptions/2-common.md).

Topics, plugin class names, and command examples: see that package’s README. This page does not invent `/gripper/command`, `/target_pose`, or an `arms_teleop_controller` package.

The command package in the same repo is `command/` (`arms_target_manager`, `arms_teleop`, …) — not a fabricated `arms_teleop_controller` / `target_manager_controller`. Demo launch starts `arms_target_manager` when `enable_arms_target_manager` is `true`.

## Related

- [ocs2_arm_controller](2-ocs2_arm_controller.md)
- [ros2_control here](../../3-concepts/1-ros2_control_here.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
