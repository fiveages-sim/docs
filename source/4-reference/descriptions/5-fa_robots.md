# FiveAges Robot Descriptions

Usage reference for FiveAges wheeled-arm humanoid descriptions.

```{admonition} Access Required
:class: warning

These packages require private repository access.
```

## Available Robots

| Robot | Package | Type |
|-------|---------|------|
| W2 | `fa-w2-description` | Full humanoid |
| W2R | `fa-w2r-description` | W2 variant |
| S2 | `fa-s2-description` | Humanoid |
| S2R | `fa-s2r-description` | S2 variant |

## Usage

These packages are private. After you have access, follow the **package README** and [fa-deploy-ws Setup](../../1-getting_started/4-fa_deploy_ws.md). This page does not invent `fiveages_bringup`, `--robot` flags, or `hardware:=mock`. Public `hardware:=` keys are `mock_components` / `gz` / `isaac` / `real` — [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md).

## fa-w2-components

Shared components for W2-based robots:

- Common joint definitions
- Sensor mounts
- End-effector attachments

```xml
<xacro:include filename="$(find fa-w2-components)/urdf/common.urdf.xacro"/>
```

## Configuration

### OCS2 Configuration

Each robot includes OCS2 MPC configuration:

:::{code-block} none
fa-w2-description/
└── config/
    └── ocs2_config.yaml
:::

### WBC Configuration

Whole-body control configuration for wheeled-arm humanoids:

:::{code-block} none
fa-w2-description/
└── config/
    └── wbc_config.yaml
:::

## Related

- [robot-descriptions-fiveages](4-fiveages_umbrella.md)
- [fa-deploy-ws Setup](../../1-getting_started/4-fa_deploy_ws.md)
- [WBC Controller](../controllers/3-ocs2_wbc.md)
