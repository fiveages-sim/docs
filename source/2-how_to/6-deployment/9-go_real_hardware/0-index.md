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

The following robots can be deployed to real hardware from **lean `open-deploy-ws` branches**. Follow each branch README (`./init_repo.sh` / `./quick_start.sh`). **Acone** / **AC One** is **dual-arm**; **Lift 2S** is the full-body platform.

| Robot | Role | Branch | How-to |
|-------|------|--------|--------|
| **ARX Lift 2S** | Full-body (arms + lift + **chassis**) | `arx-lift2s` | [ARX Lift 2S](1-arx_lift2s.md) |
| **Acone** / **AC One** | **Dual-arm** (same ARX description tree; not Lift 2S) | `arx-lift2s` (`quick_start` co-debug) | [ARX Lift 2S](1-arx_lift2s.md) |
| **HighTorque Panthera HT** | Dual-arm manipulator | `panthera-ht` | [HighTorque Panthera HT](2-panthera_ht.md) |

These robots are fully supported for external users without requiring private repository access.

### Internal Path (fa-deploy-ws)

FiveAges team members can deploy to additional robots including W2, W2R, S2, S2R, and dual-arm CCS configurations. See [fa-deploy-ws setup](../../../1-getting_started/4-fa_deploy_ws.md).

## In this section

```{toctree}
:maxdepth: 1

1-arx_lift2s
2-panthera_ht
```

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
- [ ] Hardware interface plugins are loaded

### Configuration

- [ ] Correct robot model selected
- [ ] Joint limits verified
- [ ] Speed limits set conservatively
- [ ] Domain ID configured correctly

## Deployment Steps

### Verify mock operation

:::{code-block} bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=<your_robot>
# Test all planned motions
:::

### Configure the hardware interface

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

### First motion

Use the **branch README** / `./quick_start.sh`. There is no documented `<robot>_bringup hardware_test.launch.py` or `/enable_motors` service.

- Lift2S: **split body** or **full body** — [ARX Lift 2S](1-arx_lift2s.md), [分体控制 vs 全身控制](../../../3-concepts/7-split_vs_wbc.md)
- Joint FSM (HOME / HOLD / MOVEJ): [Use Basic Joint Controller](../../4-controllers/11-basic_joint.md) — `/fsm_command` is `std_msgs/Int32` (mixed stacks: `3` = OCS2, MOVEJ = `4`); MoveJ targets are `/{controller}/target_joint_position` (`Float64MultiArray`), not `/target_joint_positions` `JointState`

### Gradual testing

Start from HOLD, then HOME, then MOVEJ / OCS2 as the **running** controller allows ([FSM and Topics](../../../3-concepts/4-fsm_and_topics.md)). `/fsm_command` is `std_msgs/Int32` (not strings such as `stand` / `walk`).

## Public Robot Deployment (open-deploy-ws)

Use the matching **branch** and its README scripts. `demo.launch.py robot:=arx_acone` is Acone (dual-arm), not Lift 2S. The HighTorque launch key is `panthera_ht`.

- **[ARX Lift 2S](1-arx_lift2s.md)** — `git clone -b arx-lift2s …` then `./init_repo.sh` and `./quick_start.sh`. Full-body including chassis.
- **Acone** / **AC One** — **dual-arm**; pick ACone in that same `quick_start` menu for co-debug.
- **[HighTorque Panthera HT](2-panthera_ht.md)** — `git clone -b panthera-ht …` then `./init_repo.sh` / `./release.sh --install` and `./quick_start.sh`. Isomorphic teleop: `./teleop_start.sh`.

## Internal Deployment (fa-deploy-ws)

The `fa-deploy-ws` README is not public. After you have access, run the **init / quick-start scripts named in that README**. Flags and robot IDs are documented only there. Public-side pattern: [fa-deploy-ws Setup](../../../1-getting_started/4-fa_deploy_ws.md).

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
- [ARX Lift 2S](1-arx_lift2s.md) and [HighTorque Panthera HT](2-panthera_ht.md) for public robots
- [Add a Robot](../10-add_a_robot.md) for custom integrations
