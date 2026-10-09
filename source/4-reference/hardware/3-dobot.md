# Dobot CR

TCP hardware interface plugin for Dobot CR. Dashboard / real-time TCP (README: 29999 command, 30004 realtime). There is no `robot_port` `<param>` in `on_init`.

**Repository:** [fiveages-sim/dobot-cr-ros2-control](https://github.com/fiveages-sim/dobot-cr-ros2-control) · [README 配置参数](https://github.com/fiveages-sim/dobot-cr-ros2-control/blob/main/README.md)

**Plugin:** `dobot_ros2_control/DobotHardware`. No `on_set_parameters`.

How to read **Startup only** / **Runtime**: [Hardware Interfaces](0-index.md).

## Parameters

All rows in this table are **Startup only**.

| Parameter | Type / default | Meaning |
|---|---|---|
| `robot_ip` | string / `"192.168.5.38"` | Robot IP |
| `servo_time` | double / `0.03` | ServoJ duration (s); README: match `1 / controller_manager.update_rate` |
| `aheadtime` | double / `20.0` | Trajectory look-ahead (README range 20–100) |
| `gain` | double / `500.0` | Tracking gain (README range 200–1000) |
| `speed_factor` | int / `5` | Global speed percent (README range 1–100) |
| `verbose` | bool / `false` | TCP / command logs |
| `gripper_type` | string / `"changingtek"` (source; not in README table) | Used when a gripper joint is present |
| `gripper_read_frequency_divider` | int / `4` (source; not in README table) | Gripper read divider |
