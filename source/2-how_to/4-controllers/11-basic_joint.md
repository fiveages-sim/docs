# Use basic_joint_controller

Run the joint-position controller (Home / Hold / MoveJ) from [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control).

```{admonition} Source of truth
:class: important

Steps and topics below are from [basic_joint_controller/README.md](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/basic_joint_controller/README.md) (and [README_zh.md](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/basic_joint_controller/README_zh.md)).

`/fsm_command` is **`std_msgs/Int32`**, not `String`.
```

On the public `open-deploy-ws` **`arx-lift2s`** branch, `basic_joint_controller` is in the README’s `colcon build --packages-up-to` list (simulation and real-hardware). Lift2S **split body** / **full body** are chosen in `./quick_start.sh` — see [ARX Lift 2S](../6-deployment/9-go_real_hardware/1-arx_lift2s.md) and [分体控制 vs 全身控制](../../3-concepts/7-split_vs_wbc.md).

## Prerequisites

- Workspace that already contains `arms_ros2_control` (for example `open-deploy-ws` after `./init_repo.sh`)
- Package built: `colcon build --packages-up-to basic_joint_controller --symlink-install`

## Launch (README demo)

:::{code-block} bash
source ~/open-deploy-ws/install/setup.bash   # or your workspace install/

ros2 launch basic_joint_controller demo.launch.py robot:=fiveages_w1
# Head only
ros2 launch basic_joint_controller demo.launch.py robot:=fiveages_w1 enable_body:=false
# Body only
ros2 launch basic_joint_controller demo.launch.py robot:=fiveages_w1 enable_head:=false
:::

| Argument | Default (README / launch) |
|----------|---------------------------|
| `robot` | `fiveages_w1` |
| `type` | empty (do not pass a type arg to xacro) |
| `hardware` | `mock_components` (`gz` / `isaac` / `mock_components`) |
| `enable_head` / `enable_body` | `true` |

This demo declares **`type` only**. It does not declare `left_type` / `right_type`. Mixed L/R EEF is on OCS2 `demo` / `split_body` / `full_body` via [robot_common_launch](../../4-reference/descriptions/2-common.md).

## Switch FSM

:::{code-block} bash
ros2 topic pub --once /fsm_command std_msgs/msg/Int32 "data: 1"   # HOLD → HOME
ros2 topic pub --once /fsm_command std_msgs/msg/Int32 "data: 2"   # → HOLD
ros2 topic pub --once /fsm_command std_msgs/msg/Int32 "data: 4"   # HOLD → MOVEJ (canonical)
:::

| Value | Action (README) |
|-------|-----------------|
| `1` | HOME (only from HOLD) |
| `2` | HOLD (from HOME / MOVEJ) |
| `4` | MOVEJ (only from HOLD; same canonical value as the whole-body stack) |
| `3` | MOVEJ if this controller is standalone; on mixed OCS2/WBC stacks `3` means **OCS2** |

MOVEJ returns only to HOLD (`2`). Full table and home-config `100`+ commands: [basic_joint_controller reference](../../4-reference/controllers/7-basic_joint_controller.md).

## Command joints in MOVEJ

Topics are namespaced to the controller name. README example:

:::{code-block} bash
ros2 topic pub --once /my_controller/target_joint_position \
  std_msgs/msg/Float64MultiArray "{data: [0.1, 0.2, 0.3]}"
:::

Type is `std_msgs/Float64MultiArray`, not `sensor_msgs/JointState`. Optional trajectory: `/{controller}/target_joint_trajectory` (`trajectory_msgs/JointTrajectory`). Hand / waist topics: the reference page (README §5–6).

## Related

- [basic_joint_controller reference](../../4-reference/controllers/7-basic_joint_controller.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
- [分体控制 vs 全身控制](../../3-concepts/7-split_vs_wbc.md)
- [ARX Lift 2S](../6-deployment/9-go_real_hardware/1-arx_lift2s.md)
