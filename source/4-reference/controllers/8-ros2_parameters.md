# Controller ROS 2 parameters

ROS 2 parameters for public controllers in [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control). Code pin: [`9a1da3ba`](https://github.com/fiveages-sim/arms_ros2_control/tree/9a1da3ba3747b3042866422c2269c1d49bb02f48). **Startup / Runtime** wording matches the READMEs in [pull request #120](https://github.com/fiveages-sim/arms_ros2_control/pull/120) (`e1b7a147`). How to load and inspect: [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md). Topics and FSM integers: the per-controller pages (not repeated here).

```{admonition} Source of truth
:class: important

Names, types, and defaults come from the linked README (or `auto_declare` / `declare_parameter` at the code pin when the README says so). **When** tags are **Runtime** / **Startup only** / **Unverified** as in #120. Framework commons (`joints`, `update_rate`, `command_interfaces`, `state_interfaces`, optional `command_prefix`) are on the [how-to](../../2-how_to/4-controllers/12-ros2_parameters.md#framework-common-parameters) only.
```

## How to read the tables

Three columns: **Parameter**, **Type / default**, **Meaning** (the **When** tag is the last sentence of Meaning).

| Tag | Evidence (#120) |
|-----|-----------------|
| **Runtime** | `get_parameter` on the next HOME enter, MOVEJ enter / joint command, waist position plan, interpolating MoveL, or MOVEJ `cartesian_defaults` |
| **Startup only** | Member set in `on_init` / constructor / first waist-planner create; or README “reload / restart” |
| **Unverified** | No documented key in these tables is Unverified in #120 |

`config/ocs2/*.info` is **not** the ROS 2 parameter server. `robot_name` selects `{robot_name}_description`; the task file is `{pkg}/config/ocs2/task.info` unless launch YAML sets `info_file_name`.

(basic-joint-controller)=
## Basic Joint Controller

Plugin `basic_joint_controller/BasicJointController`. Also declares the [framework-common keys](../../2-how_to/4-controllers/12-ros2_parameters.md#framework-common-parameters). Home keys: [shared Home](../../2-how_to/4-controllers/12-ros2_parameters.md#home-statehome). README [#120](https://github.com/fiveages-sim/arms_ros2_control/blob/e1b7a147effca2f29f7cced0b2942837b096c1ff/controller/basic_joint_controller/README.md) / [README_zh](https://github.com/fiveages-sim/arms_ros2_control/blob/e1b7a147effca2f29f7cced0b2942837b096c1ff/controller/basic_joint_controller/README_zh.md). Topics: [Basic Joint Controller](7-basic_joint_controller.md). How-to: [Use Basic Joint Controller](../../2-how_to/4-controllers/11-basic_joint.md).

This is the **primary MoveJ parameter table**. 灵巧手 uses `target_command_*` on this controller (not **Adaptive Gripper Controller**).

### MoveJ

README defaults below. Shared C++ `auto_declare` on **OCS2 Arm Controller** uses `movej_interpolation_type` `"linear"` and `movej_trajectory_blend_ratio` `0.2` — see that page’s delta, not a second MoveJ table.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `movej_duration` | double / `3.0` | Lower bound for `target_joint_position` (tanh / linear / doubles). **Runtime**. |
| `movej_interpolation_type` | string / `"tanh"` (README YAML) | `"tanh"` \| `"linear"` \| `"doubles"` \| `"none"` (README_zh also `"servo"`). **Runtime**. |
| `movej_tanh_scale` | double / `3.0` | tanh scale. **Runtime**. |
| `movej_trajectory_duration` | double / `3.0` | Multi-waypoint duration. **Runtime**. |
| `movej_trajectory_blend_ratio` | double / `0.0` | Waypoint blend. **Runtime**. |
| `movej_max_velocity` | double / `2.0` | Peak joint speed; may extend duration. **Runtime**. |
| `movej_max_acceleration` | double / `4.0` | doubles only. **Runtime**. |
| `movej_max_jerk` | double / `20.0` | doubles only. **Runtime**. |
| `movej_auto_extend_duration` | bool / `true` | `false` keeps a fixed duration. **Runtime**. |

`none` is not duration-extended. `joint_trajectory_with_para` uses the same vel/acc/jerk when a waypoint omits those arrays.

MOVEJ `cartesian_defaults.*` (IK MoveL when `lina_planning` is present) are **Runtime** on the next MOVEJ command — [`arms_target_manager` README in #120](https://github.com/fiveages-sim/arms_ros2_control/blob/e1b7a147effca2f29f7cced0b2942837b096c1ff/command/arms_target_manager/README.md).

### 灵巧手 (`target_command`)

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `target_command_enabled` | bool / `false` | Switch/percent topics. **Startup only**. |
| `target_command_close_config` | int / `1` | Close pose index in Home configs (0-based). **Startup only**. |
| `target_command_open_config` | int / `0` | Open pose index. **Startup only**. |

### Waist

Only `waist_lifting_duration` is **Runtime**. Type, speed triples, kinematics, and TF frames are **Startup only** (first planner create or `on_init`).

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `waist_lifting_enabled` | bool / `false` | Declares waist params and topics. **Startup only**. |
| `waist_lifting_type` | string / `"three_joint"` | `"three_joint"` \| `"single_joint"`. **Startup only**. |
| `waist_lifting_duration` | double / `3.0` | Re-read on the next waist position plan. **Runtime**. |
| `waist_lifting_default_parameter` | double[3] / `[0.25, 1.0, 5.0]` | `[max_speed, accel, decel]`. **Startup only**. |
| `waist_turning_default_parameter` | double[3] / `[0.25, 1.0, 5.0]` | `[max_speed, accel, decel]`. **Startup only**. |
| `waist_absolute_source_frame` | string / `"base_footprint"` | Absolute `(x, z)` (W2 default). **Startup only**. |
| `waist_absolute_target_frame` | string / `"body_base"` | `phi` / relative planning. **Startup only**. |
| `waist_l1` / `waist_l2` | double / `0.322` / `0.355` | three_joint. **Startup only**. |
| `waist_rotation_direction` | double[3] / `[1, 1, 1]` | three_joint. **Startup only**. |
| `waist_angle_offset` | double[3] / `[0, 0, 0]` | three_joint. **Startup only**. |
| `waist_single_joint_direction` | double / `1.0` | single_joint (ARX Lift / Lift 2S). **Startup only**. |
| `waist_single_joint_offset` | double / `0.0` | single_joint. **Startup only**. |
| `waist_single_joint_pitch_joint` | string / `"_no_pitch_"` (README) | Name not in `joints` → pitch disabled. Source `auto_declare` default is `"body_joint2"`. **Startup only**. |
| `waist_single_joint_pitch_direction` | double / `1.0` | single_joint. **Startup only**. |
| `waist_single_joint_pitch_offset` | double / `0.0` | single_joint. **Startup only**. |

Lift 2S example (`body_joint_controller`): `waist_lifting_enabled: true`, `waist_lifting_type: single_joint`, `waist_absolute_source_frame: base_link`, `waist_absolute_target_frame: lift_link`. Overlay: [`arx_lift2s_description/.../ros2_controllers.yaml`](https://github.com/fiveages-sim/robot-descriptions-arx/blob/main/arx_lift2s_description/config/ros2_control/ros2_controllers.yaml).

## Adaptive Gripper Controller

夹爪. Plugin `adaptive_gripper_controller/AdaptiveGripperController`. README [配置参数](https://github.com/fiveages-sim/arms_ros2_control/blob/e1b7a147effca2f29f7cced0b2942837b096c1ff/controller/adaptive_gripper_controller/README.md). Command channels: [Adaptive Gripper Controller](6-gripper_teleop_plugins.md). Open/close limits come from `/robot_description`.

Uses `joint` (singular), not `joints`. `update_rate` and ControllerInterface command/state lists are **Startup only** at load. No `on_set_parameters` callback and no re-read in `update()`.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `joint` | string / `"gripper_joint"` | Controlled joint. **Startup only**. |
| `use_effort_interface` | bool / `true` | Bind effort state for force feedback. **Startup only**. |
| `force_threshold` | double / `0.1` | Effort magnitude that triggers feedback. **Startup only**. |
| `force_feedback_ratio` | double / `0.5` | After trigger: `0.0` stop here, `1.0` continue to original target. **Startup only**. |

## OCS2 Arm Controller

Plugin `ocs2_arm_controller/Ocs2ArmController`. Also declares the [framework-common keys](../../2-how_to/4-controllers/12-ros2_parameters.md#framework-common-parameters) and the [shared Home](../../2-how_to/4-controllers/12-ros2_parameters.md#home-statehome) names. README [#120](https://github.com/fiveages-sim/arms_ros2_control/blob/e1b7a147effca2f29f7cced0b2942837b096c1ff/controller/ocs2_arm_controller/README.md). FSM / launch: [OCS2 Arm Controller](2-ocs2_arm_controller.md). Public YAML: [`cr5_description/.../ros2_controllers.yaml`](https://github.com/fiveages-sim/robot-descriptions-dobot/blob/main/cr5_description/config/ros2_control/ros2_controllers.yaml). Optional dual-arm overlay on `robot_descriptions` **`feature/agilex` only**: [`taku_description/.../ros2_controllers.yaml`](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/humanoid/Dyna/taku_description/config/ros2_control/ros2_controllers.yaml).

README FSM is **HOME / HOLD / OCS2** (`3` = OCS2). Source also constructs `StateMoveJ` for canonical `/fsm_command` `4` (and IK MoveL when `lina_planning` is present). **Do not copy the Basic Joint MoveJ table here.** Declare-time deltas vs Basic Joint: `movej_interpolation_type` default `"linear"`, `movej_trajectory_blend_ratio` `0.2`. Waist keys, when `waist_lifting_enabled`, follow the Basic Joint waist table (only `waist_lifting_duration` is Runtime).

Older README names that are **not** parameters at this pin: `zero_pos` (use `rest_pos`), `robot_pkg` (use `robot_name`), `force_gains` (use `default_gains` / `pd_gains`).

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `home_pos` | double[] | Legacy single Home if `home_1`… are absent. **Startup only**. |
| `rest_pos` | double[] | Extra Home slot when `home_1` is already set. **Startup only**. |
| `robot_name` | string / `"cr5"` | Selects `{robot_name}_description` and OCS2 files. **Startup only**. |
| `default_gains` | double[] | HOME / HOLD impedance `[kp, kd]` when MIX interfaces are present. **Startup only**. |
| `pd_gains` | double[] | OCS2-state impedance `[kp, kd]`. **Startup only**. |
| `base_frame` | `task.info` `baseFrame` | Model / reference base. **Startup only** — not hot like `movel_duration`; change tip → restart. |
| `left_ee_frame` | `task.info` `eeFrame` | Left tip (YAML may set `left_tcp`). **Startup only**. |
| `right_ee_frame` | `task.info` `eeFrame1` | Right tip. **Startup only**. |
| `movel_duration` | `2.0` (CR5 YAML `0.5`) | MoveL duration (s). **Runtime** (next interpolating / stamped command). |
| `movel_trajectory_duration` | `2.0` | MoveL trajectory duration. **Runtime**. |
| `movel_sample_interval` | `0.04` | Sample interval. **Runtime**. |
| `movel_max_linear_velocity` | `0.3` | Linear vel limit. **Runtime**. |
| `movel_max_linear_acceleration` | `1.0` | Linear acc limit. **Runtime**. |
| `movel_max_linear_jerk` | `2.0` | Linear jerk limit. **Runtime**. |
| `movel_max_angular_velocity` | `1.0` | Angular vel limit. **Runtime**. |
| `movel_max_angular_acceleration` | `2.0` | Angular acc limit. **Runtime**. |
| `movel_max_angular_jerk` | `4.0` | Angular jerk limit. **Runtime**. |
| `movel_auto_extend_duration` | `true` | Extend MoveL duration when limits require it. **Runtime**. |

YAML frame overrides are injected in memory at Interface construction.

## arms_target_manager

This is a **command node**, not a ros2_control controller. README: [#120](https://github.com/fiveages-sim/arms_ros2_control/blob/e1b7a147effca2f29f7cced0b2942837b096c1ff/command/arms_target_manager/README.md). Cartesian topics: [FSM and Topics](../../3-concepts/4-fsm_and_topics.md), [Adaptive Gripper Controller](6-gripper_teleop_plugins.md).

YAML: package [`config/default.yaml`](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/config/default.yaml), or a robot `config/ocs2/target_manager.yaml`.

`declare_parameter` in `main` then values go into constructors. No `on_set_parameters` callback and no later `get_parameter`. Every row below is **Startup only**. Controller frames (`base_frame`, `left_ee_frame`, `right_ee_frame`, WBC `body_frame`) belong to the **controller** node — **Startup only** there.

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `dual_arm_mode` | launch / task.info; C++ `false` | Dual-arm markers. **Startup only**. |
| `control_base_frame` | launch / task.info; C++ `"world"` | Control base. **Startup only**. |
| `hand_controllers` | launch / task.info; C++ `[]` | Hand controller names. **Startup only**. |
| `marker_fixed_frame` | `"base_link"` | RViz marker fixed frame. **Startup only**. |
| `enable_movej_cartesian_markers` | `true` if `lina_planning`, else `false`; `full_body.launch.py` sets `false` under WBC | MOVEJ arm markers → stamped IK MoveL. **Startup only**. |
| `enable_head_control` | `false` | Legacy head RPY-to-joint marker (`/head_joint_controller/target_joint_position`). **Startup only**. |
| `enable_wbc_head_tracking_marker` | `false` | WBC Head 6D marker; still needs FSM=OCS2 and `HEAD_TRACKING`. **Startup only**. |
| `linear_scale` | `0.1` | Full-stick linear twist (m/s). **Startup only**. |
| `angular_scale` | `0.25` | Full-stick angular twist (rad/s). **Startup only**. |
| `control_input_rate` | `50.0` | Typical `control_input` Hz (feel only). **Startup only**. |
| `vr_thumbstick_linear_scale` | `0.005` | VR stick linear step (m/step). **Startup only**. |
| `vr_thumbstick_angular_scale` | `0.05` | VR stick angular step (rad/step). **Startup only**. |
| `enable_vr` | `false` in `default.yaml`; C++ declare `true` | Enable VR handler. Launch YAML overrides the C++ default. **Startup only**. |

## OCS2 WBC Controller

`controller/ocs2_wbc_controller` is a **private** submodule. Parameter names after access: that package README. Public launch: `ros2 launch ocs2_arm_controller full_body.launch.py` — [OCS2 WBC Controller](3-ocs2_wbc.md). Extra frame `body_frame` is **Startup only** per the target-manager notes in #120.

Public YAML may still list an `ocs2_wbc_controller:` block (Lift 2S `home_3` / `home_4`; Taku on `feature/agilex`). Treat those keys as machine overlays; the private README is the parameter list.

## Related

- [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md)
- [Driver layer parameters](../hardware/4-ros2_parameters.md)
- [Basic Joint Controller](7-basic_joint_controller.md)
- [OCS2 Arm Controller](2-ocs2_arm_controller.md)
- [Adaptive Gripper Controller](6-gripper_teleop_plugins.md)
- [OCS2 WBC Controller](3-ocs2_wbc.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
