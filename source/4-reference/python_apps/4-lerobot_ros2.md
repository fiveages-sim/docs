# lerobot_ros2

LeRobot ↔ ROS 2 integration monorepo. LeRobot talks to the robot over ROS 2 topics.

**Repository:** [fiveages-sim/lerobot_ros2](https://github.com/fiveages-sim/lerobot_ros2) `main` (`f750af76`). `feature/sim-grasp-datagen` was merged in [#10](https://github.com/fiveages-sim/lerobot_ros2/pull/10) (`147ea78d`, 2026-10-23) and is no longer a branch.

**README:** [README.md](https://github.com/fiveages-sim/lerobot_ros2/blob/main/README.md)

## Purpose

This checkout is a monorepo, not a single `pip install -e .` package. It wires:

- `submodules/ros2_robot_interface` — ROS 2 robot interface
- `submodules/robot_action_composer` — task-queue YAML and motion generation (see [robot_action_composer](5-robot_action_composer.md))
- `lerobot_robot_ros2` — LeRobot ROS 2 robot plugin (`ROS2Robot` / `ROS2RobotConfig` / `ROS2RobotInterfaceConfig`)
- `lerobot_camera_ros2` — LeRobot ROS 2 camera plugin

The LeRobot core library is installed from PyPI. The default pin is `lerobot==0.5.1` in `.fa-env.toml` (first created from [`.fa-env.toml.example`](https://github.com/fiveages-sim/lerobot_ros2/blob/main/.fa-env.toml.example)).

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
| `./init.sh all-motion` | Submodules + env + `ros2_robot_interface` + `robot_action_composer`. NumPy stays 1.x |
| `./init.sh all-grasp` | `all-motion` plus dex submodules, `install-grasp` (`viser`, `wuji-sdk`), and the HUG env. NumPy stays 1.x |
| `./init.sh install-lerobot` | PyTorch + PyPI `lerobot` + `lerobot_robot_ros2` / `lerobot_camera_ros2`. Upgrades NumPy to 2 |
| `./init.sh all` | Submodules + env + orchestration + LeRobot plugins (NumPy 2) |
| `./init.sh set-backend uv` | Write `backend` in `.fa-env.toml` (`uv` or `conda`) |

Orchestration and dexterous grasp share one environment on NumPy 1.x so they match ROS 2’s system OpenCV / `cv_bridge`. Recording and policy inference install NumPy 2 for `lerobot` 0.5. Use a separate environment for that step. `./init.sh install-lerobot` in the grasp environment upgrades NumPy and then head-camera capture through `cv_bridge` no longer matches the system build. Dexterous grasp is optional (the reference robot is FiveAges W2 with Wuji Hand2). A robot without that grasp config still runs `all-motion`.

Optional submodules in [`.gitmodules`](https://github.com/fiveages-sim/lerobot_ros2/blob/main/.gitmodules): [HUG](https://github.com/fiveages-sim/HUG) (private; Python 3.10 env under `submodules/hug/.venv`), [wuji-retargeting](https://github.com/fiveages-sim/wuji-retargeting), [internnav_w2](https://github.com/fiveages-sim/internnav_w2), [internnav_arx_lift2s](https://github.com/fiveages-sim/internnav_arx_lift2s), [LightNav-0_W2](https://github.com/fiveages-sim/LightNav-0_W2). `internnav_w2` and `LightNav-0_W2` need access. Runtime retargeting installs PyPI `wuji-sdk` (`./init.sh install-grasp`); do not recurse into the nested MuJoCo repos inside `wuji-retargeting`.

Runtime config lives in local `.fa-env.toml` (gitignored; copied from the example). Keys documented in the README:

| Key | Meaning |
|-----|---------|
| `backend` | `uv` or `conda` |
| `[conda].name` | Conda env name (default `lerobot-ros2`) |
| `[uv].venv` | uv venv path (default `.venv`) |
| `[lerobot].version` | PyPI LeRobot version (default `0.5.1`) |
| `[ros2].workspace` | ROS 2 workspace; sourced when the env is activated |

Personal overrides: `.fa-env.local.toml`. Env notes: [docs/ENV_THIS_CHECKOUT.md](https://github.com/fiveages-sim/lerobot_ros2/blob/main/docs/ENV_THIS_CHECKOUT.md). Use `uv pip` inside this checkout's `.venv`, not system `pip` (PEP 668). Do not install `ros2-stack` / `grasp-generation` into `submodules/hug/.venv` (HUG's Python 3.10 env).

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

More examples are under `examples/`. `lerobot_robot_ros2` depends on the local `ros2-robot-interface` install (`submodules/ros2_robot_interface` first).

## Isaac workspace

Shared steps: [`examples/IsaacSim/README.md`](https://github.com/fiveages-sim/lerobot_ros2/blob/main/examples/IsaacSim/README.md). That README still lists Isaac Sim 6.0. FaSim `config/fa_sim.conf` is the version menu for this stack (fallback `6.2.0` / `6.1.0` / `6.0.1`).

`motion-generation` runs in any directory that contains `robots/` or a project `robot.yaml`. A [fa-project-usd](https://github.com/fiveages-sim/fa-project-usd) project directory (private; needs access) can be that workspace when `LEROBOT_ROOT` points at this checkout and `robot.yaml` `extends` a profile under `examples/IsaacSim/robots/`. The public example in that README is:

:::{code-block} bash
export LEROBOT_ROOT=/path/to/lerobot_ros2
cd "/path/to/fa-project-usd/Aimbo/2026-04 Bosch German&Poland POC"
motion-generation --robot fiveages_w2 --task-key poc_port4_bimanual_carry
:::

`ros2-stack`, `check-robot-status`, and `record_datasets.py --workspace <project>` take the same directory. Orchestration files beside those scenes (`robot.yaml`, `task_configs/`, `maps/` or `map/`) are on `fa-project-usd` branch `feature/sinopec-test-tube-picking`, which is ahead of that repo’s `main`.

Public G1D profile [`examples/IsaacSim/robots/Unitree/G1D/robot.yaml`](https://github.com/fiveages-sim/lerobot_ros2/blob/main/examples/IsaacSim/robots/Unitree/G1D/robot.yaml): `ee_target_frame` is `{arm}_eef`, `ee_command_frame` is `{arm}_tcp`, and there is no `ee_tip`. `ros2_stack.motion.required` is `false` with `args.hardware: isaac`, because the scene USD already starts in-process control on Play. That YAML `hardware: isaac` is the composer stack preset. It is not the in-process plugin name `isaac_sim`. Leaving `required: true` would start a second controller manager.

## Camera plugin

`lerobot_camera_ros2` defaults to **manual image conversion** (no `cv_bridge`) so it can run with `lerobot==0.5.1` and numpy 2.x. If `cv_bridge` is usable it may be selected automatically. Force the manual path with:

:::{code-block} bash
export LEROBOT_ROS2_DISABLE_CV_BRIDGE=1
:::

The uv path also expects system `ffmpeg` (for example `sudo apt install ffmpeg`). `install-plugins` additionally installs `scipy>=1.14` so `--system-site-packages` does not pick up a system SciPy that is incompatible with numpy 2.x.

## In-repo docs (`main`)

| Doc | Role |
|-----|------|
| [docs/ENV_THIS_CHECKOUT.md](https://github.com/fiveages-sim/lerobot_ros2/blob/main/docs/ENV_THIS_CHECKOUT.md) | Develop and install only in this checkout's env |
| [docs/HUG_SUBMODULE.md](https://github.com/fiveages-sim/lerobot_ros2/blob/main/docs/HUG_SUBMODULE.md) | HUG submodule notes |
| [docs/WUJI_RETARGETING.md](https://github.com/fiveages-sim/lerobot_ros2/blob/main/docs/WUJI_RETARGETING.md) | Wuji retargeting |
| Composer [GRASP_GENERATION.md](https://github.com/fiveages-sim/robot_action_composer/blob/main/docs/GRASP_GENERATION.md) | Motion + grasp smoke (linked from the lerobot README) |

Sim-grasp handoff / EE-align notes also live under `docs/SIM_GRASP_*.md`. Nav deploy notes: `docs/INTERNAV_W2_SUBMODULE.md`, `docs/INTERNAV_ARX_LIFT2S_SUBMODULE.md`, `docs/LIGHTNAV_W2_SUBMODULE.md`.

## Related

- [ros2_robot_interface](1-ros2_robot_interface.md)
- [robot_action_composer](5-robot_action_composer.md)
- [Synthetic Data](../../2-how_to/7-synthetic_data/0-index.md) — record/export only (no training)
- [HUG](6-hug.md)
- [wuji-retargeting](7-wuji_retargeting.md)
