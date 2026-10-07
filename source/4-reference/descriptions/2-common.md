# robot-descriptions-common

Shared end-effector, hand, and sensor descriptions, plus **`robot_common_launch`** (common launch entry, xacro mappings, machine-profile merge).

**Repository:** [fiveages-sim/robot-descriptions-common](https://github.com/fiveages-sim/robot-descriptions-common)

```{admonition} Source of truth
:class: important

End-effector / `type` behavior is documented from [`robot_common_launch/README.md`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/README.md). There is no `gripper:=` launch argument.
```

In-tree folders (browse the repo; do not invent extra package names): `gripper/`, `dexhands/`, `sensor_models/`, `component_models/`, `robot_common_launch/`.

## Merge priority

**Launch CLI > `robot_profile` YAML > xacro defaults**

| YAML section | When `robot_profile:=` is set | Notes |
|--------------|-------------------------------|-------|
| `platform` | Always | Chassis / dual-arm kit / `variant` / `chassis_joints_movable` → xacro |
| `defaults.end_effectors` | Only if `use_profile_eef:=true` (**default**) | End-effector keys; turn off to force CLI `type` / `left_type` / `right_type` |
| `defaults.ft` | Always | Force-torque; **not** gated by `use_profile_eef` |
| `defaults.tcp_offset` | Always | Virtual tip offset; expressions evaluated before mappings |
| `hardware` | Only `hardware:=real` | Real-robot xacro (serial, `arm_ctrl_mode`, …) |
| `control.patch` | Always | Deep-merged into ros2_control config |

## End-effectors (`type` / `left_type` / `right_type`)

Select the **end-effector** with launch arguments (not `gripper:=`):

| Argument | Meaning |
|----------|---------|
| `type` | Symmetric end-effector key, **or** arm topology `left` / `right` / `dual`. Topology does **not** expand into `left_type` / `right_type`. |
| `left_type` / `right_type` | Per-side EEF keys. `create_eef_side_launch_arguments()` lists example keys `rg75`, `ag2f90_c`, `linkerhand_o7`. Use together for asymmetric setups; **do not pass `type:=`** then. |
| `use_profile_eef` | Apply `defaults.end_effectors` from the profile (default `true`) |
| `robot_profile` | Path to a machine-profile YAML |

Profile schema (README):

:::{code-block} yaml
defaults:
  end_effectors:
    type: <eef_key>            # symmetric; or write left / right
:::

- Default: `use_profile_eef:=true` → profile `defaults.end_effectors` is applied.
- Set **`use_profile_eef:=false`** to ignore that block and force CLI `type` / `left_type` / `right_type`. `platform`, `ft`, and `tcp_offset` from the profile still apply.

README example (CLI EEF, profile still used for the rest):

:::{code-block} bash
ros2 launch <pkg> <file>.launch.py \
  robot_profile:=/path/to/machine_profile.yaml \
  use_profile_eef:=false \
  left_type:=rg75 right_type:=linkerhand_o7
:::

## Force-torque and TCP offset

Not controlled by `use_profile_eef`.

| Argument | Meaning |
|----------|---------|
| `ft` / `left_ft` / `right_ft` | Force-torque keys; override profile `defaults.ft` |
| `tcp_offset_xyz` / `tcp_offset_rpy` | Symmetric TCP offset |
| `left_tcp_offset_*` / `right_tcp_offset_*` | Per-side TCP offset |

Profile `defaults.ft.type`: `none` | `kwr75_485` | `kwr75_usb` (or left / right). `end_effectors` / `ft` / `tcp_offset` all accept a symmetric key that expands to both sides; a missing side falls back to the symmetric value.

TCP strings are evaluated **before** xacro (`${PI/2}`, `pi/2`, `radians(90)`, numbers). Failed evaluation errors; they are not written silently. Virtual tip also needs `left_ee_frame` / `right_ee_frame` in `control.patch` (or controller params), e.g. `left_tcp_offset`.

:::{code-block} bash
ros2 launch robot_common_launch humanoid.launch.py robot:=<robot_name> \
  robot_profile:=/path/to/machine_profile.yaml \
  ft:=kwr75_485 \
  tcp_offset_rpy:="0 0 ${PI/2}"
:::

## Launch entries (README)

:::{code-block} bash
colcon build --packages-up-to robot_common_launch --symlink-install
:::

| Scene | Launch |
|-------|--------|
| Visualization | `visualize.launch.py` / `humanoid.launch.py` / `manipulator.launch.py` |
| Gripper / hand | `gripper.launch.py` / `hand.launch.py` |
| Component | `component.launch.py` |
| Controller manager | `controller_manager.launch.py` |
| Navigation | `navigation*.launch.py` |

OCS2 `demo` / `split_body` / `full_body` also declare these first-class arguments via `create_robot_profile_launch_arguments()` / `create_platform_launch_arguments()`.

## GitHub Release `.deb`

`ros-jazzy-robot-descriptions-common` is **not** published to Debian / ROS apt software sources.

**Primary path:** in `open-deploy-ws` / `fa-deploy-ws`, run `./init_repo.sh` and choose `d` for common, or `./scripts/install_core_debs.sh --only common`. Switch source ↔ deb with menu **2) 切换模块安装方式**.

:::{admonition} Manual fallback
:class: note

Download the matching asset from [robot-descriptions-common Releases](https://github.com/fiveages-sim/robot-descriptions-common/releases), then `sudo dpkg -i ros-jazzy-robot-descriptions-common_*.deb` and `sudo apt-get install -f` if needed.
:::

## Related

- [Switch Robot](../../2-how_to/1-basic_operations/2-switch_robot.md)
- [ocs2_arm_controller](../controllers/2-ocs2_arm_controller.md) — `demo` / `split_body` / `full_body` declare these args
- [Naming Conventions](../../3-concepts/3-naming_conventions.md)
- [Brand packages](3-brand_public.md)
