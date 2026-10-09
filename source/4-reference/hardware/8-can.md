# CAN

SocketCAN / CAN FD hardware interface plugins for 灵巧手. Freedom V2 and 夹爪 are out of scope on that README.

**Repository:** [fiveages-sim/can-ros2-control](https://github.com/fiveages-sim/can-ros2-control) · [README](https://github.com/fiveages-sim/can-ros2-control/blob/main/README.md) §4

**Plugins:** `O6CanHardware`, `L6CanHardware`, `O7CanHardware`, `FreedomCanHardware`, `InspireCanfdHardware`.

How to read **Startup only** / **Runtime**: [Hardware Interfaces](0-index.md#how-to-read-the-tables).

## LinkerHand `O6CanHardware` / `L6CanHardware` / `O7CanHardware`

| Parameter | Type / default | When | Meaning |
|---|---|---|---|
| `can_interface` | string / `"can0"` | **Startup only** | SocketCAN |
| `hand_side` | string / `"right"` | **Startup only** | Left `0x28`, right `0x27` |
| `can_id` | optional | **Startup only** | Overrides default ID |
| `read_feedback` | bool / `true` | **Startup only** | Read device feedback |
| `read_tactile` | bool / `false` | **Startup only** | Five-finger tactile topics |
| `tactile_timeout_ms` | int / `100` | **Startup only** | Tactile timeout (ms) |
| `tactile_period_ms` | int / `20` | **Startup only** | Tactile period (ms) |
| `feedback_timeout_ms` | ignored | — | README: non-blocking read. |
| `command_deadband_raw` | `0` | **Startup only** | README: kept for old xacro; not used to suppress sends |
| `hand_type` / `send_initial_command` | source | **Startup only** | See type / default |
| `left_tool_torque` / `right_tool_torque` | double / `1.0` | **Runtime** | Side-matched, 0–255 on the wire |
| `left_tool_velocity` / `right_tool_velocity` | double / `1.0` | **Runtime** | Side-matched |

## `can_ros2_control/FreedomCanHardware`

All rows in this table are **Startup only**.

| Parameter | Type / default | Meaning |
|---|---|---|
| `can_interface` | string / `"can0"` | SocketCAN / CAN FD interface |
| `device_id` | int / `0` | 0–31 (`slave_id` alias in source) |
| `read_feedback` | bool / `true` | Read device feedback |
| `feedback_timeout_ms` | int / `1` | Feedback timeout (ms) |
| `command_deadband_deg` | `0` | Command deadband (deg) |

## `can_ros2_control/InspireCanfdHardware`

All rows in this table are **Startup only**.

| Parameter | Type / default | Meaning |
|---|---|---|
| `can_interface` | string / `"can0"` | CAN FD |
| `hand_side` | string / `"left"` | `hand_id:=auto` → left `2`, right `1` |
| `hand_id` | `"auto"` | Aliases `slave_id` / `device_id` |
| `read_feedback` | bool / `true` | Read device feedback |
| `feedback_timeout_ms` | int / `2` | Feedback timeout (ms) |
| `default_speed` / `default_force` | int / `4000` / `6000` | Init registers |
| `wait_write_ack` | (README; no default listed) | Wait for write ACK |
| `command_deadband_raw` / `frame_tx_retries` / `inter_frame_delay_us` | source | Command deadband |
