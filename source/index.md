# FiveAges Sim Documentation

Welcome to the documentation for **FiveAges Sim** — a multi-repository ROS 2 robotics ecosystem for control, simulation, and deployment developed by [FiveAges](https://github.com/fiveages-sim).

```{admonition} Getting Started
:class: tip

New here? Start with the [Learning Path](0-overview/2-learning_path.md) to understand the stack, then follow [Quick Demo (Public Path)](1-getting_started/1-quick_demo_public.md) to get a robot moving in simulation within minutes.
```

## About This Ecosystem

FiveAges Sim provides:

- **Unified robot descriptions** — URDF/xacro packages for wheeled-arm humanoids, manipulators, and mobile robots
- **Hardware interfaces** — ROS 2 control plugins for various robot platforms (Dobot, ARX, Galbot, HT, and more)
- **MPC controllers** — OCS2-based arm and whole-body controllers
- **Simulation backends** — Gazebo Harmonic and NVIDIA Isaac Sim integration
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
1-getting_started/1-quick_demo_public
1-getting_started/2-install_environment
1-getting_started/3-open_deploy_ws
1-getting_started/4-fa_deploy_ws
1-getting_started/5-faq
```

```{toctree}
:maxdepth: 2
:caption: How-To Guides

2-how_to/0-index
2-how_to/1-run_mock_demo
2-how_to/2-switch_robot
2-how_to/3-gazebo_sim
2-how_to/4-isaac_sim
2-how_to/5-python_interface
2-how_to/6-vr_teleop
2-how_to/7-isomorphic_teleop
2-how_to/8-dexcap_teleop
2-how_to/9-go_real_hardware
2-how_to/10-add_a_robot
```

```{toctree}
:maxdepth: 2
:caption: Concepts

3-concepts/0-index
3-concepts/1-ros2_control_here
3-concepts/2-workspace_layout
3-concepts/3-naming_conventions
3-concepts/4-fsm_and_topics
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

```{toctree}
:maxdepth: 2
:caption: Synthetic Data

6-synthetic_data/0-index
6-synthetic_data/1-isaac_scenes
6-synthetic_data/2-orchestration
6-synthetic_data/3-record_export
```

## Quick Links

- [GitHub Organization](https://github.com/fiveages-sim)
- [OCS2 ROS 2 Port](https://github.com/legubiao/ocs2_ros2)
- [Report Documentation Issues](https://github.com/fiveages-sim/docs/issues)
