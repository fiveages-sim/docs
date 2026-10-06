# open-deploy-ws Setup

Detailed setup guide for the public `open-deploy-ws` workspace.

## Repository Overview

**URL:** [https://github.com/fiveages-sim/open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws)

`open-deploy-ws` is the public entry point for the FiveAges Sim ecosystem. It provides:

- Pre-configured submodule structure
- Public-only visibility by default
- Lean branches for minimal builds
- Debian package integration for OCS2

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
2. Prompt for OCS2 installation method
3. Initialize selected submodules

### OCS2 Options

When prompted, choose:

| Option | Description | When to Use |
|--------|-------------|-------------|
| `d` | Debian package | Quick start, no OCS2 development |
| `s` | Source build | OCS2 development, debugging |

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

```
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
└── deb_versions.txt
```

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

| Robot | Description Package | Hardware Interface |
|-------|--------------------|--------------------|
| Dobot CR5 | robot-descriptions-dobot | dobot-cr-ros2-control |
| ARX X5 | robot-descriptions-arx | arx-ros2-control |
| ARX ACone | robot-descriptions-arx | arx-ros2-control |
| ARX Lift2S | robot-descriptions-arx | arx-ros2-control |
| Galbot | robot-descriptions-galbot | (varies) |
| HT Panthera | robot-descriptions-ht | ht-ros2-control |
| Quadruped | robot-descriptions-quadruped | unitree-ros2-control |

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

```bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=dobot_cr5 gripper:=dh_ag95 hardware:=mock
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

## Debian vs Source Matrix

| Component | Debian Package | Source Path |
|-----------|---------------|-------------|
| OCS2 | `ros-jazzy-ocs2` | `src/ocs2_ros2` |
| Common descriptions | `ros-jazzy-robot-descriptions-common` | `src/robot_descriptions/robot-descriptions-common` |
| arms_ros2_control | (optional) | `src/arms_ros2_control` |

Check `deb_versions.txt` for compatible Debian versions when mixing source and packages.

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
