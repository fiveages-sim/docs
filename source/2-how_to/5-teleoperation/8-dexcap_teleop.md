# DexCap Teleoperation

Use the DexCap V4 exoskeleton and gloves for combined arm and hand teleoperation. The exoskeleton measures waist and arm joints; the gloves measure finger joints.

```{admonition} Internal Access Required
:class: warning

DexCap components require access to private repositories. Contact your team lead for access.
```

## Overview

DexCap teleoperation enables:
- Waist and arm joint measurement from the exoskeleton
- Finger joint mapping from the gloves to robot hands
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

Follow that **private workspace’s README** for its init / setup scripts.

### 3. Start the driver

```bash
ros2 launch dexcap_ros2_control dexcap_driver.launch.py
```

To start only the exoskeleton or only one glove, pass `start_upper_body`, `start_left_hand`, and `start_right_hand` as in the private package README. That README is also the place to look for first-connection safety; `publish_command` is not a current launch argument.

## Launch Order

```{admonition} Important
:class: important

Launch components in this order:
1. Robot control stack (arm + hand)
2. DexCap driver
3. Teleop joint mapper
```

Launch order, package names, and topics: the **private README**.

## Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/dexcap/waist` | `JointState` | Waist joints from the exoskeleton |
| `/dexcap/left_arm` | `JointState` | Left arm joints from the exoskeleton |
| `/dexcap/right_arm` | `JointState` | Right arm joints from the exoskeleton |
| `/dexcap/left_hand` | `JointState` | Left glove, 21 joints |
| `/dexcap/right_hand` | `JointState` | Right glove, 21 joints |

Mapper outputs and further topics are in the private README.

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
2. `/dexcap/left_hand` and `/dexcap/right_hand` publish glove joint angles; `/dexcap/waist`, `/dexcap/left_arm`, and `/dexcap/right_arm` publish when the exoskeleton is started
3. The robot hand follows the gloves; the arms follow the exoskeleton when arm mapping is enabled

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
- [wuji-ros2-control](../../4-reference/teleop/7-wuji_hand_hi.md) (Hand hardware) — private names: [Hardware Interfaces](../../4-reference/hardware/0-index.md)
