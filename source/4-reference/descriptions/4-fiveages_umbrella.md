# FiveAges robot descriptions

One page for FiveAges (中科第五纪) wheeled-arm humanoid descriptions and their public USD mapping. The two older pages (“fiveages umbrella” vs “FA robot descriptions”) are merged here.

```{admonition} Access Required
:class: warning

URDF / xacro packages and `fa-deploy-ws` are **private**. Contact your team lead. After access, follow **those READMEs** and their init scripts.
```

```{admonition} Source of truth
:class: important

- Public USD layout: [robot_usds README](https://github.com/fiveages-sim/robot_usds/blob/main/README.md) §3.1 Humanoid → FiveAges
- Workspace pattern (script name only): [fa-deploy-ws Setup](../../1-getting_started/4-fa_deploy_ws.md) — same `./init_repo.sh` name as open-deploy-ws
- Public launch / `hardware:=`: [robot_common_launch](2-common.md) (`mock_components` / `gz` / `isaac` / `real`)
- The public [robot_descriptions README](https://github.com/fiveages-sim/robot_descriptions/blob/main/README.md) does **not** list FiveAges packages
- `robot-descriptions-fiveages` README is **not public** (404 without access). Do **not** invent `--robot`, `./scripts/init-sim.sh`, `fiveages_bringup`, `ocs2_config.yaml`, `wbc_config.yaml`, or a `common/` / `arms/` / `robot/` tree
```

FiveAges **humanoid** platforms in this docs set (W2, W2R, S2, S2R) are **wheeled-arm humanoids** (mobile base + arms), not bipedal.

## Public: Isaac USD (`robot_usds`)

[robot_usds](https://github.com/fiveages-sim/robot_usds) maps FiveAges assets under `robots/humanoid/FiveAges/` as **Git submodules** (private USD repos). From that README:

| Path (under `robot_usds` root) | Upstream | README names |
|--------------------------------|----------|--------------|
| `humanoid/FiveAges/Gen1` | [fiveages-gen1-robot-usds](https://github.com/fiveages-sim/fiveages-gen1-robot-usds) | W1 / Gen1 |
| `humanoid/FiveAges/Gen2` | [fiveages-gen2-robot-usds](https://github.com/fiveages-sim/fiveages-gen2-robot-usds) | W2 / S2 / Gen2 |
| `humanoid/FiveAges/Gen3` | [fiveages-gen3-robot-usds](https://github.com/fiveages-sim/fiveages-gen3-robot-usds) | WCE3 / Gen3 |

Those three USD repos and their READMEs are **not public**. Do not invent USD prim paths or a `galbot.usd`-style load snippet here.

Checkout: FaSim-Isaac **`./init.sh`** (operation that inits `robots/` via `submodules_visibility.conf`), then **`./run.sh`**. See [robot_usds](../simulation/3-robot_usds.md).

## Private: URDF / deploy

Description packages and `fa-deploy-ws` are internal. This page does **not** list unverified package names, launch files, or `--robot` IDs.

After access:

1. Read the private umbrella / package README (not this page).
2. In `fa-deploy-ws`, run **`./init_repo.sh`** (do not recursive-init). Extra flags live in that README.
3. `colcon build`, then `source install/setup.bash` in the launch terminal (or that repo’s official quick-start script if it has one).
4. EEF / `hardware:=` follow [robot_common_launch](2-common.md). There is no `gripper:=` and no `hardware:=mock`.

Copy an existing public `{robot}_description` only as a **layout hint** — [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md).

## Related

- [fa-deploy-ws Setup](../../1-getting_started/4-fa_deploy_ws.md)
- [robot_usds](../simulation/3-robot_usds.md)
- [robot_common_launch](2-common.md)
- [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md)
- [WBC controller](../controllers/3-ocs2_wbc.md)
