# Driver layer

This section documents the **driver layer** (驱动层) — ros2_control hardware plugins (Hardware Interface).

## Overview

The driver layer bridges ROS 2 controllers to the bus or vendor SDK:

:::{code-block} none
Controller Manager
       ↓
Driver layer plugin
       ↓
CAN / TCP / Serial / Vendor SDK
:::

Launch `hardware:=` chooses which plugin the robot xacro instantiates: [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md). URDF / xacro `<param>` tables: [Driver layer parameters](4-ros2_parameters.md).

## Simulation keys

`mock_components`, `gz`, and `isaac` are launch / xacro keys. They are **not** gitmodules under `arms_ros2_control/hardwares/`.

| `hardware:=` | Plugin | Where it lives |
|--------------|--------|----------------|
| `mock_components` | `mock_components/GenericSystem` | ros2_control; Acone xacro |
| `gz` | `gz_ros2_control/GazeboSimSystem` | `ros-jazzy-gz-ros2-control` |
| `isaac` | `topic_based_ros2_control/TopicBasedSystem` | in-tree under `hardwares/topic_based_ros2_control` (not a nested vendor repo) |

How-to: [Gazebo Simulation](../../2-how_to/2-simulation/3-gazebo_sim.md), [Isaac Sim](../../2-how_to/2-simulation/4-isaac_sim.md). Joint layout and topic names come from that robot’s `xacro/ros2_control/*.xacro`.

## In This Section

```{toctree}
:maxdepth: 1

1-public_hi
2-private_hi
3-sdk_notes
4-ros2_parameters
```

## Quick Reference

### Public driver layer

| Package | Bus | Plugins / robots |
|---------|-----|------------------|
| [topic_based_ros2_control](4-ros2_parameters.md) | ROS 2 topics | Isaac (`hardware:=isaac`) |
| [arx-ros2-control](1-public_hi.md) | CAN | ARX X5, Acone (dual-arm), Lift 2S |
| [dobot-cr-ros2-control](1-public_hi.md) | TCP | Dobot CR |
| [unitree-ros2-control](1-public_hi.md) | unitree_sdk2 | Unitree G1 / quadruped |
| [ht-ros2-control](1-public_hi.md) | Serial (`ttyACM`) | HighTorque Panthera HT |
| [marvin-ros2-control](1-public_hi.md) | Marvin SDK + RS485/CAN tools | Tianji Marvin |
| [modbus-ros2-control](1-public_hi.md) | RS485 / Modbus RTU | Grippers, 灵巧手, KWR75 |
| [can-ros2-control](1-public_hi.md) | SocketCAN / CAN FD | LinkerHand, Freedom V1, Inspire RH56 |
| [juxie-ros2-control](1-public_hi.md) | CAN FD | JX CSP |

### Private driver layer

Names only — parameters stay in that repository’s README after access: [Private driver layer](2-private_hi.md).

| Package | Bus | Robots |
|---------|-----|--------|
| rokae-ros2-control | TCP | Rokae arms |
| eyou-ros2-control | CANopen | Harmonic drives |
| eyou_canfd_ros2_control | CAN FD | PHU CSP |
| inex-ros2-control | Custom | iNexus + LinkerHand |
| wuji-ros2-control | Ethernet | Wuji Hand2 |
| dexcap-ros2-control | Custom | DexCap V4 |
| fairino-ros2-control | SDK | Fairino ART |
