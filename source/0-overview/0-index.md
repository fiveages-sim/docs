# Overview

This section introduces the FiveAges Sim ecosystem — what it is, how its components fit together, and how to navigate the documentation.

## What is FiveAges Sim?

FiveAges Sim is a collection of ROS 2 packages and workspaces that enable:

- **Robot Description** — URDF/xacro models with ros2_control integration
- **Hardware Control** — Interface plugins for real robot hardware
- **MPC Controllers** — OCS2-based motion planning and control
- **Simulation** — Gazebo Harmonic and NVIDIA Isaac Sim backends
- **Teleoperation** — VR, isomorphic teleop, and glove-based control
- **Python Applications** — High-level APIs for data collection and autonomous tasks

```{admonition} Terminology
:class: note

In this documentation, **humanoid** means a **wheeled-arm humanoid** (mobile base + arms, e.g. FiveAges W2/W2R). It does **not** mean a bipedal or footed humanoid.
```

## Public vs Internal

The ecosystem has two entry points:

| Path | Workspace | Audience | Robots |
|------|-----------|----------|--------|
| **Public** | [open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws) | Open source users | Dobot CR5, ARX ACone, Galbot, HT Panthera, etc. |
| **Internal** | fa-deploy-ws | FiveAges team | W2, W2R, S2, S2R, dual-arm CCS |

**If you're new**, start with the public path. It uses only public submodules and can run demos without special access.

```{admonition} Real Hardware on Public Path
:class: tip

**ARX Acone** and **HT Panthera** are fully supported for real hardware deployment on the public path. External users can deploy to these physical robots without needing private repository access.
```

## Documentation Map

- **[Architecture](1-architecture.md)** — Layer diagram and dependency relationships
- **[Learning Path](2-learning_path.md)** — Day-by-day onboarding guide
- **[Repository Map](3-repo_map.md)** — Complete list of repositories by layer
- **[Public vs Internal](4-public_vs_internal.md)** — Detailed comparison of the two paths

## Next Steps

1. Review the [Architecture](1-architecture.md) to understand component relationships
2. Follow the [Learning Path](2-learning_path.md) for structured onboarding
3. Jump to [Quick Demo](../1-getting_started/1-quick_demo_public.md) to see a robot move
