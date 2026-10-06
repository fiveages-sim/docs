# Source vs GitHub Release `.deb`

This page explains when to use prebuilt `.deb` files from GitHub Releases versus source builds for stack components.

These packages are **not** published to Debian / ROS apt software sources (`packages.ros.org` or Ubuntu apt). `sudo apt install ros-jazzy-ocs2` will not find them there.

## Available GitHub Release `.deb` packages

| Package | `.deb` name | GitHub Releases | Purpose |
|---------|-------------|-----------------|---------|
| OCS2 | `ros-jazzy-ocs2` | [legubiao/ocs2_ros2](https://github.com/legubiao/ocs2_ros2/releases) | MPC library |
| Common descriptions | `ros-jazzy-robot-descriptions-common` | [fiveages-sim/robot-descriptions-common](https://github.com/fiveages-sim/robot-descriptions-common/releases) | Shared components |
| arms_ros2_control | `ros-jazzy-arms-ros2-control` | [fiveages-sim/arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control/releases) | Controllers (optional) |

**Recommended for most users:** run `./init_repo.sh` in `open-deploy-ws` or `fa-deploy-ws` and choose `d` (deb) for the modules you want. Deb mode downloads those release assets via `scripts/install_core_debs.sh`.

## Decision Matrix

| Scenario | Recommendation |
|----------|----------------|
| Quick start / learning | GitHub Release `.deb` (especially OCS2) |
| Production deployment | GitHub Release `.deb` |
| Controller development | Source build |
| OCS2 development | Source build |
| Custom robot integration | Source descriptions, GitHub Release `.deb` for OCS2 |
| Contributing to the stack | Source build |

## OCS2: Deb vs Source

### GitHub Release `.deb`

**Recommended:** in the deploy workspace, choose deb mode for OCS2:

```bash
./init_repo.sh
# When prompted for ocs2_ros2, choose d (deb)
```

That calls `scripts/install_core_debs.sh`, which downloads the matching `.deb` from GitHub Releases and installs it.

**Manual install:** download the matching asset for your architecture and ROS distro from the [ocs2_ros2 Releases](https://github.com/legubiao/ocs2_ros2/releases) page (filename pattern `ros-jazzy-ocs2_*_<arch>.deb`), then:

```bash
sudo dpkg -i ros-jazzy-ocs2_*.deb
sudo apt-get install -f   # if dpkg reports missing dependencies
```

Do not hardcode a version; pick the asset that matches your machine. The package **name** is `ros-jazzy-ocs2`; it is not available from the ROS apt index.

**Pros:**
- Fast installation
- Tested and stable
- No build time

**Cons:**
- Cannot modify OCS2 code
- Locked to the release asset version

### Source Build

```bash
# In workspace src/
git clone -b ros2 https://github.com/legubiao/ocs2_ros2.git
colcon build --packages-up-to ocs2
```

**Pros:**
- Full access to source
- Can modify and debug
- Latest features

**Cons:**
- Long build time
- Requires more disk space
- Must manage updates manually

## Mixing Source and Deb

You can mix source trees and GitHub Release `.deb` packages, but be careful of version conflicts.

### Recommended Combinations

| OCS2 | Descriptions | arms_ros2_control | Notes |
|------|--------------|-------------------|-------|
| Deb | Source | Source | Typical development (`init_repo.sh` default) |
| Source | Source | Source | Full stack development |
| Deb | Deb | Deb | Fastest install; all three from GitHub Releases |

### Avoid

| Combination | Problem |
|-------------|---------|
| Source OCS2 + Deb arms | ABI mismatch possible |
| Newer Deb + Older source | API incompatibility |

## Version Tracking

### deb_versions.conf

The `open-deploy-ws` includes `deb_versions.conf` listing package prefixes, GitHub repos, and release tags used by `install_core_debs.sh`:

:::{code-block} none
# package prefix | release tag | GitHub repo
ros-jazzy-ocs2|latest|legubiao/ocs2_ros2
ros-jazzy-robot-descriptions-common|latest|fiveages-sim/robot-descriptions-common
ros-jazzy-arms-ros2-control|latest|fiveages-sim/arms_ros2_control
:::

### Checking Installed Versions

```bash
# Check installed .deb version
dpkg-query -W -f='${Package} ${Version}\n' ros-jazzy-ocs2

# Check source version (if available)
cd src/ocs2_ros2 && git describe --tags
```

## Switching Between

### Deb → Source

1. Remove the installed `.deb` (or leave it; workspace source takes priority):
   ```bash
   sudo apt-get remove ros-jazzy-ocs2  # Optional
   ```

2. Clone source:
   ```bash
   cd src
   git clone -b ros2 https://github.com/legubiao/ocs2_ros2.git
   ```

3. Rebuild:
   ```bash
   colcon build --packages-up-to ocs2
   ```

### Source → Deb

1. Remove source directory:
   ```bash
   rm -rf src/ocs2_ros2
   ```

2. Install the GitHub Release `.deb` (recommended via the workspace script):
   ```bash
   ./scripts/install_core_debs.sh --only ocs2
   ```

   Manual alternative: download the matching asset from [ocs2_ros2 Releases](https://github.com/legubiao/ocs2_ros2/releases) and run `sudo dpkg -i ros-jazzy-ocs2_*.deb`.

3. Clean and rebuild:
   ```bash
   rm -rf build/ocs2* install/ocs2*
   colcon build
   ```

## init_repo.sh Options

The initialization script handles this choice per module (`d` = GitHub Release `.deb`, `s` = source; Enter accepts the default):

```bash
./init_repo.sh
# Prompts:
# 核心模块安装方式（d=deb, s=source）
#   ocs2_ros2                  default: d  (GitHub Release .deb)
#   arms_ros2_control          default: s  (source)
#   robot-descriptions/common  default: s  (source)
```

Choosing `d` downloads the prebuilt `.deb` from GitHub Releases via `scripts/install_core_debs.sh`. It does **not** install from packages.ros.org.

## Build Time Comparison

| Configuration | Approximate Build Time |
|---------------|----------------------|
| All Deb | Minutes |
| Deb OCS2 + Source arms | 10-15 minutes |
| All Source | 20-40 minutes |

Times vary by machine. OCS2 is the largest component.

## Troubleshooting

### Symbol/ABI Errors

If you see errors about undefined symbols or ABI mismatches:

1. Check version compatibility
2. Clean and rebuild from scratch:
   ```bash
   rm -rf build install
   colcon build
   ```
3. Ensure consistent source/Deb choice

### Package Not Found After Install

These `.deb` files are not in the ROS apt index. `sudo apt update` will not make `ros-jazzy-ocs2` appear.

```bash
# Confirm the package is installed
dpkg-query -W ros-jazzy-ocs2

# Re-source ROS
source /opt/ros/jazzy/setup.bash

# If missing, reinstall from GitHub Releases via the workspace script
./scripts/install_core_debs.sh --only ocs2
```

### Conflicting Installations

```bash
# Check for duplicate packages
ros2 pkg list | grep ocs2

# Remove installed .deb if using source
sudo apt-get remove ros-jazzy-ocs2
```
