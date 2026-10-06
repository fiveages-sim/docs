# Teleoperation Reference

This section documents the teleoperation systems.

## Overview

The stack supports multiple teleoperation methods:

| Method | Input Device | Use Case |
|--------|-------------|----------|
| VR | VR headset (Pico, Meta Quest) | Remote manipulation |
| Isomorphic | Master–slave (HT Panthera) | Joint-space following |
| DexCap | Gloves | Dexterous teleop |
| Vive | Trackers | Arm tracking |
| Wuji | Gloves | Hand tracking |

```{admonition} VR Headset Recommendation
:class: tip

For VR teleoperation, **Pico** and **Meta Quest** are the primary tested headsets. Both support **Web** and **XROtoolkit** modes. **Pico has better support** — the enterprise edition offers a faster release cadence and lower-latency tracking (更跟手).
```

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
