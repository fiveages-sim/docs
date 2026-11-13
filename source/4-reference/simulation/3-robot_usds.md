# robot_usds

USD robot asset superproject for Isaac Sim. In FaSim-Isaac this tree is the `robots/` submodule.

**Repository:** [fiveages-sim/robot_usds](https://github.com/fiveages-sim/robot_usds)

Brand labels in this docs set follow [README_zh-CN.md §3.1](https://github.com/fiveages-sim/robot_usds/blob/main/README_zh-CN.md#31-中文简称与英文标识对照). English folder names match that table. Examples: 方舟无限 = **ARX**; 高擎 = **HighTorque** / Panthera; 越疆 = **Dobot**; 银河通用 = **Galbot**; 第五纪 = **FiveAges**.

The [upstream README](https://github.com/fiveages-sim/robot_usds/blob/main/README.md) is the gallery and the full model list. This page records how the tree is checked out and which paths are git submodules.

## Purpose

`robot_usds` holds the robot USD models used in Isaac Sim, including in-tree brand folders and a small set of git submodules. Environment and project scenes are not in this repository; they sit beside it under FaSim `environment/`. See [Environment assets](5-env_assets.md).

## Checkout

**Primary path:** inside FaSim-Isaac, `./init.sh` operation 1 initializes `robots/` according to `submodules_visibility.conf`. Start Sim with `./run.sh`. There is no `./run.sh --robot`; open the USD from `robots/` or from a scene under `environment/`. Steps: [Isaac Sim](../../2-how_to/2-simulation/4-isaac_sim.md).

FaSim’s visibility file, as checked on 2026-11-13 (`submodules_visibility.conf` on FaSim-Isaac `main`), marks:

| Path under `robots/` | Visibility in FaSim | GitHub remote |
|----------------------|---------------------|---------------|
| `humanoid/FiveAges/Gen1` | public | [fiveages-gen1-robot-usds](https://github.com/fiveages-sim/fiveages-gen1-robot-usds) (public) |
| `humanoid/FiveAges/Gen2` | public | [fiveages-gen2-robot-usds](https://github.com/fiveages-sim/fiveages-gen2-robot-usds) (public) |
| `humanoid/FiveAges/Gen3` | private | [fiveages-gen3-robot-usds](https://github.com/fiveages-sim/fiveages-gen3-robot-usds) (private; needs access) |
| `humanoid/Galbot` | public | [galbot-usds](https://github.com/fiveages-sim/galbot-usds) |
| `humanoid/Ubtech` | private | [ubtech-usds](https://github.com/fiveages-sim/ubtech-usds) (needs access) |

Public rows start checked in operation 1. Private rows stay unchecked until you can open them. A later run only adds what you check.

:::{admonition} Manual fallback
:class: note

Standalone clone only if you are not using FaSim. After a plain clone, submodule directories are empty until you init them at the paths in `.gitmodules`:

:::{code-block} bash
git clone https://github.com/fiveages-sim/robot_usds.git
cd robot_usds
git submodule update --init
:::

To init one public gitlink, for example Gen2: `git submodule update --init humanoid/FiveAges/Gen2`. If you use robot_usds outside FaSim, put `environment/fiveages_env` next to this tree so scene USDs can reference it ([environment README note](https://github.com/fiveages-sim/robot_usds/blob/main/README.md)).
:::

(robot-usds-submodules)=

## Git submodules

These are the only USD remotes in `robot_usds/.gitmodules` on `main`. Each gitlink has `branch = main`. The superproject still pins a commit; `git submodule update` checks out that revision.

| Path | Repository | What is in the public tree |
|------|------------|----------------------------|
| `humanoid/FiveAges/Gen1` | [fiveages-gen1-robot-usds](https://github.com/fiveages-sim/fiveages-gen1-robot-usds) | W1 / Gen1 (public) |
| `humanoid/FiveAges/Gen2` | [fiveages-gen2-robot-usds](https://github.com/fiveages-sim/fiveages-gen2-robot-usds) | W2 / S2 / Gen2 (public; `W2/`, `S2/`, `components/`). W2R and S2R are not in this repo. Their URDF remotes stay private. |
| `humanoid/FiveAges/Gen3` | [fiveages-gen3-robot-usds](https://github.com/fiveages-sim/fiveages-gen3-robot-usds) | Gen3 (private remote; needs access) |
| `humanoid/Galbot` | [galbot-usds](https://github.com/fiveages-sim/galbot-usds) | Galbot mobile manipulator USD |
| `humanoid/Ubtech` | [ubtech-usds](https://github.com/fiveages-sim/ubtech-usds) | Ubtech humanoid USD (private remote; needs access) |

URDF / deploy for FiveAges robots: [FiveAges robot descriptions](../descriptions/4-fiveages_umbrella.md). Gen1 and Gen2 under `humanoid/FiveAges/` are wheeled-arm USD. They are not bipeds.

To see the pin, or to move one submodule (example: Galbot):

:::{code-block} bash
cd robot_usds
git submodule status
git submodule update --remote humanoid/Galbot
# or pin: cd humanoid/Galbot && git checkout <commit> && cd ../.. && git add humanoid/Galbot
:::

Prefer FaSim `./init.sh --update` when you work inside the Isaac workspace.

## In-tree categories

Assets that are not git submodules live in the superproject itself. Category roots on `main`:

| Directory | Content |
|-----------|---------|
| `humanoid/` | Humanoid and wheeled-arm USD, including the FiveAges, Galbot, and Ubtech gitlinks above, and in-tree brands such as Dyna Taku (`humanoid/Dyna/Taku`) |
| `manipulators/` | Arm models |
| `mobile_base/` | Chassis models, including Linkhou S2 (`mobile_base/Linkhou/S2_V1`) |
| `mobile_manipulator/` | Mobile + arm (singular directory name) |
| `grippers/` | Gripper USD |
| `dexhands/` | Dexterous-hand USD |
| `suction_cup/` | Suction-cup USD |
| `components/` | Shared wheels and fixtures |
| `sensors/` | Camera, lidar, and related models |

The full product list is in the [robot_usds README §3](https://github.com/fiveages-sim/robot_usds/blob/main/README.md). Swerve graph examples used by the FaSim steering extension: [Swerve extension](2-fasim_isaac.md#swerve-extension).

## Related

- [FaSim-Isaac](2-fasim_isaac.md)
- [Environment assets](5-env_assets.md)
- [Isaac Sim how-to](../../2-how_to/2-simulation/4-isaac_sim.md)
