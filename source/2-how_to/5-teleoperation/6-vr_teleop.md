# VR Teleoperation

Control robots using a VR headset and controllers.

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

## Overview

VR teleoperation publishes end-effector pose targets from VR controller tracking. The MPC controller then generates joint trajectories to follow these targets.

How the arm **complies** with those poses depends on the robot. Two different paths are used with VR teleop:

| Path | Robots | Who provides compliance | What the controller commands |
|------|--------|-------------------------|------------------------------|
| **MIT-mode force control** | **HighTorque** (高擎) **Panthera HT**; **ARX** (方舟无限) arms | Controller + hardware interface in MIT / `full_control` (pos + vel + effort; stiffness on the HI) | Force-capable / MIX when the interfaces allow it |
| **Vendor joint impedance** | **Tianji** (天玑); **Rokae** (珞石) | Vendor stack, exposed on the hardware interface | **Position only** |

**Payload identification (负载辨识)** belongs to the **vendor-impedance** path (Tianji / Rokae), not the MIT path. Details below.

## Force control and compliance

### MIT-mode force control (Panthera HT / ARX)

Use this path on **Panthera HT** and **ARX** arms. The hardware interface must run a **force-capable** MIT configuration; the controller then tracks VR poses with that mix of position / velocity / effort.

**HighTorque Panthera HT** — [ht-ros2-control README](https://github.com/fiveages-sim/ht-ros2-control/blob/main/README.md):

- HI `control_mode:=mit` (default; older name `full_control` still accepted)
- The driver sends position + velocity + effort + kp/kd (`pos_vel_tqe_kp_kd`)
- Stiffness is HI parameters `joint_kp` / `joint_kd` (rqt / `ros2 param`), **not** kp/kd command interfaces
- Other documented HI modes: `effort` (torque only), `position` (position only)

**ARX arms** — [arx-ros2-control README](https://github.com/fiveages-sim/arx-ros2-control/blob/main/README.md):

- Arms support only `full_control` / MIT MIX. Other `control_mode` values in xacro are warned and ignored
- `write()` always sends position + velocity + effort
- MIT `kp` / `kd` come from HI `joint_k_gains` / `joint_d_gains` (no kp/kd command interface)
- README mapping: OCS2 trajectory → position; OCS2 `future_input` → velocity; OCS2 effort → gravity / static feedforward torque

**Controller** — [ocs2_arm_controller README — Interface Configuration](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/README.md):

- Mode is **auto-detected** from the robot config (no extra launch flag named `force:=`)
- Position-only: command `position`; state `position` + `velocity`
- Force / MIX: command `position`, `velocity`, `effort`, `kp`, `kd` all present; YAML `force_gains` is `[kp, kd]`
- ARX documents OCS2 MIX as pos + vel + effort with kp/kd on the HI. HT notes that when kp/kd are **not** command interfaces, OCS2 may stay in position mode; gravity compensation then uses `ht_gravity_compensation` or larger `joint_kp` (same HT README)

Bring the robot up with the lean-branch `./quick_start.sh` / `hardware:=real` path on [HighTorque Panthera HT](../6-deployment/9-go_real_hardware/2-panthera_ht.md) or [ARX Lift 2S](../6-deployment/9-go_real_hardware/1-arx_lift2s.md), then start VR as below.

This MIT path is **not** isomorphic teleop. Master–slave `mode:=mit` / `effort` on Panthera HT is [Isomorphic Teleop](7-isomorphic_teleop.md).

### Vendor joint impedance (Tianji / Rokae)

Use this path on **Tianji** (天玑) and **Rokae** (珞石). The controller only sends **joint position**. Joint impedance / compliance is the **vendor** feature, switched on the hardware interface.

**Tianji** — [marvin-ros2-control README](https://github.com/fiveages-sim/marvin-ros2-control/blob/master/README.md):

- Command interfaces: joint **`position` only**. State: `position`, `velocity`, `effort`
- Runtime `ctrl_mode`: `POSITION` / `JOINT_IMPEDANCE` / `CART_IMPEDANCE` / `POWER_OFF`
- Joint impedance gains: `joint_k_gains` / `joint_d_gains` (7 values). Cartesian: `cart_k_gains` / `cart_d_gains`
- Example: `ros2 param set /<hardware_node> ctrl_mode JOINT_IMPEDANCE`

**Rokae** — same pattern (position commands; compliance in the vendor HI). Parameter names are in the private `rokae-ros2-control` README after access. Overview: [Private hardware interfaces](../../4-reference/hardware/2-private_hi.md).

Internal FA robots that use Tianji / Rokae arms live in [fa-deploy-ws Setup](../../1-getting_started/4-fa_deploy_ws.md). Extra robot IDs and launch flags are in that workspace README after access.

### Payload identification (负载辨识)

负载辨识 is **only** on the Tianji / Rokae (vendor impedance) path. It is not an MIT / OCS2 `force_gains` procedure.

**Public, verified Tianji wizard** (semi-automatic tool-dynamics ID on CCS): [marvin-ros2-control `scripts/tool_dyn_identify_wizard.py`](https://github.com/fiveages-sim/marvin-ros2-control/blob/master/scripts/tool_dyn_identify_wizard.py), installed as `ros2 run marvin_ros2_control tool_dyn_identify_wizard` (`CMakeLists.txt` `install(PROGRAMS … RENAME tool_dyn_identify_wizard)`).

The wizard banner is **机械臂负载辨识向导（工具动力学参数辨识 / CCS）**. It connects to the Marvin controller IP, collects no-load then loaded PVT trajectories, and prints 10-D tool dynamics (`m, mx, my, mz, ixx, …`). Those values match HI parameters `left_dyn_param` / `right_dyn_param` on the same README.

There is **no** public `open-deploy-ws` payload-ID flow. Internal on-site Tianji payload identification is in the private **fa-deploy-ws** README after access (default branch is typically `fa-w2`). Use that README’s script names — they are not listed here.

## Setup

### 1. Install fa-py-libraries

:::{code-block} bash
cd ~/
git clone https://github.com/fiveages-sim/fa-py-libraries.git
cd fa-py-libraries
./init.sh all
:::

What `./init.sh all` does: submodules + Python 3.12 env + `ros2_robot_interface` / `ros2-viser` / `vr_pose_publisher`.

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

Requires the **edition-matching** XRoboToolkit App on the headset (Enterprise App ≠ consumer Pico App) plus PC Service. `./run.sh vr-xrt-service stop` shuts down the PC Service.

## Topics

VR teleoperation publishes to:

| Topic | Type | Description |
|-------|------|-------------|
| `/teleop/left_ee_pose` | `PoseStamped` | Left hand target pose |
| `/teleop/right_ee_pose` | `PoseStamped` | Right hand target pose |
| `/teleop/head_pose` | `PoseStamped` | Head tracking |
| `/teleop/trigger` | `Bool` | Controller trigger state |

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

## Gripper Control

VR controller buttons map to gripper:

| Button | Action |
|--------|--------|
| Trigger | Close gripper (proportional) |
| Grip | Toggle gripper state |

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
2. `ros2 topic echo /teleop/right_ee_pose` shows updates
3. Robot follows VR controller motion

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

- Verify controller is in teleop mode
- Check target poses are within workspace
- Ensure no safety limits are triggered

## Next Steps

- [Isomorphic Teleop](7-isomorphic_teleop.md) for master–slave joint following (Panthera HT `mode:=mit` / `effort` — not the VR MIT path above)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md) for mode control
- [ocs2_arm_controller](../../4-reference/controllers/2-ocs2_arm_controller.md) — `force_gains` and MIX detection
- [marvin-ros2-control](../../4-reference/hardware/1-public_hi.md) — Tianji position + `JOINT_IMPEDANCE`
