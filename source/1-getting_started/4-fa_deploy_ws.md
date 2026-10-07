# fa-deploy-ws Setup

Setup guide for the internal `fa-deploy-ws` workspace used for FiveAges robot deployment.

```{admonition} Access Required
:class: warning

This workspace requires access to private repositories. Contact your team lead for access if needed.
```

## Overview

`fa-deploy-ws` is the internal deployment workspace for:
- FiveAges wheeled-arm humanoids: W2, W2R, S2, S2R (and other prototypes)
- Dual-arm CCS configurations
- Production deployment and release packaging

## Key Differences from open-deploy-ws

| Aspect | open-deploy-ws | fa-deploy-ws |
|--------|---------------|--------------|
| Submodules | Public only | Public + private |
| Robots | Community robots | FA wheeled-arm humanoids |
| OCS2 | GitHub Release `.deb` or source | Full source (default) |
| WBC | Not included | Included |
| Release | Not available | `./release.sh` |
| Initialization | `./init_repo.sh` | `./init_repo.sh --robot <id>` |

## Prerequisites

- Access to fiveages-sim private repositories
- SSH key configured for GitHub
- ROS 2 Jazzy environment set up

## Cloning

```bash
git clone git@github.com:fiveages-sim/fa-deploy-ws.git
cd fa-deploy-ws
```

## Initialization

### Robot-Specific Init

```bash
./init_repo.sh --robot <robot-id>
```

### Available Robot IDs

| ID | Robot Type | Description |
|----|------------|-------------|
| `fiveages_w2` | Humanoid | W2 full-size humanoid |
| `fiveages_w2r` | Humanoid | W2R variant |
| `fiveages_s2` | Humanoid | S2 series |
| `fiveages_s2r` | Humanoid | S2R variant |
| `tianji_m6_ccs` | Dual-arm | M6 CCS configuration |
| `tianji_m20s_ccs` | Dual-arm | M20S CCS |
| `rokae_ar5_ccs` | Dual-arm | Rokae AR5 CCS |

Additional prototype robot IDs may be available — check `presets/` directory for the full list.

### Init Options

```bash
# Standard initialization
./init_repo.sh --robot fiveages_w2

# With release packages (pre-built binaries)
./init_repo.sh --robot fiveages_w2 --init-release
```

## Robot Configuration

### robot.local.yaml

Each robot requires a local configuration file that is **not committed to version control**:

```bash
cp robot.local.yaml.template robot.local.yaml
```

Edit `robot.local.yaml` with your robot's specific values:

```yaml
# Structure overview (actual values are robot-specific)
network:
  domain_id: <robot-specific-id>
  interface: <network-interface>
  
robot:
  type: <robot-type>
  # Additional robot-specific parameters
```

```{admonition} Configuration Security
:class: danger

Never commit `robot.local.yaml` with actual IP addresses, domain IDs, or other deployment-specific values. These are considered sensitive and vary per installation.
```

### Parameter Reference

| Parameter | Description |
|-----------|-------------|
| `domain_id` | ROS 2 Domain ID for network isolation |
| `interface` | Network interface connected to robot |
| `robot.type` | Robot model identifier |

Consult your robot's deployment documentation for specific values.

## Building

### Full Build

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
```

### Package-Specific Build

```bash
colcon build --packages-up-to ocs2_wbc_controller
```

## Quick Start Flow

### Mock Mode (Testing)

```bash
source install/setup.bash
./quick_start.sh --mock
```

### Real Hardware

```{admonition} Safety Warning
:class: danger

Before running on real hardware:
1. Verify emergency stop is accessible
2. Clear the robot's workspace
3. Start with low velocities
4. Have a trained operator present
```

```bash
source install/setup.bash
./quick_start.sh
```

## Release Packages

### Generate Release

```bash
./release.sh
```

This creates a deployable package without source code.

### Install Release

On target machine:

```bash
./release.sh --install
```

## Directory Structure

:::{code-block} none
fa-deploy-ws/
├── src/
│   ├── arms_ros2_control/
│   ├── robot-descriptions-fiveages/
│   ├── ocs2-wbc-controller/
│   ├── ocs2-humanoid/
│   └── ...
├── init_repo.sh
├── quick_start.sh
├── release.sh
├── robot.local.yaml.template
└── presets/
    ├── fiveages_w2.yaml
    ├── fiveages_s2.yaml
    └── ...
:::

## Submodule Management

The workspace nests many private submodules. Never use blind recursive init:

```bash
# DON'T do this - initializes unnecessary submodules
git submodule update --init --recursive  # AVOID

# DO use the init script with robot ID
./init_repo.sh --robot <id>
```

## Common Issues

### Submodule Access Denied

Verify your SSH key has access to the required private repositories:

```bash
ssh -T git@github.com
```

### Missing WBC Controller

Ensure you initialized with the correct robot ID that includes WBC:

```bash
./init_repo.sh --robot fiveages_w2
```

### Network Communication Fails

1. Verify `robot.local.yaml` has correct domain ID
2. Check network interface matches robot's network
3. Confirm Zenoh/DDS configuration if using multi-machine setup

## Next Steps

- [Go to real hardware](../2-how_to/9-go_real_hardware/0-index.md)
- [WBC controller reference](../4-reference/controllers/3-ocs2_wbc.md)
- [FA robot descriptions](../4-reference/descriptions/5-fa_robots.md)
