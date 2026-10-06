# Public vs Internal Paths

This page explains the differences between the public (`open-deploy-ws`) and internal (`fa-deploy-ws`) entry points.

## Quick Comparison

| Aspect | Public Path | Internal Path |
|--------|-------------|---------------|
| **Workspace** | `open-deploy-ws` | `fa-deploy-ws` |
| **Access** | Anyone (public GitHub) | FiveAges team only |
| **Robots** | Dobot, ARX, Galbot, HT, quadruped | FA W2/W2R/S2/S2R, dual-arm CCS |
| **Submodules** | Public only | Public + private |
| **OCS2** | Debian package or source | Full source (default) |
| **Purpose** | Learning, OSS development | Production deployment |

## open-deploy-ws (Public)

**Repository:** [https://github.com/fiveages-sim/open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws)

### Features

- All submodules are publicly accessible
- Supports multiple robots: Dobot CR5, ARX X5/ACone/Lift2S, Galbot, HT Panthera
- OCS2 available as Debian package (`ros-jazzy-ocs2`)
- Lean branches for minimal builds: `dobot-cr5`, `arx-acone`
- Good for learning, experimentation, and contributing

### Initialization

```bash
git clone https://github.com/fiveages-sim/open-deploy-ws.git
cd open-deploy-ws
./init_repo.sh
```

The init script will:
1. Configure submodule visibility (only public modules)
2. Prompt for OCS2 install method: Debian package or source
3. Initialize selected submodules

### Visibility Configuration

The workspace uses `submodules_visibility.conf` to track which submodules are public or private:

```ini
# Example visibility config
[public]
arms_ros2_control
robot_descriptions
robot-descriptions-common

[private]
# Private submodules are not cloned in open-deploy-ws
```

### Lean Branches

For minimal builds focusing on a single robot:

```bash
# Dobot CR5 only
git checkout dobot-cr5

# ARX ACone only
git checkout arx-acone
```

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
- Humanoids: `fiveages_w2`, `fiveages_w2r`, `fiveages_s2`, `fiveages_s2r`
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
  gripper_type: <gripper-model>
```

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

- You're deploying to FA humanoids (W2/S2 series)
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
