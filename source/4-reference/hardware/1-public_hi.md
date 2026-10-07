# Public Hardware Interfaces

Public ros2_control hardware interface plugins.

```{admonition} Real Hardware Ready
:class: tip

**ARX Lift 2S** (full-body) and **Acone** / **AC One** (arm only) use [arx-ros2-control](https://github.com/fiveages-sim/arx-ros2-control) (CAN). **HighTorque Panthera HT** uses [ht-ros2-control](https://github.com/fiveages-sim/ht-ros2-control) (serial). See [ARX Lift 2S](../../2-how_to/11-arx_lift2s.md) and [HighTorque Panthera HT](../../2-how_to/12-panthera_ht.md).
```

## ARX (方舟无限)

**Repository:** [fiveages-sim/arx-ros2-control](https://github.com/fiveages-sim/arx-ros2-control)

### Purpose

CAN bus interface for ARX robots (X5, Acone arm, Lift 2S full-body).

### Configuration

```xml
<ros2_control name="ArxSystem" type="system">
  <hardware>
    <plugin>arx_ros2_control/ArxHardwareInterface</plugin>
    <param name="can_interface">can0</param>
  </hardware>
</ros2_control>
```

### CAN Setup

```bash
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 up
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `can_interface` | string | CAN interface name |

## Dobot CR

**Repository:** [fiveages-sim/dobot-cr-ros2-control](https://github.com/fiveages-sim/dobot-cr-ros2-control)

### Purpose

TCP interface for Dobot CR series collaborative robots.

### Configuration

```xml
<ros2_control name="DobotSystem" type="system">
  <hardware>
    <plugin>dobot_cr_ros2_control/DobotCRHardwareInterface</plugin>
    <param name="robot_ip">192.168.1.6</param>
    <param name="robot_port">29999</param>
  </hardware>
</ros2_control>
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `robot_ip` | string | Robot IP address |
| `robot_port` | int | Control port |

```{admonition} TODO
:class: warning

Some roadmap features are not yet implemented. Check repository issues for status.
```

## Unitree

**Repository:** [fiveages-sim/unitree-ros2-control](https://github.com/fiveages-sim/unitree-ros2-control)

### Purpose

SDK2 interface for Unitree quadruped robots.

### Configuration

```xml
<ros2_control name="UnitreeSystem" type="system">
  <hardware>
    <plugin>unitree_ros2_control/UnitreeHardwareInterface</plugin>
    <param name="simulation">false</param>
  </hardware>
</ros2_control>
```

### Modes

| Mode | Description |
|------|-------------|
| `simulation` | SDK simulation mode |
| `real` | Physical hardware |

## HighTorque (高擎)

**Repository:** [fiveages-sim/ht-ros2-control](https://github.com/fiveages-sim/ht-ros2-control)

### Purpose

Serial interface for **HighTorque Panthera HT** robots.

### Configuration

```xml
<ros2_control name="HTSystem" type="system">
  <hardware>
    <plugin>ht_ros2_control/HTHardwareInterface</plugin>
    <param name="serial_port">/dev/ttyACM0</param>
  </hardware>
</ros2_control>
```

### Features

- Isomorphic master–slave teleop
- Gravity compensation on the master role

## Marvin

**Repository:** [fiveages-sim/marvin-ros2-control](https://github.com/fiveages-sim/marvin-ros2-control)

### Purpose

Interface for Tianji Marvin robots with end-effector matrix support.

### Configuration

See repository README for detailed configuration options.

### End-Effector Matrix

Supports multiple end-effector configurations:
- Grippers
- Hands
- Custom tools

## Modbus

**Repository:** [fiveages-sim/modbus-ros2-control](https://github.com/fiveages-sim/modbus-ros2-control)

### Purpose

RS485 Modbus interface for grippers and actuators.

### Supported Devices

| Device | Protocol |
|--------|----------|
| KWR75 | Modbus RTU |
| Various grippers | Modbus RTU |

### Configuration

```xml
<ros2_control name="ModbusGripper" type="system">
  <hardware>
    <plugin>modbus_ros2_control/ModbusHardwareInterface</plugin>
    <param name="serial_port">/dev/ttyUSB0</param>
    <param name="baudrate">115200</param>
  </hardware>
</ros2_control>
```

## CAN

**Repository:** [fiveages-sim/can-ros2-control](https://github.com/fiveages-sim/can-ros2-control)

### Purpose

Generic CAN/CAN FD interface for hands and actuators.

### Supported Devices

- CAN-based dexterous hands
- CAN FD actuators

### Configuration

```xml
<ros2_control name="CANHand" type="system">
  <hardware>
    <plugin>can_ros2_control/CANHardwareInterface</plugin>
    <param name="can_interface">can0</param>
  </hardware>
</ros2_control>
```

## Juxie

**Repository:** [fiveages-sim/juxie-ros2-control](https://github.com/fiveages-sim/juxie-ros2-control)

### Purpose

CAN FD interface for JX CSP actuators.

### Configuration

See repository README for configuration details.

```{admonition} TODO
:class: warning

Product mapping documentation to be expanded.
```

## Common Operations

### List Hardware Interfaces

```bash
ros2 control list_hardware_interfaces
```

### Check Controller Manager

```bash
ros2 control list_controllers
```

### Hardware State

```bash
ros2 topic echo /joint_states
```
