# LeRobot Record and Export

This page stops at **LeRobot dataset recording / export**. It does not document training, online inference, or how a policy consumes the dataset.

**Monorepo:** [lerobot_ros2 `@ feature/sim-grasp-datagen`](https://github.com/fiveages-sim/lerobot_ros2/tree/feature/sim-grasp-datagen)

**README:** [README.md on that branch](https://github.com/fiveages-sim/lerobot_ros2/blob/feature/sim-grasp-datagen/README.md)

Isaac-side shared steps: [`examples/IsaacSim/README.md`](https://github.com/fiveages-sim/lerobot_ros2/blob/feature/sim-grasp-datagen/examples/IsaacSim/README.md).

## What recording uses

| Piece | Role |
|-------|------|
| `submodules/ros2_robot_interface` | Motion / state while an episode runs (`robot.ros2_interface`) |
| `submodules/robot_action_composer` | Same `task_queue` skills as dry `motion-generation`; package `dataset_recording` + `cli.record_main` |
| `lerobot_robot_ros2` | LeRobot robot plugin (`ROS2Robot`) that **writes frames** |
| `lerobot_camera_ros2` | Camera plugin (images for the dataset) |
| PyPI `lerobot` | Dataset container (`LeRobotDataset.create` / `add_frame` / `save_episode`). Default pin `lerobot==0.5.1` in `.fa-env.toml` |

Composer `pyproject.toml` extra `[recording]` is `lerobot` + `lerobot-robot-ros2`. Motion/queue does **not** need it; recording does.

`examples/IsaacSim/record_datasets.py` is a thin wrapper: it calls `robot_action_composer.cli.record_main.run_record_datasets` with `isaac_dir` set to that folder.

## Install (scripts first)

From the lerobot_ros2 README. **Python 3.12**, ROS 2 Jazzy, [uv](https://docs.astral.sh/uv/) recommended.

:::{code-block} bash
git clone --recursive git@github.com:fiveages-sim/lerobot_ros2.git
cd lerobot_ros2
./init.sh all
# motion / task queue only:     ./init.sh all-motion
# recording plugins (if you skipped all):  ./init.sh install-lerobot
source .venv/bin/activate
:::

`./init.sh all` = submodules + env + task orchestration + LeRobot plugins. Bare `pip install -e .` at the repo root is not the install path.

Isaac example README also lists `./init.sh install-plugins` for this checkout. Use the **lerobot_ros2** `./init.sh`, not a handwritten PyPI `rclpy` install.

## Before you record

1. Isaac scene running ([Isaac scenes and USD](1-isaac_scenes.md)).
2. ROS 2 control + (if the task has `nav.*`) official Nav2 via `ros2-stack` ([orchestration](2-orchestration.md)).
3. Example README: Isaac ROS 2 **simulation state** and **prim** services enabled so reset / object pose work.
4. Task YAML must include a non-empty **`task_queue`** (the recorder raises otherwise).

## Record

There is **no** `record-datasets` console script in composer `pyproject.toml`. The documented entry is the example wrapper:

:::{code-block} bash
cd examples/IsaacSim
python record_datasets.py
:::

Interactive prompts (from `record_main` / `dataset_recording.launcher` on this branch):

- Robot (registry under `examples/IsaacSim/robots`; default `dobot_cr5` if present)
- Task folder / task (`task_key`)
- Scene preset when the YAML has `scene_presets`
- Record profile
- Episode count
- Optional depth+pointcloud at keypoints (only if `lerobot_config.py` has depth topics)
- Optional manual review after return-to-home

Per-robot `lerobot_config.py` (`LEROBOT_CFG`) is the LeRobot side of the split documented in [ROBOT_CONFIG.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/ROBOT_CONFIG.md); `robot.yaml` stays the motion/stack side.

## Export (what lands on disk)

On this branch the runner creates a local LeRobot dataset:

:::{code-block} none
<cwd>/lerobot_dataset/grasp_record_<unix_time>/
:::

via `LeRobotDataset.create` (`repo_id` = that path, `use_videos=True`, fps from the record profile). Episodes are `dataset.add_frame` then `dataset.save_episode`. That **is** the export this chapter covers. Do not assume a Hugging Face upload CLI unless a README on this branch says so.

## Stop here

Not in this chapter (they exist on the branch; use the example README if you need them later):

- `examples/IsaacSim/policy_training/train.py`
- `examples/IsaacSim/inference.py` / `online_infer/`

Package pages: [lerobot_ros2](../4-reference/python_apps/4-lerobot_ros2.md), [robot_action_composer](../4-reference/python_apps/5-robot_action_composer.md).
