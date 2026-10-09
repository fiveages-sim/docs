# Marvin

Marvin SDK hardware interface plugin (M6 and related). Command interfaces are joint **`position` only**. Compliance is vendor `ctrl_mode` (`POSITION` / `JOINT_IMPEDANCE` / `CART_IMPEDANCE` / `POWER_OFF`) plus `joint_k_gains` / `joint_d_gains`. USB-dongle 夹爪 / 灵巧手 use [Modbus](7-modbus.md) or [CAN](8-can.md), not this package.

**Repository:** [fiveages-sim/marvin-ros2-control](https://github.com/fiveages-sim/marvin-ros2-control) · [README](https://github.com/fiveages-sim/marvin-ros2-control/blob/master/README.md)

**Plugin:** `marvin_ros2_control/MarvinHardware`. URDF `<param>` are declared as node parameters. README §4 lists the Runtime set; `paramCallback` matches those plus `drag_mode`, `cart_type`, `*_kine_param` / `*_dyn_param`, `tool_debug_log`.

Tianji control SDK (`TJ_FX_ROBOT_CONTRL_SDK`, private submodule) is a pre-built library linked when this hardware interface compiles; it is not redistributed separately.

`left_ee_channel` / `right_ee_channel`: `1` = CAN/CAN FD, `2` = COM1 RS485 (source `COM1_CHANNEL`).

Tool-dynamics / 负载辨识 wizard: `ros2 run marvin_ros2_control tool_dyn_identify_wizard`. VR path: [VR Teleoperation](../../2-how_to/5-teleoperation/6-vr_teleop.md).

How to read **Startup only** / **Runtime**: [Hardware Interfaces](0-index.md#how-to-read-the-tables).

## Startup (bus / tool type)

| Parameter | Type / default | Meaning |
|---|---|---|
| `arm_type` | string / `"LEFT"` | `left` / `right` / `dual` (normalized) |
| `device_ip` | string / `"192.168.1.190"` | Controller IP |
| `device_port` | int / `8080` | Port |
| `left_ee_type` / `right_ee_type` | string / empty | Tool key (README §1) |
| `left_ee_channel` / `right_ee_channel` | int / `2` | Tool bus |
| `use_async_tool_comm` | bool / `true` (source; not in README §3.1) | Async tool IO |
| `kwr75_ft_enabled` / `left_ft_enabled` / `right_ft_enabled` | bool (source; not in README §3.1) | COM2 KWR75 |
| `left_ft_channel` / `right_ft_channel` | int (source) | FT SDK channels |
| `ft_poll_interval_ms` / `ft_command_code` / `ft_convert_to_si` / `ft_gravity` / `ft_warmup_timeout_ms` | source | KWR75 on the arm bus |

`pd_k_gains` / `pd_d_gains` / `pd_control_period_ms` / `use_drag_mode` are declared in `on_init` (source defaults `[14,14,14,10.5,5.6,5.6,5.6]`, `[0.3×7]`, `5`, `false`). They are **not** in `paramCallback` or README §4 — **Startup only**.

## Runtime (README §4 + `paramCallback`)

| Parameter | Type / default | Meaning |
|---|---|---|
| `ctrl_mode` | string / `"POSITION"` | `POSITION` / `JOINT_IMPEDANCE` / `CART_IMPEDANCE` / `POWER_OFF` |
| `joint_k_gains` / `joint_d_gains` | double[7] / `[2,2,2,1.6,1,1,1]` / `[0.4×7]` | Joint impedance |
| `cart_k_gains` / `cart_d_gains` | double[7] / `[1800,1800,1800,40,40,40,20]` / `[0.6,0.6,0.6,0.4,0.4,0.4,0.4]` | Cartesian impedance |
| `cart_type` | int / `2` | Cartesian impedance type |
| `drag_mode` | int / `-1` | `-1` no update, `0` off, `1` joint drag, `2` cartesian drag |
| `max_joint_speed` | double / `10.0` | Joint speed limit (README XML example uses `50`) |
| `max_joint_acceleration` | double / `10.0` | Joint acc limit (README XML example uses `30`) |
| `left_dyn_param` / `right_dyn_param` | double[10] / zeros | Tool dynamics |
| `left_kine_param` / `right_kine_param` | double[6] / zeros | Tool kinematics |
| `left_tool_torque` / `left_tool_velocity` | double / `1.0` | Left tool scale `[0,1]` |
| `right_tool_torque` / `right_tool_velocity` | double / `1.0` | Right tool scale `[0,1]` |
| `left_brake_release` / `right_brake_release` | bool / `false` | Brake; README: only in `POWER_OFF` with hardware inactive |
| `tool_debug_log` | bool / `false` (source) | Tool-frame logs |
