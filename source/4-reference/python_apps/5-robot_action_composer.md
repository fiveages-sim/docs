# robot_action_composer

Motion generation and **task_queue** YAML orchestration: a skill registry turns YAML blocks into **`StageTarget`** sequences and runs them through **`ROS2RobotInterface`**. Optional LeRobot dataset recording is an extra, not the core path.

```{admonition} Documented branch
:class: note

Documented against branch `feature/dex-grasp-generator` (tip 2026-09-20). That branch is newer than `main`; follow it, not `main`.
```

**Repository:** [fiveages-sim/robot_action_composer @ `feature/dex-grasp-generator`](https://github.com/fiveages-sim/robot_action_composer/tree/feature/dex-grasp-generator)

**README:** [README.md on this branch](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/README.md)

There is no `ActionSequence` / `actions.MoveJ` / `CustomAction` API. Skills are **registered names** in YAML (`task_queue` → `skill`). Full parameter docs: [docs/SKILLS_REFERENCE.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/SKILLS_REFERENCE.md).

## Purpose

In the [lerobot_ros2](4-lerobot_ros2.md) monorepo this package:

- **Motion layer (`motion_generation`)** — turns task geometry and robot constraints into `StageTarget` sequences and executes them via `ROS2RobotInterface` (Cartesian, dual-arm sync, MoveJ, and so on).
- **Orchestration layer (`task_runtime`)** — runs a `task_queue` (YAML block list) through the skill registry and runtime context; merges `skill_defaults` / `skill_params`.
- **Around the edges** — Isaac Sim entity poses, sim reset, optional LeRobot recording.

It does **not** implement OCS2 / MPC or the Nav2 servers themselves; those stay behind existing ROS 2 interfaces. Pure motion/queue paths depend on `ROS2RobotInterface` (`ctx.interface`), not the LeRobot `ROS2Robot` class.

## Requirements

Same baseline as the lerobot_ros2 monorepo README:

- **Python 3.12**
- **ROS 2 Jazzy**, with the matching `install/setup.bash` (or overlay) sourced so `rclpy` comes from that distro

## Installation

Typical path is from a **lerobot_ros2** checkout (composer is `submodules/robot_action_composer`):

:::{code-block} bash
./init.sh all-motion          # interface + robot_action_composer
./init.sh install-lerobot     # extra: PyTorch + lerobot + plugins (record / infer)
# or once: ./init.sh all
:::

`./init.sh all-motion` creates the env and installs the two local packages. Optional extras named in composer `pyproject.toml`: `[recording]` (LeRobot / `lerobot_robot_ros2`), `[grasp]` (`viser>=0.2` for grasp-generation UI). That extra is not the fa-py-libraries `./run.sh viser` launcher.

Console scripts after install: `motion-generation`, `ros2-stack`, `grasp-generation`, `check-isaac-pose`, `check-robot-status`.

:::{admonition} Manual fallback
:class: note

From the monorepo root, after the env is active. Prefer **uv** and **`--no-deps`** so install does not pull `rclpy` from PyPI. The composer README also shows `pip install -e submodules/ros2_robot_interface` then `pip install -e submodules/robot_action_composer` inside the project venv only (system `pip` hits PEP 668).

:::{code-block} bash
uv pip install -e submodules/ros2_robot_interface --no-deps
uv pip install -e submodules/robot_action_composer --no-deps
uv pip install "viser>=0.2"   # optional; grasp-generation UI
:::
:::

## Layers

**`motion_generation`** — what each motion segment looks like and how it is sent.

- `sequence/` — `StageTarget` / `ArmTarget` / `ArmStage`, builders such as `build_single_arm_pick_sequence`, and `execute_stage_sequence` (calls `ROS2RobotInterface`, wait-for-arrival, gripper timing).
- `tasks/` — geometry wrappers on top of that (handover, bimanual carry, parallel pick, drawer, pick/place, MoveJ return used by dataset recording).

**`task_runtime`** — which skills run, in what order, with which merged params.

- `runner.run_task_queue` — connect → FSM → optional env reset → `QueueRuntimeContext` → each `task_queue` block (`ParallelSpec` allowed) → `get_skill` → `execute_stage_sequence`.
- `registry.py` — `register_skill(name, fn)` / `get_skill(name)`; unknown names raise `KeyError` listing registered skills.
- Each skill: `(ctx, params) -> (list[StageTarget], ExecutionMeta)`. Blocks with no Cartesian stages return an empty list (pure nav, pure MoveJ, side-effect-only).

YAML discovery scans `task_configs/**/*.yaml` and `robots/*/` (optional vendor grouping `robots/<Vendor>/<Robot>/`). See [docs/TASK_CONFIG_YAML.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/TASK_CONFIG_YAML.md) and [docs/ROBOT_CONFIG.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/ROBOT_CONFIG.md).

## Skills (registered names)

Do not invent a Python `MoveJ` / `GripperOpen` action class. YAML blocks set `skill:` to a **registered name**. Categories (examples from the README index; parameters live in SKILLS_REFERENCE):

| Category | Example skills |
|----------|----------------|
| Single arm | `single_arm.pick`, `single_arm.place`, `single_arm.move_to_pose`, `single_arm.move_relative`, `single_arm.move_to_object`, `single_arm.goto_cache_pose`, `single_arm.drawer.pull_open`, `single_arm.drawer.close_push` |
| Dual arm | `dual_arm.carry`, `dual_arm.parallel_pick`, `dual_arm.handover`, `dual_arm.place`, `dual_arm.bimanual_align`, `dual_arm.goto_cache_pose` |
| Navigation | `nav.navigate_to_pose`, `nav.navigate_to_object`, `nav.navigate_relative`, `nav.send_nav_goal`, `nav.wait_nav_arrived` |
| Joint | `joint.movej_to_config`, `joint.goto_cached_joints` |
| Session / robot / env | `session.scratch_put`, `robot.cache_ee_pose`, `robot.cache_joint_state`, `robot.send_mode_command`, `env.randomize_object_local_xyz` |

Full list, defaults, and YAML examples: [docs/SKILLS_REFERENCE.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/SKILLS_REFERENCE.md).

## CLI pointers

Run from a workspace that contains `robots/` (the README uses `examples/IsaacSim` in the lerobot_ros2 tree). Flags below are from the composer README; see that file for the full set.

:::{code-block} bash
# Task queue
motion-generation
motion-generation --robot dobot_cr5 --task-key pick_place --scene default
motion-generation --workspace /path/to/workspace --robot dobot_cr5 --task-key pick_place
motion-generation --lang zh
motion-generation --robot fiveages_w2 --task-key transfer_blade --ensure-ros2-stack

# ROS 2 stack (see docs/ROS2_STACK.md)
ros2-stack --lang zh launch
ros2-stack logs --robot fiveages_w2 -f
ros2-stack stop --robot fiveages_w2
ros2-stack status --robot fiveages_w2 --group "projets/siemens/Wind turbo blade"

# Grasp generation UI (does not replace the two CLIs above)
grasp-generation serve --robot fiveages_w2 --workspace examples/IsaacSim

# Isaac Sim entity pose (needs /get_entity_state)
check-isaac-pose /World/robot/FiveAges_W2/LinkHou_S2/base_footprint/base_link
check-isaac-pose /World/scene/boxes/white_box_05 \
  --relative-to /World/robot/FiveAges_W2/LinkHou_S2/base_footprint/base_link

# Current joints / EE pose (pasteable into YAML)
check-robot-status
check-robot-status --robot fiveages_w2 --workspace examples/IsaacSim
check-robot-status --wait 3.0 --show-joint-names
:::

`motion-generation` default `workspace_dir` is the current working directory. Language: `--lang` > `MOTION_GENERATION_LANG` > `.motion_last.json` > system `LANG`. Preferences such as `ensure_ros2_stack` are stored in workspace-root `.motion_last.json` (gitignored).

## In-repo docs (this branch)

Do not treat this Sphinx page as a substitute for the package docs:

| Doc | Content |
|-----|---------|
| [docs/SKILLS_REFERENCE.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/SKILLS_REFERENCE.md) | Per-skill parameters, defaults, YAML examples |
| [docs/TASK_CONFIG_YAML.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/TASK_CONFIG_YAML.md) | Task YAML shape, `skill_defaults` / `skill_params`, load/merge |
| [docs/ROBOT_CONFIG.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/ROBOT_CONFIG.md) | `robot.yaml` / `lerobot_config.py` and `robots/` layout |
| [docs/ROS2_STACK.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/ROS2_STACK.md) | Scene-level control/nav launch (`.meta/ros2_stack.yaml`, `ros2-stack`) |
| [docs/GRASP_GENERATION.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/GRASP_GENERATION.md) | Grasp-generation UI and smoke |

Isaac Sim env / USD / workspace steps, when present, are in the monorepo `examples/IsaacSim/README.md`.

## Related

- [lerobot_ros2](4-lerobot_ros2.md)
- [ros2_robot_interface](1-ros2_robot_interface.md)
- [Python Interface How-To](../../2-how_to/5-python_interface.md)
- [Synthetic Data](../../6-synthetic_data/0-index.md) — pipeline story for Isaac datagen
