# wuji-ros2-control

Driver-layer plugin for Wuji Hand2.

```{admonition} Access Required
:class: warning

This package requires private repository access.
```

**Repository:** wuji-ros2-control (private)

## Purpose

Ethernet driver-layer plugin for Wuji Hand2 dexterous hands.

## Features

- Network device discovery
- Multi-finger control
- Force feedback

## Configuration

```xml
<ros2_control name="WujiHand" type="system">
  <hardware>
    <plugin>wuji_ros2_control/WujiHardwareInterface</plugin>
    <param name="hand_side">left</param>
  </hardware>
</ros2_control>
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `hand_side` | `left` or `right` |

## Network

Hands are discovered via network scan. Configuration involves:
1. Network interface selection
2. Hand discovery
3. Side assignment

## Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/wuji_hand/joint_states` | `JointState` | Current finger positions |
| `/wuji_hand/joint_commands` | `JointState` | Target positions |

## Related

- [wuji_glove_teleop](5-wuji_glove.md)
- [Private driver layer](../hardware/2-private_hi.md)
