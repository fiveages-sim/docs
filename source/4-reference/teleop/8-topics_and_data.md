(teleop-topics-and-data)=
# Teleop topics and data

A program that watches teleoperation subscribes to the topics on this page. Each section gives the topic, the message type, the QoS, the namespace, and the fields. Headset buttons and the RViz card are on [VR Teleoperation](../../2-how_to/5-teleoperation/6-vr_teleop.md).

Definitions: [`TeleopModeState.msg`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_ros2_control_msgs/msg/TeleopModeState.msg), [`TeleopMode.msg`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_ros2_control_msgs/msg/TeleopMode.msg), [`Inputs.msg`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_ros2_control_msgs/msg/Inputs.msg), and [section 1 of the message README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_ros2_control_msgs/README.md).

## 1. Two contracts

Joystick / keyboard and the event bus run side by side. Each path has its own status message.

| Path | Change the mode | Read the current mode | Who publishes the status |
|------|-----------------|----------------------|--------------------------|
| Joystick / keyboard | `control_input` (`arms_ros2_control_msgs/Inputs`) | `teleop_mode` (`TeleopMode`) | `joystick_teleop` / `keyboard_teleop` |
| Event bus (VR, foot pedal, exoskeleton, HUD) | `teleop/controller_state` (`std_msgs/Int32`) | `teleop/mode_state` (`TeleopModeState`) | `VRInputHandler` in `arms_target_manager` |

Send a mode change on the command topic, and read the active mode on the status topic. `teleop/controller_state` carries the event code. A `0` means this frame had no button edge. UPDATE, STORAGE, pause, and mirror are fields of `TeleopModeState` on `teleop/mode_state`.

A dexterous hand, DualHand, or a UI reads `teleop/mode_state` in an event-bus session, and `teleop_mode` when it follows the joystick or the keyboard. The foot pedal writes its event codes to `teleop/controller_state`.

## 2. Namespace and QoS

The command and status names above are relative to the robot namespace. With no namespace the event-bus status topic is `/teleop/mode_state`. In namespace `/robot_a` it is `/robot_a/teleop/mode_state`. Subscribe in that same namespace. Two robots in one scene stay apart.

QoS is `Reliable` + `TransientLocal`. The status publisher sends one message at startup, then another when a field changes. A node that starts later still receives the last snapshot.

:::{code-block} bash
ros2 topic echo /robot_a/teleop/mode_state
:::

With an empty namespace, echo `/teleop/mode_state`. Match QoS `Reliable` + `TransientLocal` on the subscription.

Headset pose, stick axes, trigger pull, and the shared end-effector poses are the root names in {ref}`the teleop pose stream <teleop-pose-stream>` (`/teleop/head_pose`, `/teleop/left_ee_pose`, and the rest of that set). `teleop/mode_state` follows the robot namespace.

## 3. Event-bus status (`TeleopModeState`)

`TeleopModeState` on `teleop/mode_state` is the latched mode for the event bus. `VRInputHandler` publishes a new snapshot when a field changes. The event code for that change is on `teleop/controller_state`. Joystick and keyboard use `TeleopMode` on `teleop_mode`.

| Field | Type | Meaning |
|-------|------|---------|
| `stamp` | `builtin_interfaces/Time` | Time this snapshot was published (`sec` + `nanosec`) |
| `enabled` | `bool` | Event-bus handler is enabled |
| `update_mode` | `bool` | `true` = UPDATE (follow); `false` = STORAGE |
| `chassis_mode` | `bool` | `true` = chassis teleop (event 20); `false` = end-effector sticks |
| `yb_pause_semantics` | `bool` | 全身 Y/B latch. `false` = WBC single-arm disable (停单臂). `true` = teleop pause (停发指令) |
| `left_arm_paused` / `right_arm_paused` | `bool` | That arm’s teleop pause |
| `left_stick_plane` / `right_stick_plane` | `uint8` | Arm stick: `PLANE_XY` = `0`, `PLANE_Z_YAW` = `1` |
| `body_stick_plane` | `uint8` | Waist left stick: `0` = XY, `1` = forward + roll |
| `body_right_stick_plane` | `uint8` | Waist right stick: `0` = lift + yaw, `1` = pitch + yaw |
| `left_gripper_percent_mode` / `right_gripper_percent_mode` | `bool` | `true` = percent; `false` = open/close |
| `mirror_movement` | `bool` | Mirror on or off |
| `mirror_profile` | `uint8` | `MIRROR_PROFILE_A` = `0`, `MIRROR_PROFILE_B` = `1`. Used when `mirror_movement` is true |
| `topology` | `uint8` | `TOPOLOGY_UNKNOWN` = `0`, `TOPOLOGY_SPLIT_BODY` = `1` (分体), `TOPOLOGY_FULL_BODY` = `2` (全身) |

`mirror_movement` is the mirror latch. Pause, the gripper-mode flags, `update_mode`, and `topology` are on this message for the hand and the UI. The latched gripper mode is `left_gripper_percent_mode` / `right_gripper_percent_mode`. The open/close or percent command is on `*/target_command` and `*/target_percent`.

### 3.1 Arm pause and WBC arm enable

`left_arm_paused` and `right_arm_paused` are the event-bus teleop pause for that arm. The headset, the foot pedal, and the exoskeleton all write this latch. WBC arm enable is `left_arm_state` and `right_arm_state` on `/ocs2_wbc_controller/current_state` (`WbcCurrentState`). Teleop pause and WBC enable are separate bits: an arm can be paused here while its WBC state is `ARM_ENABLED`.

On 全身, event 16 switches what left **Y** / right **B** mean. After the switch, `yb_pause_semantics` holds the current meaning. `left_arm_state` and `right_arm_state` are the WBC enable bits. The button chord is on {ref}`Stop one arm vs stop sending VR commands <stop-one-arm-vs-stop-sending-vr-commands>`.

Field values for `WbcCurrentState`: {ref}`wbc-current-state`. Mode strings on `/mode_command`: {ref}`wbc-mode-command`. `/mode_command` (`std_msgs/String` on the 全身 stack) switches the mode. `current_state` is the status you read.

### 3.2 When VR publishes arm and gripper targets

VR end-effector targets and VR gripper output follow `update_mode`.

| `update_mode` | What VR publishes |
|---------------|-------------------|
| `true` (UPDATE) | End-effector targets from the controller pose, and trigger gripper commands |
| `false` (STORAGE) | Latest VR pose, cached until the next UPDATE. Arm targets and gripper commands wait for UPDATE |

Right stick click toggles the two while FSM is **OCS2**. In STORAGE, joystick and keyboard `hand_command` on `control_input` open and close the hand. In UPDATE, the VR trigger stream writes the gripper.

## 4. Joystick and keyboard (`TeleopMode`)

`TeleopMode` on `teleop_mode` is the latched mode for the joystick and the keyboard. QoS matches the event bus: one message at startup, and another when `active`, `control_mode`, `mirror_movement`, or speed changes. Changing the active arm leaves this snapshot as it is.

| Field | Type | Meaning |
|-------|------|---------|
| `stamp` | `builtin_interfaces/Time` | Time this snapshot was published |
| `active` | `bool` | Commands are active. Joystick is true after the enable switch. Keyboard starts true |
| `control_mode` | `uint8` | `CONTROL_ARM` = `0`, `CONTROL_CHASSIS` = `1` |
| `mirror_movement` | `bool` | Mirror on or off |
| `speed_level` | `int32` | Keyboard `1`–`10`. Joystick `0` = LOW, `1` = HIGH |
| `speed_scale` | `float32` | Speed scale in use |

The active arm is `Inputs.target` on `control_input` (`1` left, `2` right). In chassis mode the joystick may pause the periodic `Inputs` stream, so keep the last `target`. Enable switch and keyboard keys: [Joystick teleop](../../2-how_to/5-teleoperation/9-joystick_teleop.md).

`Inputs` on `control_input` is the command stream for that path.

| Field | Type | Meaning |
|-------|------|---------|
| `x`, `y`, `z` | `float32` | Position increment |
| `roll`, `pitch`, `yaw` | `float32` | Orientation increment |
| `target` | `int32` | `1` left arm, `2` right arm |
| `hand_command` | `float32` | `NaN` = no command; `0` close; `1` open; any other value in `0`–`1` is an open ratio |

Only the joystick publishes `/fsm_command`.

(teleop-pose-stream)=
## 5. Teleop pose stream

`VRInputHandler` in `arms_target_manager` reads this stream. In UPDATE it drives arm targets from `/teleop/left_ee_pose` and `/teleop/right_ee_pose`.

`/teleop/left_ee_pose` and `/teleop/right_ee_pose` are `geometry_msgs/Pose` with no `header`. One node publishes that pair for a session:

| Node | Where it runs | What it publishes |
|------|---------------|------------------------|
| `xr_target_node` | [vr_pose_publisher](1-vr_pose_publisher.md), WebXR (`./run.sh vr`) and XRoboToolkit (`./run.sh vr-xrt`) | Controller 6-DOF, or the optical palm when the preset is `wrist` / `hand` |
| `dexcap_cartesian_teleop` | `dexcap_teleop` | Both arms from exoskeleton forward kinematics. Default 100 Hz. Stale input (default 0.1 s) stops the pair |
| `tracker_openvr` | [vive_tracker_teleop](6-vive_tracker.md) | Absolute Vive Tracker poses. Default `publish_rate_hz` is 120. A side with no tracker publishes an identity pose while any live side is enabled |

With Wuji gloves (`wuji_glove_teleop`), arm pose on this pair comes from `tracker_openvr`. The glove node reads `/teleop/controller_state` and `/teleop/mirror_mode`, and publishes finger commands on its own topics. [wuji_glove_teleop](5-wuji_glove.md).

`dexcap_cartesian_teleop` reads `/teleop/controller_state` and rebases its virtual pose when the code becomes `4`. Headset pose, sticks, triggers, and `/teleop/xrt_diag` come from `xr_target_node`. In a DexCap-only session, publish a zero `Twist` on `/teleop/thumbstick_axes` so `VRInputHandler` can finish a pending stick-centered check. The command is in the [dexcap_teleop README](https://github.com/fiveages-sim/dexcap_teleop_ws/blob/main/src/dexcap_teleop/README.md). Run that zero publisher by itself on `/teleop/thumbstick_axes`.

The field layout is [PROTOCOL_CN.md](https://github.com/fiveages-sim/vr_pose_publisher/blob/main/docs/PROTOCOL_CN.md).

| Topic | Type | Who publishes | Contents |
|-------|------|---------------|----------|
| `/teleop/head_pose` | `geometry_msgs/Pose` | `xr_target_node`, every frame | Headset 6-DOF pose |
| `/teleop/left_ee_pose` | `geometry_msgs/Pose` | `xr_target_node`, `dexcap_cartesian_teleop`, or `tracker_openvr` | Left 6-DOF pose, no `header` |
| `/teleop/right_ee_pose` | `geometry_msgs/Pose` | `xr_target_node`, `dexcap_cartesian_teleop`, or `tracker_openvr` | Right 6-DOF pose, no `header` |
| `/teleop/controller_state` | `std_msgs/Int32` | `xr_target_node`, every frame | Button event code. `0` means no edge this frame. The foot pedal sends the same codes on namespaced `teleop/controller_state` |
| `/teleop/thumbstick_axes` | `geometry_msgs/Twist` | `xr_target_node`, every frame | Left stick in `linear.x` / `linear.y`, right stick in `angular.x` / `angular.y` (about −1 to 1). Inside the 0.1 deadzone the value is `0.0`. A DexCap-only session adds a zero `Twist` here |
| `/teleop/trigger_values` | `geometry_msgs/Twist` | `xr_target_node`, every frame | Left trigger pull in `linear.x`, right trigger pull in `angular.x`. `0.0` is released, `1.0` is full |
| `/teleop/xrt_diag` | `std_msgs/Int64MultiArray` | `xr_target_node`, with the pose frame | Pose-frame diagnostic. Control reads the pose topics |

Poses from `xr_target_node` are in the robot world frame (`x` forward, `y` left, `z` up). WebXR publishes on a fixed 30 Hz timer. XRoboToolkit publishes when the VR `timeStampNs` changes: about 90 Hz with the default Pico App, and about 400 Hz with the enterprise send rate over USB.

Trigger pull depth is on `/teleop/trigger_values` every frame. The press edge is its own code on `/teleop/controller_state` (`9` left, `10` right).

`VRInputHandler` subscribes to the pose topics, `/teleop/controller_state`, `/teleop/thumbstick_axes`, and `/teleop/trigger_values`. Grippers in percent mode follow `trigger_values` when that topic is present. Headset button behavior: {ref}`VR Teleoperation <controller-buttons>`.

These `/teleop/...` names are root topics. `teleop/mode_state` follows the robot namespace.

The fa-py-libraries `./run.sh vr-record` bag records the headset pose, button, stick, and trigger topics: `/teleop/head_pose`, both end-effector poses, `/teleop/controller_state`, `/teleop/thumbstick_axes`, and `/teleop/trigger_values`.

Optical wrist presets also publish `/teleop/optical_r0_caps`, `/teleop/optical_r0_request`, `/teleop/optical_r0_ready`, and `/teleop/mirror_mode`. The handshake is in [PROTOCOL_CN.md](https://github.com/fiveages-sim/vr_pose_publisher/blob/main/docs/PROTOCOL_CN.md). The dexterous-hand joint command on that path is `q_des` ([xr_hand_retarget README](https://github.com/fiveages-sim/xr_hand_retarget/blob/main/README.md)). Launch and the headset panel: {ref}`Hand tracking <vr-hand-tracking>`.

## 6. Related

- [VR Teleoperation](../../2-how_to/5-teleoperation/6-vr_teleop.md)
- [DexCap Teleoperation](../../2-how_to/5-teleoperation/8-dexcap_teleop.md)
- [wuji_glove_teleop](5-wuji_glove.md)
- [vive_tracker_teleop](6-vive_tracker.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
- [vr_pose_publisher](1-vr_pose_publisher.md)
