# Introduction

This section introduces the FiveAges Sim ecosystem — what it is, how its components fit together, and how to navigate the documentation.

## What is FiveAges Sim?

FiveAges Sim is a collection of ROS 2 packages and workspaces that enable:

- **Robot Description** — URDF/xacro models with ros2_control integration
- **Hardware interfaces** — ros2_control hardware plugins for real or simulated robots
- **MPC Controllers** — OCS2-based motion planning and control (分体控制 / 全身控制)
- **Simulation** — Gazebo Harmonic, and **FaSim** (Isaac Sim high-fidelity + the same ROS 2 运控 as the real robot, plus simulation ground truth)
- **Teleoperation** — VR, isomorphic teleop, and glove-based control
- **Python Applications** — High-level APIs for data collection and autonomous tasks
- **Synthetic data** — Isaac Sim USD → interface → composer → LeRobot record/export ([Synthetic Data](../2-how_to/7-synthetic_data/0-index.md))

```{admonition} Terminology
:class: note

In this documentation, **humanoid** means a **wheeled-arm humanoid** (mobile base + arms, e.g. FiveAges W2/W2R). It does **not** mean a bipedal or footed humanoid.
```

## Public vs Internal

The ecosystem has two entry points:

| Path | Workspace | Audience | Robots |
|------|-----------|----------|--------|
| **Public** | [open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws) | Open source users | Dobot CR5, ARX Lift 2S, Acone (dual-arm), Galbot, HighTorque Panthera HT, etc. |
| **Internal** | fa-deploy-ws | FiveAges team | W2, W2R, S2, S2R, dual-arm CCS |

**If you're new**, start with the public path. It uses only public submodules and can run demos without special access.

```{admonition} Real Hardware on Public Path
:class: tip

**ARX Lift 2S** (full-body mobile manipulator, including chassis) and **HighTorque Panthera HT** (dual-arm manipulator) have dedicated `open-deploy-ws` branches. **Acone** / **AC One** is **dual-arm**, not the Lift 2S platform. See [ARX Lift 2S](../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md) and [HighTorque Panthera HT](../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md).
```

## Documentation Map

- **[Architecture](1-architecture.md)** — Layer diagram and dependency relationships
- **[Terminology](../3-concepts/8-terminology.md)** — 驱动层 ↔ Hardware Interface, 分体 / 全身, 夹爪 / 灵巧手, simulation keys
- **[Learning Path](2-learning_path.md)** — Day-by-day onboarding guide
- **[Repository Map](3-repo_map.md)** — Complete list of repositories by layer
- **[Public vs Internal](4-public_vs_internal.md)** — Detailed comparison of the two paths
- **[Synthetic Data](../2-how_to/7-synthetic_data/0-index.md)** — Isaac datagen pipeline (USD → orchestration → LeRobot export)

## Next Steps

1. Review the [Architecture](1-architecture.md) to understand component relationships
2. Follow the [Learning Path](2-learning_path.md) for structured onboarding
3. [Install Environment](../1-getting_started/2-install_environment.md), then [Quick Demo](../1-getting_started/1-quick_demo_public.md)
