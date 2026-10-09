# OCS2 Arm Controller

ROS 2 control controller for arm MPC via OCS2 (`ocs2_arm_controller/Ocs2ArmController`).

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

README integers (package README still lists them as received on `/control_input`):

| Command | Transition |
|---------|------------|
| `1` | HOLD → HOME |
| `2` | HOME → HOLD, or OCS2 → HOLD |
| `3` | HOLD → OCS2 |

Operators and `ros2_robot_interface` send those same integers on **`/fsm_command`** (`std_msgs/Int32`). That is the stack-wide FSM topic — [FSM and Topics](../../3-concepts/4-fsm_and_topics.md). Joystick `control_input` (`arms_ros2_control_msgs/Inputs`) on `arms_target_manager` is a different message, scaled into `/left_target/twist`.

`arms_controller_common` also implements **MoveJ** (`StateMoveJ`) and `FSMCommandPublisher`, which publishes **`std_msgs/Int32`** on `/fsm_command` (values in that header: `1` HOME, `2` HOLD, `3` OCS2, `4` MOVEJ). On mixed OCS2/WBC stacks, **Basic Joint Controller** treats `3` and `4` as MOVEJ, while this controller treats `3` as **OCS2** and `4` as MOVEJ — see [Basic Joint Controller](7-basic_joint_controller.md).

## Split-body launch (分体控制)

`split_body.launch.py` is the **分体控制** path (`launch_mode` `split_body`):

- Arms: `ocs2_arm_controller`
- Body and head: `basic_joint_controller` (`setup_body_controllers` for `body` and `head`, e.g. `body_joint_controller`)
- Optional hands / FT broadcasters from the same launch helper

:::{code-block} bash
ros2 launch ocs2_arm_controller split_body.launch.py robot:=<robot>
:::

The same package also has `full_body.launch.py` (`launch_mode` `full_body`), which spawns **`ocs2_wbc_controller`** when the robot config type is `ocs2_wbc_controller/Ocs2WbcController`. That is **全身控制** — see [OCS2 WBC Controller](3-ocs2_wbc.md).

## Cartesian topics (`arms_target_manager`)

EE goals are **not** listed as a full topic table in this controller’s README. They live in [`arms_target_manager`](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/README.md) (`PoseBasedReferenceManager`): `/left_target`, `/left_target/stamped`, `/left_target/twist`, `/left_target/relative`, plus right / dual counterparts and `/left_current_target`.

On this controller, MOVEJ + `/left_target/stamped` (and right / dual) can run IK **MoveL** via [lina_planning](5-lina_planning.md) (`StateMoveJ.startLinearTrajectory`). Without that library the MOVEJ Cartesian side is a no-op. **`ocs2_wbc_controller` MOVEJ has no IK MoveL** (joint arrays only); `full_body.launch.py` sets `enable_movej_cartesian_markers:=false`. Body / head Cartesian (`/body_target…`, `/head_target…`) are WBC-only — 分体 uses `basic_joint_controller` for those joints.

Full tables: [FSM and Topics](../../3-concepts/4-fsm_and_topics.md). Parameterized **MoveL / MoveC / MoveJ** also exist as actions (`ExecuteLinear`, `MovecUseIK`, `JointTrajectory`) on this controller; Python: [ros2_robot_interface](../python_apps/1-ros2_robot_interface.md). Types: [`arms_ros2_control_msgs` README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_ros2_control_msgs/README.md).

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

Parameter tables (Startup vs Runtime): [Controller ROS 2 parameters](8-ros2_parameters.md). Machine YAML lives in `{robot}_description/config/ros2_control/ros2_controllers.yaml` (there is no in-tree `config/ocs2_arm_controller.yaml`). README package-specific keys: `home_pos`, `rest_pos`, `robot_name`, `default_gains`, `pd_gains`, frames, `movel_*`. Names that are **not** parameters: `zero_pos`, `robot_pkg`, `force_gains`.

OCS2 files (selected via `robot_name` → `{robot_name}_description`; **not** ROS 2 parameters):

- Task: `{robot_name}_description/config/ocs2/task.info`
- Planning URDF: xacro cache via `robot_common_launch` (`planning_urdf_path`)
- Generated library: `{robot_name}_description/config/ocs2/generated`

Control mode is auto-detected from hardware interfaces (position-only vs force/`MIX` when `position`, `velocity`, `effort`, `kp`, `kd` are all present).

VR teleop on Panthera HT / ARX uses that MIT / MIX path. Tianji / Rokae VR compliance is **position commands + vendor HI impedance**, not this MIX table — [VR Teleoperation](../../2-how_to/5-teleoperation/6-vr_teleop.md).

## Related

- [Controller ROS 2 parameters](8-ros2_parameters.md)
- [Basic Joint Controller](7-basic_joint_controller.md)
- [robot_common_launch](../descriptions/2-common.md) — `type` / `left_type` / `right_type`
- [Switch Robot](../../2-how_to/1-basic_operations/2-switch_robot.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
- [ros2_robot_interface](../python_apps/1-ros2_robot_interface.md) — Action / Service Python map
- [Adaptive Gripper Controller](6-gripper_teleop_plugins.md)
- [ocs2_ros2](1-ocs2_ros2.md)
- [OCS2 WBC Controller](3-ocs2_wbc.md)
- [arms_ros2_control_msgs README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_ros2_control_msgs/README.md)
