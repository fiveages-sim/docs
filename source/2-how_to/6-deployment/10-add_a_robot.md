# Add a Robot

How a new robot enters this stack. Copy an **existing** description package and the launch/xacro patterns already in the repo. Do not invent package trees, `hardware:=mock`, MPC horizon YAML, or a `display.launch.py` that no package README lists.

```{admonition} Source of truth
:class: important

- Description layout: an existing `{robot}_description` package (example below: [arx_acone_description](https://github.com/fiveages-sim/robot-descriptions-arx/tree/main/arx_acone_description)) and its package README
- Umbrella + submodule paths: [robot_descriptions README](https://github.com/fiveages-sim/robot_descriptions/blob/main/README.md) (e.g. ARX at `manipulator/ARX`)
- Launch / `hardware:=` / EEF: [robot_common_launch](../../4-reference/descriptions/2-common.md)
- Workspace init: `./init_repo.sh` in [open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws/blob/main/README.EN.md) + [`submodules_visibility.conf`](https://github.com/fiveages-sim/open-deploy-ws/blob/main/submodules_visibility.conf)
- Isaac USD: FaSim-Isaac skill **`isaac-urdf-usda-ocs2`** (folder `USDA-OCS2-PhysX-Mujoco`) — [skill](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/.cursor/skills/USDA-OCS2-PhysX-Mujoco/SKILL.md) — plus `./init.sh` / `./run.sh` and [robot_usds](https://github.com/fiveages-sim/robot_usds/blob/main/README.md)

**No `.cursor/skills` was found** on `main` for `robot_descriptions`, `robot-descriptions-common`, or `robot_usds`. Use those READMEs plus the FaSim-Isaac skills. Do not invent a description-side skill.
```

## 1. ROS description package

Public brand trees live as submodules under [robot_descriptions](https://github.com/fiveages-sim/robot_descriptions) (`common`, `manipulator/ARX`, `manipulator/Dobot`, …). In `open-deploy-ws` the same tree is `src/robot-descriptions/` after **`./init_repo.sh`**. Do not recursive-init.

Copy a real package. Acone (from that repo) looks like:

:::{code-block} none
arx_acone_description/
├── CMakeLists.txt
├── package.xml
├── README.md
├── xacro/
│   ├── robot.xacro
│   ├── arm_mount.xacro
│   ├── component.xacro
│   └── ros2_control/          # hardware plugin branches
├── config/
│   ├── ocs2/                  # task .info (not an invented ocs2_arm_config.yaml)
│   └── ros2_control/          # optional {hardware}.yaml overlay
└── meshes/
:::

Launch key is `robot:=<key>` where the package is `{key}_description` ([robot_common_launch](../../4-reference/descriptions/2-common.md)). `demo.launch.py` default is `cr5`.

`hardware:=` values that exist in Acone xacro / common launch: `mock_components` (default), `gz`, `isaac`, `real`. There is **no** `hardware:=mock`. Plugins: [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md). Do not invent a new HI class name here — use that robot’s `xacro/ros2_control/*.xacro` or an existing vendor HI README ([arx-ros2-control](https://github.com/fiveages-sim/arx-ros2-control) for ARX `hardware:=real`).

OCS2 files the controller actually loads: `{robot_pkg}/config/ocs2/<info>.info` ([ocs2_arm README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/README.md)). Planning URDF comes from the same xacro via `robot_common_launch`, not a static `urdf/*.urdf`.

EEF / FT / TCP: `type` / `left_type` / `right_type` (not `gripper:=`).

## 2. Wire it into a deploy workspace

In `open-deploy-ws`:

1. `./init_repo.sh` so nested modules match `submodules_visibility.conf`.
2. If you added a **new** nested submodule: add the Git submodule on the parent, then one pipe line `parent_dir|relative_path|public` or `private` — [Submodules Visibility](../../3-concepts/6-submodules_visibility.md).
3. `colcon build --symlink-install`. Lean branches (`arx-lift2s`, `panthera-ht`): prefer **`./quick_start.sh`** (it sources `install/setup.bash` after a successful build). On `main`, after colcon, `source install/setup.bash` in the launch terminal (standard ROS overlay; no extra env script).

[robot-descriptions-arx README](https://github.com/fiveages-sim/robot-descriptions-arx/blob/main/README.md) also shows adding the brand repo as `src/robot-descriptions-arx` or `git submodule update --init manipulator/ARX` under the umbrella. Prefer the deploy-ws init script when you are in `open-deploy-ws`.

Controllers already in [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control): `ocs2_arm_controller` `demo.launch.py` / `split_body.launch.py` / `full_body.launch.py`, plus `basic_joint_controller`. Example from the Acone README (after the workspace overlay):

:::{code-block} bash
ros2 launch robot_common_launch manipulator.launch.py robot:=arx_acone
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone
:::

Do not invent `robot_description_newrobot/display.launch.py` or a `NewRobotHardwareInterface` C++ stub.

## 3. Isaac USD (FaSim-Isaac skill)

`robot_descriptions` / `robot-descriptions-common` / `robot_usds` have **no** Cursor skill on `main`. The Isaac import pipeline is the FaSim-Isaac skill **`isaac-urdf-usda-ocs2`**:

- Skill file: [`.cursor/skills/USDA-OCS2-PhysX-Mujoco/SKILL.md`](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/.cursor/skills/USDA-OCS2-PhysX-Mujoco/SKILL.md)
- Other skills in that folder (do not invent names): `fasim-robot-mujoco-physics`, `fasim-dexhand-asset`, `fasim-rg75-pad-convert`, `fasim-usd-bake-scale`

What that skill covers (overview only — follow the skill, do not treat this list as a substitute):

1. Split / expand URDF or xacro; record mount poses.
2. Isaac 5: Import URDF → USD. Isaac 6: Asset Transformer → USDA.
3. Robot Assembler (child → parent; one articulation root).
4. Root `variantSets` + **local** adapter payloads (`payloads/Physics/{none,physics,physx,mujoco}.usda`, …).
5. PhysX vs Newton/MuJoCo layers kept separate; host side `topic_based_ros2_control` + `hardware:=isaac`.

Asset layout: [robot_usds README](https://github.com/fiveages-sim/robot_usds/blob/main/README.md) (`robots/manipulators/…`, `robots/mobile_manipulator/…`). FaSim-Isaac checkout: **`./init.sh`** (submodules + optional Isaac ROS 2 workspace), then **`./run.sh`**. Do not hand-write Isaac `PATH` or a `~/.bashrc` overlay. See [Isaac Sim](../2-simulation/4-isaac_sim.md).

## Related

- [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md)
- [Workspace Layout](../../3-concepts/2-workspace_layout.md)
- [robot_common_launch](../../4-reference/descriptions/2-common.md)
- [Go to Real Hardware](9-go_real_hardware/0-index.md)
- [Developer guide](../../5-developer/0-index.md)
