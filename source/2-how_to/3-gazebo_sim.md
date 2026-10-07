# Gazebo Simulation

Run robot demos with Gazebo Harmonic physics simulation.

## Prerequisites

- Workspace built
- Gazebo Harmonic packages installed

## Install Gazebo

```bash
sudo apt install ros-jazzy-gz-*
```

## Steps

### 1. Source Workspace

```bash
source /opt/ros/jazzy/setup.bash
source ~/open-deploy-ws/install/setup.bash
```

### 2. Launch with Gazebo

```bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz
```

This launches:
- Gazebo simulator with robot model
- ROS 2 controllers
- RViz visualization

### 3. Interact

Send commands as usual:

```bash
ros2 topic pub /target_pose geometry_msgs/msg/PoseStamped \
  "{header: {frame_id: 'base_link'}, pose: {position: {x: 0.3, y: 0.0, z: 0.4}, orientation: {w: 1.0}}}" \
  --once
```

## Launch Options

```bash
# With specific robot
# Acone arm (not Lift 2S)
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=gz

# Without RViz (Gazebo only)
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz rviz:=false

# Headless mode
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz headless:=true
```

## Gazebo Features

### Physics Tuning

The default physics parameters work for most robots. For custom tuning, modify the SDF files in the description packages.

### World Files

Custom world files can be loaded:

```bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz world:=custom_world.sdf
```

### Recording

Record simulation for playback:

```bash
gz service -s /world/default/control \
  --reqtype gz.msgs.WorldControl \
  --reptype gz.msgs.Boolean \
  --timeout 3000 \
  --req 'pause: false'
```

## Mock vs Gazebo

| Aspect | Mock | Gazebo |
|--------|------|--------|
| Physics | None | Full simulation |
| Speed | Real-time | Configurable |
| Collisions | No | Yes |
| Sensors | Placeholder | Simulated |
| Resource use | Low | Medium-high |

Use mock for controller development, Gazebo for behavior testing.

## Verification

- Gazebo window shows robot in environment
- Robot responds to ROS 2 commands
- Physics interactions (collisions, gravity) work

## Troubleshooting

### Gazebo crashes on start

```bash
# Check GPU drivers
nvidia-smi

# Try software rendering
export LIBGL_ALWAYS_SOFTWARE=1
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz
```

### Robot falls through floor

Check that the world file includes a ground plane.

### Controllers don't start

Wait for Gazebo to fully initialize before sending commands. Check for error messages about failed controller spawning.

### High CPU usage

Reduce physics update rate or run headless:

```bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz headless:=true
```
