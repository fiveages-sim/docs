# Teleoperation Reference

This section documents the teleoperation systems.

## Overview

The stack supports multiple teleoperation methods:

| Method | Input Device | Use Case |
|--------|-------------|----------|
| VR | VR headset (Pico Enterprise / consumer, Meta Quest) | Remote manipulation |
| Isomorphic | Master–slave (HT Panthera) | Joint-space following |
| DexCap | Gloves | Dexterous teleop |
| Vive | Trackers | Arm tracking |
| Wuji | Gloves | Hand tracking |

```{admonition} VR Headset Recommendation
:class: tip

For VR teleoperation, **Pico** and **Meta Quest** are the primary tested headsets. Both can use **WebXR** (`./run.sh vr`) and **XRoboToolkit** (`./run.sh vr-xrt`). **Pico Enterprise** is the preferred Pico SKU: it supports **USB shared networking (USB 网络共享)** and uses a **different headset App** from Pico consumer — do not treat one App as covering both editions.
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
