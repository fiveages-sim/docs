# Hardware Interfaces

This section documents ros2_control **hardware interfaces** — plugins that talk to the bus, vendor SDK, or simulation. Chinese **驱动层** is this same layer.

Public plugins live under [arms_ros2_control `hardwares/`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/.gitmodules) (plus in-tree `topic_based_ros2_control`). Use the plugin class from that robot’s `xacro/ros2_control/*.xacro`. Each public driver page has the intro (plugin class, repo) and its `<param>` tables.

## Terminology

Full mapping: [Terminology](../../3-concepts/8-terminology.md).

| Chinese | English |
|---------|---------|
| 驱动层 | Hardware Interface (ros2_control official) |
| 控制器 | Controller |
| 分体控制 | Split body |
| 全身控制 | Full body / WBC |
| 夹爪 | gripper |
| 灵巧手 | dexterous hand |
| 仿真路径 | `mock_components` / `isaac` / `gz` (launch keys, not `hardwares/` packages) |

Plugin class names, `type` / `left_type` / `right_type`, and `hardware:=` stay as code.

## Overview

Hardware interfaces bridge ROS 2 controllers to the bus or vendor SDK:

:::{code-block} none
Controller Manager
       ↓
Hardware Interface Plugin
       ↓
CAN / TCP / Serial / Vendor SDK
:::

Launch `hardware:=` chooses which plugin the robot xacro instantiates: [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md).

```{admonition} Real hardware ready
:class: tip

**ARX Lift 2S** (full-body) and **Acone** / **AC One** (dual-arm) use [arx-ros2-control](4-arx.md) (CAN). **HighTorque Panthera HT** uses [ht-ros2-control](5-ht.md) (serial). See [ARX Lift 2S](../../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md) and [HighTorque Panthera HT](../../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md).
```

(how-to-read-the-tables)=
## How to read the tables

These are URDF / xacro `<param>` entries under `<ros2_control><hardware>`, loaded in the plugin `on_init`. They are **not** the same API as `ros2 param list` on a controller node, unless that plugin also `declare_parameter`s them (ARX, HighTorque, Marvin, some 灵巧手).

**Startup only** vs **Runtime** appears **once** per table: a **When** column on mixed tables, a section heading (`Startup` / `Runtime`), or a one-line note above a uniform table. **Meaning** is the parameter’s actual meaning — not a repeat of that tag.

| Tag | Evidence |
|-----|----------|
| **Startup only** | Read in `on_init` from `info_.hardware_parameters`. No `add_on_set_parameters_callback` (or README does not claim a hot update). Change the xacro and restart the hardware / `controller_manager`. |
| **Runtime** | `add_on_set_parameters_callback`, or a README + source path that re-reads `ros2 param set` without reload (HighTorque kp/kd poll). |

The in-tree [`hardwares/README.md`](https://github.com/fiveages-sim/arms_ros2_control/blob/d50933d6862ad35ec7633ef522a134924827b115/hardwares/README.md) is **build-only** (`colcon build --packages-up-to …`). Names on the driver pages come from each public README and from `on_init` / plugin XML in that repository.

How to inspect: [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md).

## Simulation keys

`mock_components`, `gz`, and `isaac` are launch / xacro keys. They are **not** gitmodules under `arms_ros2_control/hardwares/`.

| `hardware:=` | Plugin | Where it lives |
|--------------|--------|----------------|
| `mock_components` | `mock_components/GenericSystem` | ros2_control; Acone xacro |
| `gz` | `gz_ros2_control/GazeboSimSystem` | `ros-jazzy-gz-ros2-control` |
| `isaac` | `topic_based_ros2_control/TopicBasedSystem` | in-tree under `hardwares/topic_based_ros2_control` (not a nested vendor repo) |

How-to: [Gazebo Simulation](../../2-how_to/2-simulation/3-gazebo_sim.md), [Isaac Sim](../../2-how_to/2-simulation/4-isaac_sim.md). Joint layout and topic names come from that robot’s `xacro/ros2_control/*.xacro`. Isaac topic `<param>` table: [topic_based_ros2_control](1-topic_based.md).

## In This Section

```{toctree}
:maxdepth: 1

1-topic_based
2-unitree
3-dobot
4-arx
5-ht
6-marvin
7-modbus
8-can
9-juxie
```

## Public Hardware Interfaces

| Package | Bus | Plugins / robots |
|---------|-----|------------------|
| [topic_based_ros2_control](1-topic_based.md) | ROS 2 topics | Isaac (`hardware:=isaac`) |
| [unitree-ros2-control](2-unitree.md) | unitree_sdk2 | Unitree G1 / quadruped |
| [dobot-cr-ros2-control](3-dobot.md) | TCP | Dobot CR |
| [arx-ros2-control](4-arx.md) | CAN | ARX X5, Acone (dual-arm), Lift 2S |
| [ht-ros2-control](5-ht.md) | Serial (`ttyACM`) | HighTorque Panthera HT |
| [marvin-ros2-control](6-marvin.md) | Marvin SDK + RS485/CAN tools | Tianji Marvin |
| [modbus-ros2-control](7-modbus.md) | RS485 / Modbus RTU | Grippers, 灵巧手, KWR75 |
| [can-ros2-control](8-can.md) | SocketCAN / CAN FD | LinkerHand, Freedom V1, Inspire RH56 |
| [juxie-ros2-control](9-juxie.md) | CAN FD | JX CSP |

## Private Hardware Interfaces

Names only — configuration keys, API details, and SDK env vars stay in **that repository’s README after access**.

```{admonition} Access Required
:class: warning

These packages require private repository access. Contact your team lead for access.
```

| Package | Bus | Robots |
|---------|-----|--------|
| rokae-ros2-control | TCP | Rokae collaborative arms |
| eyou-ros2-control | CANopen | Eyou harmonic drives |
| eyou_canfd_ros2_control | CAN FD | PHU CSP |
| inex-ros2-control | Custom | iNexus + LinkerHand |
| [wuji-ros2-control](../teleop/7-wuji_hand_hi.md) | Ethernet | Wuji Hand2 |
| [dexcap-ros2-control](../../2-how_to/5-teleoperation/8-dexcap_teleop.md) | Custom | DexCap V4 |
| fairino-ros2-control | ART SDK | Fairino arms |

`fairino-ros2-control` wraps the Fairino ART SDK (install and network setup are in that README after access).

## Common operations

```bash
ros2 control list_hardware_interfaces
ros2 control list_controllers
ros2 topic echo /joint_states
```

Hardware `<param>` values do **not** appear on `ros2 param list` unless that plugin also `declare_parameter`s them. Confirm the plugin and xacro as in [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md).

`{robot}_description/config/ocs2/*.info` are **OCS2 task / model files**, not ROS 2 parameters. `robot_name` chooses the description package at startup — [Controller ROS 2 parameters](../controllers/8-ros2_parameters.md).

## Related

- [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md)
- [Controller ROS 2 parameters](../controllers/8-ros2_parameters.md)
- [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md)
- [Terminology](../../3-concepts/8-terminology.md)
