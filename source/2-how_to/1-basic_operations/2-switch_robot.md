# Switch Robot

Change the robot model in your workspace and launches.

## Prerequisites

- Workspace cloned and initialized
- Target robot's description available

## Steps

### 1. Initialize Robot Description

If the robot description isn't already initialized:

Prefer `./init_repo.sh` in `open-deploy-ws` so nested modules under `src/robot-descriptions/` match [`submodules_visibility.conf`](https://github.com/fiveages-sim/open-deploy-ws/blob/main/submodules_visibility.conf) (`manipulator/Dobot`, `manipulator/ARX`, …). Do not `git submodule update --init --recursive`.

### 2. Rebuild

```bash
cd ~/open-deploy-ws
colcon build --symlink-install
source install/setup.bash
```

### 3. Launch with New Robot

```bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=<robot_name>
```

## Robot Names

| Brand | `robot:=` keys used in this docs set | Source |
|-------|--------------------------------------|--------|
| Dobot | `cr5` | `demo.launch.py` default |
| ARX (方舟无限) | `arx_acone` (**dual-arm**), `arx_lift2s` (**Lift 2S** full-body) | ARX how-to / description packages |
| HighTorque (高擎) | `panthera_ht` | [panthera-ht README](https://github.com/fiveages-sim/open-deploy-ws/blob/panthera-ht/README.EN.md) |
| Dyna | `taku` | `taku_description` on `robot_descriptions` **`feature/agilex`**; control `split_body.launch.py` / `full_body.launch.py` |

Use the key that matches `{key}_description` (the description packages you initialized).

## Example: Dobot to ARX

```bash
# Demo default robot key is cr5 (demo.launch.py)
ros2 launch ocs2_arm_controller demo.launch.py

# After init has ARX descriptions, launch Acone (dual-arm, not Lift 2S)
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone
```

`arx_acone` is **Acone** (dual-arm). Full-body **ARX Lift 2S** (`arx_lift2s`) uses `split_body.launch.py` / `full_body.launch.py` on the `arx-lift2s` branch — see [ARX Lift 2S](../6-deployment/9-go_real_hardware/1-arx_lift2s.md). **Taku** (`taku`) uses the same split / full launches after descriptions are on `feature/agilex`: public mock is `split_body.launch.py`; `full_body.launch.py` needs the private `ocs2_wbc_controller` submodule — [Taku / `feature/agilex`](../../1-getting_started/3-open_deploy_ws.md). HighTorque Panthera HT launch name is `panthera_ht` — see [HighTorque Panthera HT](../6-deployment/9-go_real_hardware/2-panthera_ht.md). Keep `demo.launch.py` for `cr5` / `arx_acone` / `panthera_ht`.

## End-effectors (`type` / `left_type` / `right_type`)

There is **no** `gripper:=` argument. End-effectors are selected by **`robot_common_launch`**:

- Symmetric EEF: `type:=<eef_key>`
- Different left / right: `left_type:=` and `right_type:=` together; **do not pass `type:=`** then (`create_eef_side_launch_arguments()`)
- `type` may also be arm topology `left` / `right` / `dual` (that does **not** become `left_type` / `right_type`)
- OCS2 `demo` / `split_body` / `full_body` declare these via `create_robot_profile_launch_arguments()`. `basic_joint_controller` `demo.launch.py` only declares `type`.

Profile YAML `defaults.end_effectors` is applied when `use_profile_eef:=true` (default). Set `use_profile_eef:=false` to force the CLI keys. Merge order: **CLI > profile > xacro defaults**. FT (`ft` / `left_ft` / `right_ft`) and TCP offsets are separate and always take the profile unless CLI overrides them.

:::{code-block} bash
# README: ignore profile EEF, set L/R from CLI
ros2 launch ocs2_arm_controller demo.launch.py \
  robot:=<robot_name> \
  robot_profile:=/path/to/machine_profile.yaml \
  use_profile_eef:=false \
  left_type:=rg75 right_type:=linkerhand_o7
:::

Full table: [robot-descriptions-common](../../4-reference/descriptions/2-common.md) (`robot_common_launch` README).

## Verification

- RViz shows the correct robot model
- Joint names in `/joint_states` match the new robot
- Controller accepts commands appropriate for the robot

## Troubleshooting

### Package not found

```bash
colcon build --symlink-install
source install/setup.bash
```

### URDF errors

Check the description package's README for dependencies.

### Wrong joint limits

Each robot has its own joint limits in URDF. Verify commanded poses are within limits.
