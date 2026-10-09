# Controller ROS 2 parameters

ROS 2 parameters for public controllers in [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control) at commit [`9a1da3ba`](https://github.com/fiveages-sim/arms_ros2_control/tree/9a1da3ba3747b3042866422c2269c1d49bb02f48). How to load and inspect them: [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md). Topics and FSM integers: the per-controller pages linked below (not repeated here).

```{admonition} Source of truth
:class: important

Names, types, and defaults come from the linked README or from `auto_declare` / `declare_parameter` at this pin. Runtime vs startup follows the [how-to rule](../../2-how_to/4-controllers/12-ros2_parameters.md#startup-vs-runtime-what-is-verified). Rows marked **未核实** mean **未核实（启动时加载；运行时是否可改未在源码中确认）**.
```

## How to read the tables

Each Meaning cell starts with one of these tags:

| Tag | Evidence |
|-----|----------|
| **Runtime (callback)** | `add_on_set_parameters_callback` in `CtrlComponent` |
| **Runtime (README)** | `arms_target_manager` README: frame overrides are *not* hot like `movel_duration`; `PoseBasedReferenceManager::updateParam()` re-reads the `movel_*` family |
| **Startup only (README)** | Same README: `base_frame` / `left_ee_frame` / `right_ee_frame` need a controller restart |
| **未核实** | Declared at init; no `on_set_parameters` / ParameterListener / README hot-reload claim |

`config/ocs2/*.info` (task file, generated library path, default frames) is **not** the ROS 2 parameter server. `info_file_name` / `robot_name` select which files to load at startup.

## basic_joint_controller

Package README §3: [English](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/basic_joint_controller/README.md) / [Chinese](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/basic_joint_controller/README_zh.md). Topics: [basic_joint_controller](7-basic_joint_controller.md). How-to: [Use basic_joint_controller](../../2-how_to/4-controllers/11-basic_joint.md).

| Parameter | Type / default (README) | Meaning (README) |
|-----------|-------------------------|------------------|
| `update_rate` | int / `1000` | **未核实** — Controller update rate (Hz) |
| `joints` | string[] | **未核实** — Controlled joint names |
| `command_interfaces` | string[] / `["position"]` | **未核实** — Command interfaces |
| `state_interfaces` | string[] / `["position", "velocity"]` | **未核实** — State interfaces |
| `home_1` … `home_10` | double[] (`home_1` required) | **未核实** — Up to 10 Home configurations |
| `home_duration` | double / `3.0` | **未核实** — Home interpolation duration (s) |
| `home_interpolation_type` | string / `"tanh"` | **未核实** — `"tanh"` \| `"linear"` (README_zh also lists `"servo"`) |
| `home_tanh_scale` | double / `3.0` | **未核实** — tanh scale |
| `switch_command_base` | int / `100` | **未核实** — FSM base for Home config switching |
| `movej_duration` | double / `3.0` | **未核实** — MoveJ duration lower bound (s) |
| `movej_interpolation_type` | string / `"tanh"` | **未核实** — `"tanh"` \| `"linear"` \| `"doubles"` \| `"none"` (README_zh: also `"servo"`) |
| `movej_tanh_scale` | double / `3.0` | **未核实** — tanh scale |
| `movej_trajectory_duration` | double / `3.0` | **未核实** — Trajectory duration |
| `movej_trajectory_blend_ratio` | double / `0.0` | **未核实** — Waypoint blend |
| `movej_max_velocity` | double / `2.0` | **未核实** — Peak joint speed cap |
| `movej_max_acceleration` | double / `4.0` | **未核实** — doubles only |
| `movej_max_jerk` | double / `20.0` | **未核实** — doubles only |
| `movej_auto_extend_duration` | bool / `true` | **未核实** — Extend duration to keep the velocity cap |
| `target_command_enabled` | bool / `false` | **未核实** — Hand switch / percent topics |
| `target_command_close_config` | int / `1` | **未核实** — Close pose index in Home configs (0-based) |
| `target_command_open_config` | int / `0` | **未核实** — Open pose index |
| `waist_lifting_enabled` | bool / `false` | **未核实** — Waist topics |
| `waist_lifting_type` | string / `"three_joint"` | **未核实** — `"three_joint"` \| `"single_joint"` |
| `waist_lifting_duration` | double / `3.0` | **未核实** — Waist move duration |
| `waist_lifting_default_parameter` | double[3] / `[0.25, 1.0, 5.0]` | **未核实** — `[max_speed, accel, decel]` |
| `waist_turning_default_parameter` | double[3] / `[0.25, 1.0, 5.0]` | **未核实** — `[max_speed, accel, decel]` |
| `waist_absolute_source_frame` | string / `"base_footprint"` | **未核实** — Absolute `(x, z)` frame (W2 default) |
| `waist_absolute_target_frame` | string / `"body_base"` | **未核实** — `phi` / relative planning frame |
| `waist_l1` / `waist_l2` | double / `0.322` / `0.355` | **未核实** — three_joint link lengths |
| `waist_rotation_direction` | double[3] / `[1, 1, 1]` | **未核实** — three_joint |
| `waist_angle_offset` | double[3] / `[0, 0, 0]` | **未核实** — three_joint |
| `waist_single_joint_direction` | double / `1.0` | **未核实** — single_joint (ARX Lift / Lift 2S) |
| `waist_single_joint_offset` | double / `0.0` | **未核实** — single_joint |
| `waist_single_joint_pitch_joint` | string / `"_no_pitch_"` (README) | **未核实** — Name not in `joints` → pitch disabled. Source `auto_declare` default is `"body_joint2"` |
| `waist_single_joint_pitch_direction` | double / `1.0` | **未核实** — single_joint |
| `waist_single_joint_pitch_offset` | double / `0.0` | **未核实** — single_joint |

Lift 2S example from the same README (`body_joint_controller`): `waist_lifting_enabled: true`, `waist_lifting_type: single_joint`, `waist_absolute_source_frame: base_link`, `waist_absolute_target_frame: lift_link`. Overlay: [`arx_lift2s_description/.../ros2_controllers.yaml`](https://github.com/fiveages-sim/robot-descriptions-arx/blob/main/arx_lift2s_description/config/ros2_control/ros2_controllers.yaml).

Also declared in `BasicJointController::on_init` (not in README §3): `command_prefix`, `hold_first_check_position_threshold` (`0.1`), `hold_position_threshold` (`0.1`), `target_command_hold_joints` (`[]`), `waist_turning_direction` (`1.0`). `StateHome` also declares `home_max_velocity` / `home_max_acceleration` / `home_max_jerk` (`2.0` / `4.0` / `20.0`). All **未核实**.

## adaptive_gripper_controller

README [配置参数](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/adaptive_gripper_controller/README.md). Command channels (not parameters): [Gripper and teleop plugins](6-gripper_teleop_plugins.md). Open/close limits come from `/robot_description`, not from these keys.

| Parameter | Type / default | Meaning (README) |
|-----------|----------------|------------------|
| `joint` | string / `"gripper_joint"` | **未核实** — Controlled joint |
| `use_effort_interface` | bool / `true` | **未核实** — Bind effort state for force feedback |
| `force_threshold` | double / `0.1` | **未核实** — Effort magnitude that triggers feedback |
| `force_feedback_ratio` | double / `0.5` | **未核实** — After trigger: `0.0` stop here, `1.0` continue to original target |

`on_init` stores those four values in members; there is no `on_set_parameters` callback in the public source.

## ocs2_arm_controller

README: [ocs2_arm_controller](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/ocs2_arm_controller/README.md). FSM / launch: [ocs2_arm_controller](2-ocs2_arm_controller.md). Public YAML example: [`cr5_description/.../ros2_controllers.yaml`](https://github.com/fiveages-sim/robot-descriptions-dobot/blob/main/cr5_description/config/ros2_control/ros2_controllers.yaml) (`robot:=cr5` is the demo default). Optional dual-arm overlay on `robot_descriptions` **`feature/agilex` only**: [`taku_description/.../ros2_controllers.yaml`](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/humanoid/Dyna/taku_description/config/ros2_control/ros2_controllers.yaml).

README key list vs this pin’s `auto_declare`:

| README name | In source at this pin |
|-------------|------------------------|
| `joints`, `update_rate`, `home_pos` | Yes (`home_pos` is legacy fallback if `home_1`… are absent) |
| `zero_pos` | Not declared. Source uses `rest_pos` |
| `robot_pkg` | Not declared. Source builds `{robot_name}_description` from `robot_name` (CR5 YAML: `robot_name: cr5`) |
| `force_gains` | Not declared. Source uses `default_gains` (and `pd_gains`) |

### README + machine YAML

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `joints` | string[] | **未核实** — Arm joints |
| `update_rate` | int (CR5 YAML `100`) | **未核实** — Hz; also read from `controller_manager` |
| `command_interfaces` / `state_interfaces` | string[] | **未核实** — Position vs force/MIX detection — [ros2_control here](../../3-concepts/1-ros2_control_here.md) |
| `home_pos` | double[] | **未核实** — Legacy single Home |
| `home_1` … | double[] | **未核实** — Home configs (CR5 YAML uses `home_1`) |
| `rest_pos` | double[] | **未核实** — Extra Home slot when `home_1` is already set |
| `robot_name` | string / `"cr5"` | **未核实** — Selects `{robot_name}_description` and OCS2 files |
| `info_file_name` | string / `"task"` | **未核实** — Loads `{pkg}/config/ocs2/{info_file_name}.info` (**not** a ROS param file) |
| `planning_urdf_path` / `planning_urdf_variant` | string / `""` | **未核实** — Planning URDF from `robot_common_launch` |
| `ocs2_library_folder` | string | **未核实** — Generated OCS2 library directory |
| `future_time_offset` | double / `1.0` | **未核实** — Declared in `CtrlComponent` (CR5 YAML comments: trajectory prediction, s) |
| `mpc_frequency` | int / `0` | **未核实** — Declared in `Ocs2ArmController::on_init` |
| `default_gains` | double[] | **未核实** — Source impedance `[kp, kd]` (README’s `force_gains` name is not declared) |
| `pd_gains` | double[] | **未核实** — Declared for OCS2 state |
| `home_duration` / `home_interpolation_type` / `home_tanh_scale` / `switch_command_base` | same idea as basic_joint (Home defaults `linear` here) | **未核实** — Shared `StateHome` |
| `movej_*` | same names as basic_joint (blend default `0.2` here) | **未核实** — Shared `StateMoveJ` |
| `waist_lifting_*` | subset copied from basic_joint when enabled | **未核实** — Declared only if `waist_lifting_enabled` |

### Frames (startup only)

| Parameter | Type / default | Meaning (README) |
|-----------|----------------|------------------|
| `base_frame` | `task.info` `baseFrame` | **Startup only (README)** — Model / reference base |
| `left_ee_frame` | `task.info` `eeFrame` | **Startup only (README)** — Left tip (YAML may set `left_tcp`) |
| `right_ee_frame` | `task.info` `eeFrame1` | **Startup only (README)** — Right tip |

YAML overrides are injected in memory at Interface construction. Changing a tip requires **restarting the controller**.

### MoveL family (runtime)

Declared in `CtrlComponent`; re-read by `PoseBasedReferenceManager::updateParam()` on interpolate commands. The target-manager README uses `movel_duration` as the hot-reload example.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `movel_duration` | declare `2.0`; CR5 YAML `0.5` | **Runtime (README)** |
| `movel_trajectory_duration` | declare `2.0`; CR5 YAML — | **Runtime (README)** |
| `movel_sample_interval` | declare `0.04`; CR5 YAML `0.04` | **Runtime (README)** |
| `movel_max_linear_velocity` | declare `0.3`; CR5 YAML `0.3` | **Runtime (README)** |
| `movel_max_linear_acceleration` | declare `1.0`; CR5 YAML `1.0` | **Runtime (README)** |
| `movel_max_linear_jerk` | declare `2.0`; CR5 YAML `2.0` | **Runtime (README)** |
| `movel_max_angular_velocity` | declare `1.0`; CR5 YAML `1.0` | **Runtime (README)** |
| `movel_max_angular_acceleration` | declare `2.0`; CR5 YAML `2.0` | **Runtime (README)** |
| `movel_max_angular_jerk` | declare `4.0`; CR5 YAML `4.0` | **Runtime (README)** |
| `movel_auto_extend_duration` | declare `true`; CR5 YAML `true` | **Runtime (README)** |

`cartesian_defaults.*` (`frame_id` default `base_link`, `ik_type` `AUTO`, `max_linear_velocity` `0.25`, …) are declared on `StateMoveJ` for MOVEJ IK MoveL when `lina_planning` is present. **未核实**.

### Verified `on_set_parameters` callbacks

Applied by `CtrlComponent::on_parameter_change`.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `hardware_latency` | `0.2` | **Runtime (callback)** |
| `traj_record_dir` | `"/tmp/traj_record"` | **Runtime (callback)** — applied with enable |
| `traj_record_enabled` | `false` | **Runtime (callback)** |
| `rt_timing_enabled` | `false` | **Runtime (callback)** |

Also declared in the same constructor **without** a callback branch: `cached_ob_state` (`true`), `joint_speed_threshold` (`0.1`), `thread_priority` (`0`), `cpu_affinity` (`[]`), `dds_publish_hz` (`50.0`). **未核实**.

## arms_target_manager

This is a **command node**, not a ros2_control controller. README: [arms_target_manager](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/README.md). Cartesian topics: [FSM and Topics](../../3-concepts/4-fsm_and_topics.md), [Gripper and teleop plugins](6-gripper_teleop_plugins.md).

YAML: package [`config/default.yaml`](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/config/default.yaml), or a robot `config/ocs2/target_manager.yaml`.

`declare_parameter` is in `arms_target_manager_node.cpp` / `HeadMarker::initialize()`. Values are passed into constructors; there is no `on_set_parameters` callback.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `linear_scale` | `0.1` (README/YAML and C++) | **未核实** — Full-stick linear twist (m/s) |
| `angular_scale` | `0.25` (README/YAML and C++) | **未核实** — Full-stick angular twist (rad/s) |
| `control_input_rate` | `50.0` (README/YAML and C++) | **未核实** — Typical `control_input` Hz (feel only; not used in the real-time conversion) |
| `vr_thumbstick_linear_scale` | `0.005` (README/YAML and C++) | **未核实** — VR stick linear step (m/step) |
| `vr_thumbstick_angular_scale` | `0.05` (README/YAML and C++) | **未核实** — VR stick angular step (rad/step) |
| `vr_pose_scale` | `1.0` (README/YAML and C++) | **未核实** — In `default.yaml`; node logs pose scale as fixed `1.0` after start |
| `enable_vr` | README/YAML `false` (`default.yaml`); C++ `true` | **未核实** — Enable VR handler. Launch YAML overrides the C++ default |
| `vr_follow_frame` | `base_footprint` (README/YAML and C++) | **未核实** — Frame used for VR target mapping |
| `marker_fixed_frame` | `base_link` (README and C++) | **未核实** — RViz marker fixed frame |
| `dual_arm_mode` | README/YAML: launch / task.info; C++ `false` | **未核实** — Dual-arm markers |
| `control_base_frame` | README/YAML: launch / task.info; C++ `"world"` | **未核实** — Control base |
| `hand_controllers` | README/YAML: launch / task.info; C++ `[]` | **未核实** — Used to check dual-arm consistency |
| `body_controller_name` | README/YAML —; C++ `"body_joint_controller"` | **未核实** — Body `current_target_joint` topic prefix |
| `reference_link` | README/YAML —; C++ `"head_link2"` | **未核实** — VR / headset reference link |
| `enable_movej_cartesian_markers` | README: `true` if `lina_planning`, else `false`; `full_body.launch.py` sets `false` under WBC. C++: same compile-time default | **未核实** — MOVEJ arm markers → stamped IK MoveL |
| `enable_head_control` | `false` (README/YAML and C++) | **未核实** — Legacy head RPY-to-joint marker (`/head_joint_controller/target_joint_position`) |
| `enable_wbc_head_tracking_marker` | `false` (README/YAML and C++) | **未核实** — WBC Head 6D marker; still needs FSM=OCS2 and `HEAD_TRACKING` |
| `head_link_name` | README/YAML —; C++ `"head_link2"` | **未核实** — Head marker TF link |
| `head_joint_to_rpy_mapping.*` | README/YAML: robot YAML (optional); C++ `""` for `head_joint1..3` | **未核实** — Legacy head joint → yaw/pitch/roll |
| `head_rpy_axis_direction.*` | README/YAML: robot YAML (optional); C++ `1.0` | **未核实** — Sign per RPY name |

Controller frame parameters (`base_frame`, `left_ee_frame`, `right_ee_frame`, WBC `body_frame`) are documented on the OCS2 table above; they belong to the **controller** node, not this marker node.

## ocs2_wbc_controller

`controller/ocs2_wbc_controller` is a **private** submodule. Parameter names after access: that package README. Public launch: `ros2 launch ocs2_arm_controller full_body.launch.py` — [ocs2_wbc_controller](3-ocs2_wbc.md).

Public YAML may still list an `ocs2_wbc_controller:` block (Lift 2S `home_3` / `home_4`; Taku on `feature/agilex`). Treat those keys as machine overlays; the private README is the parameter list.

## Related

- [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md)
- [Hardware interface parameters](../hardware/4-ros2_parameters.md)
- [basic_joint_controller](7-basic_joint_controller.md)
- [ocs2_arm_controller](2-ocs2_arm_controller.md)
- [Gripper and teleop plugins](6-gripper_teleop_plugins.md)
- [ocs2_wbc_controller](3-ocs2_wbc.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
