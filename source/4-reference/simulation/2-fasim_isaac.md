# FaSim-Isaac

NVIDIA Isaac Sim integration for FiveAges Sim.

**Repository:** [fiveages-sim/FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac)

## Purpose

FaSim-Isaac provides:
- One-click Isaac Sim setup
- USD robot asset management
- ROS 2 Jazzy workspace integration
- Environment assets

## Prerequisites

- NVIDIA GPU (RTX recommended)
- NVIDIA Omniverse Launcher
- Isaac Sim installed

## Installation

```bash
git clone https://github.com/fiveages-sim/FaSim-Isaac.git
cd FaSim-Isaac
./init.sh
```

### init.sh Operations

1. Initialize `robot_usds` submodule
2. Initialize environment submodules
3. Configure Isaac Sim paths
4. Set up optional jazzy_ws

## Usage

### Start Isaac Sim

```bash
./run.sh
```

### With Options

```bash
# Specific robot
./run.sh --robot galbot

# Headless mode
./run.sh --headless
```

### ROS 2 Connection

In separate terminal:

```bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=isaac
```

## Structure

```
FaSim-Isaac/
├── robots/                    # → robot_usds submodule
├── environment/
│   ├── fiveages_env/         # → fiveages-env-usds
│   └── fa-project-usd/       # → fa-project-usd (private)
├── jazzy_ws/                 # Optional ROS 2 workspace
├── init.sh
└── run.sh
```

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

## Configuration

### Robot Selection

Edit config or use command line:

```yaml
# config.yaml
robot: galbot
world: default
```

### Environment

Select environment USD:

```yaml
environment: fiveages_env/office
```

## Troubleshooting

### Isaac Sim Won't Start

1. Check Omniverse Launcher
2. Verify GPU drivers
3. Check logs: `~/.nvidia-omniverse/logs/`

### No ROS 2 Connection

1. Check domain ID matches
2. Verify ROS 2 bridge extension enabled
3. Restart both Isaac and ROS 2 nodes

## Related

- [robot_usds](3-robot_usds.md)
- [Isaac Sim How-To](../../2-how_to/4-isaac_sim.md)
