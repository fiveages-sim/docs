# Private Hardware Interfaces

Private ros2_control hardware interface plugins for internal use.

```{admonition} Access Required
:class: warning

These packages require private repository access.
```

## Rokae

**Repository:** rokae-ros2-control

### Purpose

TCP interface for Rokae collaborative arms.

### Configuration

The interface requires network configuration. Key parameters:

| Parameter | Description |
|-----------|-------------|
| `arm_ip` | Robot controller IP |
| `local_ip` | Host machine IP |

### End-Effector

Supports RS485 end-effector communication.

## Eyou (CANopen)

**Repository:** eyou-ros2-control

### Purpose

CANopen interface for Eyou harmonic drives.

### Notes

Used for specific harmonic actuator configurations.

## Eyou CAN FD

**Repository:** eyou_canfd_ros2_control

### Purpose

CAN FD interface for PHU CSP mode actuators.

### Bench Commands

The interface includes bench testing utilities. See repository for usage.

## iNex

**Repository:** inex-ros2-control

### Purpose

Interface for iNexus arms with LinkerHand integration.

### Features

- Arm control
- Integrated hand support
- Custom protocol

## Wuji

**Repository:** wuji-ros2-control

### Purpose

Ethernet interface for Wuji Hand2 dexterous hands.

### Usage

1. Scan for devices on network
2. Configure hand side (left/right)
3. Launch driver

### Key Parameters

| Parameter | Description |
|-----------|-------------|
| `hand_side` | `left` or `right` |

### Network

Devices are discovered via network scan. Specific IPs are configured at deployment time.

## DexCap

**Repository:** dexcap-ros2-control

### Purpose

Driver for DexCap V4 teleoperation gloves.

### Components

- DexCap driver node
- Joint mappers
- Calibration utilities

### Usage

See [DexCap Teleop](../../2-how_to/8-dexcap_teleop.md) for usage guide.

## Fairino

**Repository:** fairino-ros2-control

### Purpose

ART SDK interface for Fairino arms.

### Configuration

Requires Fairino SDK and network configuration.

| Parameter | Description |
|-----------|-------------|
| `device_ip` | Robot controller IP |
| `port` | Control port |

## Common Patterns

### Parameter Configuration

Private interfaces often require deployment-specific parameters. These should be:

1. Documented in `robot.local.yaml`
2. Not committed to version control
3. Configured per-installation

### Error Handling

Most interfaces provide:
- Connection status reporting
- Automatic reconnection
- Error state publishing

### Debugging

```bash
# Check hardware interface status
ros2 control list_hardware_interfaces

# Monitor joint states
ros2 topic echo /joint_states

# Check for errors
ros2 topic echo /diagnostics
```
