# Add a Robot

How a new robot enters this stack. Copy an **existing** description package and the launch/xacro patterns already in the repo. There is **no** `hardware:=mock`. Launch files and config names are those listed in that package’s README.

```{admonition} Source of truth
:class: important

- Description layout: an existing `{robot}_description` package (example below: [arx_acone_description](https://github.com/fiveages-sim/robot-descriptions-arx/tree/main/arx_acone_description)) and its package README
- Umbrella + submodule paths: [robot_descriptions README (`main`)](https://github.com/fiveages-sim/robot_descriptions/blob/main/README.md) (e.g. ARX at `manipulator/ARX`). Newer AgileX / Rokae INEX tables: [same README on `feature/agilex`](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/README.md)
- Launch / `hardware:=` / EEF: [robot_common_launch](../../4-reference/descriptions/2-common.md)
- Workspace init: `./init_repo.sh` in [open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws/blob/main/README.EN.md) + [`submodules_visibility.conf`](https://github.com/fiveages-sim/open-deploy-ws/blob/main/submodules_visibility.conf)
- Isaac USD: FaSim-Isaac skill **`isaac-urdf-usda-ocs2`** (folder `USDA-OCS2-PhysX-Mujoco`) — [skill](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/.cursor/skills/USDA-OCS2-PhysX-Mujoco/SKILL.md) — plus `./init.sh` / `./run.sh` and [robot_usds](https://github.com/fiveages-sim/robot_usds/blob/main/README.md)
- Description-side Cursor skills: **`robot_descriptions` branch `feature/agilex`** — [`.cursor/skills/README.md`](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/.cursor/skills/README.md). **`main` has no `.cursor/skills`**. `robot-descriptions-common` and `robot_usds` have none on `main`. The agilex index lists **only** `split-chassis-glb`.
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
│   ├── ocs2/                  # task .info (controller loads these, not a separate ocs2_arm_config.yaml)
│   └── ros2_control/          # optional {hardware}.yaml overlay
└── meshes/
:::

Launch key is `robot:=<key>` where the package is `{key}_description` ([robot_common_launch](../../4-reference/descriptions/2-common.md)). `demo.launch.py` default is `cr5`.

`hardware:=` values that exist in Acone xacro / common launch: `mock_components` (default), `gz`, `isaac`, `real`. There is **no** `hardware:=mock`. Plugins: [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md). Use the plugin class from that robot’s `xacro/ros2_control/*.xacro` or an existing vendor HI README ([arx-ros2-control](https://github.com/fiveages-sim/arx-ros2-control) for ARX `hardware:=real`).

OCS2 files the controller actually loads: `{robot_pkg}/config/ocs2/<info>.info` ([ocs2_arm README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/README.md)). Planning URDF comes from the same xacro via `robot_common_launch`, not a static `urdf/*.urdf`.

EEF / FT / TCP: `type` / `left_type` / `right_type` (not `gripper:=`).

### Chassis / swerve / `collider:=simple` (`feature/agilex` skill)

On **`feature/agilex` only**, the skills index currently lists one skill: **`split-chassis-glb`** ([SKILL.md](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/.cursor/skills/split-chassis-glb/SKILL.md)). Canonical example in that skill: `rokae_inex_description`.

What it does (overview; follow the skill for the full procedure):

- Split one assembled chassis GLB into `chassis` / `steer` / `wheel` meshes with joint-ready origins
- Write swerve xacro (reuse one steer + one wheel at `fl` `fr` `rl` `rr`; right modules yaw 180°, no mesh reflect)
- Add `collider:=simple` boxes from **glTF-node** AABBs (not raw accessor min/max)

How to add more skills under `.cursor/skills/`: the same [skills README](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/.cursor/skills/README.md) (folder [`.cursor/skills/`](https://github.com/fiveages-sim/robot_descriptions/tree/feature/agilex/.cursor/skills)). The index currently lists **only** `split-chassis-glb`.

**Package layout / submodules:** [README on `main`](https://github.com/fiveages-sim/robot_descriptions/blob/main/README.md) for the shared submodule table (`common`, `manipulator/ARX`, …). Use the [README on `feature/agilex`](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/README.md) when the robot is newer AgileX or Rokae INEX. That branch currently tables (paths as written there):

| Kind | Path on `feature/agilex` |
|------|--------------------------|
| Mobile manipulator | `manipulator/AgileX/cobot_magic_v1_description` (Cobot Magic V1) |
| Mobile manipulator | `manipulator/AgileX/split_aloha_description` (Split Aloha) |
| Mobile manipulator | `manipulator/AgileX/cobot_magic_v2_description` (Cobot Magic V2) |
| Manipulator | `manipulator/AgileX/piper_description` (Piper; also on `main`) |
| Manipulator | `manipulator/AgileX/nero_description` (Nero) |
| Manipulator | `manipulator/AgileX/open_nero_description` (Open Nero) |
| Wheel humanoid | `humanoid/Rokae/rokae_inex_description` (INEX; `split-chassis-glb` canonical) |

`main` still lists AgileX Aloha at `manipulator/AgileX/agilex_aloha_description` and does **not** have the `.cursor/skills` directory.

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

Launch files and hardware-interface class names come from the package you copied and its vendor HI README.

## 3. Isaac USD (FaSim-Isaac skill)

Isaac import is still the FaSim-Isaac skill **`isaac-urdf-usda-ocs2`** (not the description-side `split-chassis-glb` skill):

- Skill file: [`.cursor/skills/USDA-OCS2-PhysX-Mujoco/SKILL.md`](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/.cursor/skills/USDA-OCS2-PhysX-Mujoco/SKILL.md)
- Other skills in that folder: `fasim-robot-mujoco-physics`, `fasim-dexhand-asset`, `fasim-rg75-pad-convert`, `fasim-usd-bake-scale`

What that skill covers (overview; follow the skill for the full procedure):

1. Split / expand URDF or xacro; record mount poses.
2. Isaac 5: Import URDF → USD. Isaac 6: Asset Transformer → USDA.
3. Robot Assembler (child → parent; one articulation root).
4. Root `variantSets` + **local** adapter payloads (`payloads/Physics/{none,physics,physx,mujoco}.usda`, …).
5. PhysX vs Newton/MuJoCo layers kept separate; host side `topic_based_ros2_control` + `hardware:=isaac`.

Asset layout: [robot_usds README](https://github.com/fiveages-sim/robot_usds/blob/main/README.md) (`robots/manipulators/…`, `robots/mobile_manipulator/…`). FaSim-Isaac checkout: **`./init.sh`** (submodules + optional Isaac ROS 2 workspace), then **`./run.sh`**. See [Isaac Sim](../2-simulation/4-isaac_sim.md).

## Related

- [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md)
- [Workspace Layout](../../3-concepts/2-workspace_layout.md)
- [robot_common_launch](../../4-reference/descriptions/2-common.md)
- [Go to Real Hardware](9-go_real_hardware/0-index.md)
- [Developer guide](../../5-developer/0-index.md)
