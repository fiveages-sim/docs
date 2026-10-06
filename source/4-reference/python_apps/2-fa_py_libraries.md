# fa-py-libraries

Python utilities umbrella for FiveAges Sim.

**Repository:** [fiveages-sim/fa-py-libraries](https://github.com/fiveages-sim/fa-py-libraries)

## Purpose

Aggregates Python utilities:
- ros2_robot_interface
- viser visualization
- VR pose publisher
- Common utilities

## Installation

```bash
git clone https://github.com/fiveages-sim/fa-py-libraries.git
cd fa-py-libraries
pip install -e .
```

## Usage

### Interactive Menu

```bash
./run.sh
```

Presents menu:
1. Robot interface demo
2. Viser visualization
3. VR teleoperation
4. ...

### Direct Commands

```bash
# VR teleoperation
./run.sh vr

# Viser visualization
./run.sh viser

# Robot interface
./run.sh interface
```

## Structure

```
fa-py-libraries/
├── ros2_robot_interface/    # Robot API
├── ros2_viser/             # Viser visualization
├── vr_pose_publisher/      # VR bridge
├── utils/                  # Common utilities
├── run.sh                  # Entry point
└── setup.py
```

## Subpackages

| Package | Purpose |
|---------|---------|
| ros2_robot_interface | Robot control API |
| ros2_viser | Web visualization |
| vr_pose_publisher | VR tracking bridge |

## Related

- [ros2_robot_interface](1-ros2_robot_interface.md)
- [ros2-viser](3-ros2_viser.md)
- [VR Teleop How-To](../../2-how_to/6-vr_teleop.md)
