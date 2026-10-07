# DexCap Teleoperation

Use DexCap gloves for dexterous hand teleoperation.

```{admonition} Internal Access Required
:class: warning

DexCap components require access to private repositories. Contact your team lead for access.
```

## Overview

DexCap teleoperation enables:
- High-fidelity hand tracking via glove sensors
- Finger joint mapping to robot hands
- Combined arm + hand teleoperation

## Components

The DexCap system consists of:

| Component | Repository | Purpose |
|-----------|------------|---------|
| dexcap-ros2-control | Private | DexCap V4 driver |
| dexcap_teleop_ws | Private | Deployment workspace |
| teleop-joint-mapper | Private | DexCap to robot mapping |

## Setup

### 1. Clone Workspace

```bash
git clone <internal>/dexcap_teleop_ws.git
cd dexcap_teleop_ws
```

### 2. Initialize Environment

Follow that **private workspace’s README** for its init / setup scripts. This page does not invent `conda create -n dexcap`, `deploy/deploy_fw.sh`, or `deploy/setup_env.bash`.

### 3. Initialize Connection

First connection should disable commands for safety:

```bash
ros2 launch dexcap_ros2_control driver.launch.py publish_command:=false
```

## Launch Order

```{admonition} Important
:class: important

Launch components in this order:
1. Robot control stack (arm + hand)
2. DexCap driver
3. Teleop joint mapper
```

Launch order, package names, and topics: the **private README**. Do not invent `<robot>_bringup`, a hand-written `conda activate`, or extra launch files here.

## Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/dexcap/joint_states` | `JointState` | Raw glove joint angles |
| `/dexcap/hand_pose` | `PoseStamped` | Hand position/orientation |
| `/teleop/target_hand_joints` | `JointState` | Mapped robot hand targets |

## Joint Mapping

The mapper translates DexCap joint angles to robot-specific joints:

```yaml
# Example mapping config
mapping:
  dexcap_thumb_mcp: robot_thumb_base
  dexcap_thumb_pip: robot_thumb_proximal
  dexcap_index_mcp: robot_index_base
  # ...
```

## Safety

```{admonition} Calibration Required
:class: warning

Before each session:
1. Calibrate gloves in neutral position
2. Verify joint limits are enforced
3. Test with mock hardware first
```

## Verification

1. DexCap driver shows connected status
2. `/dexcap/joint_states` publishes hand joint angles
3. Robot hand follows glove motion
4. Arm follows hand position (if arm teleop enabled)

## Troubleshooting

### Driver fails to connect

- Check USB/Bluetooth connection
- Verify firmware is deployed
- Check device permissions

### Hand motion reversed

- Check left/right hand configuration
- Verify joint mapping signs

### Latency issues

- Use wired connection
- Reduce update rate
- Check for dropped packets

## Related

- [teleop-joint-mapper reference](../../4-reference/teleop/4-teleop_joint_mapper.md)
- [wuji-ros2-control reference](../../4-reference/hardware/2-private_hi.md) (Hand hardware)
