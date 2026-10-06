# Source vs Debian Packages

This page explains when to use Debian packages versus source builds for stack components.

## Available Debian Packages

| Package | Debian Name | Purpose |
|---------|-------------|---------|
| OCS2 | `ros-jazzy-ocs2` | MPC library |
| Common descriptions | `ros-jazzy-robot-descriptions-common` | Shared components |
| arms_ros2_control | `ros-jazzy-arms-ros2-control` | Controllers (optional) |

## Decision Matrix

| Scenario | Recommendation |
|----------|----------------|
| Quick start / learning | Debian packages |
| Production deployment | Debian packages |
| Controller development | Source build |
| OCS2 development | Source build |
| Custom robot integration | Source descriptions, Deb OCS2 |
| Contributing to the stack | Source build |

## OCS2: Deb vs Source

### Debian Package

```bash
sudo apt install ros-jazzy-ocs2
```

**Pros:**
- Fast installation
- Tested and stable
- No build time

**Cons:**
- Cannot modify OCS2 code
- Locked to package version

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

You can mix source and Deb packages, but be careful of version conflicts.

### Recommended Combinations

| OCS2 | Descriptions | arms_ros2_control | Notes |
|------|--------------|-------------------|-------|
| Deb | Source | Source | Typical development |
| Source | Source | Source | Full stack development |
| Deb | Deb | Deb | Production deployment |

### Avoid

| Combination | Problem |
|-------------|---------|
| Source OCS2 + Deb arms | ABI mismatch possible |
| Newer Deb + Older source | API incompatibility |

## Version Tracking

### deb_versions.txt

The `open-deploy-ws` includes `deb_versions.txt` showing compatible versions:

```
# Compatible Debian versions
ros-jazzy-ocs2: 1.2.3
ros-jazzy-robot-descriptions-common: 0.5.0
ros-jazzy-arms-ros2-control: 1.0.0
```

### Checking Installed Versions

```bash
# Check Debian package version
apt show ros-jazzy-ocs2 | grep Version

# Check source version (if available)
cd src/ocs2_ros2 && git describe --tags
```

## Switching Between

### Deb → Source

1. Remove the Debian package (or leave it; source takes priority):
   ```bash
   sudo apt remove ros-jazzy-ocs2  # Optional
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

2. Install Debian package:
   ```bash
   sudo apt install ros-jazzy-ocs2
   ```

3. Clean and rebuild:
   ```bash
   rm -rf build/ocs2* install/ocs2*
   colcon build
   ```

## init_repo.sh Options

The initialization script handles this choice:

```bash
./init_repo.sh
# Prompts:
# OCS2 installation method:
#   [d] Debian package (recommended for quick start)
#   [s] Source build (for development)
# Enter choice [d/s]:
```

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

```bash
# Refresh package cache
sudo apt update

# Re-source ROS
source /opt/ros/jazzy/setup.bash
```

### Conflicting Installations

```bash
# Check for duplicate packages
ros2 pkg list | grep ocs2

# Remove Deb if using source
sudo apt remove ros-jazzy-ocs2
```
