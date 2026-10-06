# vr_pose_publisher

VR pose bridge for teleoperation.

```{admonition} Access Note
:class: note

Available through fa-py-libraries (public) or as standalone (private).
```

## Purpose

Bridges VR tracking data to ROS 2 topics:
- Head tracking
- Controller poses
- Button states

## Modes

### Vuer (WebXR)

Browser-based VR:

```bash
cd fa-py-libraries
./run.sh vr --mode vuer
```

Opens WebXR session accessible from VR headset browser.

### XRoboToolkit

Native application integration:

```bash
./run.sh vr --mode xrt
```

Requires XRoboToolkit app on VR device.

## Topics Published

| Topic | Type | Rate | Description |
|-------|------|------|-------------|
| `/teleop/left_ee_pose` | `PoseStamped` | 90Hz | Left controller |
| `/teleop/right_ee_pose` | `PoseStamped` | 90Hz | Right controller |
| `/teleop/head_pose` | `PoseStamped` | 90Hz | Headset |
| `/teleop/left_trigger` | `Bool` | Event | Left trigger |
| `/teleop/right_trigger` | `Bool` | Event | Right trigger |

## Configuration

```yaml
vr_pose_publisher:
  frame_id: base_link
  publish_rate: 90
  
  controller_mapping:
    left: left_ee
    right: right_ee
```

## Network Setup

For VR device on different network:

1. Configure Zenoh or DDS discovery
2. Ensure firewall allows ROS 2 traffic
3. Match domain IDs

## Certificates

```{admonition} Security Note
:class: important

WebXR requires HTTPS. Certificates are user-generated and should not be committed to version control.
```

## Related

- [VR Teleop How-To](../../2-how_to/6-vr_teleop.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
