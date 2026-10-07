# Vendor Arms (Private)

Private vendor arm descriptions for FiveAges integrations.

```{admonition} Access Required
:class: warning

These packages require private repository access.
```

## Tianji

**Repository:** robot-descriptions-tianji

### Robots

| Robot | Description |
|-------|-------------|
| M6-SRS | 6-DOF arm, single robot system |
| M6-CCS | 6-DOF arm, coordinated control |
| M6S Lite | Lighter M6 variant |
| M20S-CCS | 20 kg payload, coordinated |
| Marvin Pro | Mobile manipulator |

### Usage

See that repository’s README after you have access. Do not invent `tianji_bringup` or `hardware:=mock`. Public `hardware:=` keys: `mock_components` / `gz` / `isaac` / `real`.

### Features

- Multiple drive type support
- Visualization with OCS2
- Real hardware integration

## Rokae

**Repository:** robot-descriptions-rokae

### Robots

| Robot | Description |
|-------|-------------|
| AR5 | 5 kg payload arm |

### Usage

See that repository’s README after you have access. Do not invent `rokae_bringup` or `hardware:=mock`.

## Fairino

**Repository:** robot-descriptions-fairino

Fairino arm descriptions for ART SDK integration.

## Gento

**Repository:** robot-descriptions-gento

Gento robot descriptions.

## Ubtech

**Repository:** robot-descriptions-ubtech

Ubtech humanoid descriptions.

## Agibot G2

**Repository:** agibot-g2-description

Agibot G2 humanoid description.

## Integration Pattern

All vendor descriptions follow the standard pattern:

1. URDF/xacro with ros2_control tags
2. Hardware-specific interface configuration
3. OCS2 controller configuration
4. Launch files

### Example Launch Integration

```python
# launch/bringup.launch.py
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                FindPackageShare('ocs2_arm_controller'),
                '/launch/demo.launch.py'
            ]),
            launch_arguments={
                'robot': 'vendor_robot',
                'hardware': 'real',
            }.items(),
        ),
    ])
```

## Related

- [Hardware Interfaces](../hardware/2-private_hi.md)
- [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md)
