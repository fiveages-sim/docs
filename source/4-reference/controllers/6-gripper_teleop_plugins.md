# Gripper and Teleop Plugins

Controller plugins for grippers and teleoperation.

**Repository:** [fiveages-sim/arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control)

## adaptive_gripper_controller

Listed in the [arms_ros2_control README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/README.md). The launch stack does **not** take `gripper:=`. Attach an end-effector with `type` / `left_type` / `right_type` (and optional `robot_profile` / `use_profile_eef`) from [robot_common_launch](../descriptions/2-common.md).

Pin: [`9a1da3ba`](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/adaptive_gripper_controller/README.md). How to refresh the pin (and recompute `:start-line:` / `:end-line:`): [Documentation Build](../../5-developer/2-docs_build.md#vendored-upstream-readme).

### Three command channels

Each channel takes effect immediately. Joint limits and open/close positions come from `/robot_description` (closer URDF limit to the initial position = closed). Example names: controller `left_gripper_controller`, joint `left_gripper_joint`.

| Topic | Type | Force feedback | Typical use |
|-------|------|----------------|-------------|
| `/left_gripper_joint/position_command` | `std_msgs/Float64` | Off | Direct stroke (rad or m), clamped to URDF limits |
| `/left_gripper_controller/target_command` | `std_msgs/Int32` | On when closing (`0`) | `0` fully closed; `1` fully open (no feedback) |
| `/left_gripper_controller/target_percent` | `std_msgs/Float64` (`0.0`–`1.0`) | Auto: on while closing, off while opening | Linear blend closed↔open |

The README topic summary (Chinese source, same commit):

```{include} ../../_vendored/arms_ros2_control/adaptive_gripper_controller/README.md
:start-line: 170
:end-line: 181
```

### Force feedback

Applies only when all of these hold (README):

1. The command used the switch or percent channel (not direct `position_command`)
2. `use_effort_interface: true` and the hardware effort interface is bound
3. Motion is in the **closing** direction
4. Feedback has not already fired for this command (a new command resets the flag)

Trigger: `|current_effort| > force_threshold`. New target = current + (original − current) × `force_feedback_ratio`. `0.0` stops here; `1.0` continues to the original target; default `0.5`.

YAML keys in the README: `joint`, `use_effort_interface` (default `true`), `force_threshold` (default `0.1`), `force_feedback_ratio` (default `0.5`).

Python: `left_gripper_handler.send_joint_positions` (direct stroke, **no** feedback), `send_target_command` (0/1), `send_position_percent` (0–1). Same `target_command` / `target_percent` names on a dexterous **hand** go to [basic_joint_controller](7-basic_joint_controller.md) Home-config blend, not this force path. Map: [ros2_robot_interface](../python_apps/1-ros2_robot_interface.md).

## Teleop command nodes

The command package in the same repo is `command/` (`arms_target_manager`, `arms_teleop`, …). There is no `arms_teleop_controller` / `target_manager_controller`. Demo launch starts `arms_target_manager` when `enable_arms_target_manager` is `true`.

`arms_target_manager` owns `/left_target` / `/stamped` / `/twist` / `/relative` (and right / dual / WBC body-head). Tables: [FSM and Topics](../../3-concepts/4-fsm_and_topics.md). README: [arms_target_manager](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/README.md). WBC body/head Cartesian topics need `ocs2_wbc_controller` and 全身 launch/config — not default mock / 分体.

## Related

- [ocs2_arm_controller](2-ocs2_arm_controller.md)
- [basic_joint_controller](7-basic_joint_controller.md)
- [ros2_control here](../../3-concepts/1-ros2_control_here.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
- [ros2_robot_interface](../python_apps/1-ros2_robot_interface.md)
