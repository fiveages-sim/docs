# Workspace Layout

This page explains the structure of the deploy workspaces and how to navigate them.

## open-deploy-ws Structure

```
open-deploy-ws/
├── src/
│   ├── arms_ros2_control/           # Main controller package
│   │   ├── ocs2_arm_controller/     # MPC controller
│   │   ├── adaptive_gripper_controller/
│   │   ├── arms_teleop_controller/
│   │   └── hardware/                # Nested HI submodules
│   │       ├── arx-ros2-control/
│   │       ├── dobot-cr-ros2-control/
│   │       └── ...
│   │
│   ├── robot_descriptions/          # Description umbrella
│   │   ├── robot-descriptions-common/
│   │   ├── robot-descriptions-dobot/
│   │   ├── robot-descriptions-arx/
│   │   └── ...
│   │
│   └── ocs2_ros2/                   # (if source build)
│
├── init_repo.sh                     # Initialization script
├── submodules_visibility.conf       # Public/private visibility
├── deb_versions.conf                # GitHub Release .deb repos and tags
└── build/, install/, log/           # Build outputs
```

## fa-deploy-ws Structure

```
fa-deploy-ws/
├── src/
│   ├── arms_ros2_control/           # Same as open-deploy-ws
│   │   └── library/                 # Additional private submodules
│   │       ├── ocs2-wbc-controller/
│   │       ├── ocs2-humanoid/
│   │       └── lina_planning/
│   │
│   ├── robot-descriptions-fiveages/ # Private FA descriptions
│   │   ├── common/
│   │   ├── arms/
│   │   └── robot/
│   │       ├── fa-w2-description/
│   │       ├── fa-s2-description/
│   │       └── ...
│   │
│   └── ocs2_ros2/                   # Full source (default)
│
├── init_repo.sh                     # Robot-specific init
├── quick_start.sh                   # Quick launch script
├── release.sh                       # Release packaging
├── presets/                         # Robot configurations
│   ├── fiveages_w2.yaml
│   ├── tianji_m6_ccs.yaml
│   └── ...
└── robot.local.yaml.template        # Local config template
```

## Key Differences

| Aspect | open-deploy-ws | fa-deploy-ws |
|--------|----------------|--------------|
| Submodules | Public only | Public + private |
| Init script | `./init_repo.sh` | `./init_repo.sh --robot <id>` |
| WBC controller | Not included | Included in library/ |
| Release script | No | Yes |
| Robot presets | No | Yes |

## Submodule Organization

### Nested Submodules

Submodules are organized hierarchically:

```
arms_ros2_control/
└── hardware/           # Hardware interfaces
    ├── arx-ros2-control/      (submodule)
    ├── dobot-cr-ros2-control/ (submodule)
    └── ...

robot_descriptions/
├── robot-descriptions-common/ (submodule)
├── robot-descriptions-dobot/  (submodule)
└── ...
```

### Initialization

**Don't use blind recursive init:**

```bash
# AVOID - initializes everything including private modules
git submodule update --init --recursive

# BETTER - use the init script
./init_repo.sh
```

The init script respects visibility and only initializes appropriate submodules.

## Build Outputs

After building:

```
workspace/
├── build/              # Build artifacts
│   ├── package_a/
│   └── package_b/
├── install/            # Installed packages
│   ├── setup.bash      # Source this!
│   ├── package_a/
│   └── package_b/
└── log/                # Build logs
```

**Always source from install:**

```bash
source install/setup.bash  # Correct
source build/...           # Wrong!
```

## Package Dependencies

Dependencies flow downward:

```
Controllers (ocs2_arm_controller)
      ↓ depends on
Hardware Interfaces (*-ros2-control)
      ↓ depends on
Descriptions (*-description)
      ↓ depends on
Common (robot-descriptions-common)
```

Build with `--packages-up-to` to build a package and its dependencies:

```bash
colcon build --packages-up-to ocs2_arm_controller
```

## Working with Submodules

### Check Status

```bash
git submodule status
```

### Update One Submodule

```bash
cd src/arms_ros2_control
git fetch origin
git checkout main
git pull
```

### Update All (Carefully)

```bash
git submodule update --remote
```

### Reset to Pinned Versions

```bash
git submodule update --init
```

## Best Practices

1. **Use init scripts** — They handle visibility and dependencies
2. **Don't commit submodule changes accidentally** — Check `git status` in root
3. **Build incrementally** — Use `--packages-up-to` for faster iteration
4. **Keep workspaces separate** — Don't mix open-deploy-ws and fa-deploy-ws
