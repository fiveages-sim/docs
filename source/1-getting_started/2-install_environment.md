# Install Environment

This page covers installing the base development environment for FiveAges Sim workspaces.

## Operating System

**Supported host:** Ubuntu 24.04 LTS (Noble Numbat) + **ROS 2 Jazzy**.

**Python:** **3.12** only (ROS 2 Jazzy on Ubuntu 24.04). Do not use 3.10/3.11 venvs for this stack.

Other Linux distros (for example Debian 13) are **not** supported natively. An `ubuntu:24.04` container on that host is a workable approach for the same apt steps below. `open-deploy-ws` does not publish an official Docker image or extra container flags; use a stock Ubuntu 24.04 userspace and the official ROS 2 Jazzy Ubuntu install.

Follow the [open-deploy-ws README](https://github.com/fiveages-sim/open-deploy-ws/blob/main/README.EN.md) after ROS 2 + rosdep are in place. The workspace entry is **`./init_repo.sh`**; after `colcon build`, `source install/setup.bash` in the launch terminal.

## ROS 2 Jazzy on a bare host or container

On a **bare** Ubuntu 24.04 machine or container, `python3-colcon-common-extensions`, `python3-rosdep`, and `python3-vcstool` are **not** in the default Ubuntu index. `apt install` of those packages fails with “Unable to locate package” until the ROS 2 apt source is added and `apt update` has run.

Source of truth: [Ubuntu (deb packages) — ROS 2 Jazzy](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html). Order:

1. Add the ROS key + Noble ROS 2 apt source
2. `apt update`
3. Install `ros-jazzy-desktop`, `ros-dev-tools`, and the colcon / rosdep / vcstool tools
4. `rosdep init` / `rosdep update`

### 1. Enable Universe, then add the ROS 2 apt source

Official current method — the `ros2-apt-source` package installs the signing key and the Noble `packages.ros.org` source:

:::{code-block} bash
sudo apt update
sudo apt install software-properties-common curl -y
sudo add-apt-repository universe

export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
:::

Equivalent **hand-added** source (same idea: `ros.key` + Noble ROS 2 list), if you are not using `ros2-apt-source`:

:::{code-block} bash
sudo apt install curl gnupg lsb-release -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}}) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
:::

On some Ubuntu 24.04 images, `/etc/apt/sources.list.d/ubuntu.sources` only lists the base `noble` suite. Official Jazzy docs: include `noble-updates` and `noble-backports` before installing `ros-dev-tools`, then `sudo apt clean && sudo apt update && sudo apt full-upgrade -y`.

In a container or CI job, `export DEBIAN_FRONTEND=noninteractive` is the usual apt setting (not an `open-deploy-ws` flag).

### 2. Update, then install desktop + dev tools

:::{code-block} bash
sudo apt update
sudo apt install ros-jazzy-desktop ros-dev-tools
sudo apt install python3-colcon-common-extensions python3-rosdep python3-vcstool
:::

`ros-dev-tools` usually already pulls colcon / rosdep / vcstool. The second line is harmless if they are installed, and it is the check that those names resolve **after** the ROS apt source exists.

### 3. Overlay and rosdep

:::{code-block} bash
source /opt/ros/jazzy/setup.bash
sudo rosdep init   # first time on this machine; skip if already initialized
rosdep update
:::

After this, clone a deploy workspace and run **`./init_repo.sh`**. CI / no TTY (after [open-deploy-ws#8](https://github.com/fiveages-sim/open-deploy-ws/pull/8), or once you pull that script): `./init_repo.sh --public --ocs2=deb --arms=source --common=source`. Details: [open-deploy-ws Setup](3-open_deploy_ws.md). Then `source install/setup.bash` after `colcon build`.

### Optional shortcut: fishros

The [open-deploy-ws README](https://github.com/fiveages-sim/open-deploy-ws/blob/main/README.EN.md) lists **fishros** first. That helper can add the ROS apt source and install Jazzy for you. It is an optional shortcut, not the only path, and it is a poor fit for a non-interactive container (the installer is a menu).

:::{code-block} bash
wget http://fishros.com/install -O fishros && bash fishros
sudo apt update
sudo apt install ros-jazzy-desktop
sudo rosdep init
rosdep update
:::

If fishros is not available, or `apt` still cannot see `python3-colcon-common-extensions` / `ros-jazzy-desktop`, use the official apt-source order above.

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

Copy `config/fa_sim.local.template.conf` → `config/fa_sim.local.conf` to change `ISAACSIM_DIR` or the default version. See the [Isaac Sim how-to](../2-how_to/2-simulation/4-isaac_sim.md).

## Verification

After `./init_repo.sh` (and `colcon build` if you already cloned a workspace):

:::{code-block} bash
ros2 --help
ros2 pkg list | grep ocs2   # after OCS2 deb or source via init
:::

`./init_repo.sh` already runs `rosdep` on source paths. After `colcon build`, `source install/setup.bash` in the launch terminal.

## Common Issues

### Unable to locate package (colcon / rosdep / vcstool / ros-jazzy-desktop)

The ROS 2 apt source is missing, or `apt update` was not run after adding it. Use the official order in [ROS 2 Jazzy on a bare host or container](#ros-2-jazzy-on-a-bare-host-or-container). `sudo apt update` alone does not add `packages.ros.org`.

### Package Not Found After apt install

This applies to packages that **are** in the ROS apt index (for example `ros-jazzy-desktop`) after the source is configured. It does **not** apply to OCS2.

```bash
sudo apt update
```

### OCS2 not found after install

OCS2 is not in packages.ros.org / Ubuntu apt. `sudo apt update` will not make `ros-jazzy-ocs2` appear.

Re-run `./init_repo.sh` in the deploy workspace: choose **1** and `d` for OCS2, or **3** (`./scripts/install_core_debs.sh --only ocs2`). To change an existing install, use menu **2) 切换模块安装方式**.

```bash
dpkg-query -W ros-jazzy-ocs2
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

- [Quick Demo](1-quick_demo_public.md) — Clone `open-deploy-ws`, `./init_repo.sh`, build, launch
- [open-deploy-ws Setup](3-open_deploy_ws.md) — Workspace details, SSH / CI init, Taku
