# teleop-joint-mapper

Maps DexCap joints to robot joints.

```{admonition} Access Required
:class: warning

This package requires private repository access.
```

**Repository:** teleop-joint-mapper (private)

## Purpose

Translates DexCap glove joint angles to robot-specific joint commands:
- Joint remapping
- Scaling and limits
- Smooth trajectory generation (ruckig)

## Supported Mappings

| Source | Target Robot |
|--------|-------------|
| DexCap | Tianji M6 |
| DexCap | Other arms (configurable) |

## Usage

```bash
ros2 launch teleop_joint_mapper mapper.launch.py robot:=tianji_m6
```

## Topics

### Subscribed

| Topic | Type | Description |
|-------|------|-------------|
| `/dexcap/joint_states` | `JointState` | Glove input |

### Published

| Topic | Type | Description |
|-------|------|-------------|
| `/target_joint_positions` | `JointState` | Robot targets |

## Configuration

```yaml
teleop_joint_mapper:
  ros__parameters:
    source: dexcap
    target: tianji_m6
    
    joint_mapping:
      dexcap_thumb_mcp: robot_thumb_base
      dexcap_thumb_pip: robot_thumb_proximal
      # ... more mappings
    
    scale_factors:
      thumb: 1.0
      index: 1.0
      # ...
```

## Trajectory Smoothing

Uses ruckig for smooth trajectories:
- Velocity limits
- Acceleration limits
- Jerk limits

## Related

- [DexCap System](3-dexcap.md)
- [DexCap Teleop How-To](../../2-how_to/8-dexcap_teleop.md)
