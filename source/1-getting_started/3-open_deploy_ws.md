# open-deploy-ws Setup

Detailed setup guide for the public `open-deploy-ws` workspace.

## Repository Overview

**URL:** [https://github.com/fiveages-sim/open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws)

`open-deploy-ws` is the public entry point for the FiveAges Sim ecosystem. It provides:

- Pre-configured submodule structure
- Public-only visibility by default
- Lean branches for minimal builds
- GitHub Release `.deb` integration for OCS2 (and optionally common / arms)

## Cloning

```bash
git clone https://github.com/fiveages-sim/open-deploy-ws.git
cd open-deploy-ws
```

## Initialization

### Basic Initialization

```bash
./init_repo.sh
```

The script will:
1. Configure submodule visibility (public only)
2. Prompt per core module for `d` (GitHub Release `.deb`) or `s` (source)
3. Initialize selected submodules; deb mode calls `scripts/install_core_debs.sh`

### Core module options (OCS2, arms, common)

When prompted (`d=deb`, `s=source`; Enter accepts the default):

| Option | Description | When to Use |
|--------|-------------|-------------|
| `d` | GitHub Release `.deb` | Quick start; no need to build that module from source |
| `s` | Source build | Development, debugging, or contributing |

Defaults in `open-deploy-ws`: OCS2=`d`, arms=`s`, common=`s`. Deb mode does **not** install from packages.ros.org.

### Lean Branches

For minimal builds with a single robot:

```bash
# Dobot CR5 only
git checkout dobot-cr5
./init_repo.sh

# ARX ACone only  
git checkout arx-acone
./init_repo.sh
```

## Directory Structure

After initialization:

:::{code-block} none
open-deploy-ws/
├── src/
│   ├── arms_ros2_control/       # Controllers + nested HIs
│   ├── robot_descriptions/      # Description umbrella
│   │   ├── robot-descriptions-common/
│   │   ├── robot-descriptions-dobot/
│   │   ├── robot-descriptions-arx/
│   │   └── ...
│   └── ocs2_ros2/              # (if source build)
├── init_repo.sh
├── submodules_visibility.conf
└── deb_versions.conf
:::

## Building

### Install Dependencies

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
```

### Full Build

```bash
colcon build --symlink-install
```

### Partial Build

Build only specific packages:

```bash
# Just descriptions
colcon build --packages-select robot-descriptions-dobot

# Up to a specific package
colcon build --packages-up-to ocs2_arm_controller
```

## Supported Robots

| Robot | Description Package | Hardware Interface | Real Hardware |
|-------|--------------------|--------------------|---------------|
| Dobot CR5 | robot-descriptions-dobot | dobot-cr-ros2-control | Simulation only |
| ARX X5 | robot-descriptions-arx | arx-ros2-control | Simulation only |
| **ARX ACone** | robot-descriptions-arx | arx-ros2-control | **Supported** |
| ARX Lift2S | robot-descriptions-arx | arx-ros2-control | Simulation only |
| Galbot | robot-descriptions-galbot | (varies) | Simulation only |
| **HT Panthera** | robot-descriptions-ht | ht-ros2-control | **Supported** |
| Quadruped | robot-descriptions-quadruped | unitree-ros2-control | Simulation only |

```{admonition} Real Hardware Deployment
:class: tip

**ARX Acone** and **HT Panthera** can be deployed to real hardware using only public packages. See [Go to Real Hardware](../2-how_to/9-go_real_hardware.md) for deployment instructions.
```

## Launch Examples

### Mock Hardware Demo

```bash
source install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=mock
```

### With Specific Robot

```bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=mock
```

### With Gripper

```{admonition} TODO
:class: note

For valid robot + gripper combinations, check the launch files in `arms_ros2_control`. Not all combinations are supported.
```

```bash
# General pattern
ros2 launch ocs2_arm_controller demo.launch.py robot:=<robot_name> gripper:=<gripper_name> hardware:=mock
```

## Adding Robot Descriptions

To add a new robot to your workspace:

```bash
cd src/robot_descriptions
git submodule update --init robot-descriptions-<brand>
cd ../..
colcon build --packages-up-to robot-descriptions-<brand>
```

## Submodule Management

### Check Status

```bash
git submodule status
```

### Update All

```bash
git submodule update --init --recursive
```

### Update Specific

```bash
cd src/arms_ros2_control
git pull origin main
```

## GitHub Release `.deb` vs Source Matrix

| Component | GitHub Release `.deb` | Source Path |
|-----------|----------------------|-------------|
| OCS2 | `ros-jazzy-ocs2` ([releases](https://github.com/legubiao/ocs2_ros2/releases)) | `src/ocs2_ros2` |
| Common descriptions | `ros-jazzy-robot-descriptions-common` ([releases](https://github.com/fiveages-sim/robot-descriptions-common/releases)) | `src/robot_descriptions/robot-descriptions-common` |
| arms_ros2_control | `ros-jazzy-arms-ros2-control` (optional; [releases](https://github.com/fiveages-sim/arms_ros2_control/releases)) | `src/arms_ros2_control` |

Check `deb_versions.conf` for the GitHub repos and release tags used by `scripts/install_core_debs.sh`. These packages are not in the ROS apt index.

## Common Issues

### Submodules Empty

```bash
git submodule update --init --recursive
```

### Access Denied to Submodule

Some submodules are private. In `open-deploy-ws`, only public submodules should be required. If you see access errors:

1. Check you're on the correct branch (not accidentally on a private branch)
2. Verify the submodule is listed as public in `submodules_visibility.conf`

### Build Fails with numpy

```bash
pip install 'numpy<2'
```

### CAN Interface Rename Needed

For CAN-based robots, you may need to rename the interface:

```bash
sudo ip link set can0 down
sudo ip link set can0 name <expected_name>
sudo ip link set <expected_name> up
```

## Next Steps

- [Run mock demo](../2-how_to/1-run_mock_demo.md)
- [Switch robots](../2-how_to/2-switch_robot.md)
- [Gazebo simulation](../2-how_to/3-gazebo_sim.md)
