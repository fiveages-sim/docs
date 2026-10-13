# Robot Descriptions Reference

This section documents the robot description packages — URDF/xacro models, meshes, and ros2_control configurations.

```{admonition} Terminology
:class: note

FiveAges **humanoid** descriptions (W1, W2, W2R, S2, S2R, WCE3) are **wheeled-arm humanoids** (mobile base + arms). They are **not** bipedal or footed humanoids.
```

## Overview

Robot descriptions are organized in a hierarchy:

:::{code-block} none
robot_descriptions/                 # umbrella paths from its README
├── common/                         # robot-descriptions-common
├── quadruped/
├── humanoid/                       # in-tree + Galbot; FiveAges = public W1/W2/S2 + private W2R/S2R gitlinks
└── manipulator/                    # Dobot, ARX, Tianji, Rokae, HighTorque, …
:::

## In This Section

```{toctree}
:maxdepth: 1

1-robot_descriptions
2-common
3-brand_public
4-fiveages_umbrella
6-vendor_arms
```

## Quick Reference

| Package | Robots | Visibility |
|---------|--------|------------|
| [robot_descriptions](1-robot_descriptions.md) | Umbrella | Public |
| [robot-descriptions-common](2-common.md) | Grippers, hands, sensors, `robot_common_launch` (path `common`) | Public |
| [Brand packages](3-brand_public.md) | Dobot, ARX, Galbot, HighTorque | Public |
| [FiveAges descriptions](4-fiveages_umbrella.md) | `humanoid/FiveAges/*` URDF gitlinks + Gen1/2/3 USD | Public W1/W2/S2 + components + Gen1/Gen2 USD; W2R, S2R, Gen3 still private |
| [Vendor arms](6-vendor_arms.md) | Tianji, Rokae, Gento (public remotes); Fairino, Agibot G2 (private) | Public remotes + private remotes |
