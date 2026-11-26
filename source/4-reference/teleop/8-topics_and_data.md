(teleop-topics-and-data)=
# Teleop topics and data

A program that watches teleoperation subscribes to the topics on this page. Each section gives the topic, the message type, the QoS, the namespace, and the fields. Headset buttons and the RViz card stay on [VR Teleoperation](../../2-how_to/5-teleoperation/6-vr_teleop.md).

Definitions: [`TeleopModeState.msg`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_ros2_control_msgs/msg/TeleopModeState.msg), [`TeleopMode.msg`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_ros2_control_msgs/msg/TeleopMode.msg), [`Inputs.msg`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_ros2_control_msgs/msg/Inputs.msg), and [section 1 of the message README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_ros2_control_msgs/README.md).

## Two contracts

Joystick / keyboard and the event bus run side by side. Each path has its own status message.

| Path | Change the mode | Read the current mode | Who publishes the status |
|------|-----------------|----------------------|--------------------------|
| Joystick / keyboard | `control_input` (`arms_ros2_control_msgs/Inputs`) | `teleop_mode` (`TeleopMode`) | `joystick_teleop` / `keyboard_teleop` |
| Event bus (VR, foot pedal, exoskeleton, HUD) | `teleop/controller_state` (`std_msgs/Int32`) | `teleop/mode_state` (`TeleopModeState`) | `VRInputHandler` in `arms_target_manager` |

Send the change on the command topic. The mode that is active now is only on the status topic. `teleop/controller_state` carries the event code. A `0` on that topic means this frame had no button edge. UPDATE, STORAGE, pause, and mirror are fields of `TeleopModeState` on `teleop/mode_state`.

A dexterous hand, DualHand, or a UI reads `teleop/mode_state` for an event-bus session, or `teleop_mode` when it follows the joystick or the keyboard. The foot pedal publishes `teleop/controller_state` only.

## Namespace and QoS

The command and status names above are relative to the robot namespace. With no namespace the event-bus status topic is `/teleop/mode_state`. In namespace `/robot_a` it is `/robot_a/teleop/mode_state`. Subscribe in that same namespace. Two robots in one scene stay apart.

QoS is `Reliable` + `TransientLocal`. The status publisher sends one message at startup, then another when a field changes. A node that starts later still receives the last snapshot.

:::{code-block} bash
ros2 topic echo /robot_a/teleop/mode_state
:::

With an empty namespace, echo `/teleop/mode_state`. Match QoS `Reliable` + `TransientLocal` on the subscription.

Headset pose, stick axes, trigger pull, and the shared end-effector poses are the root names in {ref}`the teleop pose stream <teleop-pose-stream>` (`/teleop/head_pose`, `/teleop/left_ee_pose`, and the rest of that set). `teleop/mode_state` follows the robot namespace.

## Event-bus status (`TeleopModeState`)

`TeleopModeState` on `teleop/mode_state` is the latch for the event bus. `VRInputHandler` publishes it after a field changes. The message is the current mode. It does not say which button produced the last event. `TeleopMode` is a different message, for the joystick and the keyboard.

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

Read `mirror_movement` for mirror. Read pause, the gripper-mode flags, `update_mode`, and `topology` when the hand or the UI needs them. Open/close and percent commands stay on `*/target_command` and `*/target_percent`. This message reports which gripper mode is latched. It does not carry the gripper command.

### Arm pause and WBC arm enable

`left_arm_paused` and `right_arm_paused` are teleop pause. WBC arm enable is `left_arm_state` and `right_arm_state` on `/ocs2_wbc_controller/current_state` (`WbcCurrentState`). An arm can be VR-paused and still be `ARM_ENABLED`.

On 全身, event 16 switches what left **Y** / right **B** mean. After that switch, the current meaning is `yb_pause_semantics`. `left_arm_state` and `right_arm_state` stay the WBC enable bits. The button chord is on [Stop one arm vs stop sending VR commands](../../2-how_to/5-teleoperation/6-vr_teleop.md#stop-one-arm-vs-stop-sending-vr-commands).

Field values for `WbcCurrentState`: {ref}`wbc-current-state`. Mode strings on `/mode_command`: {ref}`wbc-mode-command`. `/mode_command` is `std_msgs/String` on the 全身 stack. It is not a write path for `current_state`.

### When VR publishes arm and gripper targets

VR end-effector targets and VR gripper output follow `update_mode`.

| `update_mode` | What VR publishes |
|---------------|-------------------|
| `true` (UPDATE) | End-effector targets from the controller pose, and trigger gripper commands |
| `false` (STORAGE) | No arm targets and no VR gripper commands. The latest VR pose stays cached for the next UPDATE |

Right stick click toggles the two, and only while FSM is **OCS2**. In STORAGE, joystick and keyboard `hand_command` on `control_input` can still open and close the hand. While UPDATE is on, the VR trigger stream keeps writing the gripper.

## Joystick and keyboard (`TeleopMode`)

`TeleopMode` on `teleop_mode` is the latch for the joystick and the keyboard. Same QoS: once at startup, again when `active`, `control_mode`, `mirror_movement`, or speed changes. Switching the active arm does not republish this message.

| Field | Type | Meaning |
|-------|------|---------|
| `stamp` | `builtin_interfaces/Time` | Time this snapshot was published |
| `active` | `bool` | Commands are active. Joystick is true after the enable switch. Keyboard starts true |
| `control_mode` | `uint8` | `CONTROL_ARM` = `0`, `CONTROL_CHASSIS` = `1` |
| `mirror_movement` | `bool` | Mirror on or off |
| `speed_level` | `int32` | Keyboard `1`–`10`. Joystick `0` = LOW, `1` = HIGH |
| `speed_scale` | `float32` | Speed scale in use |

The active arm is `Inputs.target` on `control_input` (`1` left, `2` right), not a field of `TeleopMode`. In chassis mode the joystick may pause the periodic `Inputs` stream. Keep the last `target`. Enable switch and the keyboard keys: [Joystick teleop](../../2-how_to/5-teleoperation/9-joystick_teleop.md).

`Inputs` on `control_input` is the command stream for that path.

| Field | Type | Meaning |
|-------|------|---------|
| `x`, `y`, `z` | `float32` | Position increment |
| `roll`, `pitch`, `yaw` | `float32` | Orientation increment |
| `target` | `int32` | `1` left arm, `2` right arm |
| `hand_command` | `float32` | `NaN` = no command; `0` close; `1` open; any other value in `0`–`1` is an open ratio |

The keyboard does not publish `/fsm_command`. The joystick does.

(teleop-pose-stream)=
## Teleop pose stream

`VRInputHandler` in `arms_target_manager` reads this stream. In UPDATE it drives arm targets from `/teleop/left_ee_pose` and `/teleop/right_ee_pose`. The latched mode stays on `teleop/mode_state` (`TeleopModeState`). A `0` on `/teleop/controller_state` means this frame had no button edge.

`/teleop/left_ee_pose` and `/teleop/right_ee_pose` are `geometry_msgs/Pose` with no `header`. A session uses one publisher for that pair:

| Node | Where it runs | What it publishes |
|------|---------------|------------------------|
| `xr_target_node` | [vr_pose_publisher](1-vr_pose_publisher.md), WebXR (`./run.sh vr`) and XRoboToolkit (`./run.sh vr-xrt`) | Controller 6-DOF, or the optical palm when the preset is `wrist` / `hand` |
| `dexcap_cartesian_teleop` | `dexcap_teleop` | Both arms from exoskeleton forward kinematics. Default 100 Hz. Stale input (default 0.1 s) stops the pair |
| `tracker_openvr` | [vive_tracker_teleop](6-vive_tracker.md) | Absolute Vive Tracker poses. Default `publish_rate_hz` is 120. A side with no tracker publishes an identity pose while any live side is enabled |

With Wuji gloves (`wuji_glove_teleop`), arm pose on this pair comes from `tracker_openvr`. The glove node reads `/teleop/controller_state` and `/teleop/mirror_mode`, and publishes finger commands on its own topics. [wuji_glove_teleop](5-wuji_glove.md).

`dexcap_cartesian_teleop` reads `/teleop/controller_state` and rebases its virtual pose when the code becomes `4`. Headset pose, sticks, triggers, and `/teleop/xrt_diag` come from `xr_target_node`. A DexCap-only session also publishes a zero `Twist` on `/teleop/thumbstick_axes`, so `VRInputHandler` can finish a pending stick-centered check. The command is in the [dexcap_teleop README](https://github.com/fiveages-sim/dexcap_teleop_ws/blob/main/src/dexcap_teleop/README.md). Run that zero stream while no other node is publishing the topic.

The field layout is [PROTOCOL_CN.md](https://github.com/fiveages-sim/vr_pose_publisher/blob/main/docs/PROTOCOL_CN.md).

| Topic | Type | Who publishes | Contents |
|-------|------|---------------|----------|
| `/teleop/head_pose` | `geometry_msgs/Pose` | `xr_target_node`, every frame | Headset 6-DOF pose |
| `/teleop/left_ee_pose` | `geometry_msgs/Pose` | `xr_target_node`, `dexcap_cartesian_teleop`, or `tracker_openvr` | Left 6-DOF pose, no `header` |
| `/teleop/right_ee_pose` | `geometry_msgs/Pose` | `xr_target_node`, `dexcap_cartesian_teleop`, or `tracker_openvr` | Right 6-DOF pose, no `header` |
| `/teleop/controller_state` | `std_msgs/Int32` | `xr_target_node`, every frame | Button event code. `0` means no edge this frame. The foot pedal sends the same codes on namespaced `teleop/controller_state` |
| `/teleop/thumbstick_axes` | `geometry_msgs/Twist` | `xr_target_node`, every frame | Left stick in `linear.x` / `linear.y`, right stick in `angular.x` / `angular.y` (about −1 to 1). Inside the 0.1 deadzone the value is `0.0`. A DexCap-only session also publishes a zero `Twist` here |
| `/teleop/trigger_values` | `geometry_msgs/Twist` | `xr_target_node`, every frame | Left trigger pull in `linear.x`, right trigger pull in `angular.x`. `0.0` is released, `1.0` is full |
| `/teleop/xrt_diag` | `std_msgs/Int64MultiArray` | `xr_target_node`, with the pose frame | Diagnostic. Downstream control can skip it |

Poses from `xr_target_node` are in the robot world frame (`x` forward, `y` left, `z` up). WebXR publishes on a fixed 30 Hz timer. XRoboToolkit publishes when the VR `timeStampNs` changes: about 90 Hz with the default Pico App, and about 400 Hz with the enterprise send rate over USB.

Pull depth stays on `/teleop/trigger_values` every frame. The press edge is a separate code on `/teleop/controller_state` (`9` left, `10` right).

`VRInputHandler` subscribes to the pose topics, `/teleop/controller_state`, `/teleop/thumbstick_axes`, and `/teleop/trigger_values`. Grippers in percent mode follow `trigger_values` when that topic is present. Headset button behavior: {ref}`VR Teleoperation <controller-buttons>`.

These names are the root topics (`/teleop/...`). `teleop/mode_state` follows the robot namespace.

The fa-py-libraries `./run.sh vr-record` bag records the headset pose, button, stick, and trigger topics: `/teleop/head_pose`, both end-effector poses, `/teleop/controller_state`, `/teleop/thumbstick_axes`, and `/teleop/trigger_values`.

Optical wrist presets also publish `/teleop/optical_r0_caps`, `/teleop/optical_r0_request`, `/teleop/optical_r0_ready`, and `/teleop/mirror_mode`. The handshake is in [PROTOCOL_CN.md](https://github.com/fiveages-sim/vr_pose_publisher/blob/main/docs/PROTOCOL_CN.md). The dexterous-hand joint command on that path is `q_des` ([xr_hand_retarget README](https://github.com/fiveages-sim/xr_hand_retarget/blob/main/README.md)). Launch and the headset panel: {ref}`Hand tracking <vr-hand-tracking>`.

## Related

- [VR Teleoperation](../../2-how_to/5-teleoperation/6-vr_teleop.md)
- [DexCap Teleoperation](../../2-how_to/5-teleoperation/8-dexcap_teleop.md)
- [wuji_glove_teleop](5-wuji_glove.md)
- [vive_tracker_teleop](6-vive_tracker.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
- [vr_pose_publisher](1-vr_pose_publisher.md)
