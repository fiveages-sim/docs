# ocs2_wbc_controller

Whole-body MPC (**全身控制**) for wheeled dual-arm robots, using `ocs2_wheel_humanoid`.

```{admonition} Access Required
:class: warning

`controller/ocs2_wbc_controller` in [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control) is a **private** submodule (`ocs2-wbc-controller`). This page does not invent topics, FSM values, or a standalone `ocs2_wbc_controller` launch file.
```

## Role

- Unified **全身控制** stack: one `ocs2_wbc_controller` instead of arm MPC plus separate body/head joint controllers
- Motion library: `ocs2_wheel_humanoid` (see [ocs2-humanoid](4-ocs2_humanoid.md))

Contrast with **分体控制 (split)**: [ocs2_arm_controller](2-ocs2_arm_controller.md) + [basic_joint_controller](7-basic_joint_controller.md) via `split_body.launch.py`.

## Launch (from `ocs2_arm_controller`)

There is no public README listing a `ros2 launch ocs2_wbc_controller …` entry point. The in-tree path that loads this controller is:

:::{code-block} bash
ros2 launch ocs2_arm_controller full_body.launch.py robot:=<robot>
:::

`full_body.launch.py` (`launch_mode` `full_body`) spawns `ocs2_wbc_controller` when the robot’s `controller_manager` type is `ocs2_wbc_controller/Ocs2WbcController`.

The same file declares `type` and `create_robot_profile_launch_arguments()` (`left_type` / `right_type`, `use_profile_eef`). End-effectors: [ocs2_arm_controller](2-ocs2_arm_controller.md) and [robot_common_launch](../descriptions/2-common.md).

Do not treat `split_body.launch.py` as whole-body control.

## Related

- [ocs2_arm_controller](2-ocs2_arm_controller.md) — 分体控制 / `split_body.launch.py`
- [basic_joint_controller](7-basic_joint_controller.md)
- [ocs2-humanoid](4-ocs2_humanoid.md) — `ocs2_wheel_humanoid`
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
