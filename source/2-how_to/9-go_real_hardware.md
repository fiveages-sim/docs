# Go to Real Hardware

Deploy from simulation to physical robot hardware.

```{admonition} Safety First
:class: danger

Working with real robots requires:
1. Emergency stop within reach
2. Trained operator present
3. Clear workspace around robot
4. Understanding of robot's motion range
```

## Supported Robots

### Public Path (open-deploy-ws)

The following robots can be deployed to real hardware from **lean `open-deploy-ws` branches**. Follow each branch README (`./init_repo.sh` / `./quick_start.sh`); do not treat Acone as the full Lift 2s.

| Robot | Role | Branch | How-to |
|-------|------|--------|--------|
| **Ark / Lift 2s** | Full-body (arms + lift + **chassis**) | `arx-lift2s` | [Ark / Lift 2s](11-ark_lift2s.md) |
| **Acone** | **Arm only** (same 方舟 description tree; not Lift 2s) | `arx-lift2s` (`quick_start` co-debug) | [Ark / Lift 2s](11-ark_lift2s.md) |
| **Panthera HT** | Dual-arm manipulator | `panthera-ht` | [Panthera HT](12-panthera_ht.md) |

These robots are fully supported for external users without requiring private repository access.

### Internal Path (fa-deploy-ws)

FiveAges team members can deploy to additional robots including W2, W2R, S2, S2R, and dual-arm CCS configurations. See [fa-deploy-ws setup](../1-getting_started/4-fa_deploy_ws.md).

## Prerequisites

- Successfully tested in mock mode
- Successfully tested in simulation (recommended)
- Robot hardware powered and connected
- Proper network configuration
- Hardware-specific drivers installed

## Checklist

### Pre-Deployment

- [ ] Mock demo runs without errors
- [ ] Gazebo/Isaac simulation works correctly
- [ ] Robot is powered off
- [ ] Emergency stop is accessible
- [ ] Workspace is clear of obstacles
- [ ] Network connection is verified

### Hardware Setup

- [ ] Robot cables are properly connected
- [ ] Power supply is adequate
- [ ] CAN/Ethernet interfaces are up
- [ ] Hardware interface drivers are loaded

### Configuration

- [ ] Correct robot model selected
- [ ] Joint limits verified
- [ ] Speed limits set conservatively
- [ ] Domain ID configured correctly

## Deployment Steps

### Verify mock operation

:::{code-block} bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=<your_robot> hardware:=mock
# Test all planned motions
:::

### Configure hardware interface

Set hardware-specific parameters in your configuration.

For CAN-based robots:

:::{code-block} bash
# Verify CAN interface
ip link show can0

# Set CAN bitrate if needed
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 up
:::

For Ethernet-based robots:

:::{code-block} bash
# Verify network interface
ip addr show eth0
:::

### Test connection

:::{code-block} bash
# Start with hardware detection only
ros2 launch <robot>_bringup hardware_test.launch.py
:::

### Enable motors

:::{code-block} bash
# Robot-specific enable command
ros2 service call /enable_motors std_srvs/srv/Trigger
:::

### First motion

Start with minimal motion:

:::{code-block} bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=<your_robot> hardware:=real

# Send small joint space command
ros2 topic pub /target_joint_positions sensor_msgs/msg/JointState \
  "{position: [0.01, 0.0, 0.0, 0.0, 0.0, 0.0]}" --once
:::

### Gradual testing

1. Small joint motions
2. Larger joint motions
3. Cartesian motions
4. Full trajectories
5. Gripper operations

## Speed Limits

Start with conservative speed limits:

:::{code-block} yaml
# Example launch parameter
velocity_scaling: 0.1  # 10% of max speed
acceleration_scaling: 0.1
:::

Increase gradually after verifying safe operation.

## Public Robot Deployment (open-deploy-ws)

Use the matching **branch** and its README scripts. Do not treat `demo.launch.py robot:=arx_acone` as Lift 2s, and do not use the invented name `ht_panthera` (README launch name is `panthera_ht`).

- **[Ark / Lift 2s](11-ark_lift2s.md)** — `git clone -b arx-lift2s …` then `./init_repo.sh` and `./quick_start.sh`. Full-body including chassis.
- **Acone** — arm-only; pick ACone in that same `quick_start` menu for co-debug.
- **[Panthera HT](12-panthera_ht.md)** — `git clone -b panthera-ht …` then `./init_repo.sh` / `./release.sh --install` and `./quick_start.sh`. Isomorphic teleop: `./teleop_start.sh`.

## Internal Deployment (fa-deploy-ws)

For FiveAges robots:

:::{code-block} bash
cd ~/fa-deploy-ws
./init_repo.sh --robot <robot_id>

# Configure robot.local.yaml with your values
vim robot.local.yaml

# Quick start (includes safety checks)
./quick_start.sh
:::

## Common Hardware Issues

### CAN Communication Timeout

1. Check CAN interface is up: `ip link show can0`
2. Verify CAN bitrate matches robot
3. Check for loose connections
4. Monitor CAN traffic: `candump can0`

### Ethernet Communication Fails

1. Verify IP addresses
2. Check firewall rules
3. Test ping connectivity
4. Verify port numbers

### Motors Don't Enable

1. Check emergency stop is released
2. Verify power supply
3. Check for hardware faults
4. Review driver error messages

### Unexpected Motion

**Immediately press emergency stop**, then:
1. Review joint limits
2. Check coordinate frame alignment
3. Verify command scaling
4. Test in mock mode first

## Verification

- [ ] Robot enables without errors
- [ ] Small motions execute correctly
- [ ] Joint states feedback is accurate
- [ ] Emergency stop halts motion
- [ ] Robot can be safely disabled

## Next Steps

After successful deployment:
- [Ark / Lift 2s](11-ark_lift2s.md) and [Panthera HT](12-panthera_ht.md) for public robots
- [Add a Robot](10-add_a_robot.md) for custom integrations
