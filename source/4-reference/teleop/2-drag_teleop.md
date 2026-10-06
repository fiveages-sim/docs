# Isomorphic teleop (`drag_teleop_controller`)

Master–slave **isomorphic teleop** (同构遥操作) for HT Panthera dual-arm. The ROS package is still named `drag_teleop_controller`; that is **not** drag teaching.

**Repository:** [fiveages-sim/drag_teleop_controller](https://github.com/fiveages-sim/drag_teleop_controller)

**README:** [README.md](https://github.com/fiveages-sim/drag_teleop_controller/blob/main/README.md)

## Purpose

One `ros2_control` controller plugin, started twice:

- `role:=master` — operator arm with Pinocchio gravity compensation (`τ_G = rnea(q, 0, 0)`); optional force feedback
- `role:=slave` — follower; tracks mapped master joints (`position` / `mit` / `effort`)

Joint mapping (and effort mapping under power conservation) is applied **before** publishing `teleop_states`. Arm joints (12) are commanded by this controller; grippers use `adaptive_gripper_controller`.

There is **no** `enter_teach_mode`, `/start_recording`, or `/playback` service.

## Launch

Launch file: `drag_teleop_controller.launch.py` (not `drag_teleop.launch.py`).

```bash
# Mock
ros2 launch drag_teleop_controller drag_teleop_controller.launch.py \
  role:=master hardware:=mock_components
ros2 launch drag_teleop_controller drag_teleop_controller.launch.py \
  role:=slave hardware:=mock_components

# Real (see README for mode × hardware interface requirements)
ros2 launch drag_teleop_controller drag_teleop_controller.launch.py \
  role:=master hardware:=real mode:=effort \
  hardware_control_mode:=effort
ros2 launch drag_teleop_controller drag_teleop_controller.launch.py \
  role:=slave hardware:=real mode:=mit
```

Default `robot` is `panthera_ht`. Namespaces are `/drag_teleop_{role}`.

## Services

| Service | Type | Description |
|---------|------|-------------|
| `/drag_teleop_{role}/teleop_mode` | `drag_teleop_controller/srv/TeleopMode` | Runtime `position` / `mit` / `effort` |
| `/drag_teleop_{role}/teleop_feedback` | `drag_teleop_controller/srv/TeleopFeedback` | Master-only: `false` / `position` / `effort` |

## Topics

| Topic | Direction | Description |
|-------|-----------|-------------|
| `/drag_teleop_master/teleop_states` | Publish (master) / Subscribe (slave) | Forward-mapped master state |
| `/drag_teleop_slave/teleop_states` | Publish (slave) / Subscribe (master) | Inverse-mapped slave state |

## Launch arguments

| Argument | Default | Meaning |
|----------|---------|---------|
| `role` | (required) | `master` \| `slave` |
| `robot` | `panthera_ht` | `{robot}_description` package |
| `type` | `dual` | `single` \| `left` \| `right` \| `dual` |
| `hardware` | `mock_components` | `real` \| `real_usb` \| `mock_components` \| `gz` \| `isaac` |
| `mode` | (yaml) | `position` (slave only) \| `mit` \| `effort` |
| `feedback` | (yaml) | `false` \| `position` \| `effort` (master) |
| `moveJ_pub` | `false` | Master publishes OCS2 moveJ + gripper commands |
| `controller_params` | package yaml | e.g. `panthera_ht_2_panthera_ht.yaml` |

Mode × hardware command-interface matrix, control laws, and YAML keys: read the README. Do not treat DexCap [`teleop-joint-mapper`](4-teleop_joint_mapper.md) as this package.

## Related

- [Isomorphic Teleop How-To](../../2-how_to/7-isomorphic_teleop.md)
