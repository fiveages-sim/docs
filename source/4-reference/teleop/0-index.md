# Teleoperation Reference

This section documents the teleoperation systems.

## Overview

The stack supports several teleoperation inputs. They are not interchangeable: some supply **end-effector pose**, some follow in **joint space**, some drive **fingers or grippers**, and some only send **enable / pause / FSM** assists. For a first run, use [VR](../../2-how_to/5-teleoperation/6-vr_teleop.md) or a [game controller](../../2-how_to/5-teleoperation/9-joystick_teleop.md).

| Method | Input | Role |
|--------|-------|------|
| VR | Headset (Pico Enterprise / consumer, Meta Quest), controllers or optical hand tracking | Controller path (`./run.sh vr`, `./run.sh vr-xrt`): end-effector pose, triggers, FSM and pause buttons. Hand tracking (`./run.sh vr-xrt wrist`, `./run.sh vr-hand`): optical-wrist 6DoF and bare-hand gestures — {ref}`Hand tracking <vr-hand-tracking>`. |
| Game controller | Joystick / gamepad (`arms_teleop`) | Arm velocity via `control_input` → twist; chassis `/cmd_vel` in chassis mode |
| Isomorphic | Master–slave (HighTorque Panthera HT) | Joint-space following |
| DexCap (internal) | Exoskeleton + gloves | Waist/arm joints from the exoskeleton; finger joints from the gloves |
| Wuji gloves (internal) | Gloves, optional Vive Tracker | Finger / hand joints; optional arm pose from Vive Tracker |
| Vive Tracker (internal) | SteamVR Vive Tracker (`vive_tracker_teleop`) | Arm end-effector pose. Named **Vive Tracker** in the package and in these docs, not “Valve Tracker”. |
| Foot pedal | USB pedal (`arms_teleop`, SayoDevice CM6K) | Assist only: events on relative `teleop/controller_state`. Current mode is `teleop/mode_state`. |

```{admonition} VR Headset Recommendation
:class: tip

For VR teleoperation, **Pico** and **Meta Quest** are the primary tested headsets. Both can use **WebXR** (`./run.sh vr`) and **XRoboToolkit** (`./run.sh vr-xrt`). **Pico Enterprise** is the preferred Pico SKU: it supports **USB shared networking (USB 网络共享)** and uses a **different headset App** from Pico consumer.
```

## In This Section

```{toctree}
:maxdepth: 1

1-vr_pose_publisher
2-drag_teleop
3-dexcap
4-teleop_joint_mapper
5-wuji_glove
6-vive_tracker
7-wuji_hand_hi
```

## Topic Contracts

VR poses, stick axes, and trigger pull are [VR published topics](../../3-concepts/4-fsm_and_topics.md#vr-published-topics). Wuji glove topics are on [wuji_glove_teleop](5-wuji_glove.md). Vive Tracker lists its `/teleop/left_ee_pose` and `/teleop/right_ee_pose` on [vive_tracker_teleop](6-vive_tracker.md).

Joystick teleop uses `control_input`, twist, `/cmd_vel`, and `/fsm_command`.

Mode changes and the latched mode are a separate pair. Field-by-field reading is in {ref}`teleop-mode-status`.

| Path | Change the mode | Read the current mode |
|------|-----------------|----------------------|
| Joystick / keyboard | `control_input` (`Inputs`) | `teleop_mode` (`TeleopMode`), from `joystick_teleop` / `keyboard_teleop` |
| Event bus (VR, foot pedal, exoskeleton) | `teleop/controller_state` (`std_msgs/Int32`) | `teleop/mode_state` (`TeleopModeState`), from `VRInputHandler` |

The topic names are relative to the robot namespace (`/robot_a/teleop/mode_state` when the robot is `/robot_a`). QoS is `Reliable` + `TransientLocal`. A dexterous hand or a UI reads the status topic. Open/close and percent commands stay on `*/target_command` and `*/target_percent`. The foot pedal publishes `teleop/controller_state` only.
