# Environment Assets

USD environment and project scenes used with Isaac Sim. These trees are siblings of `robots/`, not submodules of `robot_usds`.

Robot models: [robot_usds](3-robot_usds.md). How to start Sim and open a file: [Isaac Sim](../../2-how_to/2-simulation/4-isaac_sim.md). There is no `./run.sh --env` flag; open the scene USD from `environment/` after `./run.sh`.

## Location in FaSim-Isaac

:::{code-block} none
FaSim-Isaac/
├── robots/                      # robot_usds
└── environment/
    ├── fiveages_env/            # → fiveages-env-usds
    ├── fa-project-usd/          # private project scenes
    ├── artvip-usd/              # ArtVIP components
    ├── labutopia-usd/           # LabUtopia components (private)
    └── ArtVIP/                  # official ArtVIP download (gitignore)
:::

Top-level URLs: [FaSim-Isaac `.gitmodules`](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/.gitmodules). `./init.sh` operation 1 uses `submodules_visibility.conf`. As checked on 2026-11-13, `environment/fa-project-usd` and `environment/labutopia-usd` are marked private (unchecked until you have access). `environment/artvip-usd` is not listed as private in that file, so operation 1 checks it with the other public-marked items. The GitHub repository itself is still private; cloning it needs access.

## fiveages_env

**Repository:** [fiveages-sim/fiveages-env-usds](https://github.com/fiveages-sim/fiveages-env-usds) (public)

Shared Isaac scenes and task composition, as described in that [README](https://github.com/fiveages-sim/fiveages-env-usds/blob/main/README.md):

| Directory | Content |
|-----------|---------|
| `static/` | Static parts: tables, boxes, shelves |
| `moveable/` | Small movable objects |
| `articulation/` | Articulated mechanisms such as drawers |
| `background/` | Room and background geometry |
| `tasks/` | Composed task scenes that reference the directories above |

Browse the repository for the current USD files. Open a scene under `environment/fiveages_env/` in Isaac after `./run.sh`.

(fa-project-usd)=

## fa-project-usd

**Repository:** [fa-project-usd](https://github.com/fiveages-sim/fa-project-usd) (private; the link needs access)

Internal project scenes. On `main`, a project is `scene.usd(a)`, `objects/`, and a runnable `env/` ([README](https://github.com/fiveages-sim/fa-project-usd/blob/main/README.md)). Projects may sit at the repository root or under a customer or series directory.

The files the orchestrator reads next to those scenes (`robot.yaml`, `task_configs/`, and `maps/` or `map/`) are on branch `feature/sinopec-test-tube-picking`. That branch was ahead of `main` and not merged when these pages were checked on 2026-11-13. Three projects there use this layout: `Fiveages/2026-11 Standard Moving Boxes`, `Siemens/2026-06 Wind Turbine Blade Detection`, and `Aimbo/2026-04 Bosch German&Poland POC`. You need access to open the branch.

`NavigationLaunch` can point `map` at a `map.yaml` stored in that project, as a path relative to the opened `env/` layer. The node itself is documented under [FaSim-Isaac Navigation](2-fasim_isaac.md#navigation). The public way to run a project directory is [lerobot_ros2 `examples/IsaacSim/README.md`](https://github.com/fiveages-sim/lerobot_ros2/blob/main/examples/IsaacSim/README.md): `motion-generation` with `LEROBOT_ROOT` set. Keep camera rigs in the scene USD.

## ArtVIP and LabUtopia

`environment/artvip-usd` ([artvip-usd](https://github.com/fiveages-sim/artvip-usd)) holds ArtVIP scene components that payload the official dataset. `./init.sh` operation 3 downloads the official data into `environment/ArtVIP/` with `tools/artvip_kitchen.py`. The FaSim README: scene components stay in `artvip-usd`; the official data is not committed.

`environment/labutopia-usd` ([labutopia-usd](https://github.com/fiveages-sim/labutopia-usd)) holds LabUtopia components. The repository is private, and FaSim marks the submodule private.

## Creating a custom scene

1. Create the USD scene in Isaac Sim.
2. Put it under `environment/fiveages_env/` or, with access, under [fa-project-usd](https://github.com/fiveages-sim/fa-project-usd) using the `scene` / `objects` / `env` layout on `main`.
3. Open that file from `./run.sh`.

## Related

- [robot_usds](3-robot_usds.md)
- [FaSim-Isaac](2-fasim_isaac.md)
- [Isaac Sim how-to](../../2-how_to/2-simulation/4-isaac_sim.md)
- [Isaac Scenes and USD](../../2-how_to/7-synthetic_data/1-isaac_scenes.md) (datagen pipeline)
