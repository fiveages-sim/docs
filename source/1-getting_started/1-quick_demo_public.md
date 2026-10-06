# Quick Demo (Public Path)

This guide gets you from zero to a moving robot in the shortest time using the public `open-deploy-ws` workspace.

## Prerequisites

- Ubuntu 24.04
- ROS 2 Jazzy installed (see [Install Environment](2-install_environment.md) if needed)
- Git with GitHub access

## Steps

### 1. Clone the Workspace

```bash
cd ~/
git clone https://github.com/fiveages-sim/open-deploy-ws.git
cd open-deploy-ws
```

### 2. Initialize Repository

Run the initialization script:

```bash
./init_repo.sh
```

The script will prompt you for:
- **OCS2 installation method**: Choose `d` for Debian package (recommended for quick start)
- **Submodule visibility**: Automatically configured for public-only access

```{admonition} Debian vs Source
:class: tip

The Debian package (`ros-jazzy-ocs2`) is faster to install but cannot be modified. Choose source if you need to develop OCS2 itself.
```

### 3. Install Dependencies

```bash
source /opt/ros/jazzy/setup.bash
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

### 4. Build the Workspace

```bash
colcon build --symlink-install
```

This typically takes 10-20 minutes on first build.

### 5. Source and Launch

```bash
source install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=mock
```

### 6. Observe the Demo

You should see:
- **RViz** window with robot visualization
- **Terminal** output showing controller status
- Robot responding to MPC target commands

To send a target pose:
```bash
# In a new terminal
source install/setup.bash
ros2 topic pub /target_pose geometry_msgs/msg/PoseStamped "{header: {frame_id: 'base_link'}, pose: {position: {x: 0.3, y: 0.0, z: 0.4}, orientation: {w: 1.0}}}" --once
```

## Troubleshooting

### Build Fails with Missing Packages

```bash
rosdep install --from-paths src --ignore-src -r -y
```

### OCS2 Package Not Found

If using Debian install:
```bash
sudo apt install ros-jazzy-ocs2
```

### Submodule Errors

```bash
git submodule update --init --recursive
```

### Workspace Not Sourced

Always source after opening a new terminal:
```bash
source /opt/ros/jazzy/setup.bash
source ~/open-deploy-ws/install/setup.bash
```

## Next Steps

- [Switch to different robots](../2-how_to/2-switch_robot.md)
- [Run Gazebo simulation](../2-how_to/3-gazebo_sim.md)
- [Connect Python interface](../2-how_to/5-python_interface.md)

## Video Demo

```{admonition} TODO
:class: warning

Video demonstration to be added showing expected RViz output and robot motion.
```
