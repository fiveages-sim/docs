# Driver layer

This section documents the **driver layer** (驱动层) — ros2_control hardware plugins (Hardware Interface).

## Overview

The driver layer bridges ROS 2 controllers to physical or simulated hardware:

:::{code-block} none
Controller Manager
       ↓
Driver layer plugin
       ↓
CAN / TCP / Serial / Simulation
:::

## In This Section

```{toctree}
:maxdepth: 1

1-public_hi
2-private_hi
3-sdk_notes
4-ros2_parameters
```

URDF / xacro `<param>` tables (including `topic_based_ros2_control`): [Driver layer parameters](4-ros2_parameters.md).

## Quick Reference

### Public driver layer

| Plugin | Bus | Robots |
|--------|-----|--------|
| [arx-ros2-control](1-public_hi.md) | CAN | ARX X5, Acone (dual-arm), Lift 2S |
| [dobot-cr-ros2-control](1-public_hi.md) | TCP | Dobot CR5, CR10 |
| [unitree-ros2-control](1-public_hi.md) | SDK | Unitree quadrupeds |
| [ht-ros2-control](1-public_hi.md) | Serial | HighTorque Panthera HT |
| [marvin-ros2-control](1-public_hi.md) | Custom | Tianji Marvin |
| [modbus-ros2-control](1-public_hi.md) | RS485 | Grippers |
| [can-ros2-control](1-public_hi.md) | CAN | Various hands |
| [juxie-ros2-control](1-public_hi.md) | CAN FD | JX CSP |

### Private driver layer

| Plugin | Bus | Robots |
|--------|-----|--------|
| rokae-ros2-control | TCP | Rokae arms |
| eyou-ros2-control | CANopen | Harmonic drives |
| eyou_canfd_ros2_control | CAN FD | PHU CSP |
| inex-ros2-control | Custom | iNexus + LinkerHand |
| wuji-ros2-control | Ethernet | Wuji Hand2 |
| dexcap-ros2-control | Custom | DexCap V4 |
| fairino-ros2-control | SDK | Fairino ART |
