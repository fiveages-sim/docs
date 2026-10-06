# lina_planning

Trajectory primitive library for motion planning.

```{admonition} Access Required
:class: warning

This package requires private repository access. Contact your team lead for access.
```

**Repository:** lina_planning (private)

## Purpose

`lina_planning` provides trajectory primitive generators for motion planning, including joint space and Cartesian space trajectories.

## Features

```{admonition} TODO
:class: note

For the complete list of available trajectory types, API documentation, and usage examples, refer to the repository's README and header files. The overview below is general; consult the in-repo docs for accurate details.
```

The library typically provides trajectory primitives such as:
- Joint space motion planning
- Cartesian space motion planning
- Smooth trajectory interpolation

## Usage

```bash
colcon build --packages-up-to lina_planning
```

```{admonition} TODO
:class: note

API details, function signatures, and code examples should be taken from the repository's documentation and header files. Do not rely on examples shown elsewhere.
```

## Configuration

```{admonition} TODO
:class: note

Configuration parameters and default values are maintained in the repository. Check the package's config files for current options.
```

## Integration

`lina_planning` is used by higher-level controllers and planners in the stack.

## Related

- [ocs2_arm_controller](2-ocs2_arm_controller.md)
