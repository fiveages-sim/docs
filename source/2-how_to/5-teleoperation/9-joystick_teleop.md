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

The joystick node publishes `control_input` (`arms_ros2_control_msgs/Inputs`). [arms_target_manager](../../4-reference/controllers/6-gripper_teleop_plugins.md) scales that message into `/left_target/twist` and `/right_target/twist`. In chassis mode it publishes `/cmd_vel`. The joystick stack also publishes `/fsm_command`.

## What you should see

After you enable the controller, stick motion changes the active arm’s target, or the chassis when you are in chassis mode. `teleop_mode` reports whether the joystick is active.

(foot-pedal)=

## Foot pedal (assist only)

`foot_pedal_teleop` is an **assist**, not a standalone teleop path. It reads one USB foot pedal (the packaged udev rule is for the SayoDevice CM6K) and publishes events on `/teleop/controller_state`. It does **not** publish `/fsm_command`. FSM transitions and teleop toggles are handled by `VRInputHandler`.

With exactly one supported pedal connected:

:::{code-block} bash
ros2 run arms_teleop foot_pedal_teleop
:::

The package README documents the event map (FSM up/down, left/right arm teleop enable, STORAGE/UPDATE, mirror), udev setup, and how to choose a device when more than one pedal is connected.

## Related

- [VR Teleoperation](6-vr_teleop.md) — headset controllers for end-effector pose
- [arms_teleop README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_teleop/README.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
