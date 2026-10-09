# Python Applications Reference

This section documents the Python libraries and applications.

## Overview

Python libraries provide high-level interfaces:
- Robot control API
- Visualization (Viser is launched from **fa-py-libraries**, `./run.sh viser`)
- LeRobot ROS 2 plugins
- Task-queue YAML orchestration

## In This Section

```{toctree}
:maxdepth: 1

1-ros2_robot_interface
2-fa_py_libraries
3-ros2_viser
4-lerobot_ros2
5-robot_action_composer
6-hug
7-wuji_retargeting
```

## Quick Reference

| Package | Purpose | Visibility |
|---------|---------|------------|
| [ros2_robot_interface](1-ros2_robot_interface.md) | `ROS2RobotInterface` topic / action client | Public |
| [fa-py-libraries](2-fa_py_libraries.md) | Utilities umbrella | Public |
| [ros2-viser](3-ros2_viser.md) | Viser library (launch via fa-py-libraries) | Public |
| [lerobot_ros2](4-lerobot_ros2.md) | LeRobot ↔ ROS 2 monorepo | Public |
| [robot_action_composer](5-robot_action_composer.md) | Task-queue YAML / motion generation | Public |
| [HUG](6-hug.md) | Grasp inference | Private |
| [wuji-retargeting](7-wuji_retargeting.md) | Hand retargeting | Public |

Datagen pipeline (Isaac USD → composer → LeRobot record/export): [Synthetic Data](../../2-how_to/7-synthetic_data/0-index.md).
