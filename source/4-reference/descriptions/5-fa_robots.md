# FiveAges Robot Descriptions

Usage reference for FiveAges humanoid descriptions.

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

### Via fa-deploy-ws

```bash
# Initialize for specific robot
./init_repo.sh --robot fiveages_w2

# Build
colcon build

# Launch
ros2 launch fiveages_bringup bringup.launch.py robot:=fiveages_w2 hardware:=mock
```

### Launch Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `robot` | Robot model | `fiveages_w2` |
| `hardware` | Hardware type | `mock`, `real` |

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

Whole-body control configuration for humanoids:

:::{code-block} none
fa-w2-description/
└── config/
    └── wbc_config.yaml
:::

## Related

- [robot-descriptions-fiveages](4-fiveages_umbrella.md)
- [fa-deploy-ws Setup](../../1-getting_started/4-fa_deploy_ws.md)
- [WBC Controller](../controllers/3-ocs2_wbc.md)
