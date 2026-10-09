# Driver layer parameters

ros2_control **driver layer** (驱动层) plugin arguments. These are URDF / xacro `<param>` entries under `<ros2_control><hardware>`, loaded in the plugin `on_init`. They are **not** the same API as `ros2 param list` on a controller node, unless that plugin also `declare_parameter`s them (ARX, HighTorque, Marvin, some 灵巧手).

How `hardware:=` selects a plugin: [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md). How to inspect: [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md). Package list: [Public driver layer](1-public_hi.md).

The in-tree [`hardwares/README.md`](https://github.com/fiveages-sim/arms_ros2_control/blob/d50933d6862ad35ec7633ef522a134924827b115/hardwares/README.md) is **build-only** (`colcon build --packages-up-to …`). Names below come from each public README and from `on_init` / plugin XML in that repository.

## How to read the tables

Three columns: **Parameter**, **Type / default**, **Meaning** (the **When** tag is the last sentence of Meaning).

| Tag | Evidence |
|-----|----------|
| **Startup only** | Read in `on_init` from `info_.hardware_parameters`. No `add_on_set_parameters_callback` (or README does not claim a hot update). Change the xacro and restart the hardware / `controller_manager`. |
| **Runtime** | `add_on_set_parameters_callback`, or a README + source path that re-reads `ros2 param set` without reload (HighTorque kp/kd poll). |

Simulation `mock_components` / `gz` / `isaac` keys: [Driver layer](0-index.md). Private packages: [Private driver layer](2-private_hi.md).

## topic_based_ros2_control

In-tree under `arms_ros2_control/hardwares/` (not a nested gitmodule). Used when `hardware:=isaac` (Acone xacro: `/isaac/joint_command`, `/isaac/joint_states`). README: [topic_based_ros2_control](https://github.com/fiveages-sim/arms_ros2_control/blob/d50933d6862ad35ec7633ef522a134924827b115/hardwares/topic_based_ros2_control/README.md). Source: [`topic_based_system.cpp`](https://github.com/fiveages-sim/arms_ros2_control/blob/d50933d6862ad35ec7633ef522a134924827b115/hardwares/topic_based_ros2_control/src/topic_based_system.cpp) at [`d50933d`](https://github.com/fiveages-sim/arms_ros2_control/tree/d50933d6862ad35ec7633ef522a134924827b115).

Plugin: `topic_based_ros2_control/TopicBasedSystem`. No `declare_parameter` and no `on_set_parameters`.

:::{code-block} xml
<ros2_control name="my_system" type="system">
  <hardware>
    <plugin>topic_based_ros2_control/TopicBasedSystem</plugin>
    <param name="joint_commands_topic">/robot_joint_commands</param>
    <param name="joint_states_topic">/robot_joint_states</param>
    <param name="initialize_commands_from_state">true</param>
  </hardware>
</ros2_control>
:::

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `joint_commands_topic` | `"/robot_joint_commands"` | Command `sensor_msgs/JointState` topic. **Startup only**. |
| `joint_states_topic` | `"/robot_joint_states"` | State `sensor_msgs/JointState` topic. **Startup only**. |
| `initialize_commands_from_state` | `true` (README: recommended for real hardware) | `true`: first received state becomes the command. `false`: use state_interface `initial_value`. **Startup only**. |
| `trigger_joint_command_threshold` | `1e-5` | Skip publish when command vs state is below this delta; `-1` always send. **Startup only**. |
| `sum_wrapped_joint_states` | `false` | `true`: unwrap ±2π (Isaac-style wrapping). **Startup only**. |
| `joint_name_prefix` | `""` | Strip this prefix from hardware joint names when matching topic names. **Startup only**. |
| `initial_value` | per `state_interface` | Used when `initialize_commands_from_state` is `false`. **Startup only**. |
| `mimic` | per joint | Name of the joint to mimic. **Startup only**. |
| `multiplier` | `1` | Mimic scale. **Startup only**. |

Isaac Sim: [Isaac Sim](../../2-how_to/2-simulation/4-isaac_sim.md).

## unitree_ros2_control

[unitree-ros2-control README](https://github.com/fiveages-sim/unitree-ros2-control/blob/main/README.md). Plugin XML: `unitree_ros2_control/HardwareUnitree`. No `on_set_parameters`.

README XML still writes `hardware_unitree_sdk2/HardwareUnitree`; the registered class is `unitree_ros2_control/HardwareUnitree`.

README xacro shows `domain` and `network_interface`. The rest of the table is from `HardwareUnitree::on_init`.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `domain` | int / `1` | unitree_sdk2 domain. **Startup only**. |
| `network_interface` | string / `"lo"` | NIC (`lo` in sim). **Startup only**. |
| `robot_type` | string / `"quadruped"` (source; not in README) | Factory key: `quadruped`, `humanoid`, `humanoid_arm_sdk`, `g1_arm_sdk`. **Startup only**. |
| `enable_high_state` | bool / `true` (source; not in README) | High-state read (sim). **Startup only**. |
| `show_foot_force` | bool / `false` (source; not in README) | Log foot force. **Startup only**. |
| `default_kp` | double / `0.0` (source; not in README) | Initial joint kp command. **Startup only**. |
| `default_kd` | double / `0.0` (source; not in README) | Initial joint kd command. **Startup only**. |

## dobot_ros2_control

GitHub: [dobot-cr-ros2-control](https://github.com/fiveages-sim/dobot-cr-ros2-control). [README 配置参数](https://github.com/fiveages-sim/dobot-cr-ros2-control/blob/main/README.md). Plugin: `dobot_ros2_control/DobotHardware`. No `on_set_parameters`. There is no `robot_port` `<param>` in `on_init`.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `robot_ip` | string / `"192.168.5.38"` | Robot IP. **Startup only**. |
| `servo_time` | double / `0.03` | ServoJ duration (s); README: match `1 / controller_manager.update_rate`. **Startup only**. |
| `aheadtime` | double / `20.0` | Trajectory look-ahead (README range 20–100). **Startup only**. |
| `gain` | double / `500.0` | Tracking gain (README range 200–1000). **Startup only**. |
| `speed_factor` | int / `5` | Global speed percent (README range 1–100). **Startup only**. |
| `verbose` | bool / `false` | TCP / command logs. **Startup only**. |
| `gripper_type` | string / `"changingtek"` (source; not in README table) | Used when a gripper joint is present. **Startup only**. |
| `gripper_read_frequency_divider` | int / `4` (source; not in README table) | Gripper read divider. **Startup only**. |

## arx_ros2_control

[arx-ros2-control README](https://github.com/fiveages-sim/arx-ros2-control/blob/main/README.md). Two plugins. URDF `<param>` are also declared as node parameters so rqt / `ros2 param set` can change the **Runtime** rows.

### `arx_ros2_control/ArxX5Hardware`

`control_mode` other than `full_control` is warned and ignored. `robot_model` is hardcoded `X5` (not a ROS param).

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `can_interface` | string / `"can0"` | CAN device (README: single-arm right often `can3`). **Startup only**. |
| `control_mode` | string / `"full_control"` | Only `full_control` (MIT MIX) is honored. **Startup only**. |
| `joint_k_gains` | double[6] / `[80, 70, 70, 30, 30, 20]` | MIT kp. README: Lift2S field default `[20,20,20,20,10,10]`. **Runtime**. |
| `joint_d_gains` | double[6] / `[2, 2, 2, 1, 1, 0.7]` | MIT kd. README: Lift2S field default `[0.8,0.8,0.8,0.8,0.5,0.5]`. **Runtime**. |
| `gripper_kp` | double / `5.0` | 夹爪 kp. **Runtime**. |
| `gripper_kd` | double / `0.2` | 夹爪 kd. **Runtime**. |
| `shutdown_return_home` | bool / `false` | Interpolate to `shutdown_home` on deactivate. **Startup only**. |
| `shutdown_home` | double[6] / zeros | Shutdown pose. **Startup only**. |
| `shutdown_home_velocity` | double / `0.3` | Shutdown interp speed. **Startup only**. |
| `shutdown_home_timeout` | double / `2.0` | Shutdown timeout (s). **Startup only**. |
| `status_debug` | bool / `false` (source) | Extra MIT/status logs. **Runtime**. |

### `arx_ros2_control/ArxLiftHardware`

URDF keys from `on_init`. README chassis table says Lift2S xacro often sets `enable_chassis_cmd_vel` true; **source default is `false`**.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `can_name` | string / `"can5"` | Lift CAN. **Startup only**. |
| `robot_type` | int / `2` | `0` LIFT / `1` X7S / `2` LIFTS. **Startup only**. |
| `lift_motor_mode` | string / `"hybrid"` | `hybrid` or `soft_p` / `position`. **Startup only** (live switch is the node param below). |
| `hybrid_kp` | double / `5.0` | Hybrid kp. **Startup only** (seed for `arx_lift.hybrid_kp`). |
| `hybrid_kd` | double / `2.0` | Hybrid kd (alias `kd`). **Startup only**. |
| `soft_p_kp` | double / `50.0` | Position-mode kp (aliases `lift_kp`, `kp`). **Startup only**. |
| `gravity_compensation_torque` | double / `-1.01` | Gravity feedforward. **Startup only**. |
| `coulomb_friction_torque` | double / `0.32` | Coulomb friction. **Startup only**. |
| `friction_vel_eps_mps` | double / `0.01` | Friction deadband (m/s). **Startup only**. |
| `lift_max_vel` | double / `0.20` | Max lift speed. **Startup only**. |
| `lift_max_torque` | double / `15.0` | Max torque. **Startup only**. |
| `height_rad_per_meter` | double / `41.54` | m↔rad (alias `height_to_motor`). **Startup only**. |
| `height_span_m` | double / `0.48` | Stroke (alias `max_height_m`). **Startup only**. |
| `sdk_max_rad` | double / `20.0` | SDK angle cap. **Startup only**. |
| `cmd_ramp_vel` | double / `0.04` | Shutdown-home ramp only. **Startup only**. |
| `enable_chassis_cmd_vel` | bool / `false` | Subscribe Twist → chassis. **Startup only**. |
| `chassis_cmd_vel_topic` | string / `"/cmd_vel"` | Chassis Twist topic. **Startup only**. |
| `chassis_cmd_timeout` | double / `0.3` | Stop after timeout (s). **Startup only**. |
| `chassis_max_vel_x` / `_y` / `_z` | double / `2` / `2` / `4` | Chassis quantize limits (README: LIFTS `.so` omits these). **Startup only**. |
| `shutdown_return_home` | bool / `false` | Return to `shutdown_height_m` on exit. **Startup only**. |
| `shutdown_height_m` | double / `0.0` | Shutdown height. **Startup only**. |
| `shutdown_home_velocity` | double / `0.10` | Shutdown speed. **Startup only**. |
| `shutdown_home_timeout` | double / `2.0` | Shutdown timeout. **Startup only**. |
| `status_debug` | bool / `false` | Debug logs. **Runtime** (also a node param). |

On activate, Lift also declares these **node** parameters (`add_on_set_parameters_callback`):

| Parameter | Seeded from | Meaning |
|-----------|-------------|---------|
| `arx_lift.motor_mode` | `lift_motor_mode` | `hybrid` or `soft_p`/`position`. **Runtime**. |
| `arx_lift.soft_p_kp` | `soft_p_kp` | **Runtime**. |
| `arx_lift.hybrid_kp` / `arx_lift.hybrid_kd` | `hybrid_kp` / `hybrid_kd` | **Runtime**. |
| `arx_lift.gravity_compensation_torque` | same URDF key | **Runtime**. |
| `arx_lift.coulomb_friction_torque` | same | **Runtime**. |
| `arx_lift.friction_vel_eps_mps` | same | **Runtime**. |

## ht_ros2_control

[ht-ros2-control README](https://github.com/fiveages-sim/ht-ros2-control/blob/main/README.md). Plugin: `ht_ros2_control/PantheraHardwareInterface`. `config_file` is required in `on_init`. Description xacro chooses `Panthera.yaml` vs `PantheraDual.yaml`; there is no `dual_config_file` hardware_parameter in source (README names that as the xacro selector).

`joint_kp` / `joint_kd` / `gripper_kp` / `gripper_kd` are exposed as node parameters. README: IO thread syncs about every 200 ms — `ros2 param set` / rqt takes effect without reload. No `on_set_parameters` callback; the poll is the Runtime path.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `config_file` | string (required) | Motor YAML path. **Startup only**. |
| `usb_select` | string / `"auto"` | Control-box USB path, or `auto` (exactly one box). **Startup only**. |
| `control_mode` | string / `"mit"` | `mit` (old name `full_control`) / `effort` / `position`. **Startup only**. |
| `gripper_rad_to_m` | double / `0.025` | Gripper rad↔m. **Startup only**. |
| `max_torques` | CSV, 7 per arm | Torque limits; source fallback `[21, 36, 36, 21, 10, 10, 0.5]`. **Startup only**. |
| `max_velocities` | CSV, 7 per arm | Velocity limits; source fallback `[4.2, 5.0, 5.0, 4.2, 3.7, 3.7, 0.3]`. **Startup only**. |
| `joint_kp` | CSV, 6 per arm / `[20, 30, 40, 20, 20, 20]` | Arm kp. **Runtime**. |
| `joint_kd` | CSV, 6 per arm / `[0.2, 0.3, 0.4, 0.2, 0.2, 0.2]` | Arm kd. **Runtime**. |
| `gripper_kp` | double / `5.0` | 夹爪 kp. **Runtime**. |
| `gripper_kd` | double / `0.1` | 夹爪 kd. **Runtime**. |
| `shutdown_return_home` | bool / `true` | Interp home then `set_stop`. **Startup only**. |
| `shutdown_home` | CSV, 6 / zeros | Shutdown pose. **Startup only**. |
| `shutdown_home_timeout` | double / `3.5` | Timeout (s). **Startup only**. |
| `shutdown_home_tolerance` | double / `0.05` | Arrive tolerance. **Startup only**. |
| `shutdown_home_velocity` | double / `0.3` | Interp speed. **Startup only**. |

## marvin_ros2_control

[marvin-ros2-control README](https://github.com/fiveages-sim/marvin-ros2-control/blob/master/README.md). Plugin: `marvin_ros2_control/MarvinHardware`. URDF `<param>` are declared as node parameters. README §4 lists the Runtime set; `paramCallback` matches those plus `drag_mode`, `cart_type`, `*_kine_param` / `*_dyn_param`, `tool_debug_log`.

`left_ee_channel` / `right_ee_channel`: `1` = CAN/CAN FD, `2` = COM1 RS485 (source `COM1_CHANNEL`).

### Startup (bus / tool type)

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `arm_type` | string / `"LEFT"` | `left` / `right` / `dual` (normalized). **Startup only**. |
| `device_ip` | string / `"192.168.1.190"` | Controller IP. **Startup only**. |
| `device_port` | int / `8080` | Port. **Startup only**. |
| `left_ee_type` / `right_ee_type` | string / empty | Tool key (README §1). **Startup only**. |
| `left_ee_channel` / `right_ee_channel` | int / `2` | Tool bus. **Startup only**. |
| `use_async_tool_comm` | bool / `true` (source; not in README §3.1) | Async tool IO. **Startup only**. |
| `kwr75_ft_enabled` / `left_ft_enabled` / `right_ft_enabled` | bool (source; not in README §3.1) | COM2 KWR75. **Startup only**. |
| `left_ft_channel` / `right_ft_channel` | int (source) | FT SDK channels. **Startup only**. |
| `ft_poll_interval_ms` / `ft_command_code` / `ft_convert_to_si` / `ft_gravity` / `ft_warmup_timeout_ms` | source | KWR75 on the arm bus. **Startup only**. |

### Runtime (README §4 + `paramCallback`)

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `ctrl_mode` | string / `"POSITION"` | `POSITION` / `JOINT_IMPEDANCE` / `CART_IMPEDANCE` / `POWER_OFF`. **Runtime**. |
| `joint_k_gains` / `joint_d_gains` | double[7] / `[2,2,2,1.6,1,1,1]` / `[0.4×7]` | Joint impedance. **Runtime**. |
| `cart_k_gains` / `cart_d_gains` | double[7] / `[1800,1800,1800,40,40,40,20]` / `[0.6,0.6,0.6,0.4,0.4,0.4,0.4]` | Cartesian impedance. **Runtime**. |
| `cart_type` | int / `2` | Cartesian impedance type. **Runtime**. |
| `drag_mode` | int / `-1` | `-1` no update, `0` off, `1` joint drag, `2` cartesian drag. **Runtime**. |
| `max_joint_speed` | double / `10.0` | Joint speed limit (README XML example uses `50`). **Runtime**. |
| `max_joint_acceleration` | double / `10.0` | Joint acc limit (README XML example uses `30`). **Runtime**. |
| `left_dyn_param` / `right_dyn_param` | double[10] / zeros | Tool dynamics. **Runtime**. |
| `left_kine_param` / `right_kine_param` | double[6] / zeros | Tool kinematics. **Runtime**. |
| `left_tool_torque` / `left_tool_velocity` | double / `1.0` | Left tool scale `[0,1]`. **Runtime**. |
| `right_tool_torque` / `right_tool_velocity` | double / `1.0` | Right tool scale `[0,1]`. **Runtime**. |
| `left_brake_release` / `right_brake_release` | bool / `false` | Brake; README: only in `POWER_OFF` with hardware inactive. **Runtime**. |
| `tool_debug_log` | bool / `false` (source) | Tool-frame logs. **Runtime**. |

`pd_k_gains` / `pd_d_gains` / `pd_control_period_ms` / `use_drag_mode` are declared in `on_init` (source defaults `[14,14,14,10.5,5.6,5.6,5.6]`, `[0.3×7]`, `5`, `false`). They are **not** in `paramCallback` or README §4 — **Startup only**.

## modbus_ros2_control

[modbus-ros2-control README](https://github.com/fiveages-sim/modbus-ros2-control/blob/main/README.md) §4. Seven plugins. Default **Startup only** except the tool-scale rows with `on_set_parameters`.

### `modbus_ros2_control/ModbusHardware`

夹爪: `changingtek` (variants `90c` / `90d`) or `jodell`.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `gripper_type` | string / `"changingtek"` | `changingtek` or `jodell`. **Startup only**. |
| `variant` | string / `"90c"` | Changingtek `90c` / `90d`. **Startup only**. |
| `serial_port` | string / `"/dev/ttyUSB0"` | USB-RS485. **Startup only**. |
| `slave_id` | int / `1` (Jodell source default `0x09`) | Modbus slave. **Startup only**. |
| `baudrate` | uint / `115200` | **Startup only**. |
| `parity` / `data_bits` / `stop_bits` | source (not in README §4) | Serial format; README: 8N1. **Startup only**. |
| `response_timeout_ms` / `byte_timeout_ms` | source | Transaction timeouts. **Startup only**. |

### `modbus_ros2_control/DexterousHandHardware`

LinkerHand O6/L6/O7 over Modbus. `hand_type` containing `INSPIRE` / `RH56` is rejected.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `serial_port` | string / `"/dev/ttyUSB0"` (README: required) | **Startup only**. |
| `hand_side` | string / `"right"` | Left `0x28`, right `0x27`. **Startup only**. |
| `hand_type` | string / `"simple_dexterous_hand"` | Distinguishes O6 / L6 / O7. **Startup only**. |
| `response_timeout_ms` | int / `20` | **Startup only**. |
| `byte_timeout_ms` | int / `5` | **Startup only**. |
| `left_tool_torque` / `right_tool_torque` | double / `1.0` | Side-matched `[0,1]`. **Runtime**. |
| `left_tool_velocity` / `right_tool_velocity` | double / `1.0` | Side-matched `[0,1]`. **Runtime**. |

### `modbus_ros2_control/InspireHandHardware`

README §4 plus `on_init` extras.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `serial_port` | string / `"/dev/ttyUSB0"` | **Startup only**. |
| `hand_side` | string / `"left"` | With `slave_id:=auto`: left `2`, right `1`. **Startup only**. |
| `slave_id` | string / `"auto"` | **Startup only**. |
| `baudrate` | int / `115200` | **Startup only**. |
| `read_feedback` | bool / `true` | **Startup only**. |
| `background_period_ms` | int (source; not in README §4) | IO period. **Startup only**. |
| `command_deadband_raw` | int (source) | **Startup only**. |
| `default_speed` / `default_force` | int (source) | **Startup only**. |

### `modbus_ros2_control/FreedomRS485Hardware`

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `protocol_version` | string / `"auto"` | `freedomv1` / `freedomv2`. **Startup only**. |
| `serial_port` | string / `"/dev/ttyUSB0"` | **Startup only**. |
| `hand_side` | string | **Startup only**. |
| `baudrate` | int / `115200` (source) | **Startup only**. |
| `slave_id` | `"auto"` (source) | **Startup only**. |
| `command_speed` | int / `100` | **Startup only**. |
| `current_limit` | int (source) | **Startup only**. |
| `command_deadband_deg` | (source) | **Startup only**. |
| `feedback_timeout_ms` / `background_period_ms` / `read_feedback` | source | **Startup only**. |

### `modbus_ros2_control/XHand1RS485Hardware`

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `serial_port` | string / `"/dev/ttyUSB0"` | **Startup only**. |
| `baudrate` | int / `3000000` | **Startup only**. |
| `hand_id` / `host_id` | int / `0` / `0xFE` | **Startup only**. |
| `kp` / `ki` / `kd` | int / `100` / `0` / `0` | Per-frame. **Startup only**. |
| `torque_limit` | int / `300` | Base torque cap. **Startup only**. |
| `tool_torque` | double / `0.8` | Ratio `[0,1]`. **Runtime**. |
| `tool_velocity` | double / `0.0` | `≤0` unlimited; `(0,1]` scaled. **Runtime**. |
| `control_mode` / `command_deadband_rad` / `feedback_timeout_ms` / `read_feedback` / `require_initial_feedback` | source | **Startup only**. |

### `modbus_ros2_control/TheoHandModbusHardware`

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `serial_port` | string / `"/dev/ttyUSB0"` | **Startup only**. |
| `baudrate` | int / `115200` | **Startup only**. |
| `slave_id` | int / left `2`, right `1` | **Startup only**. |
| `read_feedback` | bool / `true` | **Startup only**. |
| `background_period_ms` / `command_deadband_raw` / `command_settle_ms` / `feedback_quiet_after_write_ms` | source | **Startup only**. |

### `modbus_ros2_control/Kwr75ForceTorqueSensor`

`SensorInterface`. README §4 default baudrate is `115200` (matches source).

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `serial_port` | string / `"/dev/ttyUSB0"` | **Startup only**. |
| `baudrate` | int / `115200` | **Startup only**. |
| `command_code` | int / `72` (`0x48`) | Start-stream command. **Startup only**. |
| `convert_to_si` | bool / `true` | Kg→N. **Startup only**. |
| `response_timeout_ms` | int / `50` | **Startup only**. |
| `startup_delay_ms` | int / `50` | **Startup only**. |
| `warmup_attempts` | int / `20` | **Startup only**. |
| `wrench_topic` / `frame_id` | string / `""` / `"ft_sensor"` (source) | Optional `WrenchStamped`. **Startup only**. |
| `gravity` | double / `9.80665` (source) | **Startup only**. |
| `read_timeout_ms` | int / `3` (source) | **Startup only**. |
| `max_read_failures` | int / `3` (source) | **Startup only**. |

## can_ros2_control

[can-ros2-control README](https://github.com/fiveages-sim/can-ros2-control/blob/main/README.md) §4.

### LinkerHand `O6CanHardware` / `L6CanHardware` / `O7CanHardware`

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `can_interface` | string / `"can0"` | SocketCAN. **Startup only**. |
| `hand_side` | string / `"right"` | Left `0x28`, right `0x27`. **Startup only**. |
| `can_id` | optional | Overrides default ID. **Startup only**. |
| `read_feedback` | bool / `true` | **Startup only**. |
| `read_tactile` | bool / `false` | Five-finger tactile topics. **Startup only**. |
| `tactile_timeout_ms` | int / `100` | **Startup only**. |
| `tactile_period_ms` | int / `20` | **Startup only**. |
| `feedback_timeout_ms` | ignored | README: non-blocking read. |
| `command_deadband_raw` | `0` | README: kept for old xacro; not used to suppress sends. **Startup only**. |
| `hand_type` / `send_initial_command` | source | **Startup only**. |
| `left_tool_torque` / `right_tool_torque` | double / `1.0` | Side-matched, 0–255 on the wire. **Runtime**. |
| `left_tool_velocity` / `right_tool_velocity` | double / `1.0` | Side-matched. **Runtime**. |

### `can_ros2_control/FreedomCanHardware`

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `can_interface` | string / `"can0"` | **Startup only**. |
| `device_id` | int / `0` | 0–31 (`slave_id` alias in source). **Startup only**. |
| `read_feedback` | bool / `true` | **Startup only**. |
| `feedback_timeout_ms` | int / `1` | **Startup only**. |
| `command_deadband_deg` | `0` | **Startup only**. |

### `can_ros2_control/InspireCanfdHardware`

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `can_interface` | string / `"can0"` | CAN FD. **Startup only**. |
| `hand_side` | string / `"left"` | `hand_id:=auto` → left `2`, right `1`. **Startup only**. |
| `hand_id` | `"auto"` | Aliases `slave_id` / `device_id`. **Startup only**. |
| `read_feedback` | bool / `true` | **Startup only**. |
| `feedback_timeout_ms` | int / `2` | **Startup only**. |
| `default_speed` / `default_force` | int / `4000` / `6000` | Init registers. **Startup only**. |
| `wait_write_ack` | (README; no default listed) | Wait for write ACK. **Startup only**. |
| `command_deadband_raw` / `frame_tx_retries` / `inter_frame_delay_us` | source | **Startup only**. |

## juxie_ros2_control

[juxie-ros2-control README](https://github.com/fiveages-sim/juxie-ros2-control/blob/main/README.md). Plugin: `juxie_ros2_control/JxHardware`. No `on_set_parameters`. README lists `max_position_step_nct` `25` and `max_position_accel_nct` `5`; **source `on_init` fallbacks are `90` and `10`**.

| Parameter | Type / default | Meaning |
|-----------|----------------|---------|
| `can_interface` | string / `"can0"` | CAN FD interface. **Startup only**. |
| `motor_ids` | string (required) | `"1,2,3"` or `"[1,2,3]"`; order matches URDF joints. **Startup only**. |
| `control_period_ms` | int / `1` | Cycle (ms); default 1000 Hz. **Startup only**. |
| `max_position_step_nct` | int / `90` (source) | Max per-cycle position step. **Startup only**. |
| `max_position_accel_nct` | int / `10` (source) | Max delta change; `0` disables. **Startup only**. |

## Private driver layer

[Private driver layer](2-private_hi.md) names Rokae, Eyou, iNex, Wuji, DexCap, Fairino. Keys, IP/serial layout, and SDK env vars are in **that repository’s README after access**.

SDK build notes: [SDK Notes](3-sdk_notes.md).

## OCS2 `.info` files

`{robot}_description/config/ocs2/*.info` are **OCS2 task / model files**, not ROS 2 parameters. `robot_name` chooses the description package at startup — [Controller ROS 2 parameters](../controllers/8-ros2_parameters.md).

## Related

- [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md)
- [Public driver layer](1-public_hi.md)
- [Private driver layer](2-private_hi.md)
- [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md)
