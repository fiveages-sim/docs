# Brand Packages (Public)

Public robot description packages for specific brands.

Brand **EN/ZH** labels follow [robot_usds README_zh-CN.md §3.1](https://github.com/fiveages-sim/robot_usds/blob/main/README_zh-CN.md#31-中文简称与英文标识对照). Do not invent brands. Display names used in this docs set:

| 中文简称 | English brand / identifier |
|----------|----------------------------|
| 越疆 | Dobot |
| 方舟无限 | ARX |
| 银河通用 | Galbot |
| 高擎 | HighTorque, Panthera |
| 中科第五纪 | FiveAges |
| 天机智能 | Tianji, Gento |
| 智元 | Agibot |
| 因时 | Inspire |
| 舞肌 | Wuji |
| 法奥 | Fairino |
| 珞石 | Rokae |
| 优必选 | Ubtech |

## Dobot (越疆)

**Repository:** [fiveages-sim/robot-descriptions-dobot](https://github.com/fiveages-sim/robot-descriptions-dobot)

### Robots

| Robot | Package | DOF | Payload |
|-------|---------|-----|---------|
| CR5 | `dobot_cr5_description` | 6 | 5 kg |
| CR10 | `dobot_cr10_description` | 6 | 10 kg |

### Usage

```bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=dobot_cr5 hardware:=mock
```

### Parameters

| Parameter | Values |
|-----------|--------|
| `robot` | `dobot_cr5`, `dobot_cr10` |

End-effectors: `type` / `left_type` / `right_type` via [robot_common_launch](2-common.md). Not `gripper:=`.

## ARX (方舟无限)

**Repository:** [fiveages-sim/robot-descriptions-arx](https://github.com/fiveages-sim/robot-descriptions-arx)

### Robots

| Robot | Package | Type | Real Hardware |
|-------|---------|------|---------------|
| X5 | `arx_x5_description` | Arm | Co-debug in `arx-lift2s` |
| **Acone** / **AC One** | `arx_acone_description` | **Arm only** | Not Lift 2S; `quick_start` co-debug |
| **Lift 2S** | `arx_lift2s_description` | Full-body (arms + lift + chassis) | Branch `arx-lift2s` |

```{admonition} Real Hardware Ready
:class: tip

**ARX Lift 2S** is the full-body mobile manipulator. **Acone** / **AC One** is the arm only. See [ARX Lift 2S](../../2-how_to/9-go_real_hardware/1-arx_lift2s.md).
```

### Usage

```bash
# Acone arm mock (not Lift 2S). Full-body ARX Lift 2S: see the dedicated how-to.
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=mock
```

### CAN Configuration

ARX robots use CAN bus. Ensure interface is configured:

```bash
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 up
```

## Galbot (银河通用)

**Repository:** [fiveages-sim/robot-descriptions-galbot](https://github.com/fiveages-sim/robot-descriptions-galbot)

### Robots

| Robot | Package | Type |
|-------|---------|------|
| G1 | `galbot_g1_description` | Mobile manipulator |

### Usage

```bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=galbot_g1 hardware:=mock
```

### Features

- Mobile base with arm
- Integrated navigation
- Multiple arm configurations

## HighTorque (高擎)

**Repository:** [fiveages-sim/robot-descriptions-ht](https://github.com/fiveages-sim/robot-descriptions-ht)

### Robots

| Robot | Package | Type | Real Hardware |
|-------|---------|------|---------------|
| **Panthera HT** | `panthera_ht_description` | Dual-arm manipulator | Branch `panthera-ht` |

```{admonition} Real Hardware Ready
:class: tip

**HighTorque Panthera HT** real-hardware deploy is the `panthera-ht` branch. See [HighTorque Panthera HT](../../2-how_to/9-go_real_hardware/2-panthera_ht.md). Launch name in that README is `panthera_ht`.
```

### Usage

```bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=panthera_ht hardware:=mock
```

### Features

- Isomorphic master–slave teleop (real hardware)
- Serial communication
- Gravity compensation on the master role

## Quadruped

**Repository:** [fiveages-sim/robot-descriptions-quadruped](https://github.com/fiveages-sim/robot-descriptions-quadruped)

### Robots

Quadruped robot descriptions for legged locomotion.

### Usage

Typically used with separate quadruped controller stacks.

## Package Structure

Each brand package follows the standard layout:

:::{code-block} none
robot-descriptions-<brand>/
├── <robot>_description/
│   ├── CMakeLists.txt
│   ├── package.xml
│   ├── urdf/
│   │   ├── <robot>.urdf.xacro
│   │   └── <robot>.ros2_control.xacro
│   ├── meshes/
│   │   ├── visual/
│   │   └── collision/
│   ├── config/
│   │   └── ocs2_arm_config.yaml
│   └── launch/
│       └── display.launch.py
└── ...
:::

## Adding a New Brand

1. Create repository following naming convention
2. Add description packages for each robot
3. Include ros2_control configurations
4. Add as submodule to `robot_descriptions`
5. Update documentation

See [Add a Robot](../../2-how_to/10-add_a_robot.md) for detailed steps.
