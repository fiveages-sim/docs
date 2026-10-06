# ocs2-wbc-controller

Whole-body control for FiveAges humanoid robots.

```{admonition} Access Required
:class: warning

This package requires private repository access.
```

**Repository:** ocs2-wbc-controller (private)

## Purpose

`ocs2-wbc-controller` provides whole-body control for humanoid robots:
- Full-body motion planning
- Balance and stability
- Multiple control modes
- FSM integration

## Features

### Modes

| Mode | Description |
|------|-------------|
| Stand | Static standing pose |
| Walk | Walking locomotion |
| Arm teleop | Arm tracking with balance |
| Full body | Complete body control |

### Balance

- Center of mass tracking
- Zero moment point (ZMP) control
- Foot contact management

## Usage

### Launch

```bash
ros2 launch ocs2_wbc_controller full_body.launch.py robot:=fiveages_w2 hardware:=mock
```

### Mode Switching

```bash
# Enter stand mode
ros2 topic pub /fsm_command std_msgs/msg/String "{data: 'stand'}" --once

# Enter walk mode
ros2 topic pub /fsm_command std_msgs/msg/String "{data: 'walk'}" --once

# Arm teleop
ros2 topic pub /fsm_command std_msgs/msg/String "{data: 'arm_teleop'}" --once
```

## Topics

### Commands

| Topic | Type | Description |
|-------|------|-------------|
| `/fsm_command` | `String` | Mode command |
| `/cmd_vel` | `Twist` | Velocity command (walk mode) |
| `/teleop/left_ee_pose` | `PoseStamped` | Left arm target |
| `/teleop/right_ee_pose` | `PoseStamped` | Right arm target |

### State

| Topic | Type | Description |
|-------|------|-------------|
| `/fsm_state` | `String` | Current FSM state |
| `/joint_states` | `JointState` | Full body state |

## Configuration

### WBC Parameters

```yaml
wbc:
  balance_weight: 100.0
  tracking_weight: 10.0
  
  contact_constraints:
    friction_coefficient: 0.7
```

### FSM Configuration

```yaml
fsm:
  initial_state: stand
  transitions:
    - from: stand
      to: walk
      trigger: walk
    - from: walk
      to: stand
      trigger: stand
```

## Integration

WBC integrates with:
- Arm controllers for manipulation
- Teleop systems for remote control
- Navigation for mobility

## Safety

```{admonition} Safety Warning
:class: danger

WBC controls the full body. Always:
1. Start in stand mode
2. Verify balance before walking
3. Have emergency stop ready
4. Monitor joint limits
```

## Related

- [ocs2-humanoid](4-ocs2_humanoid.md)
- [FA Robot Descriptions](../descriptions/5-fa_robots.md)
