# Isomorphic Teleop

Master–slave **isomorphic teleop** (同构遥操作) for HT Panthera dual-arm: move the master arm in joint space and the slave follows.

This is **not** drag teaching. There is no trajectory record/playback and no `enter_teach_mode` API. The implemented path is the public package [`drag_teleop_controller`](https://github.com/fiveages-sim/drag_teleop_controller).

**README:** [drag_teleop_controller README](https://github.com/fiveages-sim/drag_teleop_controller/blob/main/README.md)

## Prerequisites

- Workspace that includes `drag_teleop_controller` (public)
- HT Panthera description (`panthera_ht` / `ht_panthera`)
- Two launch processes: one `master`, one `slave` (mock or two physical arms)

## Overview

One controller plugin, two roles:

| Role | What it does |
|------|----------------|
| `master` | Operator side. Gravity compensation so you can move the arm; publishes mapped joint state. |
| `slave` | Follower. Tracks the mapped master joints (optional ruckig smoothing). |

Control modes (`mode`): `position` (slave only), `mit`, `effort`. Master-only force feedback (`feedback`): `false`, `position`, `effort`. Joint mapping runs before `teleop_states` is published. Grippers are handled by `adaptive_gripper_controller` (spawned from the same launch).

## Setup

```bash
cd ~/open-deploy-ws
colcon build --packages-select drag_teleop_controller --symlink-install
source install/setup.bash
```

## Mock (no hardware)

Two terminals:

```bash
# Terminal 1 — master
ros2 launch drag_teleop_controller drag_teleop_controller.launch.py \
  role:=master hardware:=mock_components

# Terminal 2 — slave
ros2 launch drag_teleop_controller drag_teleop_controller.launch.py \
  role:=slave hardware:=mock_components
```

Check controllers and topics:

```bash
ros2 control list_controllers --controller-manager /drag_teleop_master/controller_manager
# drag_teleop_controller / left_gripper_controller / right_gripper_controller should be active

ros2 topic echo /drag_teleop_master/teleop_states
ros2 topic echo /drag_teleop_slave/teleop_states
```

## Real hardware (HT Panthera)

Launch file and argument names below match the package README. Default `robot` is `panthera_ht`. Use `hardware:=real` (or `real_usb`).

```bash
# Master (low-stiffness, gravity-compensated)
ros2 launch drag_teleop_controller drag_teleop_controller.launch.py \
  role:=master hardware:=real mode:=effort \
  hardware_control_mode:=effort \
  hardware_gripper_kp:="1e-5" hardware_gripper_kd:="1e-5"

# Slave (MIT follow)
ros2 launch drag_teleop_controller drag_teleop_controller.launch.py \
  role:=slave hardware:=real mode:=mit
```

Optional master with external-effort feedback: add `feedback:=effort` (see README).

## Mode switching

Custom services, not `std_srvs/Trigger`:

```bash
ros2 service call /drag_teleop_master/teleop_mode \
  drag_teleop_controller/srv/TeleopMode "{mode: effort}"
ros2 service call /drag_teleop_master/teleop_feedback \
  drag_teleop_controller/srv/TeleopFeedback "{mode: position}"
```

## Launch arguments (summary)

| Argument | Default | Meaning |
|----------|---------|---------|
| `role` | (required) | `master` or `slave` |
| `robot` | `panthera_ht` | Looks up `{robot}_description` |
| `type` | `dual` | `single` / `left` / `right` / `dual` |
| `hardware` | `mock_components` | `real` / `real_usb` / `mock_components` / `gz` / `isaac` |
| `mode` | (yaml) | `position` (slave only) / `mit` / `effort` |
| `feedback` | (yaml) | `false` / `position` / `effort` (master only) |
| `moveJ_pub` | `false` | Master can publish OCS2 moveJ + gripper commands |

Control laws, hardware-interface requirements per `role` × `mode`, and YAML keys are in the [README](https://github.com/fiveages-sim/drag_teleop_controller/blob/main/README.md). Do not invent extra teach/record APIs.

## Safety

```{admonition} Physical Interaction
:class: warning

On real hardware:
1. Keep emergency stop accessible
2. Start in mock, then low-stiffness master (`effort`) before enabling the slave
3. Move slowly; watch joint limits and pinch points
4. Confirm both `role` processes are up and `teleop_states` are flowing before contacting the arm
```

## Verification

1. Mock: both controller managers list `drag_teleop_controller` as active
2. `/drag_teleop_master/teleop_states` and `/drag_teleop_slave/teleop_states` publish
3. Changing master joint state is reflected on the slave (mapped joint names)

## Troubleshooting

### Controller fails to activate

- `role` must be `master` or `slave`
- Hardware must export the command interfaces required by `mode` (position / velocity / effort). The controller checks this in `on_activate`.

### Slave does not follow

- Both processes running with matching `robot` / `type`
- Echo both `teleop_states` topics
- `input_topic` defaults to `/drag_teleop_{other_role}/teleop_states`

### DexCap / joint remapping

DexCap glove → robot mapping is a **different** package: [teleop-joint-mapper](../4-reference/teleop/4-teleop_joint_mapper.md). It is not this master–slave isomorphic path.

## Related

- [drag_teleop_controller reference](../4-reference/teleop/2-drag_teleop.md)
- [Go to Real Hardware](9-go_real_hardware.md)
