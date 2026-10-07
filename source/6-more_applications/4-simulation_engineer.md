# Simulation engineer

For engineers who import sim assets, configure a robot in this stack, and compose motions in Isaac (not Gazebo-only beginners).

## 1. Isaac line and USD assets

1. [Isaac Sim](../2-how_to/2-simulation/4-isaac_sim.md) — FaSim-Isaac `./init.sh` then `./run.sh`; ROS 2 side `hardware:=isaac`.
2. [Isaac Scenes and USD](../2-how_to/7-synthetic_data/1-isaac_scenes.md) — how FaSim pulls [robot_usds](../4-reference/simulation/3-robot_usds.md).
3. [robot_usds](../4-reference/simulation/3-robot_usds.md) and [USD submodules](../4-reference/simulation/4-usd_submodules.md) — brand folders, public vs private trees.
4. Environment assets: [env assets](../4-reference/simulation/5-env_assets.md) when the scene needs more than the robot.

Gazebo (different backend): [Gazebo Simulation](../2-how_to/2-simulation/3-gazebo_sim.md), [Gazebo reference](../4-reference/simulation/1-gazebo.md). There is **no** `hardware:=mock`; keys are `mock_components` / `gz` / `isaac` / `real`.

## 2. Robot configuration

1. [Switch Robot](../2-how_to/1-basic_operations/2-switch_robot.md) — `robot:=` and EEF `type` / `left_type` / `right_type`.
2. [robot_common_launch](../4-reference/descriptions/2-common.md) — launch args, machine profile, merge order.
3. [Naming Conventions](../3-concepts/3-naming_conventions.md).
4. [Add a Robot](../2-how_to/6-deployment/10-add_a_robot.md) — copy a real description package; use the plugin class from that robot’s `xacro/ros2_control/*.xacro`.
5. Brand packages: [Brand Packages (Public)](../4-reference/descriptions/3-brand_public.md). FiveAges wheeled-arm gitlinks: [FiveAges descriptions](../4-reference/descriptions/4-fiveages_umbrella.md).

## 3. Action composition / orchestration

Isaac datagen motions are **task_queue YAML skills**, not a Python `ActionSequence` API.

1. [Synthetic Data](../2-how_to/7-synthetic_data/0-index.md) — pipeline map.
2. [Interface and Orchestration](../2-how_to/7-synthetic_data/2-orchestration.md) — `./init.sh all-motion`, `motion-generation`, `ros2-stack`.
3. [robot_action_composer](../4-reference/python_apps/5-robot_action_composer.md) — documented branch `feature/dex-grasp-generator`; skill names and flags on that README / `docs/`.

Composer `--robot fiveages_w2` is a real key on composer `ROS2_STACK.md`. It is **not** an `./init_repo.sh --robot` flag.

## Related

- [FaSim-Isaac](../4-reference/simulation/2-fasim_isaac.md)
- [ros2_control here](../3-concepts/1-ros2_control_here.md)
- [LeRobot Record and Export](../2-how_to/7-synthetic_data/3-record_export.md) — stop at the dataset
