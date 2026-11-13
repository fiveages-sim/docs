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

`./init.sh` menu and `./run.sh` flags: [Isaac Sim](../2-simulation/4-isaac_sim.md). Operation 1 selects submodules (`public` checked, private unchecked until you have access). Operation 4 is the optional Isaac ROS 2 Jazzy overlay. The version menu queries GitHub stable tags; `config/fa_sim.conf` falls back to `6.2.0` / `6.1.0` / `6.0.1`. Override with `ISAAC_SIM_VERSION=… ./init.sh`. Operation 5 installs `fasim.ros2.nodes` (needed before Play on an in-process `ROS2ControlLaunch` graph).

The datagen example README ([`examples/IsaacSim/README.md`](https://github.com/fiveages-sim/lerobot_ros2/blob/main/examples/IsaacSim/README.md) on `main`) still lists Ubuntu 24.04, ROS 2 Jazzy, and Isaac Sim 6.0. Keep path and version in FaSim config. The FaSim fallback list above is newer than that 6.0 line.

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
└── isaac_jazzy_ws/         # created by init.sh operation 4
:::

Open the target robot USD from `robots/` (robot_usds) in Isaac and run the simulation. Enable Isaac’s ROS 2 simulation-control and prim services as in the [NVIDIA Isaac ROS 2 workspace docs](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_ros.html#setup-ros-2-workspaces) linked from the example README (`/set_simulation_state`, prim service for object pose).

Package details: [FaSim-Isaac reference](../../4-reference/simulation/2-fasim_isaac.md).

## robot_usds (robot USD only)

**Repository:** [fiveages-sim/robot_usds](https://github.com/fiveages-sim/robot_usds)

This chapter documents USD **as referenced by robot_usds** (and as the FaSim `robots/` submodule). **Primary path:** FaSim `./init.sh` operation 1 initializes that submodule (public items by default).

:::{admonition} Manual fallback
:class: note

After a plain clone of robot_usds (outside FaSim), submodule directories are empty until:

:::{code-block} bash
git clone git@github.com:fiveages-sim/robot_usds.git
cd robot_usds
git submodule update --init --recursive
:::
:::

Git submodules recorded there:

| Path | Upstream |
|------|----------|
| `humanoid/FiveAges/Gen1` | fiveages-gen1-robot-usds |
| `humanoid/FiveAges/Gen2` | fiveages-gen2-robot-usds |
| `humanoid/Ubtech` | ubtech-usds |
| `humanoid/Galbot` | galbot-usds |

FaSim `submodules_visibility.conf` marks Galbot public and the FiveAges and Ubtech trees private, so `./init.sh` does not select FiveAges by default. The Gen1 remote (`fiveages-gen1-robot-usds`) and the Gen2 remote (`fiveages-gen2-robot-usds`) are public. W2R and S2R are not in the Gen2 USD repo. robot_usds also keeps grippers, dexterous hands, manipulators, mobile bases, mobile manipulators, and sensors in the tree itself. Browse the repo for the current roots.

Gen1 and Gen2 under `humanoid/FiveAges/` are wheeled-arm USD. The README maps Gen1 to W1 and Gen2 to W2 and S2. They are not bipeds. URDF status: [FiveAges robot descriptions](../../4-reference/descriptions/4-fiveages_umbrella.md).

Full tree: [robot_usds reference](../../4-reference/simulation/3-robot_usds.md), [USD submodules](../../4-reference/simulation/4-usd_submodules.md).

## Environment and private project USD

Environment assets are **siblings** of `robots/`, not robot_usds submodules.

| Tree | Visibility | Role |
|------|------------|------|
| `environment/fiveages_env/` → [fiveages-env-usds](https://github.com/fiveages-sim/fiveages-env-usds) | Public | Shared Isaac scenes: `static/` (tables, shelves, boxes), `moveable/` (small objects), `articulation/` (drawers, …), `background/`, `tasks/` (composed task scenes). |
| `environment/fa-project-usd/` → fa-project-usd | Private | Project-specific USD used by internal task scenes. `./init.sh` leaves this unchecked unless you have access. |

robot_usds README: if you use robot_usds **outside** FaSim, put `environment/fiveages_env` next to `robots/` so scene USDs can reference it.

`fa-project-usd` is a private project scene tree, not a public robot model. Product names on this page follow the public robot_usds gallery text.

[Environment assets reference](../../4-reference/simulation/5-env_assets.md).

## Next on the pipeline

With Isaac running and ROS 2 topics/services up, motion and recording talk to the robot through **ros2_robot_interface**, orchestrated by **robot_action_composer**. Continue at [Interface and orchestration](2-orchestration.md).
