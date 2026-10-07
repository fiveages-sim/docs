# robot-descriptions-common

Shared grippers, dexterous hands, sensor models, and **`robot_common_launch`**. Under the [robot_descriptions](https://github.com/fiveages-sim/robot_descriptions) umbrella this repo is the **`common`** submodule.

**Repository:** [fiveages-sim/robot-descriptions-common](https://github.com/fiveages-sim/robot-descriptions-common)

```{admonition} Source of truth
:class: important

- Repo inventory / xacro include / launch file list: [README.md](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/README.md)
- Launch args / profile merge / `hardware:=`: [`robot_common_launch/README.md`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/README.md)
- GitHub Release `.deb`: [README.deb.md](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/README.deb.md)
- **No** `.cursor/skills` on `main`. Do not invent extra common skills or package names.
```

There is no `gripper:=` launch argument. Attach an end-effector with `type` / `left_type` / `right_type` (below).

## Layout

Folders on `main` (browse the repo; do not invent extra package names):

:::{code-block} none
common/                          # umbrella checkout path
├── gripper/                     # one ROS package per brand
├── dexhands/
├── sensor_models/               # single package: meshes + URDF
├── component_models/            # single package: meshes + xacro (not tabulated in the README)
└── robot_common_launch/
    ├── config/                  # RViz, Nav2, …
    ├── launch/
    ├── worlds/
    └── xacro/
:::

README package-structure tree also lists `xhand1_description` under `dexhands/` (not in the Dexterous Hands table).

## Grippers (`gripper/`)

From the [repo README](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/README.md):

| Brand | Package | Models |
|-------|---------|--------|
| ChangingTek | `gripper/changingtek_description` | AG2F90-C, AG2F120S |
| DH | `gripper/dh_description` | PGC_140_50 |
| Robotiq | `gripper/robotiq_description` | 2F-85 |
| Inspire | `gripper/inspire_description` | EG2-4C2 (hands RH56E2 / RH56F2 live here too) |
| Jodell | `gripper/jodell_description` | RG75-300 |
| Hitbot | `gripper/hitbot_description` | Z-EFG-100 |
| Eincinx | `gripper/eincinx_description` | EPGI180 |
| Marvin | `gripper/marvin_gripper_description` | marvin_gripper, marvin_gripper45 |

README: each gripper package includes URDF/xacro, meshes, ros2_control configs, and mount configs.

## Dexterous hands (`dexhands/`)

| Brand | Package | Models |
|-------|---------|--------|
| BrainCo | `dexhands/brainco_description` | REVO1, REVO2 |
| LinkerHand | `dexhands/linkerhand_description` | O6, O7, L6, L10 |
| Inspire | `gripper/inspire_description` | RH56E2, RH56F2 |
| OyMotion | `dexhands/oymotion_description` | RoHand Gen2 |
| FreeDom | `dexhands/freedom_description` | V1, V2 |
| TheoHand | `dexhands/theohand_description` | STD16A |
| Wuji | `dexhands/wuji_description` | Hand2, Beta2 |

## Sensors (`sensor_models/`)

README lists URDF + meshes for:

- Intel RealSense D405
- Intel RealSense D435
- Orbbec Dabai
- Livox Mid-360

## Use a component from xacro

README example (Robotiq). Copy an **existing** include from a real `{robot}_description` rather than inventing macros:

:::{code-block} xml
<xacro:include filename="$(find robotiq_description)/xacro/gripper.xacro"/>

<xacro:robotiq_gripper
  parent="arm_link_6"
  name="gripper">
  <origin xyz="0 0 0" rpy="0 0 0"/>
</xacro:robotiq_gripper>
:::

## `robot_common_launch`

Cross-robot launch entry, xacro mappings, and **machine profile** YAML (`robot_profile:=`). Downstream visualization / `controller_manager` / controller packages generate `robot_description` and planning URDF through this API.

```{admonition} Mechanism
:class: note

`robot_profile:=/path/to/profile.yaml` → `load_robot_profile` / `normalize_robot_profile` → `build_xacro_mappings` (or `build_visualization_xacro_mappings`) → xacro → `robot_description` / planning URDF.

Implementation: [`launch_arg_utils.py`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/robot_common_launch/common/launch_arg_utils.py). Any launch that forwards `robot_profile` (e.g. `create_robot_profile_launch_arguments()`) uses the same path.
```

### Merge priority

**Launch CLI > `robot_profile` YAML > xacro defaults**

| YAML section | When `robot_profile:=` is set | Notes |
|--------------|-------------------------------|-------|
| `platform` | Always | Chassis / dual-arm kit / `variant` / `chassis_joints_movable` → xacro |
| `defaults.end_effectors` | Only if `use_profile_eef:=true` (**default**) | End-effector keys; turn off to force CLI `type` / `left_type` / `right_type` |
| `defaults.ft` | Always | Force-torque; **not** gated by `use_profile_eef` |
| `defaults.tcp_offset` | Always | Virtual tip offset; expressions evaluated before mappings |
| `hardware` | Only `hardware:=real` | Real-robot xacro (serial, `arm_ctrl_mode`, …) |
| `control.patch` | Always | Deep-merged into ros2_control config |

Profile schema (README):

:::{code-block} yaml
defaults:
  end_effectors:
    type: <eef_key>            # symmetric; or write left / right
:::

### End-effectors (`type` / `left_type` / `right_type`)

| Argument | Meaning |
|----------|---------|
| `type` | Symmetric end-effector key, **or** arm topology `left` / `right` / `dual`. Topology does **not** expand into `left_type` / `right_type`. |
| `left_type` / `right_type` | Per-side EEF keys. `create_eef_side_launch_arguments()` description examples: `rg75`, `ag2f90_c`, `linkerhand_o7`. Use together for asymmetric setups; **do not pass `type:=`** then. |
| `use_profile_eef` | Apply `defaults.end_effectors` from the profile (default `true`) |
| `robot_profile` | Path to a machine-profile YAML |

- Default: `use_profile_eef:=true` → profile `defaults.end_effectors` is applied.
- Set **`use_profile_eef:=false`** to ignore that block and force CLI `type` / `left_type` / `right_type`. `platform`, `ft`, and `tcp_offset` from the profile still apply.

README example (CLI EEF, profile still used for the rest):

:::{code-block} bash
ros2 launch <pkg> <file>.launch.py \
  robot_profile:=/path/to/machine_profile.yaml \
  use_profile_eef:=false \
  left_type:=rg75 right_type:=linkerhand_o7
:::

### Force-torque and TCP offset

Not controlled by `use_profile_eef`.

| Argument | Meaning |
|----------|---------|
| `ft` / `left_ft` / `right_ft` | Force-torque keys; override profile `defaults.ft` |
| `tcp_offset_xyz` / `tcp_offset_rpy` | Symmetric TCP offset |
| `left_tcp_offset_*` / `right_tcp_offset_*` | Per-side TCP offset |

Profile `defaults.ft.type`: `none` \| `kwr75_485` \| `kwr75_usb` (or left / right). `end_effectors` / `ft` / `tcp_offset` all accept a symmetric key that expands to both sides; a missing side falls back to the symmetric value.

TCP strings are evaluated **before** xacro (`${PI/2}`, `pi/2`, `radians(90)`, numbers). Failed evaluation errors; they are not written silently. Virtual tip also needs `left_ee_frame` / `right_ee_frame` in `control.patch` (or controller params), e.g. `left_tcp_offset`.

:::{code-block} bash
ros2 launch robot_common_launch humanoid.launch.py robot:=<robot_name> \
  robot_profile:=/path/to/machine_profile.yaml \
  ft:=kwr75_485 \
  tcp_offset_rpy:="0 0 ${PI/2}"
:::

### ros2_control config merge

[`load_robot_config`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/robot_common_launch/common/robot_utils.py):

:::{code-block} none
common.yaml
  → <type>.yaml / ros2_controllers.yaml
  → {variant}.yaml          # opt-in: config/ros2_control/<variant>.yaml
  → {hardware}.yaml         # opt-in: config/ros2_control/<hardware>.yaml
  → EEF compose (if any)
  → control.patch (profile)
:::

`hardware:=` values in that README: `mock_components` / `gz` / `isaac` / `real`. Overlay YAML is merged **only if the file exists**. Profile YAML `hardware:` (serial, `arm_ctrl_mode`) is a different layer and applies only when `hardware:=real`.

### Launch entries

From the repo README (paths under `robot_common_launch/launch/`):

| Kind | Files the README names |
|------|------------------------|
| Visualization | `visualize/gripper.launch.py`, `visualize/hand.launch.py`, `visualize/manipulator.launch.py`, `visualize/humanoid.launch.py` |
| Control | `control/controller_manager.launch.py`, `control/diff_drive.launch.py`, `control/hardware_visualize.launch.py` |
| Manipulation | `manipulation/manipulator_ocs2.launch.py` |
| Navigation | `navigation/navigation.launch.py`, `navigation/cartographer.launch.py`, `navigation/navigation_slam.launch.py`, `navigation/amr_rctk.launch.py` |

Also on `main` under `launch/` (not named in that README table; do not invent others):

| Kind | Extra files |
|------|-------------|
| Visualization | `visualize/visualize.launch.py`, `visualize/component.launch.py` (named in the `robot_common_launch` README invoke table) |
| Control | `control/cartesian_controller.launch.py` |
| Manipulation | `manipulation/humanoid_ocs2.launch.py` |
| Navigation | `navigation/navigation_cartographer.launch.py`, `navigation/navigation_isaac_gt.launch.py` |

`navigation_isaac_gt.launch.py` is the default Nav2 launch cited by [robot_action_composer ROS2_STACK.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/ROS2_STACK.md).

`robot_common_launch` README invoke table (same package; install first):

:::{code-block} bash
colcon build --packages-up-to robot_common_launch --symlink-install
source install/setup.bash
:::

| Scene | Launch |
|-------|--------|
| Visualization | `visualize.launch.py` / `humanoid.launch.py` / `manipulator.launch.py` |
| Gripper / hand | `gripper.launch.py` / `hand.launch.py` |
| Component | `component.launch.py` |
| Controller manager | `controller_manager.launch.py` |
| Navigation | `navigation*.launch.py` |

Repo README examples:

:::{code-block} bash
ros2 launch robot_common_launch gripper.launch.py
ros2 launch robot_common_launch manipulator_ocs2.launch.py
ros2 launch robot_common_launch navigation_slam.launch.py
:::

OCS2 `demo` / `split_body` / `full_body` also declare the first-class EEF / profile arguments via `create_robot_profile_launch_arguments()` / `create_platform_launch_arguments()`.

## GitHub Release `.deb`

`ros-jazzy-robot-descriptions-common` is **not** on Debian / ROS apt. Workflow: [`.github/workflows/build-common-deb.yml`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/.github/workflows/build-common-deb.yml). Rules: [README.deb.md](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/README.deb.md).

**Primary path:** in `open-deploy-ws` / `fa-deploy-ws`, run `./init_repo.sh` and choose `d` for common, or `./scripts/install_core_debs.sh --only common`.

README.deb.md example:

:::{code-block} bash
gh release download pre-release --repo fiveages-sim/robot-descriptions-common --pattern '*_amd64.deb'
sudo dpkg -i ros-jazzy-robot-descriptions-common_*.deb
:::

## Related

- [robot_descriptions](1-robot_descriptions.md) — umbrella path `common`
- [Switch Robot](../../2-how_to/1-basic_operations/2-switch_robot.md)
- [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md)
- [ocs2_arm_controller](../controllers/2-ocs2_arm_controller.md)
- [Naming Conventions](../../3-concepts/3-naming_conventions.md)
