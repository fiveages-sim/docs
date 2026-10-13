# FiveAges robot descriptions

One page for FiveAges (中科第五纪) wheeled-arm humanoid **URDF** packages and their **USD** mapping.

```{admonition} Public now (Gen1 W1 + Gen2 W2 / S2 + components + USD)
:class: tip

These remotes are public (HTTPS):

- URDF: [fa-w1-description](https://github.com/fiveages-sim/fa-w1-description) (W1 / Gen1), [fa-w2-description](https://github.com/fiveages-sim/fa-w2-description) (W2), [fa-s2-description](https://github.com/fiveages-sim/fa-s2-description) (S2), [fa-w2-components](https://github.com/fiveages-sim/fa-w2-components) (shared Gen2 components)
- USD: [fiveages-gen1-robot-usds](https://github.com/fiveages-sim/fiveages-gen1-robot-usds) (W1; `robot_usds` path `humanoid/FiveAges/Gen1`) and [fiveages-gen2-robot-usds](https://github.com/fiveages-sim/fiveages-gen2-robot-usds) (`W2/`, `S2/`, `components/`; path `humanoid/FiveAges/Gen2`)

Launch names and xacro details: those **public package READMEs**. There is no `open-deploy-ws` Gen1 or Gen2 branch.
```

```{admonition} Still private — W2R and S2R are not open
:class: warning

These remotes are **not** public (GitHub 404 without access): **W2R** (`fa-w2r-description`), **S2R** (`fa-s2r-description`), **Gen3** (`fa-wce3-description`, `fiveages-gen3-robot-usds`), and `fa-deploy-ws`. There is **no** public `robot-descriptions-fiveages` umbrella. Contact your team lead. After access, follow **those package READMEs**.
```

```{admonition} Source of truth
:class: important

- URDF gitlinks: [robot_descriptions `.gitmodules` on `main`](https://github.com/fiveages-sim/robot_descriptions/blob/main/.gitmodules) and the [same file on `feature/agilex`](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/.gitmodules)
- On-disk path: `humanoid/FiveAges/` inside the public [robot_descriptions](https://github.com/fiveages-sim/robot_descriptions) umbrella
- The public [robot_descriptions README](https://github.com/fiveages-sim/robot_descriptions/blob/main/README.md) **does not** table these packages — use `.gitmodules`, not the README brand tables
- Public USD: [robot_usds README](https://github.com/fiveages-sim/robot_usds/blob/main/README.md) §3.1 Humanoid → FiveAges, [fiveages-gen1-robot-usds](https://github.com/fiveages-sim/fiveages-gen1-robot-usds), [fiveages-gen2-robot-usds](https://github.com/fiveages-sim/fiveages-gen2-robot-usds)
- Workspace pattern (script name only): [fa-deploy-ws Setup](../../1-getting_started/4-fa_deploy_ws.md) — `./init_repo.sh`. Extra flags and robot IDs are in that private README after access.
- Public launch / `hardware:=`: [robot_common_launch](2-common.md) (`mock_components` / `gz` / `isaac` / `real`)
```

FiveAges **humanoid** platforms in this docs set (W1, W2, W2R, S2, S2R, WCE3) are **wheeled-arm humanoids** (mobile base + arms), not bipedal.

## URDF packages (`robot_descriptions`)

FiveAges descriptions live as **git submodules** of the public umbrella. Checkout names and remotes below are from `.gitmodules`.

**Public remotes** (W1, W2, S2, `fa-w2-components`): browse the HTTPS repos, or `git submodule update --init` the matching path on [robot_descriptions](https://github.com/fiveages-sim/robot_descriptions). Launch / xacro: each package README ([W1](https://github.com/fiveages-sim/fa-w1-description), [W2](https://github.com/fiveages-sim/fa-w2-description), [S2](https://github.com/fiveages-sim/fa-s2-description), [components](https://github.com/fiveages-sim/fa-w2-components)). W1 reuses Rokae `ar5_*` descriptions ([robot-descriptions-rokae](https://github.com/fiveages-sim/robot-descriptions-rokae)); W2 and S2 reuse Tianji `m6_ccs_description` ([robot-descriptions-tianji](https://github.com/fiveages-sim/robot-descriptions-tianji)). Those vendor remotes are **public**.

**Still private remotes** (**W2R**, **S2R**, Gen3): 404 without access. **W2R and S2R are not open yet.**

[`open-deploy-ws` `submodules_visibility.conf`](https://github.com/fiveages-sim/open-deploy-ws/blob/main/submodules_visibility.conf) still marks the FiveAges description paths `private`, so `./init_repo.sh` does **not** pull them. Do not recursive-init from `open-deploy-ws`. There is no public `open-deploy-ws` Gen1 or Gen2 branch.

### `main` (flat under `humanoid/FiveAges/`)

| Path | Package dir | Remote | Visibility |
|------|-------------|--------|------------|
| `humanoid/FiveAges/fiveages_w1_description` | `fiveages_w1_description` | [fa-w1-description](https://github.com/fiveages-sim/fa-w1-description) | Public |
| `humanoid/FiveAges/fiveages_w2_description` | `fiveages_w2_description` | [fa-w2-description](https://github.com/fiveages-sim/fa-w2-description) | Public |
| `humanoid/FiveAges/fiveages_w2r_description` | `fiveages_w2r_description` | `fa-w2r-description` | Private — **not open** |
| `humanoid/FiveAges/fiveages_s2_description` | `fiveages_s2_description` | [fa-s2-description](https://github.com/fiveages-sim/fa-s2-description) | Public |
| `humanoid/FiveAges/fiveages_w2_common_description` | `fiveages_w2_common_description` | [fa-w2-components](https://github.com/fiveages-sim/fa-w2-components) | Public |

`main` has **no** `fiveages_s2r_description` and **no** `fiveages_wce3_description` gitlink.

### `feature/agilex` (grouped like USD: Gen1 / Gen2 / Gen3)

| Gen | Path | Package dir | Remote | Visibility |
|-----|------|-------------|--------|------------|
| Gen1 | `humanoid/FiveAges/Gen1/fiveages_w1_description` | `fiveages_w1_description` | [fa-w1-description](https://github.com/fiveages-sim/fa-w1-description) | Public |
| Gen2 | `humanoid/FiveAges/Gen2/fiveages_w2_description` | `fiveages_w2_description` | [fa-w2-description](https://github.com/fiveages-sim/fa-w2-description) | Public |
| Gen2 | `humanoid/FiveAges/Gen2/fiveages_w2r_description` | `fiveages_w2r_description` | `fa-w2r-description` | Private — **not open** |
| Gen2 | `humanoid/FiveAges/Gen2/fiveages_s2_description` | `fiveages_s2_description` | [fa-s2-description](https://github.com/fiveages-sim/fa-s2-description) | Public |
| Gen2 | `humanoid/FiveAges/Gen2/fiveages_s2r_description` | `fiveages_s2r_description` | `fa-s2r-description` | Private — **not open** |
| Gen2 | `humanoid/FiveAges/Gen2/fiveages_w2_common_description` | `fiveages_w2_common_description` | [fa-w2-components](https://github.com/fiveages-sim/fa-w2-components) | Public |
| Gen3 | `humanoid/FiveAges/Gen3/fiveages_wce3_description` | `fiveages_wce3_description` | `fa-wce3-description` | Private |

`feature/agilex` adds Gen2 **W2R** and **S2R** gitlinks; those remotes stay private.

After access to a private remote, init the path named in `.gitmodules` (or let `fa-deploy-ws` `./init_repo.sh` do it).

## Isaac USD (`robot_usds`)

[robot_usds](https://github.com/fiveages-sim/robot_usds) maps FiveAges assets under `humanoid/FiveAges/` as **Git submodules**. From that README and the Gen1 / Gen2 USD READMEs:

| Path (under `robot_usds` root) | Upstream | README names | Visibility |
|--------------------------------|----------|--------------|------------|
| `humanoid/FiveAges/Gen1` | [fiveages-gen1-robot-usds](https://github.com/fiveages-sim/fiveages-gen1-robot-usds) | W1 / Gen1 | Public |
| `humanoid/FiveAges/Gen2` | [fiveages-gen2-robot-usds](https://github.com/fiveages-sim/fiveages-gen2-robot-usds) | W2 / S2 / Gen2 (`W2/`, `S2/`, `components/`) | Public |
| `humanoid/FiveAges/Gen3` | `fiveages-gen3-robot-usds` | WCE3 / Gen3 | Private |

Gen2 USD is **W2 and S2** only. It does **not** publish W2R or S2R.

Checkout: standalone `git submodule update --init humanoid/FiveAges/Gen2` (and `…/Gen1`) as in the [robot_usds README](https://github.com/fiveages-sim/robot_usds/blob/main/README.md) §2.1, or FaSim-Isaac **`./init.sh`** (operation that inits `robots/` via `submodules_visibility.conf`), then **`./run.sh`**. FaSim’s visibility file still marks the FiveAges Gen\* trees `private`, so `./init.sh` does not select them by default. See [robot_usds](../simulation/3-robot_usds.md).

## Private: deploy

`fa-deploy-ws` is internal. Extra flags and robot IDs live in **that** README — not here. There is no public `open-deploy-ws` Gen1 or Gen2 branch.

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
- [Vendor arms](6-vendor_arms.md)
- [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md)
- [WBC controller](../controllers/3-ocs2_wbc.md)
