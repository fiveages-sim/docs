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

- [Isomorphic Teleop](7-isomorphic_teleop.md) for master–slave joint following
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md) for mode control
