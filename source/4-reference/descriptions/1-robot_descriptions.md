# robot_descriptions

Public umbrella repository for all robot descriptions.

**Repository:** [fiveages-sim/robot_descriptions](https://github.com/fiveages-sim/robot_descriptions)

## Purpose

`robot_descriptions` aggregates brand-specific description packages as submodules, providing a single entry point for all robot models.

## Structure

:::{code-block} none
robot_descriptions/
├── robot-descriptions-common/    # Shared components
├── robot-descriptions-dobot/     # Dobot robots
├── robot-descriptions-arx/       # ARX robots
├── robot-descriptions-galbot/    # Galbot robots
├── robot-descriptions-ht/        # HT robots
├── robot-descriptions-quadruped/ # Quadruped robots
└── ... (more brands)
:::

## Usage

### Initialize Specific Brand

In `open-deploy-ws`, prefer `./init_repo.sh` (nested paths under `src/robot-descriptions/`). Do not recursive-init.

### Build All Descriptions

```bash
colcon build --symlink-install
```

The umbrella directory in `open-deploy-ws` is `src/robot-descriptions/` (hyphen). Nested modules follow `submodules_visibility.conf`.

### Use in Launch

```bash
ros2 launch ocs2_arm_controller demo.launch.py
```

`demo.launch.py` default `robot` is `cr5`. Pass `robot:=<key>` for other `{key}_description` packages.

## Submodules

| Submodule | Visibility | Robots |
|-----------|------------|--------|
| robot-descriptions-common | Public | Grippers, sensors, hands |
| robot-descriptions-dobot | Public | CR5, CR10 |
| robot-descriptions-arx | Public | X5, Acone (arm), Lift 2S |
| robot-descriptions-galbot | Public | G1 mobile manipulator |
| robot-descriptions-ht | Public | HighTorque Panthera HT |
| robot-descriptions-quadruped | Public | Quadrupeds |
| robot-descriptions-tianji | Private | M6, M6S, M20S |
| robot-descriptions-rokae | Private | Rokae arms |
| robot-descriptions-ubtech | Private | Ubtech humanoids |
| agibot-g2-description | Private | Agibot G2 |

## Adding a Robot

1. Create description package (see [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md))
2. Add as submodule:
   ```bash
   git submodule add https://github.com/fiveages-sim/robot-descriptions-newbrand.git
   ```
3. Update visibility configuration
4. Create PR

## Related

- [robot-descriptions-common](2-common.md)
- [Brand packages](3-brand_public.md)
