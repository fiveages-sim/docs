# Submodules Visibility

This page explains how the stack manages public and private submodules.

## The Visibility Problem

The FiveAges Sim ecosystem includes both:
- **Public repositories** — Open source, anyone can clone
- **Private repositories** — FiveAges internal, require access

Without careful management, users would encounter access errors when initializing submodules.

## Visibility Configuration

### submodules_visibility.conf

The `open-deploy-ws` uses a configuration file to track visibility:

```ini
# submodules_visibility.conf

[public]
src/arms_ros2_control
src/robot_descriptions
src/robot_descriptions/robot-descriptions-common
src/robot_descriptions/robot-descriptions-dobot
src/robot_descriptions/robot-descriptions-arx
# ... more public modules

[private]
# These are NOT initialized in open-deploy-ws
src/robot-descriptions-fiveages
src/arms_ros2_control/library/ocs2-wbc-controller
# ... private modules
```

### How It Works

1. `init_repo.sh` reads the visibility config
2. Only initializes submodules marked as `[public]`
3. Skips private submodules silently
4. Users with access can manually init private modules

## Public vs Private Submodules

### Public (open-deploy-ws)

| Category | Examples |
|----------|----------|
| Descriptions | dobot, arx, galbot, ht, quadruped, common |
| Hardware interfaces | arx, dobot, unitree, ht, marvin, modbus, can, juxie |
| Controllers | ocs2_arm_controller, adaptive_gripper_controller |
| Simulation | robot_usds, galbot-usds |

### Private (fa-deploy-ws only)

| Category | Examples |
|----------|----------|
| Descriptions | fiveages umbrella, tianji, rokae, fairino, FA robots |
| Hardware interfaces | rokae, eyou, wuji, dexcap, fairino |
| Controllers | ocs2-wbc-controller, ocs2-humanoid, lina_planning |
| Teleop | vr_pose_publisher, teleop-joint-mapper, wuji_glove_teleop |

## Working with Visibility

### Check Current Status

```bash
# See which submodules are initialized
git submodule status

# See which are registered (all)
git config --file .gitmodules --get-regexp path
```

### Initialize Specific Submodule

```bash
# Public submodule (should work for everyone)
git submodule update --init src/robot_descriptions/robot-descriptions-arx

# Private submodule (requires access)
git submodule update --init src/robot-descriptions-fiveages
```

### Force Skip Access Errors

```bash
# Continue even if some submodules fail
git submodule update --init || true
```

## Access Management

### Getting Private Access

1. Request access from your team lead
2. Add SSH key to GitHub account
3. Verify access:
   ```bash
   ssh -T git@github.com
   ```
4. Re-run initialization or manually init private submodules

### Testing Access

```bash
# Test if you can access a private repo
git ls-remote git@github.com:fiveages-sim/fa-deploy-ws.git
```

## Common Issues

### Access Denied During Init

**Symptom:**
```
Permission denied (publickey)
fatal: Could not read from remote repository
```

**Solution:**
- You don't have access to that private submodule
- Use `open-deploy-ws` for public-only access
- Or request private access

### Submodule Path Conflicts

**Symptom:**
```
fatal: destination path 'src/xxx' already exists
```

**Solution:**
```bash
# Remove and re-init
rm -rf src/xxx
git submodule update --init src/xxx
```

### Detached HEAD Warnings

**Symptom:**
```
HEAD is now at abc123... Commit message
```

**This is normal** — submodules are pinned to specific commits.

To update to latest:
```bash
cd src/submodule_path
git checkout main
git pull
```

## Best Practices

1. **Use init scripts** — They respect visibility configuration
2. **Don't blind recursive init** — `git submodule update --init --recursive` will fail on private modules
3. **Keep workspaces separate** — Use open-deploy-ws for public, fa-deploy-ws for private
4. **Document access requirements** — Note which features need private access

## Nested Submodules

Some submodules contain their own submodules:

```
arms_ros2_control/
├── hardware/
│   ├── arx-ros2-control/      # Public
│   ├── rokae-ros2-control/    # Private
│   └── ...
└── library/
    ├── ocs2-wbc-controller/   # Private
    └── ...
```

The init script handles nested visibility automatically. If manually initializing:

```bash
# Init parent first
git submodule update --init src/arms_ros2_control

# Then specific children
cd src/arms_ros2_control
git submodule update --init hardware/arx-ros2-control
```

## Updating Visibility Config

If contributing a new submodule:

1. Add to `.gitmodules`:
   ```ini
   [submodule "src/new-package"]
       path = src/new-package
       url = https://github.com/fiveages-sim/new-package.git
   ```

2. Update visibility config:
   ```ini
   [public]
   src/new-package
   ```

3. Test initialization in a clean clone
