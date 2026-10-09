# HighTorque (高擎)

Serial hardware interface plugin for **HighTorque Panthera HT**.

**Repository:** [fiveages-sim/ht-ros2-control](https://github.com/fiveages-sim/ht-ros2-control) · [README](https://github.com/fiveages-sim/ht-ros2-control/blob/main/README.md)

**Plugin:** `ht_ros2_control/PantheraHardwareInterface`. `config_file` is required in `on_init`. Description xacro chooses `Panthera.yaml` vs `PantheraDual.yaml`; there is no `dual_config_file` hardware_parameter in source (README names that as the xacro selector). Motor YAML in `external/motor_cpp/robot_param/` (`Panthera.yaml` / `PantheraDual.yaml`). Default devices `/dev/ttyACM*`.

Features from that README: isomorphic master–slave teleop path on the description launch; gravity compensation via `ht_gravity_compensation` when kp/kd are not command interfaces. Field how-to: [HighTorque Panthera HT](../../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md).

`joint_kp` / `joint_kd` / `gripper_kp` / `gripper_kd` are exposed as node parameters. README: IO thread syncs about every 200 ms — `ros2 param set` / rqt takes effect without reload. No `on_set_parameters` callback; the poll is the Runtime path.

How to read **Startup only** / **Runtime**: [Hardware Interfaces](0-index.md#how-to-read-the-tables).

## Parameters

| Parameter | Type / default | When | Meaning |
|---|---|---|---|
| `config_file` | string (required) | **Startup only** | Motor YAML path |
| `usb_select` | string / `"auto"` | **Startup only** | Control-box USB path, or `auto` (exactly one box) |
| `control_mode` | string / `"mit"` | **Startup only** | `mit` (old name `full_control`) / `effort` / `position` |
| `gripper_rad_to_m` | double / `0.025` | **Startup only** | Gripper rad↔m |
| `max_torques` | CSV, 7 per arm | **Startup only** | Torque limits; source fallback `[21, 36, 36, 21, 10, 10, 0.5]` |
| `max_velocities` | CSV, 7 per arm | **Startup only** | Velocity limits; source fallback `[4.2, 5.0, 5.0, 4.2, 3.7, 3.7, 0.3]` |
| `joint_kp` | CSV, 6 per arm / `[20, 30, 40, 20, 20, 20]` | **Runtime** | Arm kp |
| `joint_kd` | CSV, 6 per arm / `[0.2, 0.3, 0.4, 0.2, 0.2, 0.2]` | **Runtime** | Arm kd |
| `gripper_kp` | double / `5.0` | **Runtime** | 夹爪 kp |
| `gripper_kd` | double / `0.1` | **Runtime** | 夹爪 kd |
| `shutdown_return_home` | bool / `true` | **Startup only** | Interp home then `set_stop` |
| `shutdown_home` | CSV, 6 / zeros | **Startup only** | Shutdown pose |
| `shutdown_home_timeout` | double / `3.5` | **Startup only** | Timeout (s) |
| `shutdown_home_tolerance` | double / `0.05` | **Startup only** | Arrive tolerance |
| `shutdown_home_velocity` | double / `0.3` | **Startup only** | Interp speed |
