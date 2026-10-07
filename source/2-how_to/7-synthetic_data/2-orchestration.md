# Interface and Orchestration

After the Isaac USD scene is up, datagen does **not** call OCS2 or Nav2 servers from Python by name. YAML `task_queue` blocks resolve to **registered skills**; skills emit **`StageTarget`** sequences and send them through **`ROS2RobotInterface`**.

APIs below are from [robot_action_composer `@ feature/dex-grasp-generator`](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/README.md) and its `docs/`. Do not invent `ActionSequence` / `actions.MoveJ` classes.

## ros2_robot_interface (motion and recording)

**Repository:** [fiveages-sim/ros2_robot_interface](https://github.com/fiveages-sim/ros2_robot_interface)

Composer’s README: the pure motion / queue path depends on **`ROS2RobotInterface`** (`ctx.interface`), not LeRobot’s `ROS2Robot` class. Recording still **moves** the robot through that same interface; the LeRobot plugin is only the episode writer ([next page](3-record_export.md)).

Typical install is the lerobot_ros2 script, not a one-off `pip` on system Python:

:::{code-block} bash
cd lerobot_ros2
./init.sh all-motion    # ros2_robot_interface + robot_action_composer
:::

Reference: [ros2_robot_interface](../../4-reference/python_apps/1-ros2_robot_interface.md), [Python Interface how-to](../3-programming/5-python_interface.md).

## robot_action_composer (task_queue + skills)

**Branch:** [`feature/dex-grasp-generator`](https://github.com/fiveages-sim/robot_action_composer/tree/feature/dex-grasp-generator)

In the lerobot_ros2 monorepo this package is `submodules/robot_action_composer`. Two layers:

| Layer | Job |
|-------|-----|
| **`motion_generation`** | Geometry → `StageTarget` / `ArmTarget` sequences; `execute_stage_sequence` calls `ROS2RobotInterface` (Cartesian, dual-arm, MoveJ, gripper timing). |
| **`task_runtime`** | `runner.run_task_queue`: connect → FSM → optional Isaac reset → each YAML block → `get_skill` → execute. Unknown `skill:` names raise `KeyError` with the registered list. |

YAML lives under `robots/<Robot>/task_configs/**/*.yaml` (optional vendor grouping `robots/<Vendor>/<Robot>/`). Discovery, merge rules, and `robot.yaml`: [TASK_CONFIG_YAML.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/TASK_CONFIG_YAML.md), [ROBOT_CONFIG.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/ROBOT_CONFIG.md).

Skill names (examples from the README index; parameters in [SKILLS_REFERENCE.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/SKILLS_REFERENCE.md)):

| Category | Registered `skill:` names |
|----------|---------------------------|
| Single arm | `single_arm.pick`, `single_arm.place`, `single_arm.move_to_pose`, `single_arm.move_relative`, `single_arm.move_to_object`, `single_arm.goto_cache_pose`, `single_arm.drawer.pull_open`, `single_arm.drawer.close_push` |
| Dual arm | `dual_arm.carry`, `dual_arm.parallel_pick`, `dual_arm.handover`, `dual_arm.place`, `dual_arm.bimanual_align`, `dual_arm.goto_cache_pose` |
| Navigation | `nav.navigate_to_pose`, `nav.navigate_to_object`, `nav.navigate_relative`, `nav.send_nav_goal`, `nav.wait_nav_arrived` |
| Joint / session / env | `joint.movej_to_config`, `joint.goto_cached_joints`, `robot.cache_ee_pose`, `robot.send_mode_command`, `env.randomize_object_local_xyz`, … |

Datagen workspace used in the README is **`examples/IsaacSim`** inside lerobot_ros2 (contains `robots/`). Robot-specific notes, including wheeled-arm **FiveAges W2** dual-arm tasks, are next to those trees (e.g. [`robots/FiveAges_W2/README.md`](https://github.com/fiveages-sim/lerobot_ros2/blob/feature/sim-grasp-datagen/examples/IsaacSim/robots/FiveAges_W2/README.md)).

## Official Nav2, not a custom nav stack

Composer **does not implement Nav2 servers**. `nav.*` skills wrap **`ROS2RobotInterface`’s Nav2 client API**. Scene-level launch is separate from the task YAML.

From [docs/ROS2_STACK.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/ROS2_STACK.md):

- Do **not** put `ros2_stack` inside task-queue YAML.
- Merge: `robot.yaml` → `ros2_stack:` then leaf **`.meta/ros2_stack.yaml`**.
- Motion presets: `ocs2-fullbody` / `ocs2-split-body` / `ocs2-demo` (`ocs2_arm_controller` launches).
- Navigation: `navigation.profile` `default` or `map_only` expands to **`nav2_profile:=…`**. Default launch: `robot_common_launch` / **`navigation/navigation_isaac_gt.launch.py`** (file exists on that repo’s `main`; see [robot-descriptions-common](../../4-reference/descriptions/2-common.md)).
- `navigation.required: auto` starts Nav2 only when the `task_queue` contains `nav.*` skills.

That is the **official Nav2** install/launch already used by the robot workspace, not a fiveages-specific planner.

## CLIs (after `./init.sh`)

Console scripts from composer `pyproject.toml`: `motion-generation`, `ros2-stack`, `grasp-generation`, `check-isaac-pose`, `check-robot-status`.

Run from a directory that contains `robots/` (usually `examples/IsaacSim`):

:::{code-block} bash
cd examples/IsaacSim

# Scene-level OCS2 + Nav2 (background logs under .ros2_stack/<robot>/)
ros2-stack --lang zh launch
ros2-stack status
ros2-stack stop

# Task queue (dry motion; optional --ensure-ros2-stack)
motion-generation
motion-generation --robot dobot_cr5 --task-key pick_place --scene default
motion-generation --robot fiveages_w2 --task-key transfer_blade --ensure-ros2-stack
:::

`grasp-generation serve …` is an optional grasp-setup UI on this branch ([GRASP_GENERATION.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/GRASP_GENERATION.md)); it is **not** the recording entry and is **not** ros2-viser.

Isaac entity pose / joint dump helpers (`check-isaac-pose`, `check-robot-status`) need the sim and `/get_entity_state` as documented in the composer README.

Full CLI flag lists: [robot_action_composer reference](../../4-reference/python_apps/5-robot_action_composer.md).

## Next on the pipeline

Recording is an extra on top of this queue: same YAML `task_queue`, plus LeRobot plugins. Continue at [LeRobot record and export](3-record_export.md).
