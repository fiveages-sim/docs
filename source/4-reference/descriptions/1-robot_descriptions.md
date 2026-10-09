# robot_descriptions

Public umbrella repository. Brand trees are **git submodules** at the paths in the official README (not a flat list of `robot-descriptions-*` folders).

**Repository:** [fiveages-sim/robot_descriptions](https://github.com/fiveages-sim/robot_descriptions)

```{admonition} Source of truth
:class: important

- Paths and submodule table: [README.md](https://github.com/fiveages-sim/robot_descriptions/blob/main/README.md)
- In `open-deploy-ws` the checkout is `src/robot-descriptions/` after **`./init_repo.sh`**. Do not recursive-init there.
- Description-side Cursor skills: **`feature/agilex` only** (`split-chassis-glb`) — [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md). **`main` has no `.cursor/skills`**. Newer AgileX / Rokae INEX rows: [README on `feature/agilex`](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/README.md). **Taku** is in-tree on that branch at `humanoid/Dyna/taku_description` ([package README](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/humanoid/Dyna/taku_description/README.md) §3.1 / §3.2); meshes under `meshes/{chassis,body,head,arm,dynaclaw}/`. Control is `split_body.launch.py` / `full_body.launch.py` with `robot:=taku`, not `demo.launch.py`. It is not on `main` and is not a row in that branch’s brand tables.
```

## Layout (README)

:::{code-block} none
robot_descriptions/
├── common/                              # robot-descriptions-common
├── quadruped/                           # robot-descriptions-quadruped
├── humanoid/                            # in-tree wheeled / leg humanoids
│   ├── FiveAges/                        # private gitlinks (not in README tables)
│   ├── Dyna/taku_description            # in-tree on feature/agilex only
│   ├── Galbot/                          # robot-descriptions-galbot
│   └── Agibot/agibot_g2_description     # private
├── manipulator/
│   ├── Dobot/                           # robot-descriptions-dobot
│   ├── ARX/                             # robot-descriptions-arx
│   ├── Tianji/                          # robot-descriptions-tianji
│   ├── Rokae/                           # robot-descriptions-rokae
│   └── HighTorque/panthera_ht_description
└── … in-tree packages (see README tables)
:::

## Submodules (README)

| Name | Path | Repository |
|------|------|------------|
| Common Components | `common` | [robot-descriptions-common](https://github.com/fiveages-sim/robot-descriptions-common) |
| Quadruped Robots | `quadruped` | [robot-descriptions-quadruped](https://github.com/fiveages-sim/robot-descriptions-quadruped) |
| Dobot CR5 | `manipulator/Dobot` | [robot-descriptions-dobot](https://github.com/fiveages-sim/robot-descriptions-dobot) |
| Tianji M6 | `manipulator/Tianji` | [robot-descriptions-tianji](https://github.com/fiveages-sim/robot-descriptions-tianji) |
| Rokae AR5 | `manipulator/Rokae` | [robot-descriptions-rokae](https://github.com/fiveages-sim/robot-descriptions-rokae) |
| ARX Robots | `manipulator/ARX` | [robot-descriptions-arx](https://github.com/fiveages-sim/robot-descriptions-arx) |
| Galbot Robots | `humanoid/Galbot` | [robot-descriptions-galbot](https://github.com/fiveages-sim/robot-descriptions-galbot) |
| Agibot G2 | `humanoid/Agibot/agibot_g2_description` | [agibot-g2-description](https://github.com/fiveages-sim/agibot-g2-description) (private) |
| Panthera HT | `manipulator/HighTorque/panthera_ht_description` | [panthera_ht_description](https://github.com/fiveages-sim/panthera_ht_description) |

README also tables **in-tree** wheeled humanoids, mobile manipulators, manipulators (including HighTorque Panthera HT path above), and leg humanoids. Brand folders are those listed there.

FiveAges URDF packages are **private gitlinks** under `humanoid/FiveAges/` in [`.gitmodules`](https://github.com/fiveages-sim/robot_descriptions/blob/main/.gitmodules). They are **not** in the README brand tables and are **not** a separate `robot-descriptions-fiveages` umbrella. Paths and remotes: [FiveAges robot descriptions](4-fiveages_umbrella.md).

Standalone clone (README). In `open-deploy-ws`, prefer `./init_repo.sh` instead:

:::{code-block} bash
git submodule update --init common
git submodule update --init manipulator/ARX
:::

## Launch

`demo.launch.py` default `robot` is `cr5`. Pass `robot:=<key>` for other `{key}_description` packages.

:::{code-block} bash
ros2 launch ocs2_arm_controller demo.launch.py
:::

## Adding a robot

Copy an existing `{robot}_description` and follow [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md). New remotes and top-level folders should match the README submodule table.

## Related

- [robot-descriptions-common](2-common.md)
- [Brand packages](3-brand_public.md)
- [FiveAges robot descriptions](4-fiveages_umbrella.md)
- [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md)
