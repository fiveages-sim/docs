# robot_usds

USD robot asset superproject for Isaac Sim.

**Repository:** [fiveages-sim/robot_usds](https://github.com/fiveages-sim/robot_usds)

## Purpose

`robot_usds` provides:
- USD robot models for Isaac Sim
- Organized asset hierarchy
- Submodule management for brand-specific assets

## Structure

:::{code-block} none
robot_usds/
├── humanoid/
│   ├── FiveAges/
│   │   ├── Gen1/             # → fiveages-gen1-robot-usds
│   │   ├── Gen2/             # → fiveages-gen2-robot-usds
│   │   └── Gen3/             # → fiveages-gen3-robot-usds
│   ├── Galbot/               # → galbot-usds
│   └── Ubtech/               # → ubtech-usds
├── manipulators/             # Arm USD assets
├── mobile_manipulators/
├── grippers/
└── sensors/
:::

## Submodules

The following are managed as Git submodules:

| Path | Repository | Branch |
|------|------------|--------|
| `humanoid/FiveAges/Gen1` | fiveages-gen1-robot-usds | main |
| `humanoid/FiveAges/Gen2` | fiveages-gen2-robot-usds | main |
| `humanoid/FiveAges/Gen3` | fiveages-gen3-robot-usds | main |
| `humanoid/Galbot` | galbot-usds | main |
| `humanoid/Ubtech` | ubtech-usds | main |

## Usage

### Initialize

```bash
git clone https://github.com/fiveages-sim/robot_usds.git
cd robot_usds
git submodule update --init
```

### With FaSim-Isaac

```bash
cd FaSim-Isaac
./init.sh  # Handles robot_usds initialization
```

## In-Tree Assets

Assets directly in `robot_usds` (not submodules):

| Directory | Content |
|-----------|---------|
| `grippers/` | Gripper USD models |
| `manipulators/` | Arm models |
| `mobile_manipulators/` | Mobile + arm |
| `sensors/` | Camera, lidar models |

## Asset Naming

### Gen1/Gen2/Gen3

FiveAges robot generations:
- **Gen1** — First generation humanoid
- **Gen2** — Second generation humanoid
- **Gen3** — Third generation humanoid

These names refer to internal development generations.

## Loading in Isaac Sim

```python
from omni.isaac.core.utils.stage import add_reference_to_stage

# Load robot USD
add_reference_to_stage(
    usd_path="robot_usds/humanoid/Galbot/galbot.usd",
    prim_path="/World/Robot"
)
```

## Related

- [USD Submodules](4-usd_submodules.md)
- [FaSim-Isaac](2-fasim_isaac.md)
