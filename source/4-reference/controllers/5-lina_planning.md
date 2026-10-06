# lina_planning

Trajectory primitive library for motion planning.

```{admonition} Access Required
:class: warning

This package requires private repository access.
```

**Repository:** lina_planning (private)

## Purpose

`lina_planning` provides trajectory primitive generators:
- MoveJ — Joint space motion
- MoveL — Linear Cartesian motion
- Circular — Arc motion
- Bezier — Smooth curves

## Usage

### Build

```bash
colcon build --packages-up-to lina_planning
```

### API

```cpp
#include <lina_planning/trajectory_primitives.h>

// MoveJ: Joint space trajectory
auto traj = lina_planning::MoveJ(
    start_joints,
    end_joints,
    duration
);

// MoveL: Linear Cartesian trajectory
auto traj = lina_planning::MoveL(
    start_pose,
    end_pose,
    duration
);

// Circular: Arc trajectory
auto traj = lina_planning::Circular(
    start_pose,
    via_pose,
    end_pose,
    duration
);
```

## Trajectory Types

### MoveJ

Joint space interpolation:
- Smooth joint motion
- Respects joint limits
- Optional velocity limits

### MoveL

Linear Cartesian interpolation:
- Straight-line end-effector path
- Orientation interpolation
- Collision checking integration

### Circular

Arc motion through three points:
- Start, via, end poses
- Circular path in Cartesian space

### Bezier

Smooth curves:
- Multiple control points
- Continuous velocity/acceleration
- Configurable order

## Integration

Used by higher-level planners and controllers:

```cpp
// Example integration
class MotionExecutor {
    void execute_movej(const JointState& target) {
        auto traj = lina_planning::MoveJ(current_, target, 2.0);
        execute_trajectory(traj);
    }
};
```

## Configuration

```yaml
lina_planning:
  default_joint_velocity: 1.0  # rad/s
  default_cartesian_velocity: 0.1  # m/s
  interpolation_dt: 0.01  # seconds
```

## Related

- [ocs2_arm_controller](2-ocs2_arm_controller.md)
