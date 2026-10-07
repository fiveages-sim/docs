# Run Mock Demo

Run a robot demonstration in mock hardware mode without physical hardware or simulation.

## Prerequisites

- Workspace built and sourced
- RViz2 installed (`ros-jazzy-rviz2`)

## Steps

### 1. Source Workspace

```bash
source /opt/ros/jazzy/setup.bash
source ~/open-deploy-ws/install/setup.bash
```

### 2. Launch Mock Demo

```bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=mock
```

### 3. Send Target Pose

In a new terminal:

```bash
source ~/open-deploy-ws/install/setup.bash
ros2 topic pub /target_pose geometry_msgs/msg/PoseStamped \
  "{header: {frame_id: 'base_link'}, pose: {position: {x: 0.3, y: 0.1, z: 0.4}, orientation: {w: 1.0}}}" \
  --once
```

### 4. Observe Motion

Watch RViz — the robot should move to the target pose.

## With Different Robots

```bash
# Dobot CR5
ros2 launch ocs2_arm_controller demo.launch.py robot:=dobot_cr5 hardware:=mock

# Acone (arm only, not Lift 2S)
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=mock

# HighTorque Panthera HT
ros2 launch ocs2_arm_controller demo.launch.py robot:=panthera_ht hardware:=mock
```

### With Gripper

```{admonition} TODO
:class: note

For valid robot + gripper combinations, check the launch files in `arms_ros2_control`.
```

```bash
# General pattern
ros2 launch ocs2_arm_controller demo.launch.py robot:=<robot_name> gripper:=<gripper_name> hardware:=mock
```

## Launch Parameters

| Parameter | Options | Default |
|-----------|---------|---------|
| `hardware` | `mock`, `gz`, `isaac`, (real) | varies |
| `robot` | Robot name | `dobot_cr5` |
| `gripper` | Gripper name | none |
| `rviz` | `true`, `false` | `true` |

## Verification

Success indicators:
- RViz window opens showing robot model
- Controller logs show "Controller started"
- Robot responds to target pose commands

## Troubleshooting

### Robot doesn't move

- Check target pose is reachable
- Verify no error messages in controller output
- Ensure correct robot parameter

### RViz shows broken model

- Rebuild description packages
- Check URDF for errors: `check_urdf <file>.urdf`

### Command not found

```bash
source install/setup.bash  # Must source after building
```
