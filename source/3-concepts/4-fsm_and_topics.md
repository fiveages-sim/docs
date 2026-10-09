# FSM and Topics

Finite-state machines in this stack live in [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control). Shared primitives are in `libraries/arms_controller_common/` (`StateHome`, `StateHold`, `StateMoveJ`, `FSMCommandPublisher`). Cartesian EE topics are owned by [`arms_target_manager`](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/README.md) (`PoseBasedReferenceManager`).

```{admonition} Source of truth
:class: important

`/fsm_command` is **`std_msgs/Int32`**, not `String`, and not wheeled-arm strings such as `stand` / `walk` / `arm_teleop`.

`/fsm_state` is also **`std_msgs/Int32`** (latched) — [ros2_robot_interface API_REFERENCE](https://github.com/fiveages-sim/ros2_robot_interface/blob/main/API_REFERENCE.md) and the [panthera-ht README](https://github.com/fiveages-sim/open-deploy-ws/blob/panthera-ht/README.EN.md).

`/mode_command` is **`std_msgs/String`** on the WBC stack (`send_mode_command` in ros2_robot_interface: `BODY_TRACKING`, `ARMS_COUPLED`, `BASE_LOCK`, …). It is **not** an FSM String and not a stand-in for `/fsm_command`.

Cartesian EE goals are `/left_target`, `/left_target/stamped`, `/left_target/twist`, and `/left_target/relative` (and the right / dual counterparts), not a stack-wide `/target_pose`. Per-controller extras: the controller pages and package READMEs. Python mapping: [ros2_robot_interface](../4-reference/python_apps/1-ros2_robot_interface.md).
```

## `/fsm_command` (`std_msgs/Int32`)

`FSMCommandPublisher` publishes `std_msgs/Int32` on `/fsm_command`. Shared integers:

| Value | Constant / label | Role |
|-------|------------------|------|
| `1` | `FSM_HOME` / HOME | Move to a preset home configuration |
| `2` | `FSM_HOLD` / HOLD | Hold; safe stop. Typical return path from OCS2 / MOVEJ |
| `3` | `FSM_OCS2` / OCS2 | Arm / WBC MPC (Cartesian targets). On **standalone** `basic_joint_controller`, `3` is a **legacy MOVEJ alias** |
| `4` | `FSM_MOVEJ` / MOVEJ | Direct joint-position mode (canonical MOVEJ on mixed OCS2/WBC stacks) |
| `5` | `FSM_COMPLIANCE` | Compliance / FT force mode in ros2_robot_interface (`enter_compliance()`). Must go through HOLD |
| `100` | `switch_command_base` (default) | While already in HOME: cycle to the next `home_*` configuration ([basic_joint_controller](../4-reference/controllers/7-basic_joint_controller.md)) |
| `101`, `102`, … | `switch_command_base + 1 + index` | While in HOME: select configuration index `0`, `1`, … |

Exact transitions depend on the **running controller**:

| Controller | States | Commands |
|------------|--------|----------|
| [Basic Joint Controller](../4-reference/controllers/7-basic_joint_controller.md) | HOME / HOLD / MOVEJ | README: `1` HOME, `2` HOLD, `4` MOVEJ (canonical); `3` is a **legacy MOVEJ alias** when this controller is standalone, and means **OCS2** on mixed OCS2/WBC stacks |
| [OCS2 Arm Controller](../4-reference/controllers/2-ocs2_arm_controller.md) | HOME / OCS2 / HOLD | README integers: `1` HOME, `2` HOLD, `3` **OCS2**. Operators and `ros2_robot_interface` send them on **`/fsm_command`**. Starts in HOLD; OCS2 returns only to HOLD. Shared `FSMCommandPublisher` also defines `4` MOVEJ |
| [OCS2 WBC Controller](../4-reference/controllers/3-ocs2_wbc.md) | 全身 stack | Private package; extra states are in that README after access. Public Python still uses the same `/fsm_command` integers plus `/mode_command` strings |

On mixed stacks, head / split-waist `basic_joint_controller` treats **`3` and `4` as MOVEJ**, while the arm / WBC controller treats **`3` as OCS2** and **`4` as MOVEJ**.

The [ocs2_arm_controller README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/ocs2_arm_controller/README.md) still names `/control_input` for those 1/2/3 integers. That is **not** the stack-wide FSM topic. Joystick `control_input` (`arms_ros2_control_msgs/Inputs`) on `arms_target_manager` is a different message: it is scaled into `/left_target/twist` / `/right_target/twist`.

:::{code-block} bash
ros2 topic pub --once /fsm_command std_msgs/msg/Int32 "data: 2"   # HOLD
:::

Split vs whole-body launches (and the Lift2S `quick_start` **split body** / **full body** menu) are on [分体控制 vs 全身控制](7-split_vs_wbc.md). Teleop is a separate interface, not an extra FSM state — [Isomorphic Teleop](../2-how_to/5-teleoperation/7-isomorphic_teleop.md).

## Status and command topics

Names below are those the public [ros2_robot_interface](https://github.com/fiveages-sim/ros2_robot_interface) config and API_REFERENCE subscribe / publish, plus the public controller READMEs. `connect()` rewrites split vs WBC joint prefixes when both are present (WBC wins).

### State

| Topic | Type | Typical use |
|-------|------|-------------|
| `/joint_states` | `sensor_msgs/JointState` | All joints (arms, head, waist, grippers) |
| `/left_current_pose`, `/right_current_pose` | `geometry_msgs/PoseStamped` | Current EE pose (`frame_id` is **base**, or WBC wheeled world — not the EE link) |
| `/left_current_target`, `/right_current_target` | `geometry_msgs/PoseStamped` | Active Cartesian command echo; arrival checks (`check_arrival()`) |
| `/body_current_pose` | `geometry_msgs/PoseStamped` | WBC current body pose |
| `/body_current_target` | `geometry_msgs/PoseStamped` | WBC body command echo (`body_target_enabled`) |
| `/head_current_target` | `geometry_msgs/PoseStamped` | WBC Head 6D final-target echo; `arms_target_manager` subscribes only |
| `/ocs2_wbc_controller/current_state` | `arms_ros2_control_msgs/WbcCurrentState` | WBC constraint snapshot; used to confirm `/mode_command` |

```bash
ros2 topic echo /joint_states
ros2 topic echo /left_current_pose
ros2 topic echo /left_current_target
```

### Cartesian arm targets (`arms_target_manager`)

Left arm; right arm is symmetric (`/right_target…`). From the [arms_target_manager README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/README.md) `PoseBasedReferenceManager` table.

Unstamped `/left_target` replaces the current EE goal with **one** pose (VR / high-rate teleop). Stamped `/left_target/stamped` runs TF into the controller frame and interpolates a **MoveL** sequence (vision pick / RViz absolute). Far unstamped jumps can jerk.

| Topic | Type | Typical use |
|-------|------|-------------|
| `/left_target`, `/right_target` | `geometry_msgs/Pose` | Immediate absolute pose in `base_frame` |
| `/left_target/stamped`, `/right_target/stamped` | `geometry_msgs/PoseStamped` | Absolute **MoveL**; non-base `frame_id` is TF’d to base |
| `/left_target/twist`, `/right_target/twist` | `geometry_msgs/Twist` | **Velocity stream** (m/s, rad/s) in base; latch + `dt` integrate. Joystick `control_input` is mapped here |
| `/left_target/relative`, `/right_target/relative` | `geometry_msgs/TwistStamped` | **One-shot relative** increment (m, rad) + MoveL; `header.frame_id` is the increment frame (base / EE / other TF) |
| `/dual_target/stamped` | `nav_msgs/Path` | Dual-arm; Path poses `[left, right]` (optional body as a third pose on WBC). MOVEJ dual send ignores a body pose if three are present |
| `/target_path` | `nav_msgs/Path` | Dual-arm waypoint path (Python API marks this topic deprecated in favor of the `execute_path` service) |

`relative` uses **TwistStamped**: `twist` is a displacement increment, not a velocity. Non-base `frame_id` rotates `linear` / `angular` into base before composing. `twist` stays a bare `Twist` (velocity, base only). `angular.{x,y,z}` is roll / pitch / yaw (`R' = RΔ(yaw)·RΔ(pitch)·RΔ(roll)·R`).

### Body targets (全身 OCS2)

:::{admonition} Whole-body (WBC) availability
:class: warning

`/body_target*`, `/head_target*`, `/mode_command`, and `WbcCurrentState` (`/ocs2_wbc_controller/current_state`) need **`ocs2_wbc_controller`** and that robot’s 全身 launch/config (`full_body.launch.py` when the controller type is `ocs2_wbc_controller/Ocs2WbcController`). Default mock demos (`demo.launch.py`) and 分体 (`split_body.launch.py`) do **not** imply these features are present.

The controller is a **private** submodule; extra FSM states stay in that README after access. Which constraints are live is machine-dependent (`WbcCapability` in the [msgs README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_ros2_control_msgs/README.md): mobile base, body relative, head 6D, midpoint gaze, …). Public Taku mock uses `split_body.launch.py robot:=taku` (arm MPC + body/head `basic_joint_controller` + `adaptive_gripper_controller`) — that is **not** WBC. `full_body.launch.py robot:=taku` needs the private `ocs2_wbc_controller` submodule; shipping `config/ocs2/fixed_base_tcp.info` in the public description is not enough. When that config and the private module are present, Taku full-body default `headMode` is `HEAD_GAZE` (gaze on `head_camera_mid_optical_frame`); `target_manager.yaml` has `enable_head_control: false` so the head follows OCS2 rather than a joint-space marker. Split-body still teleops the head through `head_joint_controller`. Taku body-relative rest is around x≈−0.21, not Bot2 `[0, 0.25]`. Head 6D tracking (`HEAD_TRACKING`) is only there when the controller reports `head_tracking_ee_enabled`.
:::

These Cartesian body topics are on the **全身 / WBC** path (`full_body.launch.py`, `body_target_enabled`). **分体** (`split_body.launch.py`) drives the waist with [basic_joint_controller](../4-reference/controllers/7-basic_joint_controller.md) joint topics (`/body_joint_controller/target_joint_position`, …), not this set.

| Topic | Type | Typical use |
|-------|------|-------------|
| `/body_target` | `geometry_msgs/Pose` | Immediate absolute body pose |
| `/body_target/stamped` | `geometry_msgs/PoseStamped` | Absolute body **MoveL** (RViz TRACKING) |
| `/body_target/relative` | `geometry_msgs/TwistStamped` | One-shot relative body increment + MoveL (`frame_id` = base / `body_frame`) |
| `/body_current_target` | `geometry_msgs/PoseStamped` | Active body command echo |

Python `send_body_target*` / `send_body_relative` also publish `/mode_command` `BODY_TRACKING` (skipped if already in that mode). Dual-arm `/dual_target/stamped` may carry a **third** body pose on WBC only; MOVEJ dual send ignores a body pose if three are present.

### Head 6D targets (全身 OCS2)

WBC Head XYZ+RPY. `arms_target_manager` inserts the 6D marker when FSM is **OCS2** and `WbcCurrentState.head_state` is **`HEAD_TRACKING`**. Leaving that mode removes the marker. `HEAD_GAZE` (midpoint gaze) uses the same gate and hides the marker. `split_body` does not turn this marker on. 分体 head joints stay on `/head_joint_controller/target_joint_position`.

| Topic | Type | Typical use |
|-------|------|-------------|
| `/head_target` | `geometry_msgs/Pose` | WBC Head 6D final target, continuous |
| `/head_target/stamped` | `geometry_msgs/PoseStamped` | WBC Head 6D interpolated target, one-shot |
| `/head_current_target` | `geometry_msgs/PoseStamped` | Final-target echo; `arms_target_manager` subscribes only |

API_REFERENCE maps head **joints** (`send_head_joint_positions`), not `/head_target`. `head_state` constants: msgs README (`HEAD_DISABLED` / `HEAD_TRACKING` / `HEAD_GAZE` / `HEAD_FORWARD`).

### MOVEJ + stamped → IK MoveL

`PoseBasedReferenceManager` is the sole holder of `left` / `right` / `dual_target/stamped` and the TF buffer. While FSM is **OCS2**, stamped writes the Cartesian reference buffer. While FSM is **not** OCS2, stamped is forwarded to `StateMoveJ.startLinearTrajectory` (lina **MoveL** + per-point IK), same semantics as `execute_linear`. Empty vel/acc/jerk fall back to controller `cartesian_defaults` (README defaults: `max_linear_velocity=0.25`, `ik_type=AUTO`, `time_mode=false`). Without [lina_planning](../4-reference/controllers/5-lina_planning.md) the MOVEJ side is a no-op.

This IK MoveL path is on **`ocs2_arm_controller`**. `ocs2_wbc_controller` MOVEJ is **joint-only** (no IK MoveL). `full_body.launch.py` sets `enable_movej_cartesian_markers:=false` on WBC, so MOVEJ arm markers stay hidden. Python `send_target_stamped` publishes the same stamped topic; keep FSM at MOVEJ (turn off pose auto-switch to OCS2) for the IK path. The RViz Joint panel MOVEJ path still publishes joint arrays only.

### MoveJ

| Topic | Type | Typical use |
|-------|------|-------------|
| `/ocs2_wbc_controller/target_joint_position/left` (and `/right`, `/body`, `/head`) | `std_msgs/Float64MultiArray` | 全身 / `full_body.launch.py` |
| `/ocs2_arm_controller/target_joint_position/left` (and `/right`) | `std_msgs/Float64MultiArray` | 分体 arms / `split_body.launch.py` |
| `/ocs2_arm_controller/target_joint_position` | `std_msgs/Float64MultiArray` | Single-arm OCS2 |
| `/body_joint_controller/target_joint_position` | `std_msgs/Float64MultiArray` | 分体 waist |
| `/head_joint_controller/target_joint_position` | `std_msgs/Float64MultiArray` | Head (`basic_joint_controller`) |
| `/{controller}/target_joint_trajectory` | `trajectory_msgs/JointTrajectory` | Multi-waypoint MoveJ. Split examples: `/body_joint_controller/…`, `/head_joint_controller/…`. WBC: `/ocs2_wbc_controller/target_joint_trajectory` |

### Gripper (`adaptive_gripper_controller`)

Three independent channels; each command takes effect immediately. From the [adaptive_gripper_controller README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/adaptive_gripper_controller/README.md). Example names: controller `left_gripper_controller`, joint `left_gripper_joint`.

| Topic | Type | Typical use |
|-------|------|-------------|
| `/left_gripper_joint/position_command` | `std_msgs/Float64` | Direct stroke (rad or m). **No** force feedback. Clamped to URDF limits |
| `/left_gripper_controller/target_command` | `std_msgs/Int32` (`0`/`1`) | `0` close **with** force feedback; `1` open, no feedback |
| `/left_gripper_controller/target_percent` | `std_msgs/Float64` (`0.0`–`1.0`) | Linear blend closed↔open. Closing direction enables force feedback; opening does not |

Force feedback runs only on the switch / percent channels, when `use_effort_interface` is true, the motion is **closing**, and `|effort| > force_threshold`. Then the remaining stroke is scaled by `force_feedback_ratio` (`0.0` stop here, `1.0` continue to the original target). Direct `position_command` never uses that path.

### Hand (`basic_joint_controller`)

Requires `target_command_enabled` and MOVEJ. Open/close poses are Home configurations.

| Topic | Type | Typical use |
|-------|------|-------------|
| `/{hand_controller}/target_command` | `std_msgs/Int32` (`0`/`1`) | `0` close pose, `1` open pose |
| `/{hand_controller}/target_percent` | `std_msgs/Float64` (`0.0`–`1.0`) | Per-joint blend between those two Home configs |

### Waist (`basic_joint_controller`)

Requires `waist_lifting_enabled` and MOVEJ. README topics are namespaced to the controller (often `/body_joint_controller/…` on 分体). [API_REFERENCE](https://github.com/fiveages-sim/ros2_robot_interface/blob/main/API_REFERENCE.md) maps the same names under `/ocs2_wbc_controller/…` on 全身.

| Topic | Type | Typical use |
|-------|------|-------------|
| `/{controller}/waist_lifting` | `std_msgs/Float64` | Height delta (m) from the current pose |
| `/{controller}/waist_lifting_pose_relative` | `std_msgs/Float64MultiArray` | Local `[dx, dz, dphi]` (no world/ground TF) |
| `/{controller}/waist_lifting_pose_absolute` | `std_msgs/Float64MultiArray` | Absolute `[x, z, phi]` (TF frames configurable) |
| `/{controller}/waist_lifting_command` | `std_msgs/Float64` | Lifting velocity factor `[-1, 1]` |
| `/{controller}/waist_turning_command` | `std_msgs/Float64` | Turning velocity factor `[-1, 1]` |

Waist absolute-pose defaults match **FiveAges W2** (`base_footprint` / `body_base`). README example for **ARX Lift / Lift 2S**: `waist_lifting_type: single_joint` with `base_link` / `lift_link`. Height-only commands (`waist_lifting`, `waist_lifting_command`, `target_joint_position`) do **not** use those frames.

Python method names for every row that API_REFERENCE documents: [ros2_robot_interface](../4-reference/python_apps/1-ros2_robot_interface.md).

:::{admonition} Lift 2S vendor `/body_control`
:class: note

ARX Lift 2S vendor chassis/lift (`/body_control`) is a **different** stack from these OCS2 / `basic_joint_controller` topics. `ros2_robot_interface` uses the body joint topics in the MoveJ table, not that vendor command.
:::

## Topic vs Action vs Service

Same motion can exist as a **topic** (fire-and-forget), an **action** (goal, progress feedback, result), and sometimes a **service** (one-shot RPC). Definitions: [`arms_ros2_control_msgs` README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_ros2_control_msgs/README.md). Which names a controller actually advertises is on that controller; the tables below list the types in that README.

| Kind | Behaviour | Example |
|------|-----------|---------|
| Topic | Publish and continue; no result | `/left_target/stamped`, `/{controller}/target_joint_trajectory` |
| Action | Send a goal; wait for result (and optional `progress`) | `ExecuteLinear`, `JointTrajectory`, `WaistLiftingPose` |
| Service | One request / response | `ExecutePath`, `KinematicsService` |

Python wrappers: [ros2_robot_interface](../4-reference/python_apps/1-ros2_robot_interface.md). Several srv types in the msgs README have **no** Python method.

## Whole-body mode (`/mode_command`)

`/mode_command` is **`std_msgs/String`** on the **全身 / WBC** stack. It is not `/fsm_command`. Same availability as the body/head Cartesian topics above: 分体 and default mock demos do not start this path. Typical Python: `send_mode_command`, then `wait_until_mode_commands_applied` against `/ocs2_wbc_controller/current_state` (`arms_ros2_control_msgs/WbcCurrentState`). API_REFERENCE: FSM is usually already **OCS2**, or the controller may ignore the mode. API_REFERENCE does **not** map `HEAD_*` strings onto `send_mode_command`; head 6D is gated by `WbcCurrentState.head_state`.

Documented command strings and the `WbcCurrentState` fields they check ([API_REFERENCE](https://github.com/fiveages-sim/ros2_robot_interface/blob/main/API_REFERENCE.md) `MODE_COMMAND_TO_WBC_EXPECT`):

| `/mode_command` | `WbcCurrentState` field |
|-----------------|-------------------------|
| `BODY_*` (examples: `BODY_TRACKING`, `BODY_FREE`; `BODY_VERTICAL` is an alias) | `body_state` |
| `ARMS_COUPLED` / `ARMS_INDEPENDENT` | `bimanual_state` |
| `BASE_LOCK` / `BASE_UNLOCK` | `base_state` |

`WbcCurrentState` constants from the msgs README (not extra FSM integers on `/fsm_command`):

| Field | Values |
|-------|--------|
| `base_state` | `BASE_LOCKED=0` / `BASE_UNLOCKED=1` |
| `body_state` | `BODY_FREE=0` / `VERTICAL=1` / `TRACKING=2` / `LOCKED=3` / `CUSTOM_LOCKED=5` (`4` was a former lock-head value and is no longer published) |
| `bimanual_state` | `BIMANUAL_INDEPENDENT=0` / `BIMANUAL_COUPLED=1` |
| `left_arm_state` / `right_arm_state` | `ARM_DISABLED=0` / `ARM_ENABLED=1` |
| `head_state` | `HEAD_DISABLED=0` / `HEAD_TRACKING=1` / `HEAD_GAZE=2` / `HEAD_FORWARD=3` |

Capability bits (`WbcCapability`: mobile base, body relative, head 6D, midpoint gaze, …) are in the same README. Extra WBC **FSM** states stay in the private `ocs2_wbc_controller` README after access.

## Actions

From the msgs README. Default **arm** action names on `ROS2RobotInterfaceConfig` point at `ocs2_arm_controller`; override the config if the controller has a namespace. Waist action name is auto-detected (`/ocs2_wbc_controller/waist_lifting_pose` or `/body_joint_controller/waist_lifting_pose`).

| Name | Type | Typical path | Role |
|------|------|--------------|------|
| `ExecuteLinear` | action | `/ocs2_arm_controller/execute_linear` | Parameterized MoveL (`LinearMessage` goal) |
| `MovecUseIK` | action | `/ocs2_arm_controller/execute_circle_use_ik` | MoveC (`CircleMessage`; three-point or parametric) |
| `JointTrajectory` | action | `/ocs2_arm_controller/joint_trajectory_with_para` | Parameterized MoveJ (`JointWaypoint[]`) |
| `WaistLiftingPose` | action | `…/waist_lifting_pose` | Waist pose; goal `MODE_ABSOLUTE=0` / `MODE_RELATIVE=1` |

Python: `execute_movel_action`, `execute_movec_action_three_point` / `execute_movec_action_parametric`, `execute_joint_trajectory_action` / `execute_dual_arm_movej_action`, `execute_waist_lifting_pose_absolute_action` / `execute_waist_lifting_pose_relative_action`. These block until a result or timeout. The matching topics (`*/stamped`, `target_joint_trajectory`, `waist_lifting_pose_*`) have **no** result.

`execute_movel_action` with `auto_switch_fsm=True` switches FSM to **MOVEJ**. Unstamped / stamped **topics** switch to **OCS2**.

## Services

From the msgs README. Service is a single request/response; action adds progress. Names a running controller advertises win.

| Name | Type | Role |
|------|------|------|
| `ExecuteLinear` | srv | Same `LinearMessage` as the action, without progress |
| `ExecuteCircle` | srv | `CircleMessage` |
| `MovecUseIK` | srv | `CircleMessage` (action of the same name has duration + progress) |
| `JointTrajectory` | srv | `joint_names` + `JointWaypoint[]` |
| `ExecutePath` | srv | Left/right `nav_msgs/Path` + `trajectory_duration` |
| `CartesianPath` | srv | Left/right `Path` + `duration` |
| `KinematicsService` | srv | FK / IK (`operation_type` `"fk"` / `"ik"`) |

Python wraps **`ExecutePath`** as `execute_path` / `execute_left_path` / `execute_right_path` (service name `execute_path`). The other srv types in that README have no `ros2_robot_interface` method — call them with ROS 2 clients if the controller advertises them.

## Related

- [Use Basic Joint Controller](../2-how_to/4-controllers/11-basic_joint.md)
- [basic_joint_controller](../4-reference/controllers/7-basic_joint_controller.md)
- [ocs2_arm_controller](../4-reference/controllers/2-ocs2_arm_controller.md)
- [ocs2-wbc-controller](../4-reference/controllers/3-ocs2_wbc.md)
- [Adaptive Gripper Controller](../4-reference/controllers/6-gripper_teleop_plugins.md)
- [Controllers reference](../4-reference/controllers/0-index.md)
- [ros2_robot_interface](../4-reference/python_apps/1-ros2_robot_interface.md)
- [arms_target_manager README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/README.md)
- [arms_ros2_control_msgs README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_ros2_control_msgs/README.md) — msg / srv / action types
