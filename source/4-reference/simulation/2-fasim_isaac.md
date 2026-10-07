# FaSim-Isaac

NVIDIA Isaac Sim integration for FiveAges Sim.

**Repository:** [fiveages-sim/FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac)

**README:** [README.md](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/README.md)

## Purpose

FaSim-Isaac is the one-click Isaac asset workspace: it pulls robot USD and scene submodules, can install the Isaac ROS 2 Jazzy overlay, and starts Sim.

## Prerequisites

- NVIDIA Isaac Sim binary (GPU + matching drivers)
- Default path `ISAACSIM_DIR` (`~/isaacsim`); override in `config/fa_sim.local.conf` or the environment

Do not hardcode a single Isaac minor version. `./init.sh` operation 2 queries GitHub stable tags; fallback list in `config/fa_sim.conf` currently `6.0.1` / `6.0.0` / `5.1.0`.

## Installation

:::{code-block} bash
git clone git@github.com:fiveages-sim/FaSim-Isaac.git
cd FaSim-Isaac
./init.sh
./run.sh
:::

What `./init.sh` does:

1. Initialize selected submodules (`.gitmodules` / `submodules_visibility.conf`; public default)
2. Optional Isaac ROS 2 Jazzy workspace (`isaac_jazzy_ws/`). Override version with `ISAAC_SIM_VERSION=… ./init.sh`

What `./run.sh` does: optional CPU governor, optional Zenoh router, then a menu — **PhysX** / **Newton** / **Headless Streaming**. There is no `./run.sh --robot`, `--headless`, or `--env`.

Local config:

:::{code-block} bash
cp config/fa_sim.local.template.conf config/fa_sim.local.conf
# edit ISAACSIM_DIR / ISAAC_SIM_DEFAULT_VERSION
:::

## ROS 2 Connection

In a separate terminal (robot name is a ROS 2 launch argument, not a FaSim flag):

:::{code-block} bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=isaac
:::

## Structure

:::{code-block} none
FaSim-Isaac/
├── init.sh
├── run.sh
├── config/                    # fa_sim.conf + optional fa_sim.local.conf
├── robots/                    # → robot_usds
├── environment/
│   ├── fiveages_env/          # → fiveages-env-usds
│   └── fa-project-usd/        # → fa-project-usd (private)
└── isaac_jazzy_ws/            # created by init.sh operation 2
:::

## Submodules

| Path | Repository | Visibility |
|------|------------|------------|
| `robots/` | robot_usds | Public |
| `environment/fiveages_env/` | fiveages-env-usds | Public |
| `environment/fa-project-usd/` | fa-project-usd | Private |

## Topic Bridge

FaSim-Isaac bridges Isaac Sim to ROS 2:

| Isaac Topic | ROS 2 Topic | Direction |
|-------------|-------------|-----------|
| Joint positions | `/joint_states` | Isaac → ROS |
| Joint commands | `/joint_commands` | ROS → Isaac |

Open robot USD from `robots/` and scene USD from `environment/` in Isaac. Selection is not a `run.sh` CLI flag.

## Troubleshooting

### Isaac Sim Won't Start

1. Confirm `ISAACSIM_DIR` contains `isaac-sim.sh` (and the Newton / streaming launchers named in `fa_sim.conf`)
2. Override the path in `config/fa_sim.local.conf`
3. Check GPU drivers: `nvidia-smi`
4. Check logs: `~/.nvidia-omniverse/logs/`

### No ROS 2 Connection

1. Check domain ID matches
2. Verify ROS 2 bridge extension enabled
3. Restart `./run.sh` and the ROS 2 nodes

## Related

- [robot_usds](3-robot_usds.md)
- [Isaac Sim How-To](../../2-how_to/4-isaac_sim.md)
- [Synthetic Data](../../6-synthetic_data/0-index.md)
