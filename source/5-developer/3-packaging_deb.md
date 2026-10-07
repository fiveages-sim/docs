# Debian Packaging

Creating `.deb` packages for FiveAges Sim components.

## Overview

Several components ship prebuilt `.deb` files on GitHub Releases (not on packages.ros.org / Ubuntu apt):
- OCS2 (`ros-jazzy-ocs2`) — [legubiao/ocs2_ros2 releases](https://github.com/legubiao/ocs2_ros2/releases)
- robot-descriptions-common (`ros-jazzy-robot-descriptions-common`) — [fiveages-sim/robot-descriptions-common releases](https://github.com/fiveages-sim/robot-descriptions-common/releases)
- arms_ros2_control (`ros-jazzy-arms-ros2-control`, optional) — [fiveages-sim/arms_ros2_control releases](https://github.com/fiveages-sim/arms_ros2_control/releases)

## Package Documentation

Detailed packaging instructions are in repository-specific `README.deb.md` files:

### arms_ros2_control

See `arms_ros2_control/README.deb.md` for:
- Build configuration
- Dependencies
- Release process

### robot-descriptions-common

See `robot-descriptions-common/README.deb.md` for:
- URDF packaging
- Mesh handling
- Version management

## General Process

### Prerequisites

```bash
sudo apt install python3-bloom fakeroot debhelper
```

### Create Package

```bash
cd <package>
bloom-generate rosdebian --ros-distro jazzy
fakeroot debian/rules binary
```

### Resulting Package

Output: `../<package>_<version>_amd64.deb`

### Install

```bash
sudo dpkg -i <package>_<version>_amd64.deb
sudo apt install -f  # Fix dependencies
```

## Version Management

### Semantic Versioning

Use semantic versioning: `MAJOR.MINOR.PATCH`

- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

### Changelog

Maintain changelog for releases:

:::{code-block} none
package (1.2.3-1) jazzy; urgency=medium

  * Fix gripper control bug
  * Add new robot support

 -- Maintainer <email>  Date
:::

## CI/CD Integration

Packages are built and tested in CI:
- Build on each release tag
- Publish `.deb` assets to GitHub Releases
- Test installation

```{admonition} TODO
:class: warning

Document the per-repo GitHub Release workflow (asset names, tags, and `deb_versions.conf`) in more detail.
```

## Related

- [Source vs Deb](../3-concepts/5-source_vs_deb.md)
