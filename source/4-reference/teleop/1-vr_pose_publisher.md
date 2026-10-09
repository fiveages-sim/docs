# vr_pose_publisher

VR pose bridge for teleoperation.

```{admonition} Access Note
:class: note

Available through fa-py-libraries (public) or as standalone (private).
```

## Supported Headsets

| Headset | Support Level | Notes |
|---------|---------------|-------|
| **Pico Enterprise** | **Recommended** | USB 网络共享; **different App** from consumer Pico |
| **Pico consumer** | Supported | Own App (not the Enterprise App); no USB-tether path here |
| **Meta Quest** | Supported | Good consumer availability |

```{admonition} Pico Enterprise vs consumer
:class: important

Pico **Enterprise** and Pico **consumer** are not the same SKU:

1. Enterprise supports **USB shared networking (USB 网络共享)**.
2. They use **different headset Apps** — do not install one App and expect it to cover both.

fa-py-libraries documents XRoboToolkit as “XRoboToolkit App + PC Service” vs browser WebXR (`./run.sh vr` / `./run.sh vr-xrt`). It does not publish store links or ADB steps for either Pico edition.
```

## Purpose

Bridges VR tracking data to ROS 2 topics:
- Head tracking
- Controller poses
- Button states

## Modes

Both Pico and Meta Quest support **WebXR (Vuer)** and **XRoboToolkit** backends. Launch from **fa-py-libraries** (`./init.sh all` first). There is no `./run.sh vr --mode` flag.

### Web Mode (WebXR/Vuer)

:::{code-block} bash
cd fa-py-libraries
./run.sh vr
:::

Opens a WebXR session accessible from the VR headset browser.

### XRoboToolkit Mode

Native application — lower latency, recommended for production:

:::{code-block} bash
./init.sh install-xrobotoolkit-pc-service
./init.sh install-xrobotoolkit
./run.sh vr-xrt-service
./run.sh vr-xrt
:::

Requires the **edition-matching** XRoboToolkit App on the headset (Enterprise ≠ consumer Pico App). `./run.sh vr-xrt-service stop` shuts down the PC Service.

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

Robot-side VR insertion is separate: set `enable_vr: true` in the description’s `config/ocs2/target_manager.yaml` (most robots default off). Same file: `vr_update_rate`, `vr_follow_frame`. Button map and follow-frame troubleshooting: [VR Teleop How-To](../../2-how_to/5-teleoperation/6-vr_teleop.md).

## Network Setup

- **Pico Enterprise:** USB shared networking (USB 网络共享) can put the headset and PC on one network. Use the headset UI; no ADB steps here.
- **Pico consumer / Quest:** Wi-Fi (or other IP) only for this doc.

If the VR device is on a different network: Zenoh or DDS discovery, firewall, matching Domain IDs.

## Certificates

```{admonition} Security Note
:class: important

WebXR requires HTTPS. Certificates are user-generated and should not be committed to version control.
```

## Related

- [VR Teleop How-To](../../2-how_to/5-teleoperation/6-vr_teleop.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
