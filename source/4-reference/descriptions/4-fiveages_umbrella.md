# FiveAges robot descriptions

One page for FiveAges (中科第五纪) wheeled-arm humanoid **URDF** packages and their **public USD** mapping.

```{admonition} Access Required
:class: warning

FiveAges URDF remotes and `fa-deploy-ws` are **private** (GitHub 404 without access). Contact your team lead. After access, follow **those package READMEs** and that workspace’s init scripts.
```

```{admonition} Source of truth
:class: important

- URDF gitlinks: [robot_descriptions `.gitmodules` on `main`](https://github.com/fiveages-sim/robot_descriptions/blob/main/.gitmodules) and the [same file on `feature/agilex`](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/.gitmodules)
- On-disk path: `humanoid/FiveAges/` inside the public [robot_descriptions](https://github.com/fiveages-sim/robot_descriptions) umbrella. There is **no** public `robot-descriptions-fiveages` repo (404)
- The public [robot_descriptions README](https://github.com/fiveages-sim/robot_descriptions/blob/main/README.md) **does not** table these packages — use `.gitmodules`, not the README brand tables
- Public USD: [robot_usds README](https://github.com/fiveages-sim/robot_usds/blob/main/README.md) §3.1 Humanoid → FiveAges
- Workspace pattern (script name only): [fa-deploy-ws Setup](../../1-getting_started/4-fa_deploy_ws.md) — `./init_repo.sh`. Extra flags and robot IDs are in that private README after access.
- Public launch / `hardware:=`: [robot_common_launch](2-common.md) (`mock_components` / `gz` / `isaac` / `real`)
```

FiveAges **humanoid** platforms in this docs set (W1, W2, W2R, S2, S2R, WCE3) are **wheeled-arm humanoids** (mobile base + arms), not bipedal.

## URDF packages (`robot_descriptions`)

FiveAges descriptions are **private git submodules** of the public umbrella. Checkout names and remotes below are from `.gitmodules`. The remotes themselves 404 without access; launch files, xacro trees, and controller YAML are in those package READMEs.

### `main` (flat under `humanoid/FiveAges/`)

| Path | Package dir | Remote |
|------|-------------|--------|
| `humanoid/FiveAges/fiveages_w1_description` | `fiveages_w1_description` | `fa-w1-description` |
| `humanoid/FiveAges/fiveages_w2_description` | `fiveages_w2_description` | `fa-w2-description` |
| `humanoid/FiveAges/fiveages_w2r_description` | `fiveages_w2r_description` | `fa-w2r-description` |
| `humanoid/FiveAges/fiveages_s2_description` | `fiveages_s2_description` | `fa-s2-description` |
| `humanoid/FiveAges/fiveages_w2_common_description` | `fiveages_w2_common_description` | `fa-w2-components` |

`main` has **no** `fiveages_s2r_description` and **no** `fiveages_wce3_description` gitlink.

### `feature/agilex` (grouped like USD: Gen1 / Gen2 / Gen3)

| Gen | Path | Package dir | Remote |
|-----|------|-------------|--------|
| Gen1 | `humanoid/FiveAges/Gen1/fiveages_w1_description` | `fiveages_w1_description` | `fa-w1-description` |
| Gen2 | `humanoid/FiveAges/Gen2/fiveages_w2_description` | `fiveages_w2_description` | `fa-w2-description` |
| Gen2 | `humanoid/FiveAges/Gen2/fiveages_w2r_description` | `fiveages_w2r_description` | `fa-w2r-description` |
| Gen2 | `humanoid/FiveAges/Gen2/fiveages_s2_description` | `fiveages_s2_description` | `fa-s2-description` |
| Gen2 | `humanoid/FiveAges/Gen2/fiveages_s2r_description` | `fiveages_s2r_description` | `fa-s2r-description` |
| Gen2 | `humanoid/FiveAges/Gen2/fiveages_w2_common_description` | `fiveages_w2_common_description` | `fa-w2-components` |
| Gen3 | `humanoid/FiveAges/Gen3/fiveages_wce3_description` | `fiveages_wce3_description` | `fa-wce3-description` |

Do not recursive-init these from `open-deploy-ws`; visibility is private. After access, init the path named in `.gitmodules` (or let `fa-deploy-ws` `./init_repo.sh` do it).

## Public: Isaac USD (`robot_usds`)

[robot_usds](https://github.com/fiveages-sim/robot_usds) maps FiveAges assets under `robots/humanoid/FiveAges/` as **Git submodules** (private USD repos). From that README:

| Path (under `robot_usds` root) | Upstream | README names |
|--------------------------------|----------|--------------|
| `humanoid/FiveAges/Gen1` | [fiveages-gen1-robot-usds](https://github.com/fiveages-sim/fiveages-gen1-robot-usds) | W1 / Gen1 |
| `humanoid/FiveAges/Gen2` | [fiveages-gen2-robot-usds](https://github.com/fiveages-sim/fiveages-gen2-robot-usds) | W2 / S2 / Gen2 |
| `humanoid/FiveAges/Gen3` | [fiveages-gen3-robot-usds](https://github.com/fiveages-sim/fiveages-gen3-robot-usds) | WCE3 / Gen3 |

Those three USD remotes and their READMEs are **not public**. Load assets through FaSim-Isaac (`./init.sh` / `./run.sh`) and that robot’s USDA.

Checkout: FaSim-Isaac **`./init.sh`** (operation that inits `robots/` via `submodules_visibility.conf`), then **`./run.sh`**. See [robot_usds](../simulation/3-robot_usds.md).

## Private: deploy

`fa-deploy-ws` is internal. Extra flags and robot IDs live in **that** README — not here.

After access:

1. Read the private package README for the checkout you have (not this page).
2. In `fa-deploy-ws`, run **`./init_repo.sh`** (do not recursive-init). Extra flags live in that README.
3. `colcon build`, then `source install/setup.bash` in the launch terminal (or that repo’s official quick-start script if it has one).
4. EEF / `hardware:=` follow [robot_common_launch](2-common.md). There is no `gripper:=` and no `hardware:=mock`.

Composer `--robot fiveages_w2` is a real key on [robot_action_composer ROS2_STACK.md](https://github.com/fiveages-sim/robot_action_composer/blob/feature/dex-grasp-generator/docs/ROS2_STACK.md). It is **not** a documented `./init_repo.sh --robot` flag.

Copy an existing public `{robot}_description` only as a **layout hint** — [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md).

## Related

- [fa-deploy-ws Setup](../../1-getting_started/4-fa_deploy_ws.md)
- [robot_usds](../simulation/3-robot_usds.md)
- [robot_common_launch](2-common.md)
- [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md)
- [WBC controller](../controllers/3-ocs2_wbc.md)
