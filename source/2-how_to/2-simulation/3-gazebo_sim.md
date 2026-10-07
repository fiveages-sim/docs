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

From the workspace root after `./init_repo.sh` and `colcon build`:

```bash
source install/setup.bash
```

### 2. Launch with Gazebo

`hardware:=gz` sets xacro `ros2_control_hardware_type` to `gz` and `gazebo` to `true` ([`build_xacro_mappings()`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/robot_common_launch/common/launch_arg_utils.py)). [ocs2_arm README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/README.md): install `ros-jazzy-ros-gz` and `ros-jazzy-gz-ros2-control`.

```bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz
```

Acone xacro plugin for this key: `gz_ros2_control/GazeboSimSystem`.

### 3. Interact

FSM: `/fsm_command` (`std_msgs/Int32`). Do **not** publish `/target_pose`. See [FSM and Topics](../../3-concepts/4-fsm_and_topics.md).

## Launch Options

```bash
# Acone arm (not Lift 2S)
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=gz
```

`demo.launch.py` declares `world` (default `dart`). It does **not** declare `rviz:=false` or `headless:=true`.

## Gazebo Features

### Physics Tuning

The default physics parameters work for most robots. For custom tuning, modify the SDF files in the description packages.

### World Files

`demo.launch.py` declares `world` (default `dart`). Use only world keys that exist in the description / launch you are running.

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

See the Gazebo / `ros-jazzy-ros-gz` docs for renderer settings. This launch file does not document a `headless:=` argument.
