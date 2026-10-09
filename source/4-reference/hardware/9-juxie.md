# Juxie

CAN FD hardware interface plugin for JX motors in cyclic synchronous position (CSP) mode.

**Repository:** [fiveages-sim/juxie-ros2-control](https://github.com/fiveages-sim/juxie-ros2-control) · [README](https://github.com/fiveages-sim/juxie-ros2-control/blob/main/README.md)

**Plugin:** `juxie_ros2_control/JxHardware`. No `on_set_parameters`. README lists `max_position_step_nct` `25` and `max_position_accel_nct` `5`; **source `on_init` fallbacks are `90` and `10`**.

How to read **Startup only** / **Runtime**: [Hardware Interfaces](0-index.md).

## Parameters

All rows in this table are **Startup only**.

| Parameter | Type / default | Meaning |
|---|---|---|
| `can_interface` | string / `"can0"` | CAN FD interface |
| `motor_ids` | string (required) | `"1,2,3"` or `"[1,2,3]"`; order matches URDF joints |
| `control_period_ms` | int / `1` | Cycle (ms); default 1000 Hz |
| `max_position_step_nct` | int / `90` (source) | Max per-cycle position step |
| `max_position_accel_nct` | int / `10` (source) | Max delta change; `0` disables |
