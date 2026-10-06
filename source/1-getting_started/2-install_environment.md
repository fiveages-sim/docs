# Install Environment

This page covers installing the base development environment for FiveAges Sim workspaces.

## Operating System

**Supported:** Ubuntu 24.04 LTS (Noble Numbat)

Other platforms are not officially supported but may work:
- Ubuntu 22.04 with ROS 2 Humble (limited compatibility)
- Other Linux distributions with manual ROS 2 installation

## ROS 2 Jazzy Installation

### Option A: Official Installation (Recommended)

Follow the official ROS 2 Jazzy installation guide:

```bash
# Set locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS 2 repository
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 Jazzy
sudo apt update
sudo apt install ros-jazzy-desktop ros-dev-tools
```

### Option B: fishros (Alternative for China)

For users in China with slow access to official mirrors:

```bash
wget http://fishros.com/install -O fishros && bash fishros
```

Select ROS 2 Jazzy when prompted.

## Development Tools

### Essential Packages

```bash
sudo apt install -y \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    git \
    build-essential \
    cmake
```

### Initialize rosdep

```bash
sudo rosdep init  # Skip if already done
rosdep update
```

## OCS2 Installation

OCS2 (Optimal Control for Switched Systems) is a core dependency.

OCS2 is **not** published to Debian / ROS apt software sources. The `.deb` package name is still `ros-jazzy-ocs2`, but you must install it from GitHub Releases (or let the deploy workspace do that for you).

### Option A: GitHub Release `.deb` (Recommended)

**Most users:** run `./init_repo.sh` in `open-deploy-ws` or `fa-deploy-ws` and choose `d` (deb) for OCS2. That downloads and installs the release `.deb` via `scripts/install_core_debs.sh`.

**Manual install:** download the matching asset for your architecture and ROS distro from the [ocs2_ros2 Releases](https://github.com/legubiao/ocs2_ros2/releases) page (filename pattern `ros-jazzy-ocs2_*_<arch>.deb`), then:

```bash
sudo dpkg -i ros-jazzy-ocs2_*.deb
sudo apt-get install -f   # if dpkg reports missing dependencies
```

Do not hardcode a version; pick the asset that matches your machine.

### Option B: From Source

Clone within workspace (handled by `init_repo.sh` in deploy workspaces when you choose `s`):

```bash
cd ~/your_ws/src
git clone -b ros2 https://github.com/legubiao/ocs2_ros2.git
```

## Simulation Dependencies

### Gazebo Harmonic

```bash
sudo apt install ros-jazzy-gz-*
```

### Isaac Sim

```{admonition} Required Version and Path
:class: warning

FaSim-Isaac requires **Isaac Sim 6.1 binary** installed at **`~/isaacsim`**. The run scripts assume this exact path.
```

**Requirements:**
- **Isaac Sim 6.1** (not older versions)
- Install path: **`~/isaacsim`** (scripts expect this exact path)
- NVIDIA GPU with drivers compatible with Isaac Sim 6.1

**Installation:**
1. Download Isaac Sim 6.1 from NVIDIA
2. Extract or install to `~/isaacsim`
3. Verify: `ls ~/isaacsim/python.sh` should exist

If you install Isaac Sim to a different path, create a symlink:
```bash
ln -s /your/actual/path ~/isaacsim
```

See the [Isaac Sim how-to](../2-how_to/4-isaac_sim.md) for usage details.

## Network Configuration (Optional)

For multi-machine setups or connecting to real robots:

### Zenoh Bridge

```bash
sudo apt install ros-jazzy-rmw-zenoh-cpp
```

Configure via environment variables:
```bash
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
```

### ROS Domain ID

Set a unique Domain ID to isolate your ROS 2 traffic:

```bash
export ROS_DOMAIN_ID=<your-id>
```

```{admonition} Domain ID Selection
:class: important

When working with real robots, the Domain ID must match the robot's configured value. Consult your robot's documentation or team lead for the correct ID.
```

## Shell Configuration

Add to your `~/.bashrc` for convenience:

```bash
# ROS 2 Jazzy
source /opt/ros/jazzy/setup.bash

# Workspace (adjust path as needed)
if [ -f ~/open-deploy-ws/install/setup.bash ]; then
    source ~/open-deploy-ws/install/setup.bash
fi

# Optional: Zenoh
# export RMW_IMPLEMENTATION=rmw_zenoh_cpp

# Optional: Domain ID
# export ROS_DOMAIN_ID=42
```

## Verification

Test your installation:

```bash
# Source ROS 2
source /opt/ros/jazzy/setup.bash

# Check ROS 2
ros2 --help

# Check Gazebo
gz sim --version

# Check OCS2 (if installed via GitHub Release .deb)
ros2 pkg list | grep ocs2
```

## Common Issues

### Package Not Found After apt install

This applies to packages that **are** in the ROS apt index (for example `ros-jazzy-desktop`). It does **not** apply to OCS2.

```bash
sudo apt update
source /opt/ros/jazzy/setup.bash
```

### OCS2 not found after install

OCS2 is not in packages.ros.org / Ubuntu apt. `sudo apt update` will not make `ros-jazzy-ocs2` appear.

```bash
dpkg-query -W ros-jazzy-ocs2
source /opt/ros/jazzy/setup.bash
```

If the package is missing, re-run `./init_repo.sh` and choose `d` for OCS2, or download the matching `.deb` from [ocs2_ros2 Releases](https://github.com/legubiao/ocs2_ros2/releases) and install with `sudo dpkg -i ros-jazzy-ocs2_*.deb`.

### rosdep Errors

```bash
rosdep update --include-eol-distros
```

### Colcon Build Warnings

Most warnings can be ignored. For "missing resource index" warnings:
```bash
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
```

## Next Steps

- [Quick Demo](1-quick_demo_public.md) — Run your first demo
- [open-deploy-ws Setup](3-open_deploy_ws.md) — Detailed workspace setup
