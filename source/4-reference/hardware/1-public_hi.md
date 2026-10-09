# Public driver layer

Public ros2_control hardware plugins in the **driver layer** (驱动层), nested under [arms_ros2_control `hardwares/`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/.gitmodules) (plus in-tree `topic_based_ros2_control`). Use the plugin class from that robot’s `xacro/ros2_control/*.xacro`. `<param>` tables: [Driver layer parameters](4-ros2_parameters.md).

## topic_based_ros2_control

In-tree under `arms_ros2_control/hardwares/` (not a nested gitmodule). Plugin: `topic_based_ros2_control/TopicBasedSystem`. Used for `hardware:=isaac`. Parameters: [Driver layer parameters](4-ros2_parameters.md).

```{admonition} Real hardware ready
:class: tip

**ARX Lift 2S** (full-body) and **Acone** / **AC One** (dual-arm) use [arx-ros2-control](https://github.com/fiveages-sim/arx-ros2-control) (CAN). **HighTorque Panthera HT** uses [ht-ros2-control](https://github.com/fiveages-sim/ht-ros2-control) (serial). See [ARX Lift 2S](../../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md) and [HighTorque Panthera HT](../../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md).
```

## ARX (方舟无限)

**Repository:** [fiveages-sim/arx-ros2-control](https://github.com/fiveages-sim/arx-ros2-control) · [README](https://github.com/fiveages-sim/arx-ros2-control/blob/main/README.md)

CAN driver-layer plugins for **ARX** X5 / Acone (dual-arm) and Lift 2S lift + chassis.

| Plugin | Role |
|--------|------|
| `arx_ros2_control/ArxX5Hardware` | One instance per arm (X5 SDK). MIT MIX: `position` + `velocity` + `effort`; kp/kd from `joint_k_gains` / `joint_d_gains` |
| `arx_ros2_control/ArxLiftHardware` | Lift2S column (default CAN `can5`). `hybrid` or `soft_p` / `position`; optional `/cmd_vel` chassis |

Acone `hardware:=real` xacro uses `arx_ros2_control/ArxX5Hardware` ([ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md)).

## Dobot CR

**Repository:** [fiveages-sim/dobot-cr-ros2-control](https://github.com/fiveages-sim/dobot-cr-ros2-control) · [README](https://github.com/fiveages-sim/dobot-cr-ros2-control/blob/main/README.md)

TCP driver-layer plugin for Dobot CR. Plugin: `dobot_ros2_control/DobotHardware`. Dashboard / real-time TCP (README: 29999 command, 30004 realtime). There is no `robot_port` `<param>` in `on_init`.

## Unitree

**Repository:** [fiveages-sim/unitree-ros2-control](https://github.com/fiveages-sim/unitree-ros2-control) · [README](https://github.com/fiveages-sim/unitree-ros2-control/blob/main/README.md)

unitree_sdk2 driver-layer plugin. Plugin XML: `unitree_ros2_control/HardwareUnitree` (the README XML still shows a former `hardware_unitree_sdk2/…` name; use the pluginlib class). That README’s launch examples use `hardware:=unitree_sim` / `unitree_real` with `robot:=unitree_g1`.

## HighTorque (高擎)

**Repository:** [fiveages-sim/ht-ros2-control](https://github.com/fiveages-sim/ht-ros2-control) · [README](https://github.com/fiveages-sim/ht-ros2-control/blob/main/README.md)

Serial driver-layer plugin for **HighTorque Panthera HT**. Plugin: `ht_ros2_control/PantheraHardwareInterface`. Motor YAML in `external/motor_cpp/robot_param/` (`Panthera.yaml` / `PantheraDual.yaml`). Default devices `/dev/ttyACM*`.

Features from that README: isomorphic master–slave teleop path on the description launch; gravity compensation via `ht_gravity_compensation` when kp/kd are not command interfaces.

## Marvin

**Repository:** [fiveages-sim/marvin-ros2-control](https://github.com/fiveages-sim/marvin-ros2-control) · [README](https://github.com/fiveages-sim/marvin-ros2-control/blob/master/README.md)

Marvin SDK driver-layer plugin (M6 and related). Plugin: `marvin_ros2_control/MarvinHardware`. Command interfaces are joint **`position` only**. Compliance is vendor `ctrl_mode` (`POSITION` / `JOINT_IMPEDANCE` / `CART_IMPEDANCE` / `POWER_OFF`) plus `joint_k_gains` / `joint_d_gains`. USB-dongle 夹爪 / 灵巧手 use [Modbus](#modbus) or [CAN](#can), not this package.

Tool-dynamics / 负载辨识 wizard: `ros2 run marvin_ros2_control tool_dyn_identify_wizard`. VR path: [VR Teleoperation](../../2-how_to/5-teleoperation/6-vr_teleop.md).

## Modbus

**Repository:** [fiveages-sim/modbus-ros2-control](https://github.com/fiveages-sim/modbus-ros2-control) · [README](https://github.com/fiveages-sim/modbus-ros2-control/blob/main/README.md)

RS485 / Modbus RTU driver-layer plugins for 夹爪, 灵巧手, and KWR75. Plugins: `ModbusHardware`, `DexterousHandHardware`, `InspireHandHardware`, `FreedomRS485Hardware`, `XHand1RS485Hardware`, `TheoHandModbusHardware`, `Kwr75ForceTorqueSensor`.

## CAN

**Repository:** [fiveages-sim/can-ros2-control](https://github.com/fiveages-sim/can-ros2-control) · [README](https://github.com/fiveages-sim/can-ros2-control/blob/main/README.md)

SocketCAN / CAN FD driver-layer plugins for 灵巧手. Plugins: `O6CanHardware`, `L6CanHardware`, `O7CanHardware`, `FreedomCanHardware`, `InspireCanfdHardware`. Freedom V2 and 夹爪 are out of scope on that README.

## Juxie

**Repository:** [fiveages-sim/juxie-ros2-control](https://github.com/fiveages-sim/juxie-ros2-control) · [README](https://github.com/fiveages-sim/juxie-ros2-control/blob/main/README.md)

CAN FD driver-layer plugin for JX motors in cyclic synchronous position (CSP) mode. Plugin: `juxie_ros2_control/JxHardware`.

## Common operations

```bash
ros2 control list_hardware_interfaces
ros2 control list_controllers
ros2 topic echo /joint_states
```

Hardware `<param>` values do **not** appear on `ros2 param list` unless that plugin also `declare_parameter`s them. Confirm the plugin and xacro as in [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md).
