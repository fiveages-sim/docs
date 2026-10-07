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

- Internal workspace for FiveAges wheeled-arm humanoids (W2, W2R, S2, S2R) and dual-arm CCS
- Description remotes live as private gitlinks under [robot_descriptions `humanoid/FiveAges/`](../4-reference/descriptions/4-fiveages_umbrella.md) — not a separate `robot-descriptions-fiveages` umbrella
- Full OCS2 + WBC source when that workspace’s README says so

```{admonition} Source of truth
:class: important

The `fa-deploy-ws` README is **not public**. Flags, robot IDs, and on-robot YAML are documented only in that README after you have access. Public-side pattern: [fa-deploy-ws Setup](../1-getting_started/4-fa_deploy_ws.md).
```

### Initialization

```bash
git clone <internal-url>/fa-deploy-ws.git
cd fa-deploy-ws
./init_repo.sh
```

Same script **name** as `open-deploy-ws`. Extra flags, robot IDs, and on-robot YAML live in the private README — copy them from there.

Public end-effector selection is launch `type` / `left_type` / `right_type` (and `robot_profile`), not a `gripper:=` argument. See [robot_common_launch](../4-reference/descriptions/2-common.md).

## Choosing Your Path

### Use the Public Path If:

- You're new to the ecosystem
- You're developing with publicly available robots
- You're contributing to open source packages
- You don't have FiveAges private repo access

### Use the Internal Path If:

- You're deploying to FA wheeled-arm humanoids (W2/S2 series)
- You need WBC whole-body control
- You have authorized access to private repositories

## Transitioning Between Paths

### Public → Internal

1. Request access to private repositories
2. Clone `fa-deploy-ws` fresh (don't try to convert open-deploy-ws)
3. Follow that repository’s README

### Internal Users on Public Hardware

If you have internal access but want to work with public robots, use `open-deploy-ws` for a public-only checkout.

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
