# Unitree

unitree_sdk2 hardware interface plugin.

**Repository:** [fiveages-sim/unitree-ros2-control](https://github.com/fiveages-sim/unitree-ros2-control) · [README](https://github.com/fiveages-sim/unitree-ros2-control/blob/main/README.md)

**Plugin:** `unitree_ros2_control/HardwareUnitree` (the README XML still shows a former `hardware_unitree_sdk2/…` name; use the pluginlib class). No `on_set_parameters`.

That README’s launch examples use `hardware:=unitree_sim` / `unitree_real` with `robot:=unitree_g1`. README xacro shows `domain` and `network_interface`. The rest of the table is from `HardwareUnitree::on_init`.

How to read **Startup only** / **Runtime**: [Hardware Interfaces](0-index.md#how-to-read-the-tables).

## Parameters

All rows in this table are **Startup only**.

| Parameter | Type / default | Meaning |
|---|---|---|
| `domain` | int / `1` | unitree_sdk2 domain |
| `network_interface` | string / `"lo"` | NIC (`lo` in sim) |
| `robot_type` | string / `"quadruped"` (source; not in README) | Factory key: `quadruped`, `humanoid`, `humanoid_arm_sdk`, `g1_arm_sdk` |
| `enable_high_state` | bool / `true` (source; not in README) | High-state read (sim) |
| `show_foot_force` | bool / `false` (source; not in README) | Log foot force |
| `default_kp` | double / `0.0` (source; not in README) | Initial joint kp command |
| `default_kd` | double / `0.0` (source; not in README) | Initial joint kd command |
