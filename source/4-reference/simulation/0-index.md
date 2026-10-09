# Simulation Reference

This section documents the simulation backends and USD assets.

## Overview

The stack supports multiple simulation backends. **FaSim** is Isaac Sim high-fidelity simulation combined with the same ROS 2 运控 as the real robot, so you get matching motion plus simulation ground truth.

| Backend | Use Case |
|---------|----------|
| Mock | Fast testing, no physics (`hardware:=mock_components`) |
| Gazebo Harmonic | Physics simulation |
| FaSim / Isaac Sim | High-fidelity USD; same 运控 as hardware + sim ground truth |

## In This Section

```{toctree}
:maxdepth: 1

1-gazebo
2-fasim_isaac
3-robot_usds
4-usd_submodules
5-env_assets
```

## Quick Comparison

| Aspect | Mock | Gazebo | Isaac |
|--------|------|--------|-------|
| Physics | No | Yes | Yes (PhysX) |
| Rendering | RViz only | Basic | Photorealistic |
| Setup | None | `apt install` | FaSim-Isaac `./init.sh` + `./run.sh` |
| Speed | Real-time | ~Real-time | Configurable |
| USD support | No | No | Native |

```{admonition} Isaac Sim Requirements
:class: warning

Isaac Sim integration uses **FaSim-Isaac** (`./init.sh`, `./run.sh`). Default path is `ISAACSIM_DIR` (`~/isaacsim`); version comes from FaSim config / the init menu. See [FaSim-Isaac](2-fasim_isaac.md).
```

Isaac **datagen** (USD → orchestration → LeRobot export, no Gazebo): [Synthetic Data](../../2-how_to/7-synthetic_data/0-index.md).
