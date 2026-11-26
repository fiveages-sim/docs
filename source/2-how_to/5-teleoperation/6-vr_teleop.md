# VR Teleoperation

Control robots from a VR headset: controllers, or optical hand tracking.

## Supported Headsets

| Headset | Support Level | Modes | Notes |
|---------|---------------|-------|-------|
| **Pico Enterprise** | **Recommended** | Web, XRoboToolkit | USB shared networking (USB 网络共享); **its own App**, not the consumer Pico App |
| **Pico consumer** | Supported | Web, XRoboToolkit | Different headset App from Enterprise; no USB-tether path documented here |
| **Meta Quest** | Supported | Web, XRoboToolkit | Good consumer availability |

```{admonition} Pico Enterprise vs consumer
:class: important

Treat **Pico Enterprise** and **Pico consumer** as different SKUs. Each edition has its own headset App.

1. **USB shared networking (USB 网络共享)** — Pico Enterprise can share a network with the ROS 2 PC over USB. That is an Enterprise capability; it is not the consumer Pico path.
2. **Different Apps** — Enterprise and consumer Pico use **different** headset Apps. Install the App that matches the headset edition. The fa-py-libraries README’s XRoboToolkit path is “XRoboToolkit App + PC Service” versus browser WebXR; it does not name a single store listing for both Pico editions.

Store listings, extra package names, and ADB steps are in the headset / fa-py-libraries READMEs when they document them.
```

```{admonition} Pico Recommended
:class: tip

**Pico Enterprise** is the preferred Pico SKU for VR teleop (USB 网络共享, matching Enterprise App, lower-latency tracking / 更跟手). Consumer Pico and Meta Quest still work with the WebXR (`./run.sh vr`) and XRoboToolkit (`./run.sh vr-xrt`) backends.
```

## Prerequisites

- Working robot demo (mock, sim, or real)
- VR headset (**Pico Enterprise** recommended; Pico consumer or **Meta Quest** also used)
- fa-py-libraries installed
- Network between the headset and the ROS 2 machine (Wi-Fi, or **USB 网络共享** on Pico Enterprise)
- **`enable_vr: true`** in the robot description’s `config/ocs2/target_manager.yaml` (most robots default off)

Before the controller will consume VR targets, set `enable_vr: true` in that YAML. Related fields on the same file: `vr_update_rate` (used when VR is on) and `vr_follow_frame` (full-body follow frame; see [Troubleshooting](#troubleshooting)).

## Overview

With controllers, VR teleoperation publishes end-effector pose targets from controller tracking. The MPC controller then generates joint trajectories to follow these targets. Optical wrist and bare-hand gestures are [Hand tracking](#vr-hand-tracking).

On a real arm, use [force control and compliance](../4-controllers/13-force_control.md) when the arm should comply with contact. MIT-mode force control covers Panthera HT and ARX. Vendor joint impedance and payload identification cover Tianji and Rokae.

## Setup

### 1. Install fa-py-libraries

:::{code-block} bash
cd ~/
git clone https://github.com/fiveages-sim/fa-py-libraries.git
cd fa-py-libraries
./init.sh all
:::

HTTPS is the public clone. SSH (`git clone git@github.com:fiveages-sim/fa-py-libraries.git`) is optional if you already have keys.

What `./init.sh all` does: submodules + Python 3.12 env + `ros2_robot_interface` / `ros2-viser` / `vr_pose_publisher` / `xr_hand_retarget`.

### 2. Start Robot Demo

```bash
source ~/open-deploy-ws/install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py
```

### 3. Start VR Bridge

In a new terminal, from fa-py-libraries (README commands — there is no `./run.sh vr --mode`):

:::{code-block} bash
cd ~/fa-py-libraries
./run.sh vr
:::

This starts the Vuer/WebXR VR pose publisher.

## VR Modes

Both **Pico** and **Meta Quest** support two connection modes:

| Mode | Connection | Setup | Latency | Command |
|------|------------|-------|---------|---------|
| **Web** (WebXR) | Browser-based | Easy | Higher | `./run.sh vr` |
| **XRoboToolkit** | Native app + PC Service | Requires app install | Lower | `./run.sh vr-xrt-service` then `./run.sh vr-xrt` |

### Web Mode (WebXR)

Browser-based VR using Vuer — works on both Pico and Meta Quest:

:::{code-block} bash
./run.sh vr
:::

Open the displayed URL on your VR headset's browser. No app installation required.

### XRoboToolkit Mode

Native application for lower latency — recommended for production. From the fa-py-libraries README:

:::{code-block} bash
./init.sh install-xrobotoolkit-pc-service
./init.sh install-xrobotoolkit
./run.sh vr-xrt-service
./run.sh vr-xrt
:::

`./run.sh vr-xrt` is the controller path (`./run.sh vr-xrt controller` is the same path). Optical wrist and bare-hand gestures are below.

Requires the **edition-matching** XRoboToolkit App on the headset (Enterprise App ≠ consumer Pico App) plus PC Service. `./run.sh vr-xrt-service stop` shuts down the PC Service.

On Pico, after XRoboToolkit reports Network Status **WORKING**, close the settings panel with the **X** at its top-right. The clip is the headset view in XRoboToolkit 1.1.2: the panel is already up, shared network is checked, and the right-controller ray closes it. With the panel gone, later rays stay on the passthrough view.

```{raw} html
<video controls preload="metadata" width="100%">
  <source src="../../_static/videos/pico-hide-xrobotoolkit-ui.mp4" type="video/mp4">
</video>
```

(vr-hand-tracking)=
## Hand tracking (手势)

`./run.sh vr` and `./run.sh vr-xrt` follow the controllers. This path uses the optical wrists and the bare hands.

PC Service is already running (`./run.sh vr-xrt-service`). From fa-py-libraries:

:::{code-block} bash
./run.sh vr-xrt wrist
:::

`wrist` sends optical-wrist 6DoF to the arms and the bare-hand gesture (空手手势) to the dexterous hands. The hand is `FA_HAND`, or `hands.type` in `configs/local.yaml`: `xhand1`, `wuji`, `o6`, `l6`, `o7`. `FA_HAND` overrides `local.yaml`. `FA_HAND=none` or `--no-hands` keeps the wrist and does not start the hands.

:::{code-block} bash
FA_HAND=wuji ./run.sh vr-xrt wrist
FA_HAND=none ./run.sh vr-xrt wrist
./run.sh vr-xrt wrist --no-hands
:::

`./run.sh vr-hand` asks which hand, then starts this same wrist path. A choice other than `none` is written to `configs/local.yaml`.

One PC Service takes one SDK client. While `vr-xrt` is running, leave `xr_hand_retarget` stopped.

Hand on/off is the XRoboToolkit floating settings panel, not the RViz teleop HUD. In the clip (Pico Enterprise passthrough, XRoboToolkit 1.1.2), Network Status is already **WORKING**, shared network is on, and Enterprise tracking is checked. Under Tracking, Head stays on; turn **Hand** on and **Controller** off. The physical controllers can stay on the desk. Close the panel with the top-right **X** before teleop, so later rays stay on the passthrough view. That close is the clip above.

```{raw} html
<video controls preload="metadata" width="100%">
  <source src="../../_static/videos/vr-gesture-hand-tracking.mp4" type="video/mp4">
</video>
```

After the panel closes, the operator uses bare hands. The wheeled dual-arm in the “VR 遥操作” view follows the gestures.

The foot pedal still publishes events on `teleop/controller_state` (FSM, UPDATE / STORAGE, mirror). With no pedal, `./run.sh vr-ocs2` publishes `/fsm_command` `3` (OCS2).

Wrist and headset poses are on `/teleop/head_pose`, `/teleop/left_ee_pose`, and `/teleop/right_ee_pose` ({ref}`teleop-pose-stream`). The dexterous-hand joint command is `q_des` ([xr_hand_retarget README](https://github.com/fiveages-sim/xr_hand_retarget/blob/main/README.md)).

## Topics

Which topic to subscribe to, the message type, QoS, namespace, and the status fields: {ref}`Teleop topics and data <teleop-topics-and-data>`.

Mode changes and the latched mode use a separate pair of topics. [Read the current teleop mode](#teleop-mode-status).

## Arm Following

Configure which arm follows which controller:

```python
# In configuration or launch
teleop_config:
  left_arm: "left_controller"
  right_arm: "right_controller"
  # or for single arm:
  right_arm: "any_controller"
```

(controller-buttons)=
## Controller buttons (分体 vs 全身)

Bindings depend on whether the robot is running **分体** (`split_body.launch.py`) or **全身** (`full_body.launch.py`). Shared on both:

| Control | Action |
|---------|--------|
| Trigger | Gripper — pull for proportional open/close; in open/close mode, tap toggles |
| Right **A** / left **X** | FSM forward (`HOLD`→`OCS2`, `HOME`→`HOLD`) / back (`OCS2`→`HOLD`, `HOLD`→`HOME`) |
| Left stick click | Mirror |
| Right stick click | `STORAGE` ↔ `UPDATE` (**OCS2 only**) |
| Grip (short press) | Toggle stick plane (`XY` ↔ `Z+Yaw`) |
| Left **Y** / right **B** | Per-arm: **分体** = VR pause/resume (停发指令). **全身** default = that arm’s WBC ENABLE/DISABLE (停单臂); after event 16, same pause/resume. See [Stop one arm vs stop sending VR commands](#stop-one-arm-vs-stop-sending-vr-commands). |

**全身** adds grip + stick (ignored in 分体; FSM must already be **OCS2**):

| Control | Action |
|---------|--------|
| Left grip + left stick | Body: up = upright, down = lock waist, left = follow, right = custom lock |
| Right grip + right stick | WBC: up = dual-arm couple on/off, down = chassis unlock/lock, left = reserved, right = reference-joint track |
| Both grips + left **Y** + right **B** | Event 16: toggle the Y/B latch between WBC arm disable and VR pause/resume |

Grip + same-hand trigger switches that trigger’s gripper between percent and open/close. Pressing left **Y** and right **B** together (no grips) is scale-align (turns mirror off and returns to `STORAGE`). Both sticks together toggle chassis teleop ↔ end-effector control.

(stop-one-arm-vs-stop-sending-vr-commands)=
### Stop one arm vs stop sending VR commands

```{admonition} 停单臂 vs 停发指令
:class: important

On **全身**, default left **Y** / right **B** requests that arm’s WBC ENABLE/DISABLE (**停单臂**). That is not the same as freezing VR input for that arm (**停发指令** / pause). Event 16 flips which of those two Y/B does.
```

Y/B disable and event 16 apply when **全身** is active (`ocs2_wbc_controller`), VR is enabled, and FSM is **OCS2**. Implementation: [VRInputHandler README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_target_manager/VR_INPUT_HANDLER_README.md) (「单臂启用 / 禁用与 Y/B 语义锁存」).

| What you want | Control | Result |
|---------------|---------|--------|
| **Stop one arm** (停单臂) | Default left **Y** / right **B** | Request that arm’s WBC ENABLE/DISABLE. After WBC confirms `ARM_DISABLED`, VR stops publishing pose to that arm and stops accumulating that arm’s stick offset. The other arm stays controllable. Re-enable rebases from the current robot pose and the current headset / controller pose, then clears that arm’s stick offset. Does not require `UPDATE` / `STORAGE`. |
| **Stop sending VR commands** (停发指令) | After event 16, same left **Y** / right **B** | Freeze / resume VR input for that arm (pause). Needs `UPDATE`. |
| Switch Y/B meaning | Event 16: both grips + left **Y** + right **B** | Latch toggles between “WBC arm disable” and “VR pause/resume”. |

**分体** ignores event 16. Left **Y** / right **B** stay VR pause/resume.

Mirror swaps which physical button maps to which arm. WBC enabled/disabled state and rebase stay on the real arm.

When event 16 switches to pause and that arm is already `ARM_DISABLED`, the handler requests ENABLE, rebases, then freezes as paused. When it switches back to disable and that arm is already VR-paused, it requests DISABLE, then clears pause after WBC confirms. Under pause semantics, entering `UPDATE` with the right stick click does not clear the pause.

Constraints on **全身**:

- While the arms are coupled, Y/B cannot toggle a single arm.
- You cannot enable couple while any arm is disabled.
- While coupled, event 16 cannot switch the latch from pause back to disable (the latch stays).
- While a WBC switch or an event-16 conversion is still pending, event 16 and Y/B are ignored.
- If the topology leaves 全身, the latch returns to the default disable meaning.

Which meaning is latched is `yb_pause_semantics` on `teleop/mode_state`. Per-arm teleop pause is `left_arm_paused` / `right_arm_paused`. Those pause flags are independent of WBC `left_arm_state` / `right_arm_state` on `WbcCurrentState`. [Read the current teleop mode](#teleop-mode-status).

(teleop-mode-status)=
## Read the current teleop mode

VR, a foot pedal, and an exoskeleton that sends the same event codes share one contract. A game controller and the keyboard share another. The two run side by side.

| Path | Change the mode | Read the current mode | Who publishes the status |
|------|-----------------|----------------------|--------------------------|
| Joystick / keyboard | `control_input` (`Inputs`) and the related command topics | `teleop_mode` (`TeleopMode`) | `joystick_teleop` / `keyboard_teleop` |
| Event bus (VR, foot pedal, exoskeleton) | `teleop/controller_state` (`std_msgs/Int32` event code) | `teleop/mode_state` (`TeleopModeState`) | `VRInputHandler` in `arms_target_manager` |

Publish on the change topic to request a new mode. Subscribe to the status topic to see the mode that is active now. A dexterous hand, DualHand, or a UI reads `teleop/mode_state` for an event-bus session, or `teleop_mode` when it is following the joystick or the keyboard. `teleop/controller_state` carries the change event. The current mode is the status message.

The names above are relative. They follow the robot namespace, so two robots in one scene stay apart. With no namespace the event-bus status topic is `/teleop/mode_state`. In namespace `/robot_a` it is `/robot_a/teleop/mode_state`. Subscribe in that same namespace.

Use QoS `Reliable` + `TransientLocal`. The publisher sends one message at startup, then another when a field changes. A node that starts later still receives the last snapshot.

Definitions: [`TeleopModeState.msg`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_ros2_control_msgs/msg/TeleopModeState.msg), [`TeleopMode.msg`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_ros2_control_msgs/msg/TeleopMode.msg), and [section 1 of the message README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_ros2_control_msgs/README.md).

### Event-bus status (`TeleopModeState`)

`TeleopModeState` is the latch for the event bus. `TeleopMode` is a different message, for the joystick and the keyboard. Body lock and whether WBC has an arm enabled stay on {ref}`wbc-current-state` (`/ocs2_wbc_controller/current_state`).

`left_arm_paused` and `right_arm_paused` are that arm’s teleop pause. They stand apart from `left_arm_state` / `right_arm_state`: an arm can be VR-paused and still be `ARM_ENABLED`. On 全身, `yb_pause_semantics` reports which meaning left **Y** / right **B** currently have. `false` is WBC single-arm disable (停单臂). `true` is teleop pause (停发指令). The buttons that flip the latch are in [Stop one arm vs stop sending VR commands](#stop-one-arm-vs-stop-sending-vr-commands).

| Field | Type | Meaning |
|-------|------|---------|
| `stamp` | `builtin_interfaces/Time` | Time this snapshot was published |
| `enabled` | `bool` | Event-bus handler is enabled |
| `update_mode` | `bool` | `true` = UPDATE (follow; HUD `TELEOP ON`); `false` = STORAGE (`TELEOP OFF`) |
| `chassis_mode` | `bool` | `true` = chassis teleop (event 20); `false` = end-effector sticks |
| `yb_pause_semantics` | `bool` | 全身 Y/B latch: `false` = WBC arm disable; `true` = teleop pause |
| `left_arm_paused` / `right_arm_paused` | `bool` | That arm’s teleop pause |
| `left_stick_plane` / `right_stick_plane` | `uint8` | Arm stick: `0` = `PLANE_XY`, `1` = `PLANE_Z_YAW` |
| `body_stick_plane` | `uint8` | Waist left stick: `0` = XY, `1` = forward + roll |
| `body_right_stick_plane` | `uint8` | Waist right stick: `0` = lift + yaw, `1` = pitch + yaw |
| `left_gripper_percent_mode` / `right_gripper_percent_mode` | `bool` | `true` = percent; `false` = open/close |
| `mirror_movement` | `bool` | Mirror on or off |
| `mirror_profile` | `uint8` | `0` = `MIRROR_PROFILE_A`, `1` = `MIRROR_PROFILE_B` (used when mirror is on) |
| `topology` | `uint8` | `0` = `TOPOLOGY_UNKNOWN`, `1` = `TOPOLOGY_SPLIT_BODY` (分体), `2` = `TOPOLOGY_FULL_BODY` (全身) |

Subscribe to `teleop/mode_state` in the robot namespace. Read `mirror_movement` for mirror. Read pause, the gripper-mode flags, `update_mode`, and `topology` when the hand or the UI needs them. Open/close and percent commands stay on `*/target_command` and `*/target_percent`.

:::{code-block} bash
ros2 topic echo /robot_a/teleop/mode_state
:::

With an empty namespace, echo `/teleop/mode_state`. Match QoS `Reliable` + `TransientLocal` on the subscription.

### Joystick and keyboard status (`TeleopMode`)

`TeleopMode` on `teleop_mode` is the latch for the joystick and the keyboard. It uses the same QoS, and the same rule: once at startup, again when a field changes. The active arm is `Inputs.target` on `control_input` (`1` left, `2` right), not a field of `TeleopMode`. In chassis mode the joystick may pause the periodic `Inputs` stream, so keep the last `target`. Fields and the enable switch: [Joystick teleop](9-joystick_teleop.md).

### When VR moves the arm and the gripper

VR end-effector targets and VR gripper output follow `update_mode`.

| `update_mode` | HUD | What VR publishes |
|---------------|-----|-------------------|
| `true` (UPDATE) | `TELEOP ON` | End-effector targets from the controller pose, and trigger gripper commands |
| `false` (STORAGE) | `TELEOP OFF` | No arm targets and no VR gripper commands. The latest VR pose stays cached for the next UPDATE. |

Right stick click toggles the two, and only while FSM is **OCS2**. In STORAGE, joystick and keyboard `hand_command` on `control_input` still open and close the hand. While UPDATE is on, the VR trigger stream keeps writing the gripper; leave UPDATE when the joystick should own the hand.

### RViz teleop HUD

`arms_rviz_control_plugin/TeleopModeDisplay` is one RViz display with two cards, stacked at the top left of the 3D view. If only one path is active, that card fills the top slot. Add it from Displays → Add → TeleopModeDisplay. `Scale` runs from 0.5 to 2.0. A card stays hidden until its message arrives, and while that path is inactive. The display runs in any FSM state. Put RViz in the same namespace as `arms_target_manager`.

| Card | Visible when | What it reads |
|------|--------------|---------------|
| Event bus (VR, foot pedal, exoskeleton) | `teleop/mode_state.enabled` is true | `teleop/mode_state` |
| Control input (joystick / keyboard) | `teleop_mode.active` is true | `teleop_mode`, and `control_input` for the active arm |

The event-bus card shows `TELEOP` `ON`/`OFF`, `MIRROR`, and `L`/`R` as `RUN` or `PAUSE`, plus the stick plane, chassis, and gripper mode for the current route. A click publishes the same `teleop/controller_state` events as the headset: `4` toggles UPDATE, `7` toggles mirror, and `L`/`R` match left **Y** / right **B**. On 全身, when `yb_pause_semantics` is still false, `L`/`R` send event `16` first, wait until the latch flips, then send `3` or `6`. The control-input card is read-only: active arm `L`/`R` or `CHASSIS`, mirror, and speed `HIGH`/`LOW`. A joystick-only view of that card is in [Joystick teleop](9-joystick_teleop.md#control-input-hud).

The clip below shows the event-bus card alone: only the active path fills the top-left slot. Read it as `TeleopModeState`. `TELEOP ON` is `update_mode` true (UPDATE) and is green; `TELEOP OFF` is STORAGE. `L`/`R` `RUN` means that arm is following; `PAUSE` is `left_arm_paused` or `right_arm_paused`, in magenta, with `RUN` in green. `STICK XY` is the arm stick plane. `WAIST XY` and `WAIST ZYAW` replace those labels while the body mode is 跟随. `GRIP %` is percent mode; `GRIP SW` is open/close.

`MIRROR` stays `OFF` for the whole clip. The card moves from TELEOP off with both arms running, to TELEOP on, through a one-arm pause, then to the waist labels. `GRIP` flips from `%` to `SW` and back; while it shows `SW`, the gripper panel’s buttons read Close.

```{raw} html
<video controls preload="metadata" width="100%">
  <source src="../../_static/videos/vr-teleop-rviz-hud.mp4" type="video/mp4">
</video>
```

Sources: [arms_rviz_control_plugin README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_rviz_control_plugin/README.md) (遥操状态 HUD), [VRInputHandler README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_target_manager/VR_INPUT_HANDLER_README.md), and [arms_target_manager README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_target_manager/README.md).

## Safety

```{admonition} Motion Limits
:class: warning

VR teleoperation can command rapid motions. When using real hardware:
1. Start with low speed limits
2. Keep hand on emergency stop
3. Clear the robot workspace
4. Use workspace limits in software
```

## Network Setup

The headset and the ROS 2 PC must be on a reachable network (same Domain ID; Zenoh or DDS as needed).

- **Pico Enterprise:** USB shared networking (USB 网络共享) is supported — tether the headset to the PC over USB so they share a network. Follow the headset’s own USB-network UI; this page does not list ADB or `usb0` commands.
- **Pico consumer / Meta Quest:** use the usual Wi-Fi (or other IP) path. Do not assume USB 网络共享.

Then:

1. Confirm both devices can reach each other
2. Configure ROS 2 domain or Zenoh bridge if they are not on one LAN
3. Set firewall rules for ROS 2 ports

## Verification

1. VR bridge logs show tracking data
2. `ros2 topic echo /teleop/right_ee_pose` shows updates (use `/<namespace>/teleop/right_ee_pose` when the robot has a namespace)
3. `ros2 topic echo /teleop/mode_state` shows `update_mode: true` while the arms follow (`/<namespace>/teleop/mode_state` in a robot namespace). Subscribe with QoS `Reliable` + `TransientLocal`.
4. Robot follows VR controller motion in UPDATE. In STORAGE the arms and the VR gripper stay put; the joystick can still move the hand.

## Troubleshooting

### No tracking data

- Check VR device is properly tracked
- Verify browser/app has WebXR permissions
- Check network (Wi-Fi, or USB 网络共享 on Pico Enterprise)
- Confirm the headset App matches the Pico edition (Enterprise vs consumer)

### High latency

- Prefer **Pico Enterprise** (USB 网络共享 when possible)
- Use **XRoboToolkit** (`./run.sh vr-xrt`) instead of WebXR
- Use wired / USB-tethered networking when the headset edition supports it
- Reduce update rate in configuration
- Check for network congestion

### Robot doesn't follow

- Confirm `enable_vr: true` in the description’s `config/ocs2/target_manager.yaml` (most robots default off)
- Confirm `update_mode` is true on `teleop/mode_state` (UPDATE / HUD `TELEOP ON`) after entering OCS2. In STORAGE, VR does not publish arm targets or VR gripper commands.
- On **全身**, confirm that arm is not WBC-disabled (`ARM_DISABLED` on `WbcCurrentState`) and that `left_arm_paused` / `right_arm_paused` is false when you expect that arm to follow — [Stop one arm vs stop sending VR commands](#stop-one-arm-vs-stop-sending-vr-commands)
- Check target poses are within workspace
- Ensure no safety limits are triggered

### `base_footprint` missing (全身 / FULL_BODY)

FULL_BODY may warn that `base_footprint` does not exist (`lookupTransform` target_frame). Default `vr_follow_frame` is `base_footprint`. Set `vr_follow_frame` in `config/ocs2/target_manager.yaml` to the robot’s real base (for example `base_link`).

## Next Steps

- [Force control and compliance](../4-controllers/13-force_control.md) — MIT-mode force control on Panthera HT / ARX; vendor joint impedance and payload identification on Tianji / Rokae
- [Isomorphic Teleop](7-isomorphic_teleop.md) — master–slave joint following (Panthera HT `mode:=mit` / `effort`)
- [Teleop topics and data](../../4-reference/teleop/8-topics_and_data.md) — which topic to subscribe to, the message type, QoS, and the fields
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md) — `/fsm_command`, and WBC `current_state` / `/mode_command`
- [ocs2_arm_controller](../../4-reference/controllers/2-ocs2_arm_controller.md) — `default_gains` / `pd_gains` and MIX detection
- [marvin-ros2-control](../../4-reference/hardware/6-marvin.md) — Tianji position + `JOINT_IMPEDANCE`
- [vr_pose_publisher](../../4-reference/teleop/1-vr_pose_publisher.md) — the node that publishes `/teleop/*`
