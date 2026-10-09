# Vendor Arms (Private)

Private brand trees that the public [robot_descriptions README](https://github.com/fiveages-sim/robot_descriptions/blob/main/README.md) lists as submodules. After access, follow **those package READMEs**. Public `hardware:=` keys remain `mock_components` / `gz` / `isaac` / `real` (there is **no** `hardware:=mock`).

```{admonition} Source of truth
:class: important

- Paths: [robot_descriptions README (`main`)](https://github.com/fiveages-sim/robot_descriptions/blob/main/README.md) and the [same file on `feature/agilex`](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/README.md) (newer Tianji / Fairino / Gento / Rokae INEX rows)
- Launch / EEF: [robot_common_launch](2-common.md)
- How to add a package: [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md)
```

| README name | Path | Repository |
|-------------|------|------------|
| Tianji | `manipulator/Tianji` | [robot-descriptions-tianji](https://github.com/fiveages-sim/robot-descriptions-tianji) |
| Rokae | `manipulator/Rokae` | [robot-descriptions-rokae](https://github.com/fiveages-sim/robot-descriptions-rokae) |
| Fairino ART7 | `manipulator/Fairino` | [robot-descriptions-fairino](https://github.com/fiveages-sim/robot-descriptions-fairino) (`feature/agilex` table) |
| Gento | `humanoid/Gento` | [robot-descriptions-gento](https://github.com/fiveages-sim/robot-descriptions-gento) (`feature/agilex` table) |
| Agibot G2 | `humanoid/Agibot/agibot_g2_description` | [agibot-g2-description](https://github.com/fiveages-sim/agibot-g2-description) |
| Rokae INEX | `humanoid/Rokae/rokae_inex_description` | in-tree on `feature/agilex`; `split-chassis-glb` canonical |

`feature/agilex` README text for those brands:

- Tianji: M6-CCS, M6-SRS, M20S-CCS, Marvin Pro
- Rokae arms: AR5-SRS, AR5-CCS; INEX is the wheel humanoid at `humanoid/Rokae`
- Fairino: ART7 dual-arm
- Gento: Skye, Luna; Linkhou S2 v2 + Tianji M6-CCS / M6S Lite
- Agibot G2: private humanoid description

## Related

- [robot_descriptions](1-robot_descriptions.md)
- [robot_common_launch](2-common.md)
- [Add a Robot](../../2-how_to/6-deployment/10-add_a_robot.md)
- [Driver layer](../hardware/2-private_hi.md)
