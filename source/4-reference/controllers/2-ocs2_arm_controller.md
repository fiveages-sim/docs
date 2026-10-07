# ocs2_arm_controller

ROS 2 control controller for arm MPC via OCS2.

```{admonition} Source of truth
:class: important

FSM and launch names below come from [ocs2_arm_controller/README.md](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/README.md) and the package `launch/` files.

- README: FSM **HOME** / **OCS2** / **HOLD**
- Shared MoveJ / Home / Hold primitives: `libraries/arms_controller_common/`
```

**Repository:** [fiveages-sim/arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control) (`controller/ocs2_arm_controller/`)

## FSM

README states:

| State | Role |
|-------|------|
| **HOME** (`StateHome`) | Move the arm to a predefined home position |
| **OCS2** (`StateOCS2`) | OCS2 MPC optimal control |
| **HOLD** (`StateHold`) | Hold the position recorded when entering the state |

The controller starts in **HOLD**. OCS2 can only return to HOLD.

README transition commands (received on `/control_input`):

| Command | Transition |
|---------|------------|
| `1` | HOLD → HOME |
| `2` | HOME → HOLD, or OCS2 → HOLD |
| `3` | HOLD → OCS2 |

`arms_controller_common` also implements **MoveJ** (`StateMoveJ`) and `FSMCommandPublisher`, which publishes **`std_msgs/Int32`** on `/fsm_command` (values in that header: `1` HOME, `2` HOLD, `3` OCS2, `4` MOVEJ). On mixed OCS2/WBC stacks, `basic_joint_controller` treats `3` as OCS2 and `4` as MOVEJ — see [basic_joint_controller](7-basic_joint_controller.md).

## Split-body launch (分体控制)

`split_body.launch.py` is the **分体控制** path (`launch_mode` `split_body`):

- Arms: `ocs2_arm_controller`
- Body and head: `basic_joint_controller` (`setup_body_controllers` for `body` and `head`, e.g. `body_joint_controller`)
- Optional hands / FT broadcasters from the same launch helper

:::{code-block} bash
ros2 launch ocs2_arm_controller split_body.launch.py robot:=<robot>
:::

The same package also has `full_body.launch.py` (`launch_mode` `full_body`), which spawns **`ocs2_wbc_controller`** when the robot config type is `ocs2_wbc_controller/Ocs2WbcController`. That is **全身控制** — see [ocs2-wbc-controller](3-ocs2_wbc.md).

## Demo launch (README)

:::{code-block} bash
ros2 launch ocs2_arm_controller demo.launch.py type:=AG2F90-C
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx5 type:=r5
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz type:=AG2F120S
ros2 launch ocs2_arm_controller demo.launch.py hardware:=isaac type:=AG2F90-C
:::

Build (README): `colcon build --packages-up-to ocs2_arm_controller --symlink-install`.

## End-effectors (`type` / `left_type` / `right_type`)

`demo.launch.py`, `split_body.launch.py`, and `full_body.launch.py` declare `type` and also call `create_robot_profile_launch_arguments()` from [`robot_common_launch`](../descriptions/2-common.md). That helper adds **`left_type` / `right_type`** (and `use_profile_eef` / `robot_profile`). There is no `gripper:=` argument.

From `create_eef_side_launch_arguments()`: `left_type` is a left EEF key (`rg75`, `ag2f90_c`, `linkerhand_o7`, …). Use with `right_type` for asymmetric setups; **do not pass `type:=`** in that case.

:::{code-block} bash
# Symmetric EEF (package README)
ros2 launch ocs2_arm_controller demo.launch.py type:=AG2F90-C

# Different L/R (robot_common_launch README)
ros2 launch ocs2_arm_controller demo.launch.py \
  robot_profile:=/path/to/machine_profile.yaml \
  use_profile_eef:=false \
  left_type:=rg75 right_type:=linkerhand_o7
:::

`type` may also be arm topology `left` / `right` / `dual` (does **not** expand to `left_type` / `right_type`). Full merge rules: [robot_common_launch](../descriptions/2-common.md).

## Configuration (README)

YAML: `config/ocs2_arm_controller.yaml`. README lists `joints`, `home_pos`, `zero_pos`, `robot_pkg`, `update_rate`, `force_gains`.

OCS2 files (loaded from `robot_pkg`):

- Task: `{robot_pkg}/config/ocs2/task.info`
- Planning URDF: xacro cache via `robot_common_launch` (`planning_urdf_path`)
- Generated library: `{robot_pkg}/config/ocs2/generated`

Control mode is auto-detected from hardware interfaces (position-only vs force/`MIX` when `position`, `velocity`, `effort`, `kp`, `kd` are all present).

## Related

- [basic_joint_controller](7-basic_joint_controller.md)
- [robot_common_launch](../descriptions/2-common.md) — `type` / `left_type` / `right_type`
- [Switch Robot](../../2-how_to/1-basic_operations/2-switch_robot.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
- [ocs2_ros2](1-ocs2_ros2.md)
- [ocs2-wbc-controller](3-ocs2_wbc.md)
