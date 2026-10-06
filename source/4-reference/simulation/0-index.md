# Simulation Reference

This section documents the simulation backends and USD assets.

## Overview

The stack supports multiple simulation backends:

| Backend | Use Case |
|---------|----------|
| Mock | Fast testing, no physics |
| Gazebo Harmonic | Physics simulation |
| Isaac Sim | High-fidelity, USD assets |

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

Isaac **datagen** (USD → orchestration → LeRobot export, no Gazebo): [Synthetic Data](../../6-synthetic_data/0-index.md).
