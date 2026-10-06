# Environment Assets

USD environment and scene assets for simulation.

## Overview

Environment assets are separate from robot assets:
- **robot_usds** — Robot models
- **Environment assets** — Scenes, objects, terrain

## fiveages-env-usds

**Repository:** [fiveages-sim/fiveages-env-usds](https://github.com/fiveages-sim/fiveages-env-usds)

### Purpose

Public environment USD assets:
- Indoor scenes (office, lab)
- Objects for manipulation
- Terrain

### Location

In FaSim-Isaac:
```
FaSim-Isaac/
└── environment/
    └── fiveages_env/    # → fiveages-env-usds
```

### Usage

```python
# Load environment in Isaac Sim
from omni.isaac.core.utils.stage import add_reference_to_stage

add_reference_to_stage(
    usd_path="environment/fiveages_env/office.usd",
    prim_path="/World/Environment"
)
```

## fa-project-usd

**Repository:** fa-project-usd (private)

```{admonition} Access Required
:class: warning

This repository is private.
```

### Purpose

Internal project-specific USD scenes and assets.

### Location

```
FaSim-Isaac/
└── environment/
    └── fa-project-usd/
```

## Not robot_usds Submodules

```{admonition} Important
:class: note

Environment assets are **not** submodules of `robot_usds`. They are:
- Sibling directories in FaSim-Isaac
- Separate submodules of FaSim-Isaac itself
```

## Usage in FaSim

FaSim-Isaac configuration selects environment:

```yaml
# FaSim config
environment:
  name: fiveages_env
  scene: office
```

Or via command line:

```bash
./run.sh --env office
```

## Creating Custom Environments

1. Create USD scene in Isaac Sim
2. Export to `environment/` directory
3. Reference in configuration

```python
# Custom scene setup
scene_path = "environment/custom_scene.usd"
```

## Related

- [robot_usds](3-robot_usds.md)
- [FaSim-Isaac](2-fasim_isaac.md)
