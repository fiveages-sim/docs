# Brand Packages (Public)

Public robot description packages for specific brands.

## Dobot

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

```{admonition} TODO
:class: note

For valid gripper options, check the launch files in `arms_ros2_control`.
```

## ARX

**Repository:** [fiveages-sim/robot-descriptions-arx](https://github.com/fiveages-sim/robot-descriptions-arx)

### Robots

| Robot | Package | Type | Real Hardware |
|-------|---------|------|---------------|
| X5 | `arx_x5_description` | Arm | Simulation only |
| **ACone** | `arx_acone_description` | Arm | **Supported** |
| Lift2S | `arx_lift2s_description` | Mobile manipulator | Simulation only |

```{admonition} Real Hardware Ready
:class: tip

**ARX Acone** is fully supported for real hardware deployment. See [Go to Real Hardware](../../2-how_to/9-go_real_hardware.md).
```

### Usage

```bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=mock
```

### CAN Configuration

ARX robots use CAN bus. Ensure interface is configured:

```bash
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 up
```

## Galbot

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

## HT

**Repository:** [fiveages-sim/robot-descriptions-ht](https://github.com/fiveages-sim/robot-descriptions-ht)

### Robots

| Robot | Package | Type | Real Hardware |
|-------|---------|------|---------------|
| **Panthera** | `ht_panthera_description` | Arm | **Supported** |

```{admonition} Real Hardware Ready
:class: tip

**HT Panthera** is fully supported for real hardware deployment. See [Go to Real Hardware](../../2-how_to/9-go_real_hardware.md).
```

### Usage

```bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=ht_panthera hardware:=mock
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
