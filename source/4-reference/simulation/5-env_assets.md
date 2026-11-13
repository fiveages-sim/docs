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
:::{code-block} none
FaSim-Isaac/
└── environment/
    └── fiveages_env/    # → fiveages-env-usds
:::

### Usage

Start Isaac with FaSim `./run.sh` and open the scene USD under `environment/fiveages_env/`.

## fa-project-usd

**Repository:** [fa-project-usd](https://github.com/fiveages-sim/fa-project-usd) (private; the link needs access)

```{admonition} Access Required
:class: warning

This repository is private.
```

### Purpose

Internal project-specific USD scenes and assets.

### Location

:::{code-block} none
FaSim-Isaac/
└── environment/
    └── fa-project-usd/
:::

## Not robot_usds Submodules

```{admonition} Important
:class: note

Environment assets are **not** submodules of `robot_usds`. They are:
- Sibling directories in FaSim-Isaac
- Separate submodules of FaSim-Isaac itself
```

## Usage in FaSim

Start Isaac with FaSim `./run.sh` (PhysX / Newton / Headless Streaming menu). Open the scene USD under `environment/fiveages_env/` (or `fa-project-usd/`) in Isaac. There is no `./run.sh --env` flag.

## Creating Custom Environments

1. Create the USD scene in Isaac Sim.
2. Put it under `environment/fiveages_env/` or, with access, under [fa-project-usd](https://github.com/fiveages-sim/fa-project-usd).
3. Open that file from `./run.sh`. On `main`, a project is `scene.usd(a)`, `objects/`, and `env/` ([README](https://github.com/fiveages-sim/fa-project-usd/blob/main/README.md)). `robot.yaml`, `task_configs/`, and `maps/` or `map/` sit on branch `feature/sinopec-test-tube-picking` (ahead of `main`, not merged).

## Related

- [robot_usds](3-robot_usds.md)
- [FaSim-Isaac](2-fasim_isaac.md)
