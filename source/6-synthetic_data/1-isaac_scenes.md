# Isaac Scenes and USD

Synthetic datagen in this stack is an **Isaac Sim** line. Gazebo is not part of this pipeline.

Scene assets live in **FaSim-Isaac**. Robot USD files are the **robot_usds** superproject (FaSim submodule `robots/`). Environment and private project USDs sit beside that tree, not inside it.

## FaSim-Isaac (scene host)

**Repository:** [fiveages-sim/FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac)

FaSim-Isaac is the one-click Isaac asset workspace: it clones USD submodules, can install the Isaac ROS 2 Jazzy overlay, and starts Sim. Prefer the scripts; do not hand-assemble the tree.

:::{code-block} bash
git clone git@github.com:fiveages-sim/FaSim-Isaac.git
cd FaSim-Isaac
./init.sh
./run.sh
:::

From the FaSim README:

1. **`./init.sh` operation 1** — initialize submodules listed in `.gitmodules` / `submodules_visibility.conf`. **public** items are selected by default; **private** items are not (need repo access). Re-runs are additive (`update --init` on the selection).
2. **`./init.sh` operation 2** — optional **Isaac ROS 2 Jazzy workspace**: download matching Isaac ROS workspaces, extract `jazzy_ws` to `isaac_jazzy_ws/`, install rosdep/colcon deps, build, and append `~/.bashrc`. Version menu queries GitHub stable tags; fallback list in `config/fa_sim.conf` currently includes `6.0.1` / `6.0.0` / `5.1.0`. Override with `ISAAC_SIM_VERSION=… ./init.sh`.
3. **`./run.sh`** — start Isaac Sim. Default install path is `ISAACSIM_DIR` (`~/isaacsim` unless you copy `config/fa_sim.local.template.conf` → `config/fa_sim.local.conf`). The menu is PhysX / Newton / Headless Streaming.

The datagen example README ([`examples/IsaacSim/README.md`](https://github.com/fiveages-sim/lerobot_ros2/blob/feature/sim-grasp-datagen/examples/IsaacSim/README.md) on `feature/sim-grasp-datagen`) currently lists Ubuntu 24.04, ROS 2 Jazzy, and Isaac Sim 6.0. Keep path/version in FaSim config rather than editing launch files by hand.

Layout from that README:

:::{code-block} none
FaSim-Isaac/
├── init.sh
├── run.sh
├── config/                 # fa_sim.conf + optional fa_sim.local.conf
├── robots/                 # → robot_usds
├── environment/
│   ├── fiveages_env/       # → fiveages-env-usds (public scenes)
│   └── fa-project-usd/     # → fa-project-usd (private project USD)
└── isaac_jazzy_ws/         # created by init.sh operation 2
:::

Open the target robot USD from `robots/` (robot_usds) in Isaac and run the simulation. Enable Isaac’s ROS 2 simulation-control and prim services as in the [NVIDIA Isaac ROS 2 workspace docs](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_ros.html#setup-ros-2-workspaces) linked from the example README (`/set_simulation_state`, prim service for object pose).

Package details: [FaSim-Isaac reference](../4-reference/simulation/2-fasim_isaac.md).

## robot_usds (robot USD only)

**Repository:** [fiveages-sim/robot_usds](https://github.com/fiveages-sim/robot_usds)

This chapter documents USD **as referenced by robot_usds** (and as the FaSim `robots/` submodule). After a plain clone, submodule directories are empty until:

:::{code-block} bash
git clone git@github.com:fiveages-sim/robot_usds.git
cd robot_usds
git submodule update --init --recursive
:::

Inside FaSim, `./init.sh` does that for you. Paths in `.gitmodules` are relative to the robot_usds root so USD references resolve.

Git submodules recorded there:

| Path | Upstream |
|------|----------|
| `humanoid/FiveAges/Gen1` | fiveages-gen1-robot-usds |
| `humanoid/FiveAges/Gen2` | fiveages-gen2-robot-usds |
| `humanoid/FiveAges/Gen3` | fiveages-gen3-robot-usds |
| `humanoid/Ubtech` | ubtech-usds |
| `humanoid/Galbot` | galbot-usds |

FaSim `submodules_visibility.conf` marks Galbot **public** and the FiveAges Gen\* / Ubtech trees **private**. In-tree (not submodule) categories on robot_usds include grippers, dexhands, manipulators, mobile bases, mobile manipulators, and sensors — browse the repo; do not invent extra USD roots.

FiveAges **Gen1 / Gen2 / Gen3** are wheeled-arm USD generations under `humanoid/FiveAges/` (README maps Gen1→W1, Gen2→W2/S2). They are not bipedal humanoids.

Full tree: [robot_usds reference](../4-reference/simulation/3-robot_usds.md), [USD submodules](../4-reference/simulation/4-usd_submodules.md).

## Environment and private project USD

Environment assets are **siblings** of `robots/`, not robot_usds submodules.

| Tree | Visibility | Role |
|------|------------|------|
| `environment/fiveages_env/` → [fiveages-env-usds](https://github.com/fiveages-sim/fiveages-env-usds) | Public | Shared Isaac scenes: `static/` (tables, shelves, boxes), `moveable/` (small objects), `articulation/` (drawers, …), `background/`, `tasks/` (composed task scenes). |
| `environment/fa-project-usd/` → fa-project-usd | Private | Project-specific USD used by internal task scenes. `./init.sh` leaves this unchecked unless you have access. |

robot_usds README: if you use robot_usds **outside** FaSim, put `environment/fiveages_env` next to `robots/` so scene USDs can reference it.

Do not treat private project USD as a public robot model, and do not document product codenames that are not in the public robot_usds gallery text we rely on here.

[Environment assets reference](../4-reference/simulation/5-env_assets.md).

## Next on the pipeline

With Isaac running and ROS 2 topics/services up, motion and recording talk to the robot through **ros2_robot_interface**, orchestrated by **robot_action_composer**. Continue at [Interface and orchestration](2-orchestration.md).
