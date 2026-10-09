# ocs2_wbc_controller

Whole-body MPC (**全身控制**) for wheeled dual-arm robots, using `ocs2_wheel_humanoid`.

```{admonition} Access Required
:class: warning

`controller/ocs2_wbc_controller` in [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control) is a **private** submodule (`ocs2-wbc-controller`). Topics, FSM values, and launch names are in that package README after access. The in-tree loader on the public side is `full_body.launch.py`.
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

`split_body.launch.py` is the split (分体) path; whole-body control uses `full_body.launch.py`.

## Public command surface

Extra FSM states stay in the private package README after access. From public sources, 全身 uses:

- Cartesian body / head: `/body_target*`, `/head_target*` ([arms_target_manager](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/README.md))
- `/mode_command` (`std_msgs/String`) and `/ocs2_wbc_controller/current_state` (`WbcCurrentState`)
- Shared action / service types: [`arms_ros2_control_msgs` README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_ros2_control_msgs/README.md)

:::{admonition} Whole-body (WBC) availability
:class: warning

These topics need **`ocs2_wbc_controller`** and that robot’s 全身 launch/config. Default mock demos (`demo.launch.py`) and 分体 (`split_body.launch.py`) do **not** imply they are present. Capability bits (`WbcCapability`) are machine-dependent. Public Taku mock uses `split_body.launch.py robot:=taku` (arm MPC + body/head basic + grippers), not WBC. `full_body.launch.py robot:=taku` needs the private WBC submodule; shipping `config/ocs2/fixed_base_tcp.info` is not enough. When that config and the private module are present, Taku full-body default `headMode` is `HEAD_GAZE` (gaze on `head_camera_mid_optical_frame`); `target_manager.yaml` has `enable_head_control: false`. Head 6D tracking (`HEAD_TRACKING`) is only there when `head_tracking_ee_enabled` is true. Taku body-relative rest is around x≈−0.21, not Bot2 `[0, 0.25]`. Full tables: [FSM and Topics](../../3-concepts/4-fsm_and_topics.md).
:::

## Related

- [Controller ROS 2 parameters](8-ros2_parameters.md) — public overlay keys; full list is the private package README
- [ocs2_arm_controller](2-ocs2_arm_controller.md) — 分体控制 / `split_body.launch.py`
- [basic_joint_controller](7-basic_joint_controller.md)
- [ocs2-humanoid](4-ocs2_humanoid.md) — `ocs2_wheel_humanoid`
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
- [ros2_robot_interface](../python_apps/1-ros2_robot_interface.md)
- [分体控制 vs 全身控制](../../3-concepts/7-split_vs_wbc.md)
