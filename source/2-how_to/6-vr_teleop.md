# VR Teleoperation

Control robots using a VR headset and controllers.

## Supported Headsets

| Headset | Support Level | Modes | Notes |
|---------|---------------|-------|-------|
| **Pico** | **Recommended** | Web, XROtoolkit | Enterprise edition has faster release cadence, enabling lower-latency tracking |
| **Meta Quest** | Supported | Web, XROtoolkit | Good consumer availability |

```{admonition} Pico Recommended
:class: tip

**Pico headsets have the best support**, especially the enterprise edition which offers faster release updates and lower-latency tracking for more responsive robot control (更跟手).
```

## Prerequisites

- Working robot demo (mock, sim, or real)
- VR headset (**Pico** recommended, or **Meta Quest**)
- fa-py-libraries installed
- Network connectivity between VR device and ROS 2 machine

## Overview

VR teleoperation publishes end-effector pose targets from VR controller tracking. The MPC controller then generates joint trajectories to follow these targets.

## Setup

### 1. Install fa-py-libraries

```bash
cd ~/
git clone https://github.com/fiveages-sim/fa-py-libraries.git
cd fa-py-libraries
pip install -e .
```

### 2. Start Robot Demo

```bash
source ~/open-deploy-ws/install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=mock
```

### 3. Start VR Bridge

In a new terminal:

```bash
cd ~/fa-py-libraries
./run.sh vr
```

This starts the VR pose publisher that bridges VR tracking to ROS 2.

## VR Modes

Both **Pico** and **Meta Quest** support two connection modes:

| Mode | Connection | Setup | Latency |
|------|------------|-------|---------|
| **Web** (WebXR) | Browser-based | Easy | Higher |
| **XROtoolkit** | Native app | Requires app install | Lower |

### Web Mode (WebXR)

Browser-based VR using Vuer — works on both Pico and Meta Quest:

```bash
./run.sh vr --mode vuer
```

Open the displayed URL on your VR headset's browser. No app installation required.

### XROtoolkit Mode

Native application for lower latency — recommended for production:

```bash
./run.sh vr --mode xrt
```

Requires XROtoolkit application installed on the VR device. Provides better tracking responsiveness, especially on Pico enterprise devices.

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

For VR device on different network:

1. Ensure both devices can reach each other
2. Configure ROS 2 domain or Zenoh bridge
3. Set proper firewall rules for ROS 2 ports

## Verification

1. VR bridge logs show tracking data
2. `ros2 topic echo /teleop/right_ee_pose` shows updates
3. Robot follows VR controller motion

## Troubleshooting

### No tracking data

- Check VR device is properly tracked
- Verify browser/app has WebXR permissions
- Check network connectivity

### High latency

- Use **Pico enterprise edition** for lowest latency tracking
- Use **XROtoolkit mode** instead of Web mode
- Use wired network if possible
- Reduce update rate in configuration
- Check for network congestion

### Robot doesn't follow

- Verify controller is in teleop mode
- Check target poses are within workspace
- Ensure no safety limits are triggered

## Next Steps

- [Drag Teleop](7-drag_teleop.md) for manual teaching
- [FSM and Topics](../3-concepts/4-fsm_and_topics.md) for mode control
