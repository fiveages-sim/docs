# Hardware Interfaces Reference

This section documents the ros2_control hardware interface plugins.

## Overview

Hardware interfaces bridge ROS 2 controllers to physical or simulated hardware:

```
Controller Manager
       ↓
Hardware Interface Plugin
       ↓
CAN / TCP / Serial / Simulation
```

## In This Section

```{toctree}
:maxdepth: 1

1-public_hi
2-private_hi
3-sdk_notes
```

## Quick Reference

### Public Interfaces

| Interface | Bus | Robots |
|-----------|-----|--------|
| [arx-ros2-control](1-public_hi.md#arx) | CAN | ARX X5, ACone, Lift2S |
| [dobot-cr-ros2-control](1-public_hi.md#dobot-cr) | TCP | Dobot CR5, CR10 |
| [unitree-ros2-control](1-public_hi.md#unitree) | SDK | Unitree quadrupeds |
| [ht-ros2-control](1-public_hi.md#ht) | Serial | HT Panthera |
| [marvin-ros2-control](1-public_hi.md#marvin) | Custom | Tianji Marvin |
| [modbus-ros2-control](1-public_hi.md#modbus) | RS485 | Grippers |
| [can-ros2-control](1-public_hi.md#can) | CAN | Various hands |
| [juxie-ros2-control](1-public_hi.md#juxie) | CAN FD | JX CSP |

### Private Interfaces

| Interface | Bus | Robots |
|-----------|-----|--------|
| rokae-ros2-control | TCP | Rokae arms |
| eyou-ros2-control | CANopen | Harmonic drives |
| eyou_canfd_ros2_control | CAN FD | PHU CSP |
| inex-ros2-control | Custom | iNexus + LinkerHand |
| wuji-ros2-control | Ethernet | Wuji Hand2 |
| dexcap-ros2-control | Custom | DexCap V4 |
| fairino-ros2-control | SDK | Fairino ART |
