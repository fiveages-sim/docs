# Introduction

This section contains task-oriented recipes for common operations. Each guide focuses on a specific task and assumes you have a working workspace.

## Available Guides

### Basic Operations

- [Run Mock Demo](1-basic_operations/1-run_mock_demo.md) — Test without hardware
- [Switch Robot](1-basic_operations/2-switch_robot.md) — Change robot model; EEF via `type` / `left_type` / `right_type`

### Simulation

- [Gazebo Simulation](2-simulation/3-gazebo_sim.md) — Physics simulation with Gazebo
- [Isaac Sim](2-simulation/4-isaac_sim.md) — NVIDIA Isaac Sim integration

### Programming

- [Python Interface](3-programming/5-python_interface.md) — Control robots from Python

### Controllers

- [Use basic_joint_controller](4-controllers/11-basic_joint.md) — Home / Hold / MoveJ (`std_msgs/Int32` `/fsm_command`)

### Teleoperation

- [VR Teleop](5-teleoperation/6-vr_teleop.md) — VR headset control
- [Isomorphic Teleop](5-teleoperation/7-isomorphic_teleop.md) — Master–slave isomorphic teleop (同构遥操作, HighTorque Panthera HT)
- [Drag teaching is not implemented](5-teleoperation/7-drag_teleop.md) — 拖动遥操作 is not a supported path
- [DexCap Teleop](5-teleoperation/8-dexcap_teleop.md) — DexCap glove (internal)

### Deployment

- [Go Real Hardware](6-deployment/9-go_real_hardware/0-index.md) — Deploy to physical robots
  - [ARX Lift 2S](6-deployment/9-go_real_hardware/1-arx_lift2s.md) — Full-body ARX (方舟无限) mobile manipulator
  - [HighTorque Panthera HT](6-deployment/9-go_real_hardware/2-panthera_ht.md) — Dual-arm manipulator (`panthera-ht` branch)
- [Add a Robot](6-deployment/10-add_a_robot.md) — Integrate new robot models

### Synthetic Data

- [Synthetic Data](7-synthetic_data/0-index.md) — Isaac USD → task queue → LeRobot record/export
  - [Isaac Scenes and USD](7-synthetic_data/1-isaac_scenes.md)
  - [Interface and Orchestration](7-synthetic_data/2-orchestration.md)
  - [LeRobot Record and Export](7-synthetic_data/3-record_export.md)

## Guide Format

Each guide follows the same structure:

1. **Prerequisites** — What you need before starting
2. **Steps** — Numbered procedure
3. **Verification** — How to confirm success
4. **Troubleshooting** — Common issues

## Need Something Else?

If you can't find a guide for your task:

1. Check the [Concepts](../3-concepts/0-index.md) section for understanding
2. Look in [Reference](../4-reference/descriptions/0-index.md) for detailed documentation
3. Search repository READMEs for specific packages
