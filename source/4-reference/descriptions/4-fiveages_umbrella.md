# robot-descriptions-fiveages

Private umbrella for FiveAges robot descriptions.

```{admonition} Access Required
:class: warning

This package requires private repository access. Contact your team lead for access.
```

## Purpose

`robot-descriptions-fiveages` aggregates all FiveAges wheeled-arm humanoid and arm descriptions:
- FA wheeled-arm humanoids (W2, W2R, S2, S2R)
- FA-specific components
- Vendor arm integrations (Tianji, Rokae)

## Structure

:::{code-block} none
robot-descriptions-fiveages/
├── common/                    # Shared FA components
│   └── fa-w2-components/
├── arms/                      # Arm descriptions
│   ├── robot-descriptions-tianji/
│   ├── robot-descriptions-rokae/
│   └── ...
└── robot/                     # Complete robot descriptions
    ├── fa-w2-description/
    ├── fa-w2r-description/
    ├── fa-s2-description/
    └── fa-s2r-description/
:::

## Usage

### Via fa-deploy-ws

```bash
cd fa-deploy-ws
./init_repo.sh --robot fiveages_w2
```

### Simulation Only

For simulation without full deployment:

```bash
cd robot-descriptions-fiveages
./scripts/init-sim.sh
```

This initializes only common and robot folders, skipping hardware-specific components.

## Initialization

### Full Init (via fa-deploy-ws)

```bash
./init_repo.sh --robot <robot_id>
```

### Selective Init

```bash
# Common components only
git submodule update --init common/fa-w2-components

# Specific robot
git submodule update --init robot/fa-w2-description
```

## Nested Structure

Each robot description may include additional submodules:

:::{code-block} none
fa-w2-description/
├── urdf/
├── meshes/
├── config/
└── components/          # Nested component references
:::

## Launch Integration

Descriptions integrate with `fa-deploy-ws` launches:

```bash
ros2 launch fiveages_bringup bringup.launch.py robot:=fiveages_w2
```

## Related

- [FA Robot Descriptions](5-fa_robots.md)
- [fa-deploy-ws Setup](../../1-getting_started/4-fa_deploy_ws.md)
