# lerobot_ros2

LeRobot ↔ ROS 2 integration monorepo. LeRobot talks to the robot over ROS 2 topics.

```{admonition} Documented branch
:class: note

Documented against branch `feature/sim-grasp-datagen` (tip 2026-09-20). That branch is newer than `main`; follow it, not `main`.
```

**Repository:** [fiveages-sim/lerobot_ros2 @ `feature/sim-grasp-datagen`](https://github.com/fiveages-sim/lerobot_ros2/tree/feature/sim-grasp-datagen)

**README:** [README.md on this branch](https://github.com/fiveages-sim/lerobot_ros2/blob/feature/sim-grasp-datagen/README.md)

## Purpose

This checkout is a monorepo, not a single `pip install -e .` package. It wires:

- `submodules/ros2_robot_interface` — ROS 2 robot interface
- `submodules/robot_action_composer` — task-queue YAML and motion generation (see [robot_action_composer](5-robot_action_composer.md))
- `lerobot_robot_ros2` — LeRobot ROS 2 robot plugin (`ROS2Robot` / `ROS2RobotConfig` / `ROS2RobotInterfaceConfig`)
- `lerobot_camera_ros2` — LeRobot ROS 2 camera plugin

The LeRobot core library is installed from PyPI. The default pin is `lerobot==0.5.1` in `.fa-env.toml` (first created from [`.fa-env.toml.example`](https://github.com/fiveages-sim/lerobot_ros2/blob/feature/sim-grasp-datagen/.fa-env.toml.example)).

## Requirements

- ROS 2 (tested: **Jazzy**)
- **Python 3.12**
- [uv](https://docs.astral.sh/uv/) (recommended) or Conda

## Installation

Clone with submodules, then use `init.sh`. Do **not** treat `pip install -e .` at the repo root as the install path.

:::{code-block} bash
git clone --recursive git@github.com:fiveages-sim/lerobot_ros2.git
cd lerobot_ros2

# uv if needed: curl -LsSf https://astral.sh/uv/install.sh | sh

./init.sh all
# motion / task queue only (no LeRobot):  ./init.sh all-motion
# recording / inference plugins:          ./init.sh install-lerobot
source .venv/bin/activate   # default backend=uv
:::

`./init.sh` with no arguments opens an interactive menu (submodules, env, install, backend, ROS 2 workspace). Useful non-interactive commands from the README:

| Command | What it does |
|---------|----------------|
| `./init.sh all` | Submodules + env + task orchestration + LeRobot plugins |
| `./init.sh all-motion` | Submodules + env + `ros2_robot_interface` + `robot_action_composer` only |
| `./init.sh install-lerobot` | PyTorch + PyPI `lerobot` + `lerobot_robot_ros2` / `lerobot_camera_ros2` |
| `./init.sh set-backend uv` | Write `backend` in `.fa-env.toml` (`uv` or `conda`) |

Runtime config lives in local `.fa-env.toml` (gitignored; copied from the example). Keys documented in the README:

| Key | Meaning |
|-----|---------|
| `backend` | `uv` or `conda` |
| `[conda].name` | Conda env name (default `lerobot-ros2`) |
| `[uv].venv` | uv venv path (default `.venv`) |
| `[lerobot].version` | PyPI LeRobot version (default `0.5.1`) |
| `[ros2].workspace` | ROS 2 workspace; sourced when the env is activated |

Personal overrides: `.fa-env.local.toml`. Env notes: [docs/ENV_THIS_CHECKOUT.md](https://github.com/fiveages-sim/lerobot_ros2/blob/feature/sim-grasp-datagen/docs/ENV_THIS_CHECKOUT.md). Use `uv pip` inside this checkout's `.venv`, not system `pip` (PEP 668). Do not install `ros2-stack` / `grasp-generation` into `submodules/hug/.venv` (HUG's Python 3.10 env).

:::{admonition} Manual fallback
:class: note

Skip `init.sh` only if you must. The README uv path: create `.venv` with `--system-site-packages`, then install local packages with **`--no-deps`** so pip does not fetch `rclpy` from PyPI. ROS Python packages come from the sourced Jazzy overlay.

:::{code-block} bash
git clone --recursive git@github.com:fiveages-sim/lerobot_ros2.git
cd lerobot_ros2
git submodule update --init --recursive

uv venv --python python3.12 --system-site-packages .venv
source .venv/bin/activate

uv pip install torch==2.7.1 torchvision==0.22.1 torchaudio==2.7.1 \
  --index-url https://download.pytorch.org/whl/cu128
uv pip install "lerobot==0.5.1"

uv pip install -e submodules/ros2_robot_interface --no-deps
uv pip install numpy pyyaml
uv pip install -e submodules/robot_action_composer --no-deps
uv pip install "viser>=0.2"   # optional grasp-generation UI (PyPI viser, not ros2-viser launch)
uv pip install -e lerobot_robot_ros2 --no-deps
uv pip install -e lerobot_camera_ros2 --no-deps
:::
:::

## Usage: `ROS2Robot`

The public robot plugin is `lerobot_robot_ros2`, not a root package named `lerobot_ros2`. Example from the README:

:::{code-block} python
from lerobot_robot_ros2 import ROS2Robot, ROS2RobotConfig, ROS2RobotInterfaceConfig

config = ROS2RobotConfig(
    id="my_robot",
    ros2_interface=ROS2RobotInterfaceConfig(
        joint_states_topic="/joint_states",
        end_effector_pose_topic="/left_current_pose",
        end_effector_target_topic="/left_target",
    ),
)

robot = ROS2Robot(config)
robot.connect()
# ...
robot.disconnect()
:::

More examples are under `examples/` on this branch. `lerobot_robot_ros2` depends on the local `ros2-robot-interface` install (`submodules/ros2_robot_interface` first).

## Camera plugin

`lerobot_camera_ros2` defaults to **manual image conversion** (no `cv_bridge`) so it can run with `lerobot==0.5.1` and numpy 2.x. If `cv_bridge` is usable it may be selected automatically. Force the manual path with:

:::{code-block} bash
export LEROBOT_ROS2_DISABLE_CV_BRIDGE=1
:::

The uv path also expects system `ffmpeg` (for example `sudo apt install ffmpeg`). `install-plugins` additionally installs `scipy>=1.14` so `--system-site-packages` does not pick up a system SciPy that is incompatible with numpy 2.x.

## In-repo docs (this branch)

| Doc | Role |
|-----|------|
| [docs/ENV_THIS_CHECKOUT.md](https://github.com/fiveages-sim/lerobot_ros2/blob/feature/sim-grasp-datagen/docs/ENV_THIS_CHECKOUT.md) | Develop and install only in this checkout's env |
| [docs/HUG_SUBMODULE.md](https://github.com/fiveages-sim/lerobot_ros2/blob/feature/sim-grasp-datagen/docs/HUG_SUBMODULE.md) | HUG submodule notes |
| [docs/WUJI_RETARGETING.md](https://github.com/fiveages-sim/lerobot_ros2/blob/feature/sim-grasp-datagen/docs/WUJI_RETARGETING.md) | Wuji retargeting |
| Composer [GRASP_GENERATION.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/GRASP_GENERATION.md) | Motion + grasp smoke (linked from the lerobot README) |

Sim-grasp handoff / EE-align notes also live under `docs/SIM_GRASP_*.md` on this branch.

## Related

- [ros2_robot_interface](1-ros2_robot_interface.md)
- [robot_action_composer](5-robot_action_composer.md)
- [Synthetic Data](../../6-synthetic_data/0-index.md) — record/export only (no training)
- [HUG](6-hug.md)
- [wuji-retargeting](7-wuji_retargeting.md)
