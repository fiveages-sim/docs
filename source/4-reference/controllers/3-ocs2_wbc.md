# ocs2-wbc-controller

Whole-body control for FiveAges humanoid robots.

```{admonition} Access Required
:class: warning

This package requires private repository access. Contact your team lead for access.
```

**Repository:** ocs2-wbc-controller (private)

## Purpose

`ocs2-wbc-controller` provides whole-body control capabilities for humanoid robots, enabling:
- Full-body motion planning
- Balance and stability control
- FSM integration

## Usage

```{admonition} TODO
:class: note

For specific launch commands, available modes, parameters, and configuration options, refer to the repository's README and documentation. The content below is a general overview; consult the in-repo docs for accurate details.
```

### General Launch Pattern

```bash
ros2 launch ocs2_wbc_controller <launch_file>.launch.py robot:=<robot_id> hardware:=mock
```

Replace `<launch_file>` and `<robot_id>` with values from the repository documentation.

## Topics

```{admonition} TODO
:class: note

Topic names, types, and behaviors are defined in the repository. Check the package's message definitions and launch files for the current interface.
```

The controller typically uses:
- FSM command topics for mode switching
- Joint state topics for feedback
- Target pose topics for teleop integration

## Configuration

```{admonition} TODO
:class: note

Configuration parameters, default values, and YAML schemas are maintained in the repository. Do not rely on example values shown elsewhere; always use the actual config files from the repo.
```

## Safety

```{admonition} Safety Warning
:class: danger

WBC controls the full body of humanoid robots. Always:
1. Verify the robot is in a safe initial state
2. Have emergency stop ready
3. Monitor joint and balance limits
4. Follow the safety procedures documented in the repository
```

## Integration

WBC integrates with other components in fa-deploy-ws:
- Arm controllers for manipulation
- Teleop systems for remote control

## Related

- [ocs2-humanoid](4-ocs2_humanoid.md)
- [FA Robot Descriptions](../descriptions/5-fa_robots.md)
