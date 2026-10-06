# SDK Notes

Notes on vendor SDKs used by hardware interfaces.

## Overview

Some hardware interfaces depend on vendor SDKs that may have:
- Licensing restrictions
- Build requirements
- Distribution limitations

## Tianji SDK

**Repository:** TJ_FX_ROBOT_CONTRL_SDK (private submodule)

### Purpose

Control SDK for Tianji robot hardware.

### Usage

Used internally by `marvin-ros2-control` and related interfaces.

### Build Notes

- SDK is provided as pre-built library
- Linked during hardware interface compilation
- Not redistributed separately

```{admonition} TODO
:class: warning

SDK documentation is limited. Usage is through the hardware interface layer.
```

## Fairino ART SDK

### Purpose

Application runtime for Fairino robots.

### Integration

The `fairino-ros2-control` interface wraps the ART SDK.

### Requirements

- SDK installation required
- Network configuration for robot connection

## General SDK Patterns

### Build Integration

SDKs are typically:
1. Vendored as submodules
2. Linked during build
3. Not exposed in public API

### Runtime Requirements

- SDK libraries must be available at runtime
- Environment variables may need configuration
- Device permissions must be set

### Troubleshooting

If SDK-related errors occur:

1. Check SDK is built/installed
2. Verify library paths (`LD_LIBRARY_PATH`)
3. Check device permissions
4. Review hardware interface logs

## Related

- [Public Hardware Interfaces](1-public_hi.md)
- [Private Hardware Interfaces](2-private_hi.md)
