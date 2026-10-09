# Private Hardware Interfaces

Private ros2_control hardware interface plugins for internal use.

```{admonition} Access Required
:class: warning

These packages require private repository access. Contact your team lead for access.
```

## Overview

The following private hardware interfaces are available for internal deployments. For specific configuration parameters, API details, and usage instructions, refer to each repository's README and documentation.

## Rokae

**Repository:** rokae-ros2-control (private)

TCP interface for Rokae collaborative arms.

```{admonition} TODO
:class: note

See repository README for configuration parameters and setup instructions.
```

## Eyou (CANopen)

**Repository:** eyou-ros2-control (private)

CANopen interface for Eyou harmonic drives.

```{admonition} TODO
:class: note

See repository README for actuator configuration and usage.
```

## Eyou CAN FD

**Repository:** eyou_canfd_ros2_control (private)

CAN FD interface for PHU CSP mode actuators.

```{admonition} TODO
:class: note

See repository README for bench testing utilities and configuration.
```

## iNex

**Repository:** inex-ros2-control (private)

Interface for iNexus arms with LinkerHand integration.

```{admonition} TODO
:class: note

See repository README for arm and hand configuration details.
```

## Wuji

**Repository:** wuji-ros2-control (private)

Ethernet interface for Wuji Hand2 dexterous hands.

```{admonition} TODO
:class: note

See repository README for network discovery, hand configuration, and deployment parameters.
```

## DexCap

**Repository:** dexcap-ros2-control (private)

Driver for DexCap teleoperation gloves.

See [DexCap Teleop](../../2-how_to/5-teleoperation/8-dexcap_teleop.md) for usage guide.

```{admonition} TODO
:class: note

See repository README for driver configuration and calibration procedures.
```

## Fairino

**Repository:** fairino-ros2-control (private)

ART SDK interface for Fairino arms.

```{admonition} TODO
:class: note

See repository README for SDK setup and network configuration.
```

Parameter lists after access: each private README. Pointers only: [Hardware interface parameters](4-ros2_parameters.md).

## Common Patterns

### Parameter Configuration

Private interfaces often require deployment-specific parameters that should be:

1. Configured per-installation
2. Documented in that repository’s local / per-install config (the filename lives in its README)
3. Not committed to version control

### Debugging

```bash
# Check hardware interface status
ros2 control list_hardware_interfaces

# Monitor joint states
ros2 topic echo /joint_states
```

For interface-specific debugging, refer to each repository's documentation.
