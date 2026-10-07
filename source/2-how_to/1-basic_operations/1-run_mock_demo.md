# Run Mock Demo

Run a robot demonstration with the default `hardware:=mock_components` plugin (`mock_components/GenericSystem` on Acone xacro). No Gazebo / Isaac / physical robot.

## Prerequisites

- [Install Environment](../../1-getting_started/2-install_environment.md) done
- Workspace initialized with `./init_repo.sh` and `colcon build`
- In the launch terminal: `source install/setup.bash` (standard overlay; no extra env script)

## Steps

### 1. Source Workspace

From the workspace root after a successful build:

```bash
source install/setup.bash
```

### 2. Launch Mock Demo

[`demo.launch.py`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/launch/demo.launch.py) defaults `robot:=cr5` and `hardware:=mock_components`. Omit both, or pass them explicitly. There is **no** `hardware:=mock`.

```bash
ros2 launch ocs2_arm_controller demo.launch.py
```

### 3. Observe

- RViz (`demo_ocs2.rviz`)
- `arms_target_manager` when `enable_arms_target_manager` is `true` (default)
- FSM starts in HOLD — `/fsm_command` `std_msgs/Int32` (`1` HOME, `2` HOLD, `3` OCS2)

Do **not** publish `/target_pose`. That is not a stack-wide API. See [FSM and Topics](../../3-concepts/4-fsm_and_topics.md) and [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md).

## With Different Robots

```bash
# Acone (arm only, not Lift 2S)
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone

# HighTorque Panthera HT
ros2 launch ocs2_arm_controller demo.launch.py robot:=panthera_ht
```

### End-effector (`type`)

Not `gripper:=`. This launch includes `create_robot_profile_launch_arguments()`. Symmetric EEF: `type:=`. Different L/R: `left_type:=` and `right_type:=` together (**do not pass `type:=`** then). Profile `defaults.end_effectors` applies unless `use_profile_eef:=false`. See [Switch Robot](2-switch_robot.md) and [robot_common_launch](../../4-reference/descriptions/2-common.md).

:::{code-block} bash
ros2 launch ocs2_arm_controller demo.launch.py \
  robot:=<robot_name> \
  use_profile_eef:=false \
  left_type:=rg75 right_type:=linkerhand_o7
:::

## Launch Parameters (from `demo.launch.py` + `robot_common_launch`)

| Parameter | Documented values | Default on this launch |
|-----------|-------------------|------------------------|
| `hardware` | `mock_components`, `gz`, `isaac`, `real` | `mock_components` |
| `robot` | Description key (`{key}_description`) | `cr5` |
| `type` / `left_type` / `right_type` | EEF key, or `type` as `left`/`right`/`dual` topology | profile or xacro |
| `use_profile_eef` | `true`, `false` | `true` |
| `enable_arms_target_manager` | `true`, `false` | `true` |

Do not invent `rviz:=` / `headless:=` on this file.

## Verification

- RViz window opens showing the robot model
- Controller process is running (HOLD)
- `/fsm_command` is accepted (`std_msgs/Int32`)

## Troubleshooting

### Robot doesn't move

- FSM must leave HOLD (`/fsm_command` `3` for OCS2 on this controller)
- Check controller logs; do not assume a `/target_pose` publisher

### RViz shows broken model

- Rebuild description packages
- Check the description package README for `check_urdf` / visualize launch

### Command not found

```bash
source install/setup.bash  # Must source after building
```
