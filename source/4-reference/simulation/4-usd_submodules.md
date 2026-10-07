# USD Submodules

Details on USD submodules referenced by `robot_usds`.

## In-Scope Submodules

These are the only USD repositories in scope for this documentation (based on `robot_usds/.gitmodules`):

| Path | Repository | Description |
|------|------------|-------------|
| `humanoid/FiveAges/Gen1` | fiveages-gen1-robot-usds | W1 / Gen1 (private remote) |
| `humanoid/FiveAges/Gen2` | fiveages-gen2-robot-usds | W2 / S2 / Gen2 (private remote) |
| `humanoid/FiveAges/Gen3` | fiveages-gen3-robot-usds | WCE3 / Gen3 (private remote) |
| `humanoid/Galbot` | galbot-usds | Galbot mobile manipulator |
| `humanoid/Ubtech` | ubtech-usds | Ubtech humanoid |

## Gen1/Gen2/Gen3

FiveAges robot USD assets organized by generation. Names below are from the [robot_usds README](https://github.com/fiveages-sim/robot_usds/blob/main/README.md) Humanoid → FiveAges table. The remotes are private (404 without access). URDF gitlinks: [FiveAges robot descriptions](../descriptions/4-fiveages_umbrella.md).

### Gen1

**Repository:** fiveages-gen1-robot-usds

README name: **W1**. Path: `humanoid/FiveAges/Gen1`.

### Gen2

**Repository:** fiveages-gen2-robot-usds

README names: **W2 / S2**. Path: `humanoid/FiveAges/Gen2`.

### Gen3

**Repository:** fiveages-gen3-robot-usds

README name: **WCE3**. Path: `humanoid/FiveAges/Gen3`.

## Galbot

**Repository:** [fiveages-sim/galbot-usds](https://github.com/fiveages-sim/galbot-usds)

Galbot mobile manipulator USD assets.

### Contents

- Robot USD model
- Textures and materials
- Physics properties

## Ubtech

**Repository:** ubtech-usds

Ubtech humanoid USD assets.

Note: Referenced as a `robot_usds` submodule; minimal separate documentation.

## Out of Scope

The following USD repositories are **not** documented as they are not referenced in `robot_usds/.gitmodules`:

- `fa-w2-usds` — Not in current gitmodules
- `agibot-g2-usds` — Not in current gitmodules
- `marvin-usds` — Obsolete/unreferenced

## Updating Submodules

### Check Current Pins

```bash
cd robot_usds
git submodule status
```

### Update to Latest

```bash
git submodule update --remote humanoid/Galbot
```

### Pin to Specific Commit

```bash
cd humanoid/Galbot
git checkout <commit>
cd ../..
git add humanoid/Galbot
git commit -m "Pin Galbot to <commit>"
```

## Related

- [robot_usds](3-robot_usds.md)
- [FaSim-Isaac](2-fasim_isaac.md)
