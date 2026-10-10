# Naming Conventions

Names that this docs set actually uses, from [robot_common_launch](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/README.md) and deploy-ws / controller READMEs.

Brand **EN/ZH** labels follow [robot_usds README_zh-CN.md §3.1](https://github.com/fiveages-sim/robot_usds/blob/main/README_zh-CN.md#31-中文简称与英文标识对照). **ARX** is 方舟无限. **HighTorque** / Panthera is 高擎. Repo and script names stay as quoted (`arx-lift2s`, `./init_repo.sh`).

## Launch arguments (`robot_common_launch`)

`robot:=` selects the **description package** (`{robot}_description`). It is **not** launch `type` (EEF / topology).

| Argument | Purpose | Notes |
|----------|---------|-------|
| `robot` | Description key | Resolves `{robot}_description`. Examples used in READMEs / how-tos: `cr5` (OCS2 demo default), `arx_acone`, `arx_lift2s`, `panthera_ht` |
| `chassis` | Chassis model | Profile `platform.chassis`. Empty = do not pass to xacro |
| `arms` | Dual-arm kit | Profile `platform.arms`. Does **not** merge `config/ros2_control/{arms}.yaml`. Empty = do not pass to xacro |
| `variant` | Platform variant (appearance, column, …) | Profile `platform.variant`. May merge `config/ros2_control/{variant}.yaml` if that file exists. Empty = do not pass to xacro |
| `chassis_joints_movable` | Chassis joints movable | Profile `platform.chassis_joints_movable`. `true` / `false`. Empty = do not pass to xacro |
| `type` | Symmetric **end-effector** key, **or** arm topology `left` / `right` / `dual` | Topology does **not** expand to `left_type` / `right_type` |
| `left_type` / `right_type` | Different L/R EEF keys | Example keys: `rg75`, `ag2f90_c`, `linkerhand_o7`. **Do not pass `type:=`** with them |
| `use_profile_eef` | Apply profile `defaults.end_effectors` (default `true`) | `false` forces CLI EEF |
| `robot_profile` | Machine-profile YAML path | Merge: **CLI > profile > xacro defaults** |
| `ft` / `left_ft` / `right_ft` | Force-torque | Not gated by `use_profile_eef`. Example: `kwr75_485` |
| `hardware` | Plugin / overlay key | See below |

Platform slots (`chassis` / `arms` / `variant` / `chassis_joints_movable`) resolve **CLI > profile `platform.*` > that robot’s `xacro/robot.xacro` default**. `create_platform_launch_arguments()` declares `chassis` / `arms` / `chassis_joints_movable` (humanoid / `full_body` / `split_body` / `demo`; bare manipulator launches omit that set). `variant` is declared with `create_robot_profile_launch_arguments()`.

There is no `gripper:=` / `gripper_type:=`. Full merge: [robot_common_launch](../4-reference/descriptions/2-common.md).

:::{code-block} bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=dobot_cr5

ros2 launch ocs2_arm_controller demo.launch.py \
  use_profile_eef:=false \
  left_type:=rg75 right_type:=linkerhand_o7
:::

### `hardware:=`

Passed through as xacro `ros2_control_hardware_type` ([`build_xacro_mappings()`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/robot_common_launch/common/launch_arg_utils.py)).

| Value | Meaning |
|-------|---------|
| `mock_components` | Default on `ocs2_arm_controller` `demo.launch.py` and `basic_joint_controller` `demo.launch.py` |
| `gz` | Gazebo |
| `isaac` | Isaac (`topic_based_ros2_control`); may merge `config/ros2_control/isaac.yaml` if present |
| `real` | Vendor hardware interface; profile `hardware:` YAML applies only here |

There is **no** documented `hardware:=mock` key. Plugins: [ros2_control in This Stack](1-ros2_control_here.md).

## Packages (examples that exist)

| Kind | Pattern / example | Source |
|------|-------------------|--------|
| Description umbrella | `src/robot-descriptions/…` | open-deploy-ws README |
| Brand descriptions | `robot-descriptions-arx` (`arx_acone_description`, `arx_lift2s_description`, …) | [robot-descriptions-arx](https://github.com/fiveages-sim/robot-descriptions-arx) |
| Controllers | `basic_joint_controller`, `ocs2_arm_controller`, `adaptive_gripper_controller` | arms_ros2_control |
| Isaac hardware interface | `topic_based_ros2_control` | arms_ros2_control README |

Teleop packages are listed on the teleop reference pages (there is no `arms_teleop_controller` package in those READMEs).

## Topics

| Topic | Type | Source |
|-------|------|--------|
| `/fsm_command` | `std_msgs/Int32` | `FSMCommandPublisher` / basic_joint README (`1` HOME, `2` HOLD, `3` OCS2 / legacy MOVEJ, `4` MOVEJ) |
| `/{controller}/target_joint_position` | `std_msgs/Float64MultiArray` | basic_joint MoveJ |

Per-controller lists: [FSM and Topics](4-fsm_and_topics.md). No `/joint_commands` `JointState` contract and no `/target_pose` universal API in the READMEs cited here.

Frame names (`base_link`, `left_ee_link`, …) are **per robot URDF**. Do not assume a stack-wide frame table.
