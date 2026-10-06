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
| Setup | None | `apt install` | Isaac Sim 6.1 |
| Speed | Real-time | ~Real-time | Configurable |
| USD support | No | No | Native |

```{admonition} Isaac Sim Requirements
:class: warning

Isaac Sim integration requires **Isaac Sim 6.1** installed at **`~/isaacsim`**. See [FaSim-Isaac](2-fasim_isaac.md) for details.
```
