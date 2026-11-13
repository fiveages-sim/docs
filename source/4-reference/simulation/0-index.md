# Simulation Reference

This section is the reference for the simulation backends and their USD assets. It explains what each piece is, how the pieces fit, and which parameters or layouts are in the current trees. Step-by-step start, launch, and first checks live in the How-To pages.

**FaSim** is NVIDIA Isaac Sim plus the same ROS 2 运控 stack used on the real robot, so motion can match hardware while the sim supplies ground truth. FaSim-Isaac is more than a place to open a USD: it also installs the OmniGraph extensions that start 运控 inside Sim and that drive a swerve chassis.

## Isaac Sim reading order

Use the pages in this order. Each one points at a specific section when you need more detail; they do not repeat the full mechanism.

1. **Prepare the machine and start Sim** — [Isaac Sim](../../2-how_to/2-simulation/4-isaac_sim.md): `./init.sh`, `./run.sh`, and the first ROS 2 connection.
2. **Robot USD assets** — [robot_usds](3-robot_usds.md): the `robots/` tree, its git submodules, and public versus private checkout.
3. **FaSim extensions** — [FaSim-Isaac](2-fasim_isaac.md): how the `isaac` / `isaac_sim` hardware keys differ from the Kit extensions, then the [ROS 2 Control extension](2-fasim_isaac.md#ros-2-control-extension) and the [swerve extension](2-fasim_isaac.md#swerve-extension).
4. **Scenes and project layout** — [Environment assets](5-env_assets.md): public scenes, ArtVIP / LabUtopia components, and private project USD (including where `robot.yaml` currently lives).
5. **Run, check, and debug** — [When it fails](../../2-how_to/2-simulation/4-isaac_sim.md#when-it-fails) on the How-To page. Clock and TF details stay in [Clock](2-fasim_isaac.md#clock) and [TF](2-fasim_isaac.md#tf).

Gazebo is a separate backend: [Gazebo](1-gazebo.md), with steps in [Gazebo Simulation](../../2-how_to/2-simulation/3-gazebo_sim.md).

Isaac **datagen** (USD → orchestration → LeRobot export, not Gazebo): [Synthetic Data](../../2-how_to/7-synthetic_data/0-index.md).

## In This Section

```{toctree}
:maxdepth: 1

1-gazebo
2-fasim_isaac
3-robot_usds
5-env_assets
```

## Quick Comparison

| Aspect | Mock | Gazebo | Isaac |
|--------|------|--------|-------|
| Physics | No | Yes | Yes (PhysX or Newton, chosen in `./run.sh`) |
| Rendering | RViz only | Basic | Photorealistic |
| Setup | None | `apt install` | FaSim-Isaac `./init.sh` + `./run.sh` |
| Speed | Real-time | ~Real-time | Configurable |
| USD support | No | No | Native |

```{admonition} Isaac Sim Requirements
:class: warning

Isaac Sim integration uses **FaSim-Isaac** (`./init.sh`, `./run.sh`). Default path is `ISAACSIM_DIR` (`~/isaacsim`); the optional ROS 2 overlay version comes from FaSim config / the init menu. See [FaSim-Isaac](2-fasim_isaac.md).
```
