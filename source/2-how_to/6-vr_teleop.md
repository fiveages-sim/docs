# VR Teleoperation

Control robots using a VR headset and controllers.

## Prerequisites

- Working robot demo (mock, sim, or real)
- VR headset (Meta Quest, HTC Vive, etc.)
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

### Vuer (WebXR)

Browser-based VR using Vuer:

```bash
./run.sh vr --mode vuer
```

Open the displayed URL on your VR headset's browser.

### XRoboToolkit

For native VR application integration:

```bash
./run.sh vr --mode xrt
```

Requires XRoboToolkit application on the VR device.

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
