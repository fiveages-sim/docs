# Synthetic Data

This chapter is the **Isaac Sim datagen pipeline**: USD scenes → ROS 2 interface → task-queue orchestration → LeRobot recording / export.

This How-To category is the Isaac datagen pipeline, not Gazebo or teleop. Reference pages stay the source of APIs; this chapter only explains **how the pieces connect**.

```{admonition} Documented branches
:class: note

- [robot_action_composer](https://github.com/fiveages-sim/robot_action_composer/tree/feature/dex-grasp-generator) `@ feature/dex-grasp-generator`
- [lerobot_ros2](https://github.com/fiveages-sim/lerobot_ros2/tree/feature/sim-grasp-datagen) `@ feature/sim-grasp-datagen`

Those branches are newer than `main`. Follow them, not `main`.
```

```{admonition} Terminology
:class: note

**Humanoid** here means a **wheeled-arm humanoid** (mobile base + arms, e.g. FiveAges W2). It does **not** mean a bipedal or footed humanoid.
```

## Pipeline

:::{code-block} none
FaSim-Isaac + robot_usds (+ env / private USD)
        ↓  Isaac scene, ROS 2 bridge
ros2_robot_interface
        ↓  motion / state / gripper / Nav2 client
robot_action_composer  (task_queue YAML + skills)
        ↓  StageTarget sequences via ROS2RobotInterface
lerobot_ros2  (record_datasets.py → LeRobot dataset on disk)
:::

| Stage | Role in datagen | Start here |
|-------|-----------------|------------|
| **FaSim-Isaac** | Isaac Sim line for synthetic scenes. Scripts pull USD and start Sim. | [Isaac scenes and USD](1-isaac_scenes.md) |
| **robot_usds** | Robot USD superproject used by FaSim (`robots/`). | same page |
| **ros2_robot_interface** | Python interface used by motion **and** recording. | [Interface and orchestration](2-orchestration.md) |
| **robot_action_composer** | `task_queue` YAML + skill registry; `motion-generation` / `ros2-stack`. | same page |
| **lerobot_ros2** | Monorepo that hosts the Isaac example workspace and recording plugins. Stop at **record / export**. | [LeRobot record and export](3-record_export.md) |

## In this section

```{toctree}
:maxdepth: 1

1-isaac_scenes
2-orchestration
3-record_export
```

## Baseline

- **ROS 2 Jazzy**
- **Python 3.12** (same baseline as the lerobot_ros2 / composer READMEs on those branches)

## Out of scope

This chapter does **not** cover:

- Gazebo
- ros2-viser or fa-py-libraries
- Policy **training**, online **inference**, or dataset consumption (`examples/IsaacSim/policy_training/train.py`, `inference.py`)

Package-level APIs: [ros2_robot_interface](../../4-reference/python_apps/1-ros2_robot_interface.md), [robot_action_composer](../../4-reference/python_apps/5-robot_action_composer.md), [lerobot_ros2](../../4-reference/python_apps/4-lerobot_ros2.md), [FaSim-Isaac](../../4-reference/simulation/2-fasim_isaac.md), [robot_usds](../../4-reference/simulation/3-robot_usds.md).
