# Naming Conventions

This page documents the naming patterns used throughout the FiveAges Sim ecosystem.

Brand **EN/ZH** labels follow [robot_usds README_zh-CN.md §3.1](https://github.com/fiveages-sim/robot_usds/blob/main/README_zh-CN.md#31-中文简称与英文标识对照). **ARX** is 方舟无限 (not bare “Ark”). **HighTorque** / Panthera is 高擎. Package paths such as `arx-lift2s` stay as quoted commands.

## Launch Parameters

### Robot Selection

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `robot` | Main robot name | `dobot_cr5`, `arx_acone` (arm), `arx_lift2s`, `panthera_ht` |
| `type` | Symmetric **end-effector** key, **or** arm topology `left` / `right` / `dual` (topology does not expand to `left_type` / `right_type`) | `rg75`, `dual` |
| `left_type` / `right_type` | Different L/R end-effector keys | `rg75`, `linkerhand_o7` |
| `use_profile_eef` | Apply profile `defaults.end_effectors` (default `true`) | `false` to force CLI EEF |
| `robot_profile` | Machine-profile YAML path | `/path/to/machine_profile.yaml` |
| `ft` / `left_ft` / `right_ft` | Force-torque (not gated by `use_profile_eef`) | `kwr75_485` |

There is no `gripper:=` / `gripper_type:=` launch argument. Merge: **CLI > profile > xacro defaults**. With `left_type` / `right_type`, **do not pass `type:=`**. See [robot_common_launch](../4-reference/descriptions/2-common.md).

:::{code-block} bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=dobot_cr5

# README: different L/R end-effectors, ignore profile EEF
ros2 launch ocs2_arm_controller demo.launch.py \
  use_profile_eef:=false \
  left_type:=rg75 right_type:=linkerhand_o7
:::

### Hardware Mode

| Parameter | Options | Description |
|-----------|---------|-------------|
| `hardware` | `mock`, `gz`, `isaac`, (vendor) | Hardware interface type |

The actual hardware identifier varies by robot (e.g., `real`, `can`, `tcp`).

## Package Naming

### Description Packages

Pattern: `robot-descriptions-<brand>` or `<robot>-description`

| Package | Robot(s) |
|---------|----------|
| `robot-descriptions-dobot` | Dobot CR series |
| `robot-descriptions-arx` | ARX X5, Acone (arm), Lift 2S |
| `robot-descriptions-common` | Shared components |
| `fa-w2-description` | FiveAges W2 |

### Hardware Interface Packages

Pattern: `<brand>-ros2-control`

| Package | Hardware |
|---------|----------|
| `arx-ros2-control` | ARX CAN interface |
| `dobot-cr-ros2-control` | Dobot TCP interface |
| `ht-ros2-control` | HighTorque serial interface |

### Controller Packages

Pattern: `<function>_controller` or `ocs2_<type>_controller`

| Package | Purpose |
|---------|---------|
| `basic_joint_controller` | Joint FSM Home / Hold / MoveJ |
| `ocs2_arm_controller` | Arm MPC controller |
| `adaptive_gripper_controller` | Gripper control |
| `arms_teleop_controller` | Teleop integration |

## Topic Naming

### Joint Topics

| Topic | Type | Publisher |
|-------|------|-----------|
| `/joint_states` | `sensor_msgs/JointState` | Hardware interface |
| `/joint_commands` | `sensor_msgs/JointState` | Controller |

### FSM Topics

| Topic | Type | Purpose |
|-------|------|---------|
| `/fsm_command` | `std_msgs/Int32` | FSM command (`1` HOME, `2` HOLD, `3` OCS2 / legacy MOVEJ, `4` MOVEJ). Not `String`. |

Per-controller states and topics: [FSM and Topics](4-fsm_and_topics.md). Do not invent `/mode_command` or `/fsm_state` String contracts.

## Frame Naming

### Standard Frames

| Frame | Description |
|-------|-------------|
| `base_link` | Robot base (fixed) |
| `world` | World frame |
| `odom` | Odometry frame (mobile robots) |
| `<arm>_base_link` | Arm mounting point |
| `<arm>_ee_link` | End effector |
| `<arm>_tool0` | Tool frame |

### Dual-Arm Frames

| Frame | Description |
|-------|-------------|
| `left_base_link` | Left arm base |
| `right_base_link` | Right arm base |
| `left_ee_link` | Left end effector |
| `right_ee_link` | Right end effector |

## Configuration Files

### YAML Files

| File | Purpose |
|------|---------|
| `config/*.yaml` | Controller parameters |
| `urdf/*.urdf.xacro` | Robot model |
| `launch/*.launch.py` | Launch files |
| `ocs2_arm_config.yaml` | MPC configuration |

### Configuration Naming

```yaml
# Controller config pattern
<controller_name>:
  ros__parameters:
    joints:
      - joint_1
      - joint_2
    
    # Nested parameters
    mpc:
      dt: 0.01
      horizon: 1.0
```

## File Naming

| Pattern | Example | Purpose |
|---------|---------|---------|
| `*.urdf.xacro` | `robot.urdf.xacro` | Robot model |
| `*.ros2_control.xacro` | `robot.ros2_control.xacro` | Hardware config |
| `*.launch.py` | `demo.launch.py` | Launch file |
| `*_config.yaml` | `ocs2_arm_config.yaml` | Configuration |

## Best Practices

1. **Use underscores** in Python, launch parameters, and topics
2. **Use hyphens** in package names and repository names
3. **Be consistent** — Match existing patterns in the codebase
4. **Prefix namespaces** — Use robot/arm prefixes for multi-robot setups
