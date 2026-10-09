# ros2_control in This Stack

How FiveAges Sim **selects a hardware plugin** and **loads controllers**. This is not a generic ros2_control tutorial.

```{admonition} Source of truth
:class: important

- Launch `hardware:=` → xacro `ros2_control_hardware_type`: [`robot_common_launch` README](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/README.md) and [`launch_arg_utils.build_xacro_mappings()`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/robot_common_launch/common/launch_arg_utils.py)
- Default `hardware` on OCS2 demo: [`ocs2_arm_controller/launch/demo.launch.py`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/launch/demo.launch.py) (`mock_components`)
- Plugin names below are from [`arx_acone_description/xacro/ros2_control/robot.xacro`](https://github.com/fiveages-sim/robot-descriptions-arx/blob/main/arx_acone_description/xacro/ros2_control/robot.xacro). Other robots use the same `hardware` keys; the **real** plugin class is that robot’s own xacro.
```

Upstream lifecycle / QoS / “how Controller Manager works in general”: [ros2_control documentation](https://control.ros.org/). This stack’s launch arguments and topics are the rows and READMEs on this page.

## What the launch argument does

`build_xacro_mappings()` always sets `ros2_control_hardware_type` to the launch `hardware` string. When `hardware:=gz` it also sets `gazebo` to `true`. Profile YAML `hardware:` (serial, `arm_ctrl_mode`, …) is injected **only** when `hardware:=real`.

Documented launch values ([robot_common_launch](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/README.md), Acone xacro, `demo.launch.py`):

| `hardware:=` | Acone xacro plugin | Notes |
|--------------|--------------------|-------|
| `mock_components` (**default**) | `mock_components/GenericSystem` | No Gazebo / Isaac. There is **no** `hardware:=mock` branch in this xacro. |
| `gz` | `gz_ros2_control/GazeboSimSystem` | [ocs2_arm README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/README.md): install `ros-jazzy-ros-gz` and `ros-jazzy-gz-ros2-control` |
| `isaac` | `topic_based_ros2_control/TopicBasedSystem` | Acone params: `/isaac/joint_command`, `/isaac/joint_states`. Build `topic_based_ros2_control` ([arms_ros2_control README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/README.md)) |
| `real` | Vendor plugin (Acone: `arx_ros2_control/ArxX5Hardware`) | Other brands: use the plugin class from that description’s `xacro/ros2_control/*.xacro`. |

`REAL_HARDWARE` in `launch_arg_utils.py` is only `real`.

Optional controller overlay: if `<robot>_description/config/ros2_control/<hardware>.yaml` exists, `load_robot_config` merges it. Example from the common README: `arx_lift2s` + `hardware:=isaac` merges `isaac.yaml`. No file → no overlay.

## Controllers (this repo)

From [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control) READMEs / launches:

| Package | Role |
|---------|------|
| [basic_joint_controller](../4-reference/controllers/7-basic_joint_controller.md) | Home / Hold / MoveJ; body/head in 分体控制 |
| [ocs2_arm_controller](../4-reference/controllers/2-ocs2_arm_controller.md) | Arm MPC; `demo.launch.py` / `split_body.launch.py` |
| [ocs2_wbc_controller](../4-reference/controllers/3-ocs2_wbc.md) | 全身控制 via `full_body.launch.py` |
| `adaptive_gripper_controller` | Gripper (same repo README) |

分体 vs 全身: [分体控制 vs 全身控制](7-split_vs_wbc.md). How-to: [Use basic_joint_controller](../2-how_to/4-controllers/11-basic_joint.md).

## Command / state interfaces (OCS2 arm README)

[ocs2_arm_controller README — Interface Configuration](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/README.md): the controller **detects** the mode from interfaces present in the robot config.

| Mode | Command | State |
|------|---------|-------|
| Position (default) | `position` | `position`, `velocity` |
| Force (auto) | `position`, `velocity`, `effort`, `kp`, `kd` | `position`, `velocity`, `effort` |

That table is the **OCS2 MIX / MIT** path (Panthera HT / ARX). **Tianji** (天玑) / **Rokae** (珞石) keep the controller on **position** commands; joint impedance is a vendor `ctrl_mode` on the hardware interface (`JOINT_IMPEDANCE` on [marvin-ros2-control](https://github.com/fiveages-sim/marvin-ros2-control/blob/master/README.md)). VR comparison: [VR Teleoperation](../2-how_to/5-teleoperation/6-vr_teleop.md).

There is no stack-wide `/target_pose` or `/target_joint_positions` (`JointState`). MoveJ on `basic_joint_controller` is `/{controller}/target_joint_position` (`std_msgs/Float64MultiArray`). FSM: `/fsm_command` (`std_msgs/Int32`). Action / Service types and WBC body/head topics: [FSM and Topics](4-fsm_and_topics.md).

## Related

- [robot_common_launch](../4-reference/descriptions/2-common.md) — `type` / `left_type` / `right_type`, profile merge
- [Controllers reference](../4-reference/controllers/0-index.md)
