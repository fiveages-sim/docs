# Teleoperation Reference

This section documents the teleoperation systems.

## Overview

The stack supports multiple teleoperation methods:

| Method | Input Device | Use Case |
|--------|-------------|----------|
| VR | VR headset | Remote manipulation |
| Drag | Direct contact | Teaching |
| DexCap | Gloves | Dexterous teleop |
| Vive | Trackers | Arm tracking |
| Wuji | Gloves | Hand tracking |

## In This Section

```{toctree}
:maxdepth: 1

1-vr_pose_publisher
2-drag_teleop
3-dexcap
4-teleop_joint_mapper
5-wuji_glove
6-vive_tracker
7-wuji_hand_hi
```

## Topic Contracts

All teleop systems publish to standard topics:

| Topic | Type | Description |
|-------|------|-------------|
| `/teleop/left_ee_pose` | `PoseStamped` | Left arm target |
| `/teleop/right_ee_pose` | `PoseStamped` | Right arm target |
| `/teleop/head_pose` | `PoseStamped` | Head tracking |
