# fa-py-libraries

Python utilities umbrella for FiveAges Sim.

**Repository:** [fiveages-sim/fa-py-libraries](https://github.com/fiveages-sim/fa-py-libraries)

## Purpose

Aggregates Python utilities:
- ros2_robot_interface
- ros2-viser (Viser 3D visualization)
- VR pose publisher

Default env is **Python 3.12** (`./init.sh env 3.12`). This is also the **primary launcher** for Viser (`./run.sh viser`).

## Installation

:::{code-block} bash
git clone https://github.com/fiveages-sim/fa-py-libraries.git
cd fa-py-libraries
./init.sh all
:::

What `./init.sh all` does: initialize submodules, create a Python **3.12** env (from `.fa-env.toml` `backend`: `uv` or `conda`), then install `ros2_robot_interface`, `ros2-viser`, and `vr_pose_publisher`.

Switch backend with `./init.sh set-backend uv`. Personal overrides: `.fa-env.local.toml`.

## Usage

### Interactive Menu

:::{code-block} bash
./run.sh
:::

What `./run.sh` does: activate the env (and source `[ros2].workspace` if set), then the README menu: viser, VR (Vuer / XRoboToolkit), VR bag record/playback, interface joint record/playback, versions.

### Direct Commands

Commands from the fa-py-libraries README (do not invent flags):

| Command | What it does |
|---------|----------------|
| `./run.sh viser` | ros2-viser (primary Viser entry) |
| `./run.sh vr` | vr_pose_publisher (Vuer/WebXR) |
| `./run.sh vr-xrt` | vr_pose_publisher (XRoboToolkit SDK) |
| `./run.sh vr-xrt-service` | start XRoboToolkit PC Service (`stop` to shut down) |
| `./run.sh vr-record` | record `/teleop/*` bags |
| `./run.sh record` / `playback` | interface joint snapshot JSON |

```{admonition} Pico Enterprise vs consumer
:class: note

Headset SKU notes live on [VR Teleop](../../2-how_to/5-teleoperation/6-vr_teleop.md): Pico **Enterprise** supports USB shared networking (USB 网络共享) and uses a **different App** from Pico **consumer**. This page only lists fa-py-libraries README commands (`./run.sh vr` vs `./run.sh vr-xrt` + PC Service). It does not name store listings, package names, or ADB steps.
```

## Structure

:::{code-block} none
fa-py-libraries/
├── init.sh
├── run.sh
├── release.sh
├── .fa-env.toml
├── scripts/                 # fa-env.sh, vr-bag.sh
├── ros2_robot_interface/
├── ros2_viser/
└── vr_pose_publisher/
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
- [VR Teleop How-To](../../2-how_to/5-teleoperation/6-vr_teleop.md)
