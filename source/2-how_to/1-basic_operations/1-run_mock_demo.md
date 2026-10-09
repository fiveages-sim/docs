# Run Mock Demo

Run a robot demonstration with the default `hardware:=mock_components` plugin (`mock_components/GenericSystem` on Acone xacro). No Gazebo / Isaac / physical robot.

## Prerequisites

- [Install Environment](../../1-getting_started/2-install_environment.md) done
- Workspace initialized with `./init_repo.sh` and `colcon build`
- Lean branches (`arx-lift2s`, `panthera-ht`): `./quick_start.sh` (it sources `install/` after a successful build). On `open-deploy-ws` `main`, after `colcon build`, `source install/setup.bash` in the launch terminal (standard ROS overlay; no extra env script).

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
# Acone (dual-arm, not Lift 2S)
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone

# HighTorque Panthera HT
ros2 launch ocs2_arm_controller demo.launch.py robot:=panthera_ht
```

### Taku

Taku lives on `robot_descriptions` **`feature/agilex`** (`humanoid/Dyna/taku_description`). See [Taku / `feature/agilex`](../../1-getting_started/3-open_deploy_ws.md) before this launch. Control is **`split_body.launch.py` / `full_body.launch.py`**, not `demo.launch.py`.

```bash
colcon build --packages-up-to ocs2_arm_controller taku_description
source install/setup.bash
ros2 launch ocs2_arm_controller split_body.launch.py robot:=taku
```

Public mock is **`split_body.launch.py`**: `ocs2_arm_controller` (dual-arm MPC) plus `body_joint_controller` / `head_joint_controller` and Dynaclaw via `adaptive_gripper_controller` (`*_gripper_joint`; mimic jaw in URDF). There is no chassis or per-arm basic controller. **`full_body.launch.py robot:=taku`** needs the private `ocs2_wbc_controller` submodule; shipping `config/ocs2/fixed_base_tcp.info` is not enough. When that config and the private module are present, full-body default `headMode` is **`HEAD_GAZE`** (gaze on `head_camera_mid_optical_frame`). `target_manager.yaml` has `enable_head_control: false`. Split-body still uses `head_joint_controller`.

In RViz, set **Fixed Frame** to **`base_link`** (package root) or the coincident **`base_footprint`**. OCS2 `baseFrame` / markers use `base_link` (`marker_fixed_frame` in `config/ocs2/target_manager.yaml`).

`hardware:=gz` (Gazebo) may need a GPU. Use mock + RViz as the default verify path; see [Gazebo Simulation](../2-simulation/3-gazebo_sim.md) if you need physics.

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
| `enable_gripper` | `true`, `false` | `true` |

`demo.launch.py` does not declare `rviz:=` or `headless:=`. Use only the arguments in the table above.

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
- **Taku:** Fixed Frame is **`base_link`** (or `base_footprint`)

### Command not found

```bash
source install/setup.bash  # Must source after building
```
