# fa-py-libraries

Python utilities umbrella for FiveAges Sim.

**Repository:** [fiveages-sim/fa-py-libraries](https://github.com/fiveages-sim/fa-py-libraries)

## Purpose

Aggregates Python utilities:
- ros2_robot_interface
- ros2-viser (Viser 3D visualization)
- VR pose publisher
- Common utilities

Default env is **Python 3.12** (`./init.sh env 3.12`). This is also the **primary launcher** for Viser (`./run.sh viser`).

## Installation

```bash
git clone https://github.com/fiveages-sim/fa-py-libraries.git
cd fa-py-libraries
./init.sh all
```

`./init.sh all` initializes submodules, creates a Python 3.12 env, and installs `ros2_robot_interface`, `ros2-viser`, and `vr_pose_publisher`.

## Usage

### Interactive Menu

```bash
./run.sh
```

Presents menu (numbers from the README):
1. ros2-viser launch
2. VR pose launch
3. …

### Direct Commands

```bash
# VR teleoperation
./run.sh vr

# Viser visualization (primary entry for ros2-viser)
./run.sh viser
```

## Structure

:::{code-block} none
fa-py-libraries/
├── ros2_robot_interface/    # Robot API
├── ros2_viser/             # Viser visualization
├── vr_pose_publisher/      # VR bridge
├── utils/                  # Common utilities
├── run.sh                  # Entry point
└── setup.py
:::

## Subpackages

| Package | Purpose |
|---------|---------|
| ros2_robot_interface | Robot control API |
| ros2_viser | Viser library (start with `./run.sh viser`) |
| vr_pose_publisher | VR tracking bridge |

## Related

- [ros2_robot_interface](1-ros2_robot_interface.md)
- [ros2-viser](3-ros2_viser.md)
- [VR Teleop How-To](../../2-how_to/6-vr_teleop.md)
