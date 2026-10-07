# Public vs Internal Paths

This page explains the differences between the public (`open-deploy-ws`) and internal (`fa-deploy-ws`) entry points.

## Quick Comparison

| Aspect | Public Path | Internal Path |
|--------|-------------|---------------|
| **Workspace** | `open-deploy-ws` | `fa-deploy-ws` |
| **Access** | Anyone (public GitHub) | FiveAges team only |
| **Robots** | Dobot, ARX, Galbot, HighTorque, quadruped | FA W2/W2R/S2/S2R, dual-arm CCS |
| **Real Hardware** | ARX Lift 2S (full-body), Acone (arm only), HighTorque Panthera HT | All FA robots |
| **Submodules** | Public only | Public + private |
| **OCS2** | GitHub Release `.deb` or source | Full source (default) |
| **Purpose** | Learning, OSS development, real robot deployment | Production deployment |

```{admonition} Real Hardware on Public Path
:class: tip

**ARX Lift 2S** (方舟无限) is the full-body mobile manipulator (arms + chassis). **Acone** / **AC One** is arm-only. **HighTorque Panthera HT** (高擎) is a dual-arm manipulator. Use the branch READMEs: [ARX Lift 2S](../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md), [HighTorque Panthera HT](../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md).
```

## open-deploy-ws (Public)

**Repository:** [https://github.com/fiveages-sim/open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws)

### Features

- All submodules are publicly accessible
- Supports multiple robots: Dobot CR5, ARX (Acone arm, Lift 2S full-body), Galbot, HighTorque Panthera HT
- **Real hardware:** [ARX Lift 2S](../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md) and [HighTorque Panthera HT](../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md) via their `open-deploy-ws` branches (`arx-lift2s`, `panthera-ht`)
- OCS2 available as a GitHub Release `.deb` (`ros-jazzy-ocs2`; not from apt / packages.ros.org)
- Lean branches: `dobot-cr5`, `arx-lift2s`, `panthera-ht`
- Good for learning, experimentation, contributing, and real robot deployment

### Initialization

```bash
git clone https://github.com/fiveages-sim/open-deploy-ws.git
cd open-deploy-ws
./init_repo.sh
```

The init script will:
1. Configure submodule visibility (only public modules)
2. Prompt per core module: GitHub Release `.deb` (`d`) or source (`s`)
3. Initialize selected submodules

### Visibility Configuration

The workspace uses `submodules_visibility.conf` to control which **nested** submodules are public or private. The file is pipe-separated (`parent_dir|relative_path|visibility`); blank lines and `#` comments are ignored. It is not an INI file with `[public]` / `[private]` sections.

:::{code-block} none
# Format: parent_dir|relative_path|public or private
src/robot-descriptions|common|public
src/robot-descriptions|manipulator/Dobot|public
src/robot-descriptions|manipulator/Tianji|private
src/arms_ros2_control|controller/ocs2_wbc_controller|private
:::

### Lean Branches

For minimal builds focusing on a single robot:

:::{code-block} bash
# Dobot CR5 only
git checkout dobot-cr5

# ARX Lift 2S (full-body). Acone arm is co-debug in this branch, not a separate platform.
git checkout arx-lift2s

# HighTorque Panthera HT
git checkout panthera-ht
:::

## fa-deploy-ws (Internal)

```{admonition} Access Required
:class: warning

This workspace requires private repository access. Contact your team lead if you need access.
```

### Features

- Access to all FiveAges robots: W2, W2R, S2, S2R
- Dual-arm CCS configurations (M6, M20S, AR5)
- Full OCS2 + WBC source integration
- Release package generation (`./release.sh`)
- Robot-specific initialization presets

### Initialization

```bash
git clone <internal-url>/fa-deploy-ws.git
cd fa-deploy-ws
./init_repo.sh --robot <robot-id>
```

Available robot IDs include:
- Wheeled-arm humanoids: `fiveages_w2`, `fiveages_w2r`, `fiveages_s2`, `fiveages_s2r`
- Dual-arm: `tianji_m6_ccs`, `tianji_m20s_ccs`, `rokae_ar5_ccs`

### Robot Configuration

Each robot requires a `robot.local.yaml` file with deployment-specific settings:

```yaml
# Example structure (actual values must be configured per-robot)
network:
  domain_id: <your-domain-id>
  interface: <your-network-interface>

hardware:
  arm_type: <arm-model>
```

Public end-effector selection is launch `type` / `left_type` / `right_type` (and `robot_profile`), not a `gripper:=` argument. See [robot_common_launch](../4-reference/descriptions/2-common.md).

```{admonition} Configuration Values
:class: important

The actual values for domain IDs, network interfaces, and device addresses are robot-specific and should not be committed to version control. Consult your robot's setup documentation or team lead for the correct values.
```

### Quick Start Flow

```bash
# Initialize for specific robot
./init_repo.sh --robot fiveages_w2

# Build the workspace
colcon build --symlink-install

# Configure robot.local.yaml with your values
cp robot.local.yaml.template robot.local.yaml
# Edit robot.local.yaml...

# Run quick start
./quick_start.sh
```

### Release Packages

For deployment without source builds:

```bash
# Generate release zip
./release.sh

# Install on target machine
./release.sh --install
```

## Choosing Your Path

### Use the Public Path If:

- You're new to the ecosystem
- You're developing with publicly available robots
- You're contributing to open source packages
- You don't have FiveAges private repo access

### Use the Internal Path If:

- You're deploying to FA wheeled-arm humanoids (W2/S2 series)
- You need WBC whole-body control
- You're building release packages for deployment
- You have authorized access to private repositories

## Transitioning Between Paths

### Public → Internal

1. Request access to private repositories
2. Clone `fa-deploy-ws` fresh (don't try to convert open-deploy-ws)
3. Follow internal initialization with your robot ID

### Internal Users on Public Hardware

If you have internal access but want to work with public robots:
- Use `open-deploy-ws` for cleaner builds
- Or use `fa-deploy-ws` with public-only robot presets

## Network Configuration

Both workspaces can communicate with real robots over the network. Key configuration points:

| Setting | Purpose |
|---------|---------|
| ROS Domain ID | Isolates ROS 2 traffic between robots/users |
| Zenoh configuration | Required for cross-network communication |
| Network interface | Must match the robot's network segment |

```{admonition} Domain Isolation
:class: tip

Always verify your Domain ID matches the target robot's configuration. Mismatched IDs result in no communication without obvious errors.
```
