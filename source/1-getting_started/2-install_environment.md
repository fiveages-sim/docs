# Install Environment

This page covers installing the base development environment for FiveAges Sim workspaces.

## Operating System

**Supported:** Ubuntu 24.04 LTS (Noble Numbat)

**Python:** **3.12** only (ROS 2 Jazzy on Ubuntu 24.04). Do not use 3.10/3.11 venvs for this stack.

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

OCS2 is **not** published to Debian / ROS apt software sources. The `.deb` package name is still `ros-jazzy-ocs2`. **Do not** treat `sudo apt install` or a hand-run `dpkg -i` as the primary path.

Use the deploy-workspace scripts in `open-deploy-ws` or `fa-deploy-ws`. They already switch and install OCS2 (GitHub Release `.deb` or source).

:::{code-block} bash
cd ~/open-deploy-ws   # or fa-deploy-ws
./init_repo.sh
:::

What the script does (from the open-deploy-ws README):

| Menu | Role |
|------|------|
| **1) 初始化工作空间** | Nested visibility, then per-module `d` (GitHub Release `.deb`) or `s` (source). OCS2 default is **deb**. |
| **2) 切换模块安装方式** | Switch an already-initialized module **source ↔ deb** (cleans conflicting source or uninstalls the matching deb). Use this to change the OCS2 install path. |
| **3) 仅安装/更新核心 deb** | Skip Git; e.g. `./scripts/install_core_debs.sh --only ocs2` |
| **4) 卸载核心 deb** | e.g. `./scripts/uninstall_core_debs.sh --only ocs2` |
| **5) 仅运行 rosdep** | `rosdep install` on `src/` only |

Choosing `d` downloads the matching GitHub Release asset via `scripts/install_core_debs.sh`. It does **not** install from packages.ros.org. After init, you still `colcon build`.

:::{admonition} Manual fallback
:class: note

Only if you are not using a deploy workspace. Download the matching asset for your architecture and ROS distro from [ocs2_ros2 Releases](https://github.com/legubiao/ocs2_ros2/releases) (filename pattern `ros-jazzy-ocs2_*_<arch>.deb`), then `sudo dpkg -i ros-jazzy-ocs2_*.deb` and `sudo apt-get install -f` if dpkg reports missing dependencies. For source: clone branch `ros2` into `src/` — or choose `s` in `./init_repo.sh`.
:::

## Simulation Dependencies

### Gazebo Harmonic

```bash
sudo apt install ros-jazzy-gz-*
```

### Isaac Sim

Use **FaSim-Isaac** scripts. Path and version live in config, not in a hardcoded minor version in these docs.

- Default install directory: `ISAACSIM_DIR` (`~/isaacsim` unless you set it in `config/fa_sim.local.conf` or the environment)
- Optional Isaac ROS 2 Jazzy workspace version: `./init.sh` operation 2 menu (queries GitHub stable tags; fallback list in `config/fa_sim.conf` currently `6.0.1` / `6.0.0` / `5.1.0`). Override with `ISAAC_SIM_VERSION=… ./init.sh`

:::{code-block} bash
git clone git@github.com:fiveages-sim/FaSim-Isaac.git
cd FaSim-Isaac
./init.sh    # 1) submodules  2) optional Isaac ROS 2 Jazzy workspace
./run.sh     # menu: PhysX / Newton / Headless Streaming
:::

Copy `config/fa_sim.local.template.conf` → `config/fa_sim.local.conf` to change `ISAACSIM_DIR` or the default version. See the [Isaac Sim how-to](../2-how_to/4-isaac_sim.md).

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

# Check OCS2 (after deploy-ws init / install_core_debs.sh)
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

Re-run `./init_repo.sh` in the deploy workspace: choose **1** and `d` for OCS2, or **3** (`./scripts/install_core_debs.sh --only ocs2`). To change an existing install, use menu **2) 切换模块安装方式**.

```bash
dpkg-query -W ros-jazzy-ocs2
source /opt/ros/jazzy/setup.bash
```

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
