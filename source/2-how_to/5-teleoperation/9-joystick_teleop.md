# Joystick teleop

Use a game controller (joystick / gamepad) to command the arms and, in chassis mode, the mobile base. The package is [`arms_teleop`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_teleop/README.md) in [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control). It also contains a foot-pedal assist, which is not a complete teleop setup.

## Prerequisites

- A robot stack is already running (mock, Isaac Sim, or real). This launch does not start the controller.
- A game controller is connected. The default device is `/dev/input/js0`.

## Start the joystick

:::{code-block} bash
source install/setup.bash
ros2 launch arms_teleop joystick_teleop.launch.py
:::

By default `joy_driver:=auto` uses `game_controller_node` when `joy_enumerate_devices` reports the device as mapped, with `generic_gamepad.yaml` (SDL standard layout). Unmapped devices fall back to `joy_node` and `default.yaml`. The package README lists typical mapped gamepads; do not treat that list as a compatibility guarantee for an untested device.

Joystick control starts **disabled**. Press the **right stick** to enable it, then move the sticks. Press the right stick again to disable.

List connected devices:

:::{code-block} bash
ros2 run joy joy_enumerate_devices
:::

If more than one controller is connected, pass the device you want, for example `joy_dev:=/dev/input/js1`. Mapping overrides and keyboard teleop are in the [package README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_teleop/README.md). Do not run `joystick_teleop` and `keyboard_teleop` at the same time if they would publish to the same topics.

## What it publishes

The joystick node publishes `control_input` (`arms_ros2_control_msgs/Inputs`) and `teleop_mode` (`arms_ros2_control_msgs/TeleopMode`). `arms_target_manager` scales `control_input` into `left_target/twist` and `right_target/twist`. In chassis mode the node publishes `/cmd_vel`. The joystick also publishes `/fsm_command`. The keyboard node publishes the same `control_input` and `teleop_mode` pair, and it does not publish `/fsm_command`.

`teleop_mode` is the status for this path. QoS is `Reliable` + `TransientLocal`: one message at startup, then another when active, control mode, mirror, or speed changes. Switching the active arm does not republish it. The arm is `Inputs.target` (`1` left, `2` right). If the joystick pauses `Inputs` in chassis mode, keep the last `target`.

| Field | Type | Meaning |
|-------|------|---------|
| `stamp` | `builtin_interfaces/Time` | Time this snapshot was published |
| `active` | `bool` | Joystick is true only after the right stick enables teleop. Keyboard is always true. |
| `control_mode` | `uint8` | `0` = `CONTROL_ARM`; `1` = `CONTROL_CHASSIS` |
| `mirror_movement` | `bool` | Mirror on or off |
| `speed_level` | `int32` | Keyboard `1`–`10`. Joystick `0` = LOW, `1` = HIGH. |
| `speed_scale` | `float32` | Scale actually applied |

These names are relative to the node namespace. The other contract — VR, foot pedal, and an exoskeleton on `teleop/controller_state` / `teleop/mode_state` — is in {ref}`teleop-mode-status`. A hand or a UI that is following the joystick reads `teleop_mode`.

## What you should see

After you enable the controller, stick motion changes the active arm’s target, or the chassis when you are in chassis mode. `teleop_mode.active` is true after that enable. On the keyboard it is already true.

### Control-input HUD

With only the joystick running, RViz shows one teleop card at the top left of the 3D view. That card is `TeleopMode` plus the active arm: `ARM` `L` or `R` (`Inputs.target`), `MIRROR` for `mirror_movement`, and `SPD` `LOW`/`HIGH` for `speed_level`. On the card, `R` is orange, `L` is blue, `MIRROR ON` is gold, `MIRROR OFF` is muted, `SPD HIGH` is gold, and `SPD LOW` is blue.

The clip is a FiveAges W2 in `fullbody.rviz`. The card moves between the right arm and the left arm, turns mirror on and off, and steps speed between low and high. When the FSM enters OCS2, the FSM panel, joint panel, and MPC readout appear beside it.

```{raw} html
<video controls preload="metadata" width="100%">
  <source src="../../_static/videos/joystick-rviz-hud.mp4" type="video/mp4">
</video>
```

## Foot pedal (assist only)

`foot_pedal_teleop` is an assist, not a standalone teleop path. It reads one USB foot pedal (the packaged udev rule is for the SayoDevice CM6K) and publishes events on the relative topic `teleop/controller_state` (`std_msgs/Int32`). It does not publish a mode snapshot, and it does not publish `/fsm_command`. `VRInputHandler` applies the events and publishes the current mode on `teleop/mode_state` (`TeleopModeState`, QoS `Reliable` + `TransientLocal`).

Run the pedal in the same namespace as that robot’s `arms_target_manager`:

:::{code-block} bash
ros2 run arms_teleop foot_pedal_teleop --ros-args -r __ns:=/robot_a
ros2 topic echo /robot_a/teleop/mode_state
:::

With exactly one supported pedal and an empty namespace, `ros2 run arms_teleop foot_pedal_teleop` is enough; the status topic is then `/teleop/mode_state`. The pedal can run next to the joystick or the keyboard. The package README documents the event map (FSM up/down, left/right arm teleop, STORAGE/UPDATE, mirror), udev setup, and how to choose a device when more than one pedal is connected. The latch fields are in {ref}`teleop-mode-status`.

## Related

- [VR Teleoperation](6-vr_teleop.md) — headset controllers for end-effector pose
- [arms_teleop README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_teleop/README.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
