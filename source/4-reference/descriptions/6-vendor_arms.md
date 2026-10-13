# Vendor Arms

Brand trees that the public [robot_descriptions README](https://github.com/fiveages-sim/robot_descriptions/blob/main/README.md) lists as submodules. **Public remotes** (browse HTTPS): [robot-descriptions-tianji](https://github.com/fiveages-sim/robot-descriptions-tianji), [robot-descriptions-rokae](https://github.com/fiveages-sim/robot-descriptions-rokae), [robot-descriptions-gento](https://github.com/fiveages-sim/robot-descriptions-gento). **Still private** (404 without access; no browseable links): Fairino (`robot-descriptions-fairino`) and Agibot G2 (`agibot-g2-description`). After access to a private remote, follow **those package READMEs**. Public `hardware:=` keys remain `mock_components` / `gz` / `isaac` / `real` (there is **no** `hardware:=mock`).

```{admonition} Init selection vs GitHub remotes
:class: note

[`open-deploy-ws` `submodules_visibility.conf`](https://github.com/fiveages-sim/open-deploy-ws/blob/main/submodules_visibility.conf) still marks `manipulator/Tianji` and `manipulator/Rokae` as `private`, so `./init_repo.sh` does **not** pull them by default. That is **init selection**, not GitHub visibility — those remotes are public. The conf has no Gento line (Gento is on `robot_descriptions` `feature/agilex` only). Do not recursive-init from `open-deploy-ws`.
```

```{admonition} Source of truth
:class: important

- Paths: [robot_descriptions README (`main`)](https://github.com/fiveages-sim/robot_descriptions/blob/main/README.md), [`.gitmodules` on `main`](https://github.com/fiveages-sim/robot_descriptions/blob/main/.gitmodules) (Tianji / Rokae under `manipulator/`), and the [README](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/README.md) / [`.gitmodules` on `feature/agilex`](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/.gitmodules) (Gento at `humanoid/Gento`; Fairino; Rokae INEX)
- Public package lists: [robot-descriptions-tianji](https://github.com/fiveages-sim/robot-descriptions-tianji), [robot-descriptions-rokae](https://github.com/fiveages-sim/robot-descriptions-rokae), [robot-descriptions-gento](https://github.com/fiveages-sim/robot-descriptions-gento)
- Launch / EEF: [robot_common_launch](2-common.md)
- How to add a package: [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md)
```

| README name | Path | Repository | Visibility |
|-------------|------|------------|------------|
| Tianji | `manipulator/Tianji` | [robot-descriptions-tianji](https://github.com/fiveages-sim/robot-descriptions-tianji) | Public (`main` `.gitmodules`) |
| Rokae | `manipulator/Rokae` | [robot-descriptions-rokae](https://github.com/fiveages-sim/robot-descriptions-rokae) | Public (`main` `.gitmodules`) |
| Gento | `humanoid/Gento` | [robot-descriptions-gento](https://github.com/fiveages-sim/robot-descriptions-gento) | Public (`feature/agilex` `.gitmodules`) |
| Fairino ART7 | `manipulator/Fairino` | `robot-descriptions-fairino` | Private (`feature/agilex` table) |
| Agibot G2 | `humanoid/Agibot/agibot_g2_description` | `agibot-g2-description` | Private |
| Rokae INEX | `humanoid/Rokae/rokae_inex_description` | in-tree on `feature/agilex`; `split-chassis-glb` canonical | in-tree |

Packages named on those public READMEs / umbrella tables:

- Tianji: `m6_ccs_description`, `m6_srs_description`, `m20s_ccs_description`, `m6s_lite_ccs_description`, `marvin_pro_description`
- Rokae arms: `ar5_srs_description`, `ar5_ccs_description`; INEX is the wheel humanoid at `humanoid/Rokae`
- Gento: `gento_skye_description`, `gento_luna_description`; Linkhou S2 v2 + Tianji M6-CCS / M6S Lite
- Fairino: ART7 dual-arm (private remote)
- Agibot G2: private humanoid description

Launch / xacro: the public package READMEs above. After access to a private remote, follow that package README.

## Related

- [robot_descriptions](1-robot_descriptions.md)
- [robot_common_launch](2-common.md)
- [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md)
- [Hardware Interfaces](../hardware/0-index.md)
