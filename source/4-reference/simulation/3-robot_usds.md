# robot_usds

USD robot asset superproject for Isaac Sim.

**Repository:** [fiveages-sim/robot_usds](https://github.com/fiveages-sim/robot_usds)

Brand **EN/ZH** labels in this docs set follow [README_zh-CN.md §3.1](https://github.com/fiveages-sim/robot_usds/blob/main/README_zh-CN.md#31-中文简称与英文标识对照) (English folder names match that table). Examples: 方舟无限 = **ARX**; 高擎 = **HighTorque** / Panthera; 越疆 = **Dobot**; 银河通用 = **Galbot**; 中科第五纪 = **FiveAges**. Do not invent brands (including bare “Ark”).

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

**Primary path:** inside FaSim-Isaac, `./init.sh` operation 1 initializes `robots/` (this superproject) according to `submodules_visibility.conf`.

:::{code-block} bash
cd FaSim-Isaac
./init.sh
:::

:::{admonition} Manual fallback
:class: note

Standalone clone only if you are not using FaSim:

:::{code-block} bash
git clone https://github.com/fiveages-sim/robot_usds.git
cd robot_usds
git submodule update --init
:::
:::

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

From the [robot_usds README](https://github.com/fiveages-sim/robot_usds/blob/main/README.md) Humanoid → FiveAges table (not invented labels):

- **Gen1** — W1 (`humanoid/FiveAges/Gen1` → `fiveages-gen1-robot-usds`)
- **Gen2** — W2 / S2 (`humanoid/FiveAges/Gen2` → `fiveages-gen2-robot-usds`)
- **Gen3** — WCE3 (`humanoid/FiveAges/Gen3` → `fiveages-gen3-robot-usds`)

URDF / deploy: [FiveAges robot descriptions](../descriptions/4-fiveages_umbrella.md).

Load assets through FaSim-Isaac (`./init.sh` / `./run.sh`) and that robot’s USDA — do not invent a `galbot.usd` prim path here.

## Related

- [USD Submodules](4-usd_submodules.md)
- [FaSim-Isaac](2-fasim_isaac.md)
- [Synthetic Data](../../2-how_to/7-synthetic_data/1-isaac_scenes.md)
