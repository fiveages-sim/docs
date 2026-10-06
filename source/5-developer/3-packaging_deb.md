# Debian Packaging

Creating Debian packages for FiveAges Sim components.

## Overview

Several components are available as Debian packages:
- OCS2 (`ros-jazzy-ocs2`)
- robot-descriptions-common
- arms_ros2_control (optional)

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

```
package (1.2.3-1) jazzy; urgency=medium

  * Fix gripper control bug
  * Add new robot support

 -- Maintainer <email>  Date
```

## CI/CD Integration

Packages are built and tested in CI:
- Build on each release tag
- Publish to package repository
- Test installation

```{admonition} TODO
:class: warning

Package repository and automated release process documentation to be added.
```

## Related

- [Source vs Deb](../3-concepts/5-source_vs_deb.md)
