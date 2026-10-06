# Robot Descriptions Reference

This section documents the robot description packages — URDF/xacro models, meshes, and ros2_control configurations.

```{admonition} Terminology
:class: note

FiveAges **humanoid** descriptions (W2, W2R, S2, S2R) are **wheeled-arm humanoids** (mobile base + arms). They are **not** bipedal or footed humanoids.
```

## Overview

Robot descriptions are organized in a hierarchy:

:::{code-block} none
robot_descriptions (umbrella)
├── robot-descriptions-common
├── robot-descriptions-dobot
├── robot-descriptions-arx
├── robot-descriptions-galbot
├── robot-descriptions-ht
├── robot-descriptions-quadruped
└── ... (brand packages)
:::

## In This Section

```{toctree}
:maxdepth: 1

1-robot_descriptions
2-common
3-brand_public
4-fiveages_umbrella
5-fa_robots
6-vendor_arms_private
```

## Quick Reference

| Package | Robots | Visibility |
|---------|--------|------------|
| [robot_descriptions](1-robot_descriptions.md) | Umbrella | Public |
| [robot-descriptions-common](2-common.md) | Grippers, sensors | Public |
| [Brand packages](3-brand_public.md) | Dobot, ARX, Galbot, HT | Public |
| [robot-descriptions-fiveages](4-fiveages_umbrella.md) | FA robots | Private |
| [FA robot descriptions](5-fa_robots.md) | W2, S2, etc. | Private |
| [Vendor arms](6-vendor_arms_private.md) | Tianji, Rokae, etc. | Private |
