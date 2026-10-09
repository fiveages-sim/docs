# basic_joint_controller

Joint-position controller with a three-state FSM (Home / Hold / MoveJ). Optional dexterous-hand switch/percent control and optional waist lifting/turning.

```{admonition} Source of truth
:class: important

Documented from the package READMEs only. Topics and command types are those listed there.

- English: [basic_joint_controller/README.md](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/basic_joint_controller/README.md)
- Chinese: [README_zh.md](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/basic_joint_controller/README_zh.md)
```

**Repository:** [fiveages-sim/arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control) (`controller/basic_joint_controller/`)

Shared FSM types live in `libraries/arms_controller_common/` (`StateHome`, `StateHold`, `StateMoveJ`, `FSMCommandPublisher`).

## FSM

`/fsm_command` is **`std_msgs/Int32`**, not `String`.

| Value | Action |
|-------|--------|
| `1` | Switch to **HOME** (only from HOLD) |
| `2` | Switch to **HOLD** (from HOME / MOVEJ) |
| `4` | Switch to **MOVEJ** (only from HOLD; canonical, same as the whole-body stack) |
| `3` | Switch to **MOVEJ** (legacy alias for standalone use; on mixed OCS2/WBC stacks `3` means OCS2) |
| `switch_command_base` (default `100`) | (HOME) Cycle to next configuration |
| `switch_command_base + 1` (default `101`) | (HOME) Switch to configuration 0 |
| `switch_command_base + 2` (default `102`) | (HOME) Switch to configuration 1 |

MOVEJ can only return to HOLD (`2`). Direct MOVEJ → HOME is rejected.

:::{code-block} bash
ros2 topic pub --once /fsm_command std_msgs/msg/Int32 "data: 1"   # → HOME
ros2 topic pub --once /fsm_command std_msgs/msg/Int32 "data: 4"   # → MOVEJ
:::

- **StateHome** — interpolate to one of up to 10 preset joint configurations
- **StateHold** — hold current joint positions
- **StateMoveJ** — interpolate to target joints; supports trajectories and prefix-based partial control

## Topics

Command topics are namespaced to the controller name (README example: `/left_hand_controller/...`). The table below is the package README **Topic Summary**, pinned at commit [`9a1da3ba`](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/basic_joint_controller/README.md). How to refresh the pin (and recompute `:start-line:` / `:end-line:`): [Documentation Build](../../5-developer/2-docs_build.md#vendored-upstream-readme).

```{include} ../../_vendored/arms_ros2_control/basic_joint_controller/README.md
:start-line: 274
:end-line: 291
```

Hand `target_command` / `target_percent` need `target_command_enabled`. Waist topics need `waist_lifting_enabled`. Absolute-pose defaults match **FiveAges W2** (`base_footprint` / `body_base`). README example for **ARX Lift / Lift 2S**: `waist_lifting_type: single_joint` with `base_link` / `lift_link`. Height-only commands (`waist_lifting`, `waist_lifting_command`, `target_joint_position`) do **not** use those frames.

On **分体**, the body instance is typically `/body_joint_controller/…`. On **全身**, [API_REFERENCE](https://github.com/fiveages-sim/ros2_robot_interface/blob/main/API_REFERENCE.md) maps the same waist names under `/ocs2_wbc_controller/…`. Cartesian EE `*/twist` and `*/relative` are **not** this controller — [FSM and Topics](../../3-concepts/4-fsm_and_topics.md). Waist pose also has a `WaistLiftingPose` **action** (`…/waist_lifting_pose`); Python prefers `execute_waist_lifting_pose_*_action` when a result is needed.

## Demo launch (README)

:::{code-block} bash
ros2 launch basic_joint_controller demo.launch.py robot:=fiveages_w1
ros2 launch basic_joint_controller demo.launch.py robot:=fiveages_w1 enable_body:=false
ros2 launch basic_joint_controller demo.launch.py robot:=fiveages_w1 enable_head:=false
:::

| Argument | Default | Description |
|----------|---------|-------------|
| `robot` | `fiveages_w1` | Robot name |
| `type` | empty | Robot type; empty means do not pass `type` to xacro (launch file) |
| `hardware` | `mock_components` | `gz` / `isaac` / `mock_components` |
| `enable_head` | `true` | Head controllers |
| `enable_body` | `true` | Body controllers |
| `use_rviz` | `true` | Launch RViz |

This demo does **not** declare `left_type` / `right_type`. Those first-class args come from `create_robot_profile_launch_arguments()` on OCS2 launches — [ocs2_arm_controller](2-ocs2_arm_controller.md).

Build (README): `colcon build --packages-up-to basic_joint_controller --symlink-install`.

## Related

- [Controller ROS 2 parameters](8-ros2_parameters.md) — README §3 keys and startup vs runtime
- [Use basic_joint_controller](../../2-how_to/4-controllers/11-basic_joint.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
- [分体控制 vs 全身控制](../../3-concepts/7-split_vs_wbc.md)
- [ocs2_arm_controller](2-ocs2_arm_controller.md) — 分体控制 (`split_body.launch.py`) uses this controller for body/head
- [Gripper and teleop plugins](6-gripper_teleop_plugins.md) — adaptive gripper channels vs this controller’s hand `target_percent`
- [ocs2-wbc-controller](3-ocs2_wbc.md) — 全身控制
