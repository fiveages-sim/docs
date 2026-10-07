# Switch Robot

Change the robot model in your workspace and launches.

## Prerequisites

- Workspace cloned and initialized
- Target robot's description available

## Steps

### 1. Initialize Robot Description

If the robot description isn't already initialized:

```bash
cd ~/open-deploy-ws/src/robot_descriptions
git submodule update --init robot-descriptions-<brand>
```

Available brands:
- `robot-descriptions-dobot`
- `robot-descriptions-arx`
- `robot-descriptions-galbot`
- `robot-descriptions-ht`
- `robot-descriptions-quadruped`

### 2. Rebuild

```bash
cd ~/open-deploy-ws
colcon build --packages-up-to robot-descriptions-<brand>
source install/setup.bash
```

### 3. Launch with New Robot

```bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=<robot_name> hardware:=mock
```

## Robot Names

| Brand | Robot Names |
|-------|-------------|
| Dobot | `dobot_cr5`, `dobot_cr10` |
| ARX (方舟无限) | `arx_x5`, `arx_acone` (**arm only**), `arx_lift2s` (**Lift 2S** full-body) |
| Galbot | `galbot_g1` |
| HighTorque (高擎) | `panthera_ht` (**Panthera HT**) |

## Example: Dobot to ARX

```bash
# Current: Dobot CR5
ros2 launch ocs2_arm_controller demo.launch.py robot:=dobot_cr5 hardware:=mock

# Initialize ARX descriptions
cd src/robot_descriptions
git submodule update --init robot-descriptions-arx

# Rebuild
cd ~/open-deploy-ws
colcon build --packages-up-to robot-descriptions-arx
source install/setup.bash

# Launch with Acone (arm only, not Lift 2S)
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=mock
```

`arx_acone` is the manipulator. Full-body **ARX Lift 2S** (`arx_lift2s`) uses `split_body.launch.py` / `full_body.launch.py` on the `arx-lift2s` branch — see [ARX Lift 2S](../6-deployment/9-go_real_hardware/1-arx_lift2s.md). HighTorque Panthera HT launch name is `panthera_ht` — see [HighTorque Panthera HT](../6-deployment/9-go_real_hardware/2-panthera_ht.md).

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
colcon build --packages-up-to robot-descriptions-<brand>
source install/setup.bash
```

### URDF errors

Check the description package's README for dependencies.

### Wrong joint limits

Each robot has its own joint limits in URDF. Verify the target pose is within limits.
