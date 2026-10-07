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

`arx_acone` is the manipulator. Full-body **ARX Lift 2S** (`arx_lift2s`) uses `split_body.launch.py` / `full_body.launch.py` on the `arx-lift2s` branch — see [ARX Lift 2S](11-arx_lift2s.md). HighTorque Panthera HT launch name is `panthera_ht` — see [HighTorque Panthera HT](12-panthera_ht.md).

## With Grippers

Different robots support different grippers. The `gripper:=` parameter specifies the end-effector.

```{admonition} TODO
:class: note

For valid robot + gripper combinations and exact launch syntax, check the launch files in `arms_ros2_control` and the specific robot description packages. Not all combinations are supported.
```

```bash
# General pattern
ros2 launch ocs2_arm_controller demo.launch.py robot:=<robot_name> gripper:=<gripper_name> hardware:=mock
```

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
