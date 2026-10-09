# FiveAges Sim Documentation

Welcome to the documentation for **FiveAges Sim** — a multi-repository ROS 2 robotics ecosystem for control, simulation, and deployment developed by [FiveAges](https://github.com/fiveages-sim).

```{admonition} Getting Started
:class: tip

New here? Start with the [Learning Path](0-overview/2-learning_path.md), then [Install Environment](1-getting_started/2-install_environment.md), then [Quick Demo (Public Path)](1-getting_started/1-quick_demo_public.md). Do not skip install.
```

## About This Ecosystem

FiveAges Sim provides:

- **Unified robot descriptions** — URDF/xacro packages for wheeled-arm humanoids, manipulators, and mobile robots
- **Hardware interfaces** — ROS 2 control hardware plugins for various robot platforms (Dobot, ARX, Galbot, HighTorque, and more)
- **MPC controllers** — OCS2-based arm (分体控制) and 全身控制
- **Simulation backends** — Gazebo Harmonic, and **FaSim** (Isaac Sim high-fidelity + ROS 2 运控, matching real-robot motion plus ground truth)
- **Teleop solutions** — VR, isomorphic teleop, DexCap, and glove-based teleoperation
- **Python libraries** — High-level interfaces for robot control and data collection
- **Synthetic data pipeline** — Isaac USD scenes, task-queue orchestration, LeRobot record/export

## Two Entry Paths

| Path | Workspace | Audience |
|------|-----------|----------|
| **Public** | `open-deploy-ws` | External users, OSS contributors; public submodules only |
| **Internal** | `fa-deploy-ws` | FiveAges team; FA wheeled-arm humanoids (W2/W2R/S2/S2R) + dual-arm systems |

Start with the [public path](1-getting_started/3-open_deploy_ws.md) if you're new. Internal users should read [fa-deploy-ws setup](1-getting_started/4-fa_deploy_ws.md) after getting familiar with the stack.

## Documentation Structure

```{toctree}
:maxdepth: 2
:caption: Overview

0-overview/0-index
0-overview/1-architecture
0-overview/2-learning_path
0-overview/3-repo_map
0-overview/4-public_vs_internal
```

```{toctree}
:maxdepth: 2
:caption: Getting Started

1-getting_started/0-index
1-getting_started/2-install_environment
1-getting_started/1-quick_demo_public
1-getting_started/3-open_deploy_ws
1-getting_started/4-fa_deploy_ws
1-getting_started/5-faq
```

```{toctree}
:maxdepth: 2
:caption: More applications

6-more_applications/0-index
6-more_applications/1-field_commissioning
6-more_applications/2-classical_algorithm
6-more_applications/3-vla_collect_train_deploy
6-more_applications/4-simulation_engineer
```

```{toctree}
:maxdepth: 3
:caption: How-To Guides

2-how_to/0-index
2-how_to/1-basic_operations/0-index
2-how_to/2-simulation/0-index
2-how_to/3-programming/0-index
2-how_to/4-controllers/0-index
2-how_to/5-teleoperation/0-index
2-how_to/6-deployment/0-index
2-how_to/7-synthetic_data/0-index
```

```{toctree}
:maxdepth: 2
:caption: Concepts

3-concepts/0-index
3-concepts/8-terminology
3-concepts/1-ros2_control_here
3-concepts/2-workspace_layout
3-concepts/3-naming_conventions
3-concepts/4-fsm_and_topics
3-concepts/7-split_vs_wbc
3-concepts/5-source_vs_deb
3-concepts/6-submodules_visibility
```

```{toctree}
:maxdepth: 2
:caption: Reference

4-reference/descriptions/0-index
4-reference/hardware/0-index
4-reference/controllers/0-index
4-reference/simulation/0-index
4-reference/teleop/0-index
4-reference/python_apps/0-index
```

```{toctree}
:maxdepth: 2
:caption: Developer Guide

5-developer/0-index
5-developer/1-contributing
5-developer/2-docs_build
5-developer/3-packaging_deb
```

## Quick Links

- [GitHub Organization](https://github.com/fiveages-sim)
- [OCS2 ROS 2 Port](https://github.com/legubiao/ocs2_ros2)
- [Report Documentation Issues](https://github.com/fiveages-sim/docs/issues)
