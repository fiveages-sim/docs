# Modbus

RS485 / Modbus RTU hardware interface plugins for 夹爪, 灵巧手, and KWR75.

**Repository:** [fiveages-sim/modbus-ros2-control](https://github.com/fiveages-sim/modbus-ros2-control) · [README](https://github.com/fiveages-sim/modbus-ros2-control/blob/main/README.md) §4

**Plugins:** `ModbusHardware`, `DexterousHandHardware`, `InspireHandHardware`, `FreedomRS485Hardware`, `XHand1RS485Hardware`, `TheoHandModbusHardware`, `Kwr75ForceTorqueSensor`.

Default **Startup only** except the tool-scale rows with `on_set_parameters`. How to read **Startup only** / **Runtime**: [Hardware Interfaces](0-index.md#how-to-read-the-tables).

## `modbus_ros2_control/ModbusHardware`

夹爪: `changingtek` (variants `90c` / `90d`) or `jodell`.

All rows in this table are **Startup only**.

| Parameter | Type / default | Meaning |
|---|---|---|
| `gripper_type` | string / `"changingtek"` | `changingtek` or `jodell` |
| `variant` | string / `"90c"` | Changingtek `90c` / `90d` |
| `serial_port` | string / `"/dev/ttyUSB0"` | USB-RS485 |
| `slave_id` | int / `1` (Jodell source default `0x09`) | Modbus slave |
| `baudrate` | uint / `115200` | Serial baud rate |
| `parity` / `data_bits` / `stop_bits` | source (not in README §4) | Serial format; README: 8N1 |
| `response_timeout_ms` / `byte_timeout_ms` | source | Transaction timeouts |

## `modbus_ros2_control/DexterousHandHardware`

LinkerHand O6/L6/O7 over Modbus. `hand_type` containing `INSPIRE` / `RH56` is rejected.

| Parameter | Type / default | When | Meaning |
|---|---|---|---|
| `serial_port` | string / `"/dev/ttyUSB0"` (README: required) | **Startup only** | Serial port |
| `hand_side` | string / `"right"` | **Startup only** | Left `0x28`, right `0x27` |
| `hand_type` | string / `"simple_dexterous_hand"` | **Startup only** | Distinguishes O6 / L6 / O7 |
| `response_timeout_ms` | int / `20` | **Startup only** | Response timeout (ms) |
| `byte_timeout_ms` | int / `5` | **Startup only** | Inter-byte timeout (ms) |
| `left_tool_torque` / `right_tool_torque` | double / `1.0` | **Runtime** | Side-matched `[0,1]` |
| `left_tool_velocity` / `right_tool_velocity` | double / `1.0` | **Runtime** | Side-matched `[0,1]` |

## `modbus_ros2_control/InspireHandHardware`

README §4 plus `on_init` extras.

All rows in this table are **Startup only**.

| Parameter | Type / default | Meaning |
|---|---|---|
| `serial_port` | string / `"/dev/ttyUSB0"` | Serial port |
| `hand_side` | string / `"left"` | With `slave_id:=auto`: left `2`, right `1` |
| `slave_id` | string / `"auto"` | Modbus slave id |
| `baudrate` | int / `115200` | Serial baud rate |
| `read_feedback` | bool / `true` | Read device feedback |
| `background_period_ms` | int (source; not in README §4) | IO period |
| `command_deadband_raw` | int (source) | Command deadband |
| `default_speed` / `default_force` | int (source) | Default speed; Default force |

## `modbus_ros2_control/FreedomRS485Hardware`

All rows in this table are **Startup only**.

| Parameter | Type / default | Meaning |
|---|---|---|
| `protocol_version` | string / `"auto"` | `freedomv1` / `freedomv2` |
| `serial_port` | string / `"/dev/ttyUSB0"` | Serial port |
| `hand_side` | string | Left or right |
| `baudrate` | int / `115200` (source) | Serial baud rate |
| `slave_id` | `"auto"` (source) | Modbus slave id |
| `command_speed` | int / `100` | Command speed |
| `current_limit` | int (source) | Current limit |
| `command_deadband_deg` | (source) | Command deadband (deg) |
| `feedback_timeout_ms` / `background_period_ms` / `read_feedback` | source | Feedback timeout (ms); Read device feedback |

## `modbus_ros2_control/XHand1RS485Hardware`

| Parameter | Type / default | When | Meaning |
|---|---|---|---|
| `serial_port` | string / `"/dev/ttyUSB0"` | **Startup only** | Serial port |
| `baudrate` | int / `3000000` | **Startup only** | Serial baud rate |
| `hand_id` / `host_id` | int / `0` / `0xFE` | **Startup only** | Device id; Host id |
| `kp` / `ki` / `kd` | int / `100` / `0` / `0` | **Startup only** | Per-frame |
| `torque_limit` | int / `300` | **Startup only** | Base torque cap |
| `tool_torque` | double / `0.8` | **Runtime** | Ratio `[0,1]` |
| `tool_velocity` | double / `0.0` | **Runtime** | `≤0` unlimited; `(0,1]` scaled |
| `control_mode` / `command_deadband_rad` / `feedback_timeout_ms` / `read_feedback` / `require_initial_feedback` | source | **Startup only** | Feedback timeout (ms); Read device feedback |

## `modbus_ros2_control/TheoHandModbusHardware`

All rows in this table are **Startup only**.

| Parameter | Type / default | Meaning |
|---|---|---|
| `serial_port` | string / `"/dev/ttyUSB0"` | Serial port |
| `baudrate` | int / `115200` | Serial baud rate |
| `slave_id` | int / left `2`, right `1` | Modbus slave id |
| `read_feedback` | bool / `true` | Read device feedback |
| `background_period_ms` / `command_deadband_raw` / `command_settle_ms` / `feedback_quiet_after_write_ms` | source | Command deadband |

## `modbus_ros2_control/Kwr75ForceTorqueSensor`

`SensorInterface`. README §4 default baudrate is `115200` (matches source).

All rows in this table are **Startup only**.

| Parameter | Type / default | Meaning |
|---|---|---|
| `serial_port` | string / `"/dev/ttyUSB0"` | Serial port |
| `baudrate` | int / `115200` | Serial baud rate |
| `command_code` | int / `72` (`0x48`) | Start-stream command |
| `convert_to_si` | bool / `true` | Kg→N |
| `response_timeout_ms` | int / `50` | Response timeout (ms) |
| `startup_delay_ms` | int / `50` | Startup delay (ms) |
| `warmup_attempts` | int / `20` | Warmup attempts |
| `wrench_topic` / `frame_id` | string / `""` / `"ft_sensor"` (source) | Optional `WrenchStamped` |
| `gravity` | double / `9.80665` (source) | Gravity (m/s²) |
| `read_timeout_ms` | int / `3` (source) | Read timeout (ms) |
| `max_read_failures` | int / `3` (source) | Max consecutive read failures |
