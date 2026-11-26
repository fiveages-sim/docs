# VR Teleoperation

Control robots from a VR headset: controllers, or optical hand tracking.

## 1. Supported Headsets

| Headset | Support Level | Modes | Notes |
|---------|---------------|-------|-------|
| **Pico Enterprise** | **Recommended** | Web, XRoboToolkit | USB shared networking (USB 网络共享); **its own App**, separate from the consumer Pico App |
| **Pico consumer** | Supported | Web, XRoboToolkit | Its own headset App; Wi-Fi to the ROS 2 PC |
| **Meta Quest** | Supported | Web, XRoboToolkit | Good consumer availability |

```{admonition} Pico Enterprise vs consumer
:class: important

Treat **Pico Enterprise** and **Pico consumer** as different SKUs. Each edition has its own headset App.

1. **USB shared networking (USB 网络共享)** — Pico Enterprise shares a network with the ROS 2 PC over USB. Consumer Pico uses the Wi-Fi path.
2. **Different Apps** — Enterprise and consumer Pico each have their own headset App. Install the App that matches the headset edition. fa-py-libraries documents XRoboToolkit as “XRoboToolkit App + PC Service”, and WebXR as the browser path.

Store listings, extra package names, and ADB steps are in the headset / fa-py-libraries READMEs when they document them.
```

```{admonition} Pico Recommended
:class: tip

**Pico Enterprise** is the preferred Pico SKU for VR teleop (USB 网络共享, matching Enterprise App, lower-latency tracking / 更跟手). Consumer Pico and Meta Quest use the same WebXR and XRoboToolkit choices in the `./run.sh` menu.
```

## 2. Prerequisites

- Working robot demo (mock, sim, or real)
- VR headset (**Pico Enterprise** recommended; Pico consumer or **Meta Quest** also used)
- fa-py-libraries installed
- Network between the headset and the ROS 2 machine (Wi-Fi, or **USB 网络共享** on Pico Enterprise)
- **`enable_vr: true`** in the robot description’s `config/ocs2/target_manager.yaml` (most robots default off)

Before the controller will consume VR targets, set `enable_vr: true` in that YAML. Related fields on the same file: `vr_update_rate` (used when VR is on) and `vr_follow_frame` (full-body follow frame; see [Troubleshooting](#troubleshooting)).

## 3. Overview

With controllers, VR teleoperation publishes end-effector pose targets from controller tracking. The MPC controller then generates joint trajectories to follow these targets. Optical wrist and bare-hand gestures are [Hand tracking](#vr-hand-tracking).

On a real arm, use [How to use impedance control](../4-controllers/13-force_control.md) when the arm should give under contact. MIT-mode force control covers Panthera HT and ARX. Vendor joint impedance and payload identification cover Tianji and Rokae.

## 4. Setup

### 4.1 Install fa-py-libraries

:::{code-block} bash
cd ~/
git clone https://github.com/fiveages-sim/fa-py-libraries.git
cd fa-py-libraries
./init.sh all
:::

HTTPS is the public clone. SSH (`git clone git@github.com:fiveages-sim/fa-py-libraries.git`) is optional if you already have keys.

What `./init.sh all` does: submodules + Python 3.12 env + `ros2_robot_interface` / `ros2-viser` / `vr_pose_publisher` / `xr_hand_retarget`.

### 4.2 Start Robot Demo

```bash
source ~/open-deploy-ws/install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py
```

### 4.3 Start the VR bridge

Open a new terminal, go to fa-py-libraries, and start the menu:

:::{code-block} bash
cd ~/fa-py-libraries
./run.sh
:::

With no arguments, `./run.sh` prints `请选择要启动的功能` and waits for a number.

| You want | Choose |
|----------|--------|
| WebXR in the headset browser | `6) vr pose launch (Vuer/WebXR)` |
| XRoboToolkit with the VR controllers | `4) 启动 XRoboToolkit PC Service`, then `3) 手柄遥操 (controller)` |
| Optical wrists and hand gestures | `2) 手部遥操 (光学腕 + 灵巧手)  — 再选手型` |

The same menu entries exist as commands: `./run.sh vr`, `./run.sh vr-xrt-service` then `./run.sh vr-xrt`, and `./run.sh vr-hand`.

## 5. VR Modes

Both **Pico** and **Meta Quest** support two connection modes. Pick them from the menu above.

| Mode | Connection | Setup | Latency | Menu |
|------|------------|-------|---------|------|
| **Web** (WebXR) | Browser-based | Open the printed URL | Higher | `6) vr pose launch (Vuer/WebXR)` |
| **XRoboToolkit** | Native app + PC Service | Matching headset App, then PC Service | Lower | `4)`, then `3) 手柄遥操 (controller)` |

### 5.1 Web Mode (WebXR)

Menu item `6`, or `./run.sh vr`. Open the printed URL in the headset browser.

### 5.2 XRoboToolkit Mode

Lower latency. Install the PC side once, from the fa-py-libraries README:

:::{code-block} bash
./init.sh install-xrobotoolkit-pc-service
./init.sh install-xrobotoolkit
:::

Each session, run `./run.sh` and choose `4) 启动 XRoboToolkit PC Service`, then `3) 手柄遥操 (controller)`. The same steps as commands are `./run.sh vr-xrt-service` and `./run.sh vr-xrt`. `./run.sh vr-xrt controller` is that controller path. Optical wrists and bare-hand gestures are menu item `2`, below.

Requires the **edition-matching** XRoboToolkit App on the headset (Enterprise App ≠ consumer Pico App) plus PC Service. Menu item `5) 关闭 XRoboToolkit PC Service`, or `./run.sh vr-xrt-service stop`, shuts down the PC Service.

On Pico, after XRoboToolkit reports Network Status **WORKING**, close the settings panel with the **X** at its top-right. The clip is the headset view in XRoboToolkit 1.1.2: the panel is already up, shared network is checked, and the right-controller ray closes it. With the panel gone, later rays stay on the passthrough view.

```{raw} html
<video controls preload="metadata" width="100%">
  <source src="../../_static/videos/pico-hide-xrobotoolkit-ui.mp4" type="video/mp4">
</video>
```

(vr-hand-tracking)=
## 6. Hand tracking (手势)

Menu items `6` and `3` follow the VR controllers. Optical wrists and bare hands are menu item `2`.

PC Service is already running (menu item `4`, or `./run.sh vr-xrt-service`). From fa-py-libraries, run `./run.sh` and choose `2) 手部遥操 (光学腕 + 灵巧手)  — 再选手型`.

The terminal then prints `请选择灵巧手` and lists `xhand1`, `wuji`, `o6`, `l6`, `o7`, and `none`. A choice other than `none` is written to `configs/local.yaml`. `none` keeps the wrists and leaves the dexterous hands off.

`./run.sh vr-hand` asks the same question and starts this path. `./run.sh vr-xrt wrist` is that wrist path with the hand already chosen. `FA_HAND` overrides `configs/local.yaml` (`xhand1`, `wuji`, `o6`, `l6`, `o7`, `none`). These are the same choices as commands:

:::{code-block} bash
FA_HAND=wuji ./run.sh vr-xrt wrist
FA_HAND=none ./run.sh vr-xrt wrist
./run.sh vr-xrt wrist --no-hands
:::

One PC Service takes one SDK client. While `vr-xrt` is running, leave `xr_hand_retarget` stopped.

Turn the hand on or off in the XRoboToolkit floating settings panel. The RViz card shows the mode. In the clip (Pico Enterprise passthrough, XRoboToolkit 1.1.2), Network Status is already **WORKING**, shared network is on, and Enterprise tracking is checked. Under Tracking, Head stays on; turn **Hand** on and **Controller** off. The physical controllers can stay on the desk. Close the panel with the top-right **X** before teleop, so later rays stay on the passthrough view. That close is the clip above.

```{raw} html
<video controls preload="metadata" width="100%">
  <source src="../../_static/videos/vr-gesture-hand-tracking.mp4" type="video/mp4">
</video>
```

After the panel closes, the operator uses bare hands. The wheeled dual-arm in the “VR 遥操作” view follows the gestures.

The foot pedal publishes events on `teleop/controller_state` (FSM, UPDATE / STORAGE, mirror). With no pedal, run `./run.sh vr-ocs2` to publish `/fsm_command` `3` (OCS2).

Wrist and headset poses are on `/teleop/head_pose`, `/teleop/left_ee_pose`, and `/teleop/right_ee_pose` ({ref}`teleop-pose-stream`). The dexterous-hand joint command is `q_des` ([xr_hand_retarget README](https://github.com/fiveages-sim/xr_hand_retarget/blob/main/README.md)).

The RViz card shows the mode the headset is in. [Current mode](#teleop-mode-status). Field names are on {ref}`Teleop topics and data <teleop-topics-and-data>`.

## 7. Arm Following

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
## 8. Controller buttons (分体 vs 全身)

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
### 8.1 Stop one arm vs stop sending VR commands

```{admonition} 停单臂 vs 停发指令
:class: important

On **全身**, default left **Y** / right **B** requests that arm’s WBC ENABLE/DISABLE (**停单臂**). Teleop pause (**停发指令**) is the other meaning of those buttons. Event 16 flips which meaning **Y** / **B** uses.
```

Y/B disable and event 16 apply when **全身** is active (`ocs2_wbc_controller`), VR is enabled, and FSM is **OCS2**. Implementation: [VRInputHandler README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_target_manager/VR_INPUT_HANDLER_README.md) (「单臂启用 / 禁用与 Y/B 语义锁存」).

| What you want | Control | Result |
|---------------|---------|--------|
| **Stop one arm** (停单臂) | Default left **Y** / right **B** | Request that arm’s WBC ENABLE/DISABLE. After WBC confirms `ARM_DISABLED`, VR stops publishing pose to that arm and stops accumulating that arm’s stick offset. The other arm stays controllable. Re-enable rebases from the current robot pose and the current headset / controller pose, then clears that arm’s stick offset. Works in `UPDATE` and in `STORAGE`. |
| **Stop sending VR commands** (停发指令) | After event 16, same left **Y** / right **B** | Freeze / resume VR input for that arm (pause). Needs `UPDATE`. |
| Switch Y/B meaning | Event 16: both grips + left **Y** + right **B** | Latch toggles between “WBC arm disable” and “VR pause/resume”. |

**分体** ignores event 16. Left **Y** / right **B** stay VR pause/resume.

Mirror swaps which physical button maps to which arm. WBC enabled/disabled state and rebase stay on the real arm.

When event 16 switches to pause and that arm is already `ARM_DISABLED`, the handler requests ENABLE, rebases, then freezes as paused. When it switches back to disable and that arm is already VR-paused, it requests DISABLE, then clears pause after WBC confirms. Under pause semantics, the right-stick click into `UPDATE` leaves the pause set.

Constraints on **全身**:

- While the arms are coupled, Y/B cannot toggle a single arm.
- You cannot enable couple while any arm is disabled.
- While coupled, event 16 cannot switch the latch from pause back to disable (the latch stays).
- While a WBC switch or an event-16 conversion is still pending, event 16 and Y/B are ignored.
- If the topology leaves 全身, the latch returns to the default disable meaning.

`yb_pause_semantics` on `teleop/mode_state` is the current meaning of **Y** / **B**. Per-arm pause is `left_arm_paused` / `right_arm_paused`. WBC enable is `left_arm_state` / `right_arm_state` on `WbcCurrentState`. The RViz card shows the pause. [Current mode](#teleop-mode-status).

(teleop-mode-status)=
## 9. Current mode

The RViz card at the top left of the 3D view shows what the headset session is doing. `TELEOP ON` means the arms follow (UPDATE). `TELEOP OFF` means STORAGE: the latest VR pose stays cached, and arm targets plus the VR gripper wait for the next UPDATE. `L`/`R` `RUN` means that arm is following. `PAUSE` is `left_arm_paused` or `right_arm_paused`. Mirror and the gripper mode are on the same card.

The card reads `teleop/mode_state` (`TeleopModeState`). With no robot namespace the topic is `/teleop/mode_state`. In namespace `/robot_a` it is `/robot_a/teleop/mode_state`. Field names, types, and QoS are on {ref}`Teleop topics and data <teleop-topics-and-data>`.

Right-stick click toggles UPDATE and STORAGE while FSM is **OCS2**. In UPDATE the trigger writes the gripper.

On 全身, `yb_pause_semantics` is the current meaning of left **Y** / right **B**. `false` is WBC single-arm disable (停单臂). `true` is teleop pause (停发指令). The buttons are in [Stop one arm vs stop sending VR commands](#stop-one-arm-vs-stop-sending-vr-commands). WBC enable is on {ref}`wbc-current-state`.

### 9.1 RViz teleop HUD

Add `arms_rviz_control_plugin/TeleopModeDisplay` from Displays → Add. `Scale` runs from 0.5 to 2.0. Put RViz in the same namespace as `arms_target_manager`. The card appears when `teleop/mode_state` arrives with `enabled` true, in any FSM state.

The card shows `TELEOP` `ON`/`OFF`, `MIRROR`, and `L`/`R` as `RUN` or `PAUSE`, plus the stick plane, chassis, and gripper mode. A click publishes the same `teleop/controller_state` events as the headset: `4` toggles UPDATE, `7` toggles mirror, and `L`/`R` match left **Y** / right **B**. On 全身, when `yb_pause_semantics` is false, `L`/`R` send event `16` first, wait until that flag becomes true, then send `3` or `6`.

The clip shows this card. `TELEOP ON` is green. `TELEOP OFF` is STORAGE. `PAUSE` is magenta. `RUN` is green. `STICK XY` is the arm stick plane. `WAIST XY` and `WAIST ZYAW` replace those labels while the body mode is 跟随. `GRIP %` is percent mode. `GRIP SW` is open/close.

`MIRROR` stays `OFF` for the whole clip. The card moves from TELEOP off with both arms running, to TELEOP on, through a one-arm pause, then to the waist labels. `GRIP` flips from `%` to `SW` and back; while it shows `SW`, the gripper panel’s buttons read Close.

```{raw} html
<video controls preload="metadata" width="100%">
  <source src="../../_static/videos/vr-teleop-rviz-hud.mp4" type="video/mp4">
</video>
```

Sources: [arms_rviz_control_plugin README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_rviz_control_plugin/README.md) (遥操状态 HUD), [VRInputHandler README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_target_manager/VR_INPUT_HANDLER_README.md), and [arms_target_manager README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_target_manager/README.md).

## 10. Safety

```{admonition} Motion Limits
:class: warning

VR teleoperation can command rapid motions. When using real hardware:
1. Start with low speed limits
2. Keep hand on emergency stop
3. Clear the robot workspace
4. Use workspace limits in software
```

## 11. Network Setup

The headset and the ROS 2 PC must be on a reachable network (same Domain ID; Zenoh or DDS as needed).

- **Pico Enterprise:** USB shared networking (USB 网络共享) — tether the headset to the PC over USB so they share a network. Use the headset’s own USB-network UI.
- **Pico consumer / Meta Quest:** use the usual Wi-Fi (or other IP) path. Do not assume USB 网络共享.

Then:

1. Confirm both devices can reach each other
2. Configure ROS 2 domain or Zenoh bridge if they are not on one LAN
3. Set firewall rules for ROS 2 ports

## 12. Verification

1. VR bridge logs show tracking data
2. `ros2 topic echo /teleop/right_ee_pose` shows updates (use `/<namespace>/teleop/right_ee_pose` when the robot has a namespace)
3. `ros2 topic echo /teleop/mode_state` shows `update_mode: true` while the arms follow (`/<namespace>/teleop/mode_state` in a robot namespace). Subscribe with QoS `Reliable` + `TransientLocal`.
4. The robot follows the VR controllers in UPDATE. In STORAGE the arms and the VR gripper stay put.

(troubleshooting)=
## 13. Troubleshooting

### 13.1 No tracking data

- Check VR device is properly tracked
- Verify browser/app has WebXR permissions
- Check network (Wi-Fi, or USB 网络共享 on Pico Enterprise)
- Confirm the headset App matches the Pico edition (Enterprise vs consumer)

### 13.2 High latency

- Prefer **Pico Enterprise** (USB 网络共享 when possible)
- Use **XRoboToolkit** (menu item `3`, or `./run.sh vr-xrt`). WebXR is menu item `6`
- Use wired / USB-tethered networking when the headset edition supports it
- Reduce update rate in configuration
- Check for network congestion

### 13.3 Robot doesn't follow

- Confirm `enable_vr: true` in the description’s `config/ocs2/target_manager.yaml` (most robots default off)
- Confirm `update_mode` is true on `teleop/mode_state` (UPDATE / HUD `TELEOP ON`) after entering OCS2. In STORAGE, arm targets and the VR gripper wait for the next UPDATE.
- On **全身**, that arm’s `WbcCurrentState` is `ARM_ENABLED`, and `left_arm_paused` / `right_arm_paused` is false when you expect the arm to follow — [Stop one arm vs stop sending VR commands](#stop-one-arm-vs-stop-sending-vr-commands)
- Check target poses are within workspace
- Ensure no safety limits are triggered

### 13.4 `base_footprint` missing (全身 / FULL_BODY)

FULL_BODY may warn that `lookupTransform` cannot find `base_footprint`. Default `vr_follow_frame` is `base_footprint`. Set `vr_follow_frame` in `config/ocs2/target_manager.yaml` to the robot’s real base (for example `base_link`).

## 14. Next Steps

- [How to use impedance control](../4-controllers/13-force_control.md) — MIT-mode force control on Panthera HT / ARX; vendor joint impedance and payload identification on Tianji / Rokae
- [Isomorphic Teleop](7-isomorphic_teleop.md) — master–slave joint following (Panthera HT `mode:=mit` / `effort`)
- [Teleop topics and data](../../4-reference/teleop/8-topics_and_data.md) — topic names, message types, and fields
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md) — `/fsm_command`, and WBC `current_state` / `/mode_command`
- [ocs2_arm_controller](../../4-reference/controllers/2-ocs2_arm_controller.md) — `default_gains` / `pd_gains` and MIX detection
- [marvin-ros2-control](../../4-reference/hardware/6-marvin.md) — Tianji position + `JOINT_IMPEDANCE`
- [vr_pose_publisher](../../4-reference/teleop/1-vr_pose_publisher.md) — the node that publishes `/teleop/*`
