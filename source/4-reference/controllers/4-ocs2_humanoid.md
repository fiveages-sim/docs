# ocs2-humanoid

Wheeled-arm humanoid motion library.

```{admonition} Access Required
:class: warning

This package requires private repository access.
```

**Repository:** ocs2-humanoid (private)

## Purpose

`ocs2-humanoid` provides specialized motion planning for wheeled-arm humanoid robots:
- Wheeled locomotion
- Body balancing
- Arm coordination

## Structure

The repository contains packages for:
- `ocs2_wheel_humanoid` — Wheeled base control
- Integration libraries for WBC

## Usage

Used internally by `ocs2-wbc-controller`. Not typically launched directly.

### Integration

```cpp
#include <ocs2_wheel_humanoid/WheelHumanoidInterface.h>

// Used by WBC controller
```

## Configuration

Configuration is typically handled through the WBC controller layer.

```{admonition} TODO
:class: warning

Root-level README documentation is limited. See WBC controller for usage.
```

## Related

- [OCS2 WBC Controller](3-ocs2_wbc.md)
- [ocs2_ros2](1-ocs2_ros2.md)
