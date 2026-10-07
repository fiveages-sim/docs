# basic_joint_controller

Joint-position controller with a three-state FSM (Home / Hold / MoveJ). Optional dexterous-hand switch/percent control and optional waist lifting/turning.

```{admonition} Source of truth
:class: important

Documented from the package READMEs only. Do not invent extra topics or command types.

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

Command topics are namespaced to the controller name (README example: `/left_hand_controller/...`). Full table: the package README §6.

| Topic | Type | Active state | Notes |
|-------|------|--------------|-------|
| `/fsm_command` | `std_msgs/Int32` | any | FSM / home-config switching |
| `/{controller}/target_joint_position` | `std_msgs/Float64MultiArray` | MOVEJ | Direct joint targets |
| `/{controller}/target_joint_trajectory` | `trajectory_msgs/JointTrajectory` | MOVEJ | Multi-waypoint |
| `/{controller}/target_command` | `std_msgs/Int32` (`0`/`1`) | MOVEJ | Hand close/open (`target_command_enabled`) |
| `/{controller}/target_percent` | `std_msgs/Float64` (`0`–`1`) | MOVEJ | Hand blend (`target_command_enabled`) |
| `/{controller}/waist_lifting` | `std_msgs/Float64` | MOVEJ | Waist position delta (`waist_lifting_enabled`) |
| `/{controller}/waist_lifting_pose_relative` | `std_msgs/Float64MultiArray` | MOVEJ | Local `[dx, dz, dphi]` |
| `/{controller}/waist_lifting_pose_absolute` | `std_msgs/Float64MultiArray` | MOVEJ | Absolute `[x, z, phi]` (TF frames configurable) |
| `/{controller}/waist_lifting_command` | `std_msgs/Float64` | MOVEJ | Waist velocity factor |
| `/{controller}/waist_turning_command` | `std_msgs/Float64` | MOVEJ | Waist turning velocity factor |

Waist absolute-pose defaults match **FiveAges W2** (`base_footprint` / `body_base`). README example for **ARX Lift / Lift 2S**: `waist_lifting_type: single_joint` with `base_link` / `lift_link`.

## Demo launch (README)

:::{code-block} bash
ros2 launch basic_joint_controller demo.launch.py robot:=fiveages_w1
ros2 launch basic_joint_controller demo.launch.py robot:=fiveages_w1 enable_body:=false
ros2 launch basic_joint_controller demo.launch.py robot:=fiveages_w1 enable_head:=false
:::

| Argument | Default | Description |
|----------|---------|-------------|
| `robot` | `fiveages_w1` | Robot name |
| `hardware` | `mock_components` | `gz` / `isaac` / `mock_components` |
| `enable_head` | `true` | Head controllers |
| `enable_body` | `true` | Body controllers |
| `use_rviz` | `true` | Launch RViz |

Build (README): `colcon build --packages-up-to basic_joint_controller --symlink-install`.

## Related

- [Use basic_joint_controller](../../2-how_to/11-basic_joint.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
- [分体控制 vs 全身控制](../../3-concepts/7-split_vs_wbc.md)
- [ocs2_arm_controller](2-ocs2_arm_controller.md) — 分体控制 (`split_body.launch.py`) uses this controller for body/head
- [ocs2-wbc-controller](3-ocs2_wbc.md) — 全身控制
