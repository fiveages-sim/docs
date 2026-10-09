# Workspace Layout

Layout of the **public** deploy workspace, from the [open-deploy-ws README](https://github.com/fiveages-sim/open-deploy-ws/blob/main/README.EN.md). Top-level scripts and config files are those listed in that README (`./init_repo.sh`, `submodules_visibility.conf`, `deb_versions.conf`, and `scripts/`).

## open-deploy-ws

```{admonition} Source of truth
:class: important

Tree and init flow: [README.EN.md](https://github.com/fiveages-sim/open-deploy-ws/blob/main/README.EN.md). The repo root has `init_repo.sh`, `submodules_visibility.conf`, `deb_versions.conf`, and `scripts/` — there is **no** workspace `setup.bash` / env installer besides `./init_repo.sh`.
```

:::{code-block} none
open-deploy-ws/
├── src/
│   ├── arms_ros2_control/     # controllers / commands / hardware interfaces / shared libs
│   ├── robot-descriptions/    # common / manipulator / humanoid (hyphen)
│   └── ocs2_ros2/             # only if that module is installed as source
├── init_repo.sh
├── submodules_visibility.conf
├── deb_versions.conf
└── scripts/                   # install_core_debs.sh, uninstall_core_debs.sh
:::

**Primary path:** `./init_repo.sh` (visibility + per-module `d`/`s`). Do **not** `git submodule update --init --recursive`. After init, `colcon build` (the README does not wrap that). Then `source install/setup.bash` in that workspace — standard ROS 2 overlay, not a FiveAges env script.

Lean robot branches (`dobot-cr5`, `arx-acone`, plus `arx-lift2s` / `panthera-ht` used in the how-tos) clone only that scheme’s packages. See the same README.

## arms_ros2_control (inside `src/`)

From the [arms_ros2_control README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/README.md):

:::{code-block} none
arms_ros2_control/
├── controller/
│   ├── ocs2_arm_controller/
│   ├── ocs2_wbc_controller/      # private nested (visibility conf)
│   ├── adaptive_gripper_controller/
│   └── basic_joint_controller/   # own package README; Home / Hold / MoveJ
├── libraries/                    # ocs2_humanoid (private), …
├── hardwares/                    # topic_based_ros2_control, unitree_ros2_control, …
└── command/                      # msgs, RViz plugin, arms_target_manager, arms_teleop
:::

Nested public/private lines: [Submodules Visibility](6-submodules_visibility.md).

## fa-deploy-ws

Internal workspace (private). Tree and extra flags are in that repository’s README after you have access. Public users stay on `open-deploy-ws`.

## Related

- [Source vs Deb](5-source_vs_deb.md) — `./init_repo.sh` menus 1–4
- [open-deploy-ws setup](../1-getting_started/3-open_deploy_ws.md)
