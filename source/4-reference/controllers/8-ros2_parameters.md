# Controller ROS 2 parameters

ROS 2 parameters for public controllers in [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control) at commit [`9a1da3ba`](https://github.com/fiveages-sim/arms_ros2_control/tree/9a1da3ba3747b3042866422c2269c1d49bb02f48). How to load and inspect them: [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md). Topics and FSM integers: the per-controller pages linked below (not repeated here).

```{admonition} Source of truth
:class: important

Names, types, and defaults come from the linked README or from `auto_declare` / `declare_parameter` at this pin. Runtime vs startup follows the [how-to rule](../../2-how_to/4-controllers/12-ros2_parameters.md#startup-vs-runtime-what-is-verified). Rows marked **未核实** mean **未核实（启动时加载；运行时是否可改未在源码中确认）**.
```

## How to read the tables

| Startup / runtime | Evidence |
|-------------------|----------|
| Runtime (callback) | `add_on_set_parameters_callback` in `CtrlComponent` |
| Runtime (README) | `arms_target_manager` README: frame overrides are *not* hot like `movel_duration`; `PoseBasedReferenceManager::updateParam()` re-reads the `movel_*` family |
| Startup only (README) | Same README: `base_frame` / `left_ee_frame` / `right_ee_frame` need a controller restart |
| 未核实 | Declared at init; no `on_set_parameters` / ParameterListener / README hot-reload claim |

`config/ocs2/*.info` (task file, generated library path, default frames) is **not** the ROS 2 parameter server. `info_file_name` / `robot_name` select which files to load at startup.

## Basic Joint Controller

Package README §3: [English](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/basic_joint_controller/README.md) / [Chinese](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/basic_joint_controller/README_zh.md). Topics: [Basic Joint Controller](7-basic_joint_controller.md) (`basic_joint_controller`). How-to: [Use Basic Joint Controller](../../2-how_to/4-controllers/11-basic_joint.md).

| Parameter | Type / default (README) | Meaning (README) | Startup / runtime |
|-----------|-------------------------|------------------|-------------------|
| `update_rate` | int / `1000` | Controller update rate (Hz) | 未核实 |
| `joints` | string[] | Controlled joint names | 未核实 |
| `command_interfaces` | string[] / `["position"]` | Command interfaces | 未核实 |
| `state_interfaces` | string[] / `["position", "velocity"]` | State interfaces | 未核实 |
| `home_1` … `home_10` | double[] (`home_1` required) | Up to 10 Home configurations | 未核实 |
| `home_duration` | double / `3.0` | Home interpolation duration (s) | 未核实 |
| `home_interpolation_type` | string / `"tanh"` | `"tanh"` \| `"linear"` (README_zh also lists `"servo"`) | 未核实 |
| `home_tanh_scale` | double / `3.0` | tanh scale | 未核实 |
| `switch_command_base` | int / `100` | FSM base for Home config switching | 未核实 |
| `movej_duration` | double / `3.0` | MoveJ duration lower bound (s) | 未核实 |
| `movej_interpolation_type` | string / `"tanh"` | `"tanh"` \| `"linear"` \| `"doubles"` \| `"none"` (README_zh: also `"servo"`) | 未核实 |
| `movej_tanh_scale` | double / `3.0` | tanh scale | 未核实 |
| `movej_trajectory_duration` | double / `3.0` | Trajectory duration | 未核实 |
| `movej_trajectory_blend_ratio` | double / `0.0` | Waypoint blend | 未核实 |
| `movej_max_velocity` | double / `2.0` | Peak joint speed cap | 未核实 |
| `movej_max_acceleration` | double / `4.0` | doubles only | 未核实 |
| `movej_max_jerk` | double / `20.0` | doubles only | 未核实 |
| `movej_auto_extend_duration` | bool / `true` | Extend duration to keep the velocity cap | 未核实 |
| `target_command_enabled` | bool / `false` | Hand switch / percent topics | 未核实 |
| `target_command_close_config` | int / `1` | Close pose index in Home configs (0-based) | 未核实 |
| `target_command_open_config` | int / `0` | Open pose index | 未核实 |
| `waist_lifting_enabled` | bool / `false` | Waist topics | 未核实 |
| `waist_lifting_type` | string / `"three_joint"` | `"three_joint"` \| `"single_joint"` | 未核实 |
| `waist_lifting_duration` | double / `3.0` | Waist move duration | 未核实 |
| `waist_lifting_default_parameter` | double[3] / `[0.25, 1.0, 5.0]` | `[max_speed, accel, decel]` | 未核实 |
| `waist_turning_default_parameter` | double[3] / `[0.25, 1.0, 5.0]` | `[max_speed, accel, decel]` | 未核实 |
| `waist_absolute_source_frame` | string / `"base_footprint"` | Absolute `(x, z)` frame (W2 default) | 未核实 |
| `waist_absolute_target_frame` | string / `"body_base"` | `phi` / relative planning frame | 未核实 |
| `waist_l1` / `waist_l2` | double / `0.322` / `0.355` | three_joint link lengths | 未核实 |
| `waist_rotation_direction` | double[3] / `[1, 1, 1]` | three_joint | 未核实 |
| `waist_angle_offset` | double[3] / `[0, 0, 0]` | three_joint | 未核实 |
| `waist_single_joint_direction` | double / `1.0` | single_joint (ARX Lift / Lift 2S) | 未核实 |
| `waist_single_joint_offset` | double / `0.0` | single_joint | 未核实 |
| `waist_single_joint_pitch_joint` | string / `"_no_pitch_"` (README) | Name not in `joints` → pitch disabled. Source `auto_declare` default is `"body_joint2"` | 未核实 |
| `waist_single_joint_pitch_direction` | double / `1.0` | single_joint | 未核实 |
| `waist_single_joint_pitch_offset` | double / `0.0` | single_joint | 未核实 |

Lift 2S example from the same README (`body_joint_controller`): `waist_lifting_enabled: true`, `waist_lifting_type: single_joint`, `waist_absolute_source_frame: base_link`, `waist_absolute_target_frame: lift_link`. Overlay: [`arx_lift2s_description/.../ros2_controllers.yaml`](https://github.com/fiveages-sim/robot-descriptions-arx/blob/main/arx_lift2s_description/config/ros2_control/ros2_controllers.yaml).

Also declared in `BasicJointController::on_init` (not in README §3): `command_prefix`, `hold_first_check_position_threshold` (`0.1`), `hold_position_threshold` (`0.1`), `target_command_hold_joints` (`[]`), `waist_turning_direction` (`1.0`). `StateHome` also declares `home_max_velocity` / `home_max_acceleration` / `home_max_jerk` (`2.0` / `4.0` / `20.0`). All **未核实**.

## Adaptive Gripper Controller

README [配置参数](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/adaptive_gripper_controller/README.md) for `adaptive_gripper_controller`. Command channels (not parameters): [Gripper and teleop plugins](6-gripper_teleop_plugins.md). Open/close limits come from `/robot_description`, not from these keys.

| Parameter | Type / default | Meaning (README) | Startup / runtime |
|-----------|----------------|------------------|-------------------|
| `joint` | string / `"gripper_joint"` | Controlled joint | 未核实 |
| `use_effort_interface` | bool / `true` | Bind effort state for force feedback | 未核实 |
| `force_threshold` | double / `0.1` | Effort magnitude that triggers feedback | 未核实 |
| `force_feedback_ratio` | double / `0.5` | After trigger: `0.0` stop here, `1.0` continue to original target | 未核实 |

`on_init` stores those four values in members; there is no `on_set_parameters` callback in the public source.

## OCS2 Arm Controller

README: [ocs2_arm_controller](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/ocs2_arm_controller/README.md). FSM / launch: [OCS2 Arm Controller](2-ocs2_arm_controller.md) (`ocs2_arm_controller`). Public YAML example: [`cr5_description/.../ros2_controllers.yaml`](https://github.com/fiveages-sim/robot-descriptions-dobot/blob/main/cr5_description/config/ros2_control/ros2_controllers.yaml) (`robot:=cr5` is the demo default). Optional dual-arm overlay on `robot_descriptions` **`feature/agilex` only**: [`taku_description/.../ros2_controllers.yaml`](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/humanoid/Dyna/taku_description/config/ros2_control/ros2_controllers.yaml).

README key list vs this pin’s `auto_declare`:

| README name | In source at this pin |
|-------------|------------------------|
| `joints`, `update_rate`, `home_pos` | Yes (`home_pos` is legacy fallback if `home_1`… are absent) |
| `zero_pos` | Not declared. Source uses `rest_pos` |
| `robot_pkg` | Not declared. Source builds `{robot_name}_description` from `robot_name` (CR5 YAML: `robot_name: cr5`) |
| `force_gains` | Not declared. Source uses `default_gains` (and `pd_gains`) |

### README + machine YAML

| Parameter | Type / default | Meaning | Startup / runtime |
|-----------|----------------|---------|-------------------|
| `joints` | string[] | Arm joints | 未核实 |
| `update_rate` | int (CR5 YAML `100`) | Hz; also read from `controller_manager` | 未核实 |
| `command_interfaces` / `state_interfaces` | string[] | Position vs force/MIX detection — [ros2_control here](../../3-concepts/1-ros2_control_here.md) | 未核实 |
| `home_pos` | double[] | Legacy single Home | 未核实 |
| `home_1` … | double[] | Home configs (CR5 YAML uses `home_1`) | 未核实 |
| `rest_pos` | double[] | Extra Home slot when `home_1` is already set | 未核实 |
| `robot_name` | string / `"cr5"` | Selects `{robot_name}_description` and OCS2 files | 未核实 |
| `info_file_name` | string / `"task"` | Loads `{pkg}/config/ocs2/{info_file_name}.info` (**not** a ROS param file) | 未核实 |
| `planning_urdf_path` / `planning_urdf_variant` | string / `""` | Planning URDF from `robot_common_launch` | 未核实 |
| `ocs2_library_folder` | string | Generated OCS2 library directory | 未核实 |
| `future_time_offset` | double / `1.0` (CR5 YAML comments: trajectory prediction, s) | Declared in `CtrlComponent` | 未核实 |
| `mpc_frequency` | int / `0` | Declared in `Ocs2ArmController::on_init` | 未核实 |
| `default_gains` | double[] | Source impedance `[kp, kd]` (README’s `force_gains` name is not declared) | 未核实 |
| `pd_gains` | double[] | Declared for OCS2 state | 未核实 |
| `home_duration` / `home_interpolation_type` / `home_tanh_scale` / `switch_command_base` | same idea as basic_joint (Home defaults `linear` here) | Shared `StateHome` | 未核实 |
| `movej_*` | same names as basic_joint (blend default `0.2` here) | Shared `StateMoveJ` | 未核实 |
| `waist_lifting_*` | subset copied from basic_joint when enabled | Declared only if `waist_lifting_enabled` | 未核实 |

### Frames (startup only)

| Parameter | Default | Meaning (README) | Startup / runtime |
|-----------|---------|------------------|-------------------|
| `base_frame` | `task.info` `baseFrame` | Model / reference base | Startup only (README) |
| `left_ee_frame` | `task.info` `eeFrame` | Left tip (YAML may set `left_tcp`) | Startup only (README) |
| `right_ee_frame` | `task.info` `eeFrame1` | Right tip | Startup only (README) |

YAML overrides are injected in memory at Interface construction. Changing a tip requires **restarting the controller**.

### MoveL family (runtime)

Declared in `CtrlComponent`; re-read by `PoseBasedReferenceManager::updateParam()` on interpolate commands. The target-manager README uses `movel_duration` as the hot-reload example.

| Parameter | Default (source declare) | CR5 YAML | Startup / runtime |
|-----------|--------------------------|----------|-------------------|
| `movel_duration` | `2.0` | `0.5` | Runtime (README) |
| `movel_trajectory_duration` | `2.0` | — | Runtime (README) |
| `movel_sample_interval` | `0.04` | `0.04` | Runtime (README) |
| `movel_max_linear_velocity` | `0.3` | `0.3` | Runtime (README) |
| `movel_max_linear_acceleration` | `1.0` | `1.0` | Runtime (README) |
| `movel_max_linear_jerk` | `2.0` | `2.0` | Runtime (README) |
| `movel_max_angular_velocity` | `1.0` | `1.0` | Runtime (README) |
| `movel_max_angular_acceleration` | `2.0` | `2.0` | Runtime (README) |
| `movel_max_angular_jerk` | `4.0` | `4.0` | Runtime (README) |
| `movel_auto_extend_duration` | `true` | `true` | Runtime (README) |

`cartesian_defaults.*` (`frame_id` default `base_link`, `ik_type` `AUTO`, `max_linear_velocity` `0.25`, …) are declared on `StateMoveJ` for MOVEJ IK MoveL when `lina_planning` is present. **未核实**.

### Verified `on_set_parameters` callbacks

| Parameter | Default | Applied by `CtrlComponent::on_parameter_change` | Startup / runtime |
|-----------|---------|--------------------------------------------------|-------------------|
| `hardware_latency` | `0.2` | Yes | Runtime (callback) |
| `traj_record_dir` | `"/tmp/traj_record"` | Yes (applied with enable) | Runtime (callback) |
| `traj_record_enabled` | `false` | Yes | Runtime (callback) |
| `rt_timing_enabled` | `false` | Yes | Runtime (callback) |

Also declared in the same constructor **without** a callback branch: `cached_ob_state` (`true`), `joint_speed_threshold` (`0.1`), `thread_priority` (`0`), `cpu_affinity` (`[]`), `dds_publish_hz` (`50.0`). **未核实**.

## arms_target_manager

This is a **command node**, not a ros2_control controller. README: [arms_target_manager](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/README.md). Cartesian topics: [FSM and Topics](../../3-concepts/4-fsm_and_topics.md), [Gripper and teleop plugins](6-gripper_teleop_plugins.md).

YAML: package [`config/default.yaml`](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/config/default.yaml), or a robot `config/ocs2/target_manager.yaml`.

`declare_parameter` is in `arms_target_manager_node.cpp` / `HeadMarker::initialize()`. Values are passed into constructors; there is no `on_set_parameters` callback.

| Parameter | README / YAML default | C++ declare default | Meaning | Startup / runtime |
|-----------|----------------------|---------------------|---------|-------------------|
| `linear_scale` | `0.1` | `0.1` | Full-stick linear twist (m/s) | 未核实 |
| `angular_scale` | `0.25` | `0.25` | Full-stick angular twist (rad/s) | 未核实 |
| `control_input_rate` | `50.0` | `50.0` | Typical `control_input` Hz (feel only; not used in the real-time conversion) | 未核实 |
| `vr_thumbstick_linear_scale` | `0.005` | `0.005` | VR stick linear step (m/step) | 未核实 |
| `vr_thumbstick_angular_scale` | `0.05` | `0.05` | VR stick angular step (rad/step) | 未核实 |
| `vr_pose_scale` | `1.0` | `1.0` | In `default.yaml`; node logs pose scale as fixed `1.0` after start | 未核实 |
| `enable_vr` | `false` (`default.yaml`) | `true` | Enable VR handler. Launch YAML overrides the C++ default | 未核实 |
| `vr_follow_frame` | `base_footprint` | `base_footprint` | Frame used for VR target mapping | 未核实 |
| `marker_fixed_frame` | `base_link` (README) | `base_link` | RViz marker fixed frame | 未核实 |
| `dual_arm_mode` | launch / task.info | `false` | Dual-arm markers | 未核实 |
| `control_base_frame` | launch / task.info | `"world"` | Control base | 未核实 |
| `hand_controllers` | launch / task.info | `[]` | Used to check dual-arm consistency | 未核实 |
| `body_controller_name` | — | `"body_joint_controller"` | Body `current_target_joint` topic prefix | 未核实 |
| `reference_link` | — | `"head_link2"` | VR / headset reference link | 未核实 |
| `enable_movej_cartesian_markers` | README: `true` if `lina_planning`, else `false`; `full_body.launch.py` sets `false` under WBC | same compile-time default | MOVEJ arm markers → stamped IK MoveL | 未核实 |
| `enable_head_control` | `false` | `false` | Legacy head RPY-to-joint marker (`/head_joint_controller/target_joint_position`) | 未核实 |
| `enable_wbc_head_tracking_marker` | `false` | `false` | WBC Head 6D marker; still needs FSM=OCS2 and `HEAD_TRACKING` | 未核实 |
| `head_link_name` | — | `"head_link2"` | Head marker TF link | 未核实 |
| `head_joint_to_rpy_mapping.*` | robot YAML (optional) | `""` for `head_joint1..3` | Legacy head joint → yaw/pitch/roll | 未核实 |
| `head_rpy_axis_direction.*` | robot YAML (optional) | `1.0` | Sign per RPY name | 未核实 |

Controller frame parameters (`base_frame`, `left_ee_frame`, `right_ee_frame`, WBC `body_frame`) are documented on the OCS2 table above; they belong to the **controller** node, not this marker node.

## OCS2 WBC Controller

`controller/ocs2_wbc_controller` is a **private** submodule. Parameter names after access: that package README. Public launch: `ros2 launch ocs2_arm_controller full_body.launch.py` — [OCS2 WBC Controller](3-ocs2_wbc.md).

Public YAML may still list an `ocs2_wbc_controller:` block (Lift 2S `home_3` / `home_4`; Taku on `feature/agilex`). Treat those keys as machine overlays; the private README is the parameter list.

## Related

- [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md)
- [Hardware Interface parameters](../hardware/4-ros2_parameters.md)
- [Basic Joint Controller](7-basic_joint_controller.md)
- [OCS2 Arm Controller](2-ocs2_arm_controller.md)
- [Gripper and teleop plugins](6-gripper_teleop_plugins.md)
- [OCS2 WBC Controller](3-ocs2_wbc.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
