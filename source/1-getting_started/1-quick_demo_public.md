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

The script will:

- Configure submodule visibility (public only by default)
- Prompt per core module for `d` (GitHub Release `.deb`) or `s` (source)
- Sync selected source submodules, run `rosdep install`, and install chosen debs via `scripts/install_core_debs.sh`

You still need `colcon build` after init. Do **not** follow with a second hand-run `rosdep` unless something failed.

```{admonition} Deb vs Source
:class: tip

The GitHub Release `.deb` (`ros-jazzy-ocs2`) is faster to install but cannot be modified. Choose source if you need to develop OCS2 itself. OCS2 is not available from packages.ros.org / Ubuntu apt. To **switch** later, re-run `./init_repo.sh` and pick **2) 切换模块安装方式**.
```

### 3. Build the Workspace

```bash
colcon build --symlink-install
```

This typically takes 10-20 minutes on first build.

### 4. Source and Launch

```bash
source install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=mock
```

### 5. Observe the Demo

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

Re-run `./init_repo.sh` menu **5) 仅运行 rosdep**, or:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

### OCS2 Package Not Found

OCS2 is not in the ROS apt index. Re-run `./init_repo.sh`: menu **1** with `d` for OCS2, menu **2** to switch source ↔ deb, or menu **3**:

:::{code-block} bash
./scripts/install_core_debs.sh --only ocs2
:::

### Submodule Errors

Re-run `./init_repo.sh` (menu 1) instead of a blind recursive submodule init. The script already syncs selected source modules.

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
