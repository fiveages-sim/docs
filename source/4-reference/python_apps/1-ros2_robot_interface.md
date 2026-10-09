# ros2_robot_interface

Python client that talks to this stack over ROS 2 topics (and a few actions / services).

**Repository:** [fiveages-sim/ros2_robot_interface](https://github.com/fiveages-sim/ros2_robot_interface)

Public exports: `ROS2RobotInterface`, `ROS2RobotInterfaceConfig`, `ControlType`, FSM constants (`FSM_HOME`, `FSM_HOLD`, `FSM_OCS2`, `FSM_MOVEJ`, `FSM_COMPLIANCE`), and the `ROS2*Error` exceptions. Exhaustive method docs: [API_REFERENCE.md](https://github.com/fiveages-sim/ros2_robot_interface/blob/main/API_REFERENCE.md) on GitHub.

## Installation

Install through **fa-py-libraries** (Python 3.12 env). That repo’s `./init.sh all` installs `ros2_robot_interface` among the other submodules.

:::{code-block} bash
git clone https://github.com/fiveages-sim/fa-py-libraries.git
cd fa-py-libraries
./init.sh all
:::

Datagen / motion-queue path: from a **lerobot_ros2** checkout, `./init.sh all-motion` (or `./init.sh all`) installs the same package as `submodules/ros2_robot_interface`.

:::{admonition} Manual fallback
:class: note

Standalone clone of `ros2_robot_interface` and `pip install -e .` (inside a project venv; `--no-deps` on uv so `rclpy` is not fetched from PyPI) is only for package development outside those umbrellas. The stack entry is the deploy workspace / `fa-py-libraries`, not `pip install ros2-robot-interface` on system Python.
:::

## Quick start

The following example is the package README “Basic Example”, pinned at commit [`200ea42`](https://github.com/fiveages-sim/ros2_robot_interface/blob/200ea42d5671307cf1f3e4861fb544f356006e3d/README.md). How to refresh the pin: [Documentation Build](../../5-developer/2-docs_build.md#vendored-upstream-readme).

```{include} ../../_vendored/ros2_robot_interface/README.md
:start-after: Basic Example
:end-before: Center of Mass
```

`connect()` auto-detects dual-arm pose topics, gripper / hand controllers, and split vs whole-body joint topics when they are already in the ROS graph. `is_connected` is a **property**. Cartesian and joint sends go through handlers (`left_arm_handler`, `right_arm_handler`, `left_gripper_handler`, …), not a `move_j` / `move_l` wrapper.

With `auto_switch_fsm_before_control=True` (the config default), pose publishes switch the controller to OCS2 and joint publishes switch it to MOVEJ via `/fsm_command`.

## Topic ↔ API map

Operator-facing topics on a running OCS2 / `basic_joint_controller` stack, and the Python calls that publish or read them. Rows below are those [API_REFERENCE.md](https://github.com/fiveages-sim/ros2_robot_interface/blob/main/API_REFERENCE.md) names. Split (分体) vs whole-body (全身) prefixes: [分体控制 vs 全身控制](../../3-concepts/7-split_vs_wbc.md). Int32 FSM values: [FSM and Topics](../../3-concepts/4-fsm_and_topics.md).

### State

| Topic | Message | Python | Notes |
|-------|---------|--------|-------|
| `/joint_states` | `sensor_msgs/JointState` | `get_joint_state()` / `get_joint_state(categorized=True)` | Arms, head, waist, grippers — whatever the robot publishes |
| `/left_current_pose`, `/right_current_pose` | `geometry_msgs/PoseStamped` | `left_arm_handler.get_pose()` / `right_arm_handler.get_pose()` | Returns the inner `Pose` (or `None`) |
| `/left_current_target`, `/right_current_target` | `geometry_msgs/PoseStamped` | `left_arm_handler.get_target_pose()` | Controller echo of the active Cartesian target; used by `check_arrival()` |
| `/body_current_pose` | `geometry_msgs/PoseStamped` | `get_body_current_pose()` | WBC body pose; returns inner `Pose` |
| `/body_current_target` | `geometry_msgs/PoseStamped` | `get_body_current_target_pose()` | WBC body command echo |
| `/ocs2_wbc_controller/current_state` | `arms_ros2_control_msgs/WbcCurrentState` | `wait_until_mode_commands_applied(...)` | WBC constraint snapshot; confirms `/mode_command` |

:::{admonition} Whole-body (WBC) availability
:class: warning

`/body_target*`, `/head_target*`, `/mode_command`, and `WbcCurrentState` need **`ocs2_wbc_controller`** and that robot’s 全身 launch/config. Default mock demos (`demo.launch.py`) and 分体 (`split_body.launch.py`) do **not** imply these features are present. The controller is a **private** submodule; capability bits are machine-dependent (`WbcCapability`). Public Taku mock (`robot:=taku` on `demo.launch.py`) is arm-controller, not WBC. Details: [FSM and Topics](../../3-concepts/4-fsm_and_topics.md).
:::

### FSM and WBC mode

| Topic | Message | Python | Notes |
|-------|---------|--------|-------|
| `/fsm_command` | `std_msgs/Int32` | `send_fsm_command(command)` | `1` HOME, `2` HOLD, `3` OCS2, `4` MOVEJ, `5` COMPLIANCE (`FSM_*` constants). Not strings such as `stand` / `walk`. |
| `/fsm_state` | `std_msgs/Int32` | `get_fsm_state()` | Latched; same integer meanings |
| `/mode_command` | `std_msgs/String` | `send_mode_command(command)` | WBC strings such as `BODY_TRACKING`, `ARMS_COUPLED`, `BASE_LOCK`. Confirm with `wait_until_mode_commands_applied`. API_REFERENCE maps `BODY_*` / `ARMS_*` / `BASE_*` only — not `HEAD_*` via this method. |

### Cartesian targets (OCS2)

Unstamped `/left_target` replaces the current EE goal with **one** pose (typical for VR / high-rate teleop). Stamped `/left_target/stamped` runs TF into the controller frame and interpolates a **MoveL** sequence (typical for vision pick). Far unstamped jumps can jerk. `send_relative` is a **one-shot increment**, not an absolute pose in that frame. `send_velocity` is a **latched velocity stream**: the controller integrates each Twist; **0.2 s without a new message stops**; keep publishing at ≥5 Hz to move continuously.

On `ocs2_arm_controller`, the same `/left_target/stamped` topic in **MOVEJ** can run IK MoveL when [lina_planning](../controllers/5-lina_planning.md) is present (keep FSM at MOVEJ; turn off pose auto-switch to OCS2). WBC MOVEJ has no IK MoveL path.

| Topic | Message | Python | Notes |
|-------|---------|--------|-------|
| `/left_target`, `/right_target` | `geometry_msgs/Pose` | `left_arm_handler.send_target(pose)` | Pose already in controller `base_frame`; no TF; no MoveL interpolation |
| `/left_target/stamped`, `/right_target/stamped` | `geometry_msgs/PoseStamped` | `left_arm_handler.send_target_stamped(frame_id, pose)` | TF to `base_frame`; also `send_target_stamped(pose)` when `frame_id` is already cached |
| `/left_target/relative`, `/right_target/relative` | `geometry_msgs/TwistStamped` | `left_arm_handler.send_relative(dx, dy, dz, droll=0, dpitch=0, dyaw=0, frame_id="")` | One-shot increment (m, rad) + MoveL. Empty `frame_id` → controller `base_frame` |
| `/left_target/twist`, `/right_target/twist` | `geometry_msgs/Twist` | `left_arm_handler.send_velocity(linear, angular)` | Velocity `(vx,vy,vz)` m/s and `(wx,wy,wz)` rad/s in `base_frame`. Zero Twist stops. Not `send_cartesian_velocity` (that method is unimplemented) |
| `/dual_target/stamped` | `nav_msgs/Path` | `send_dual_arm_target_stamped(left_pose, right_pose, frame_id=...)` | Path length **2** (`[left, right]`); WBC may append a third `body` pose |
| `/target_path` | `nav_msgs/Path` | `send_target_path(left_poses, right_poses, ...)` | Dual-arm Cartesian waypoints. **Deprecated** in the Python API; new code uses `execute_path` (`ExecutePath` service) |
| `/body_target` | `geometry_msgs/Pose` | `send_body_target(pose)` | WBC; immediate absolute in `base_frame`. Also switches `/mode_command` to `BODY_TRACKING` |
| `/body_target/stamped` | `geometry_msgs/PoseStamped` | `send_body_target_stamped(frame_id, pose)` | WBC body MoveL |
| `/body_target/relative` | `geometry_msgs/TwistStamped` | `send_body_relative(dx, dy, dz, ...)` | WBC one-shot body increment + MoveL |
| `/head_target`, `/head_target/stamped` | `geometry_msgs/Pose` / `PoseStamped` | — | WBC Head 6D on `arms_target_manager`. API_REFERENCE maps head **joints** (`send_head_joint_positions`), not these Cartesian topics |

### MoveJ joint targets

`std_msgs/Float64MultiArray`. `connect()` prefers WBC topics when both exist. Implicit FSM → MOVEJ.

| Topic | Python | When |
|-------|--------|------|
| `/ocs2_wbc_controller/target_joint_position/left` (or `/right`) | `left_arm_handler.send_joint_positions(...)` | 全身 / `full_body.launch.py` |
| `/ocs2_arm_controller/target_joint_position/left` (or `/right`) | same handler | 分体 / `split_body.launch.py` |
| `/ocs2_arm_controller/target_joint_position` | same, single-arm | Single-arm OCS2 (no `/left` suffix) |
| `/ocs2_wbc_controller/target_joint_position` | `send_dual_arm_joint_positions(...)` | Unified dual-arm + body on WBC |
| `/ocs2_wbc_controller/target_joint_position/body` | `send_body_joint_positions(...)` | 全身 waist / body |
| `/body_joint_controller/target_joint_position` | `send_body_joint_positions(...)` | 分体 waist (`basic_joint_controller`) |
| `/ocs2_wbc_controller/target_joint_position/head` | `send_head_joint_positions(...)` | 全身 head |
| `/head_joint_controller/target_joint_position` | `send_head_joint_positions(...)` | 分体 / always-on head `basic_joint_controller` |
| `/{arm_controller}/target_joint_trajectory` | `send_joint_trajectory(joint_names, waypoints, …)` | e.g. `/ocs2_wbc_controller/target_joint_trajectory`; controller name from the arm joint topic |
| `/body_joint_controller/target_joint_trajectory` | `send_body_joint_trajectory(...)` | 分体 waist trajectory. WBC: same `send_joint_trajectory` with body joint names |
| `/head_joint_controller/target_joint_trajectory` | `send_head_joint_trajectory(...)` | 分体 head trajectory |

### Gripper and hand

`connect()` picks `hand_controller` vs `gripper_controller` (and left/right names). Discrete open/close is the RViz-style topic; Float64 position is the Python stroke command; `target_percent` is 0–1.

On **adaptive_gripper_controller**, `send_joint_positions` is direct position mode (**no** force feedback). `send_target_command` / `send_position_percent` use the switch / percent channels (force feedback while closing). On **basic_joint_controller** hands, the same percent/switch topics blend Home open/close configs (`target_command_enabled`).

| Topic | Message | Python | Notes |
|-------|---------|--------|-------|
| `/left_gripper_controller/target_command` (also `/right_…`, `/gripper_controller/…`) | `std_msgs/Int32` (`0` close / `1` open) | `left_gripper_handler.send_target_command(0\|1)` | Adaptive gripper switch |
| `/left_gripper_joint/position_command` (also `/right_…`, config `gripper_command_topic`) | `std_msgs/Float64` | `left_gripper_handler.send_joint_positions(position)` | Stroke in hardware units, **not** a 0–1 percent. Clamp with `gripper_min_position` / `gripper_max_position`. No adaptive force feedback |
| `/left_gripper_controller/target_percent` (also `/right_…`, `/gripper_controller/…`) | `std_msgs/Float64` (`0.0`–`1.0`) | `left_gripper_handler.send_position_percent(percent)` | Percent channel; raises if the publisher was not detected |
| `/left_hand_controller/target_command` (also `/right_…`, `/hand_controller/…`) | `std_msgs/Int32` (`0`/`1`) | same `send_target_command` after the hand controller is detected | Dexterous hand open/close when `target_command_enabled` is on |
| `/left_hand_controller/target_percent` | `std_msgs/Float64` (`0.0`–`1.0`) | same `send_position_percent` after the hand controller is detected | Home-config blend on `basic_joint_controller` |
| `/left_hand_controller/target_joint_position` | `std_msgs/Float64MultiArray` | `send_left_hand_joint_positions(...)` | Per-joint hand MoveJ |

### Waist (`basic_joint_controller` / WBC body)

Implicit FSM → MOVEJ. Split prefix `/body_joint_controller/…`; WBC prefix `/ocs2_wbc_controller/…`. Topic methods are fire-and-forget; API_REFERENCE prefers `execute_waist_lifting_pose_*_action` when you need a result.

| Topic | Message | Python | Notes |
|-------|---------|--------|-------|
| `…/waist_lifting` | `std_msgs/Float64` | `send_waist_lifting_relative_position(dz)` | Single-axis height delta (m) |
| `…/waist_lifting_pose_relative` | `std_msgs/Float64MultiArray` `[dx, dz, dphi]` | `send_waist_lifting_pose_relative(dx, dz, dphi)` | Local relative motion |
| `…/waist_lifting_pose_absolute` | `std_msgs/Float64MultiArray` `[x, z, phi]` | `send_waist_lifting_pose_absolute(x, z, phi)` | Absolute `[x, z, phi]` (TF frames on the controller) |
| `…/waist_lifting_command` | `std_msgs/Float64` | `send_waist_lifting_velocity_scale(scale)` | Velocity factor `[-1, 1]` |
| `…/waist_turning_command` | `std_msgs/Float64` | `send_waist_turning_velocity_scale(scale)` | Turning velocity factor `[-1, 1]` |

## Action ↔ API map

These wait for an action result (or timeout). They are not the topic rows above. Default **arm** names on `ROS2RobotInterfaceConfig` point at `ocs2_arm_controller`; override the config if the controller is namespaced. Waist action name is auto-detected (`/ocs2_wbc_controller/waist_lifting_pose` or `/body_joint_controller/waist_lifting_pose`). Type definitions: [`arms_ros2_control_msgs` README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_ros2_control_msgs/README.md). Topic vs Action vs Service: [FSM and Topics](../../3-concepts/4-fsm_and_topics.md).

| Action | Typical path | Python | Notes |
|--------|--------------|--------|-------|
| `ExecuteLinear` | `/ocs2_arm_controller/execute_linear` | `execute_movel_action` | Parameterized MoveL (`LinearMessage`). `auto_switch_fsm=True` (default) switches FSM to **MOVEJ** |
| `MovecUseIK` | `/ocs2_arm_controller/execute_circle_use_ik` | `execute_movec_action_three_point` / `execute_movec_action_parametric` | MoveC (`CircleMessage`; three-point or parametric). Default FSM → MOVEJ |
| `JointTrajectory` | `/ocs2_arm_controller/joint_trajectory_with_para` | `execute_joint_trajectory_action` / `execute_dual_arm_movej_action` | Parameterized MoveJ (`JointWaypoint[]`). Topic `send_joint_trajectory` has **no** result |
| `WaistLiftingPose` | `…/waist_lifting_pose` | `execute_waist_lifting_pose_absolute_action` / `execute_waist_lifting_pose_relative_action` | Goal `MODE_ABSOLUTE=0` / `MODE_RELATIVE=1`. Topic `send_waist_lifting_pose_*` is fire-and-forget |

`wait_for_*_action_server` helpers exist for each. Unstamped / stamped **topics** switch to **OCS2**; these Cartesian / joint actions default to **MOVEJ**. Signatures and `max_*` fallbacks: [API_REFERENCE.md](https://github.com/fiveages-sim/ros2_robot_interface/blob/main/API_REFERENCE.md).

## Service ↔ API map

Python wraps **`ExecutePath`** among the msgs README srv types. Service is a single request/response (no `progress`).

| Service | Name | Python | Notes |
|---------|------|--------|-------|
| `ExecutePath` | `execute_path` | `execute_path` / `execute_left_path` / `execute_right_path` | Left/right `nav_msgs/Path` + `trajectory_duration`; implicit FSM → OCS2. Replaces deprecated `/target_path` |

The msgs README also defines srv `ExecuteLinear`, `ExecuteCircle`, `MovecUseIK`, `JointTrajectory`, `CartesianPath`, and `KinematicsService`. Those have **no** `ros2_robot_interface` method — call them with ROS 2 clients if the running controller advertises them.

`call_compliance_zero_wrench()` is a separate FT zeroing service in API_REFERENCE, not one of the cartesian msgs types above.

:::{admonition} Lift 2S vendor `/body_control`
:class: note

ARX Lift 2S has a separate vendor chassis/lift command path (`/body_control`). That stack is **not** `ros2_robot_interface` and is not the OCS2 body topics in the table (`/body_joint_controller/target_joint_position` or `/ocs2_wbc_controller/target_joint_position/body`). Hardware bring-up: [ARX Lift 2S](../../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md).
:::

## Related

- [Python Interface How-To](../../2-how_to/3-programming/5-python_interface.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
- [分体控制 vs 全身控制](../../3-concepts/7-split_vs_wbc.md)
- [fa-py-libraries](2-fa_py_libraries.md)
- [arms_ros2_control_msgs README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_ros2_control_msgs/README.md) — msg / srv / action types
