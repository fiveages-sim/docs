# Controllers Reference

This section documents the ROS 2 controllers used in the stack.

## Overview

Controllers receive commands and produce joint/actuator outputs:

```
Target Pose/Joints → Controller → Command Interfaces → Hardware
```

## In This Section

```{toctree}
:maxdepth: 1

1-ocs2_ros2
2-ocs2_arm_controller
3-ocs2_wbc
4-ocs2_humanoid
5-lina_planning
6-gripper_teleop_plugins
```

## Quick Reference

| Controller | Purpose | Visibility |
|------------|---------|------------|
| [ocs2_ros2](1-ocs2_ros2.md) | MPC library | External |
| [ocs2_arm_controller](2-ocs2_arm_controller.md) | Arm MPC | Public |
| [ocs2-wbc-controller](3-ocs2_wbc.md) | Whole-body control | Private |
| [ocs2-humanoid](4-ocs2_humanoid.md) | Humanoid library | Private |
| [lina_planning](5-lina_planning.md) | Trajectory primitives | Private |
| [Plugins](6-gripper_teleop_plugins.md) | Gripper, teleop | Public |
