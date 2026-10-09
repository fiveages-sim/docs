# ARX (方舟无限)

CAN hardware interface plugins for **ARX** X5 / Acone (dual-arm) and Lift 2S lift + chassis.

**Repository:** [fiveages-sim/arx-ros2-control](https://github.com/fiveages-sim/arx-ros2-control) · [README](https://github.com/fiveages-sim/arx-ros2-control/blob/main/README.md)

| Plugin | Role |
|--------|------|
| `arx_ros2_control/ArxX5Hardware` | One instance per arm (X5 SDK). MIT MIX: `position` + `velocity` + `effort`; kp/kd from `joint_k_gains` / `joint_d_gains` |
| `arx_ros2_control/ArxLiftHardware` | Lift2S column (default CAN `can5`). `hybrid` or `soft_p` / `position`; optional `/cmd_vel` chassis |

Acone `hardware:=real` xacro uses `arx_ros2_control/ArxX5Hardware` ([ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md)). Field how-to: [ARX Lift 2S](../../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md).

URDF `<param>` are also declared as node parameters so rqt / `ros2 param set` can change the **Runtime** rows. How to read **Startup only** / **Runtime**: [Hardware Interfaces](0-index.md).

## `arx_ros2_control/ArxX5Hardware`

`control_mode` other than `full_control` is warned and ignored. `robot_model` is hardcoded `X5` (not a ROS param).

| Parameter | Type / default | When | Meaning |
|---|---|---|---|
| `can_interface` | string / `"can0"` | **Startup only** | CAN device (README: single-arm right often `can3`) |
| `control_mode` | string / `"full_control"` | **Startup only** | Only `full_control` (MIT MIX) is honored |
| `joint_k_gains` | double[6] / `[80, 70, 70, 30, 30, 20]` | **Runtime** | MIT kp. README: Lift2S field default `[20,20,20,20,10,10]` |
| `joint_d_gains` | double[6] / `[2, 2, 2, 1, 1, 0.7]` | **Runtime** | MIT kd. README: Lift2S field default `[0.8,0.8,0.8,0.8,0.5,0.5]` |
| `gripper_kp` | double / `5.0` | **Runtime** | 夹爪 kp |
| `gripper_kd` | double / `0.2` | **Runtime** | 夹爪 kd |
| `shutdown_return_home` | bool / `false` | **Startup only** | Interpolate to `shutdown_home` on deactivate |
| `shutdown_home` | double[6] / zeros | **Startup only** | Shutdown pose |
| `shutdown_home_velocity` | double / `0.3` | **Startup only** | Shutdown interp speed |
| `shutdown_home_timeout` | double / `2.0` | **Startup only** | Shutdown timeout (s) |
| `status_debug` | bool / `false` (source) | **Runtime** | Extra MIT/status logs |

## `arx_ros2_control/ArxLiftHardware`

URDF keys from `on_init`. README chassis table says Lift2S xacro often sets `enable_chassis_cmd_vel` true; **source default is `false`**.

| Parameter | Type / default | When | Meaning |
|---|---|---|---|
| `can_name` | string / `"can5"` | **Startup only** | Lift CAN |
| `robot_type` | int / `2` | **Startup only** | `0` LIFT / `1` X7S / `2` LIFTS |
| `lift_motor_mode` | string / `"hybrid"` | **Startup only** | `hybrid` or `soft_p` / `position`. Live switch is the node param below |
| `hybrid_kp` | double / `5.0` | **Startup only** | Hybrid kp. Seed for `arx_lift.hybrid_kp` |
| `hybrid_kd` | double / `2.0` | **Startup only** | Hybrid kd (alias `kd`) |
| `soft_p_kp` | double / `50.0` | **Startup only** | Position-mode kp (aliases `lift_kp`, `kp`) |
| `gravity_compensation_torque` | double / `-1.01` | **Startup only** | Gravity feedforward |
| `coulomb_friction_torque` | double / `0.32` | **Startup only** | Coulomb friction |
| `friction_vel_eps_mps` | double / `0.01` | **Startup only** | Friction deadband (m/s) |
| `lift_max_vel` | double / `0.20` | **Startup only** | Max lift speed |
| `lift_max_torque` | double / `15.0` | **Startup only** | Max torque |
| `height_rad_per_meter` | double / `41.54` | **Startup only** | m↔rad (alias `height_to_motor`) |
| `height_span_m` | double / `0.48` | **Startup only** | Stroke (alias `max_height_m`) |
| `sdk_max_rad` | double / `20.0` | **Startup only** | SDK angle cap |
| `cmd_ramp_vel` | double / `0.04` | **Startup only** | Shutdown-home ramp only |
| `enable_chassis_cmd_vel` | bool / `false` | **Startup only** | Subscribe Twist → chassis |
| `chassis_cmd_vel_topic` | string / `"/cmd_vel"` | **Startup only** | Chassis Twist topic |
| `chassis_cmd_timeout` | double / `0.3` | **Startup only** | Stop after timeout (s) |
| `chassis_max_vel_x` / `_y` / `_z` | double / `2` / `2` / `4` | **Startup only** | Chassis quantize limits (README: LIFTS `.so` omits these) |
| `shutdown_return_home` | bool / `false` | **Startup only** | Return to `shutdown_height_m` on exit |
| `shutdown_height_m` | double / `0.0` | **Startup only** | Shutdown height |
| `shutdown_home_velocity` | double / `0.10` | **Startup only** | Shutdown speed |
| `shutdown_home_timeout` | double / `2.0` | **Startup only** | Shutdown timeout |
| `status_debug` | bool / `false` | **Runtime** | Debug logs. Also a node param |

On activate, Lift also declares these **node** parameters (`add_on_set_parameters_callback`):

All rows in this table are **Runtime**.

| Parameter | Seeded from | Meaning |
|---|---|---|
| `arx_lift.motor_mode` | `lift_motor_mode` | `hybrid` or `soft_p`/`position` |
| `arx_lift.soft_p_kp` | `soft_p_kp` | Same as the URDF seed, as a node parameter |
| `arx_lift.hybrid_kp` / `arx_lift.hybrid_kd` | `hybrid_kp` / `hybrid_kd` | Same as the URDF seed, as a node parameter |
| `arx_lift.gravity_compensation_torque` | same URDF key | Same as the URDF seed, as a node parameter |
| `arx_lift.coulomb_friction_torque` | same | Same as the URDF seed, as a node parameter |
| `arx_lift.friction_vel_eps_mps` | same | Same as the URDF seed, as a node parameter |
