# FAQ

Frequently asked questions and common troubleshooting solutions.

## Installation Issues

### Q: rosdep init fails with "already initialized"

This is normal if you've used ROS 2 before. Just run update:

```bash
rosdep update
```

### Q: Package not found after apt install

Source the ROS 2 setup and update:

```bash
source /opt/ros/jazzy/setup.bash
sudo apt update
```

### Q: OCS2 `.deb` not found via apt

OCS2 is **not** published to ROS 2 / Ubuntu apt software sources. `sudo apt install ros-jazzy-ocs2` will not find it.

Install the prebuilt `.deb` from [ocs2_ros2 Releases](https://github.com/legubiao/ocs2_ros2/releases) (download the matching asset for your arch/distro, then `sudo dpkg -i ros-jazzy-ocs2_*.deb`), or run `./init_repo.sh` in `open-deploy-ws` / `fa-deploy-ws` and choose `d` for OCS2 (`scripts/install_core_debs.sh`).

To build from source instead, choose `s` during `init_repo.sh`, or clone `https://github.com/legubiao/ocs2_ros2.git` branch `ros2` and colcon build.

## Submodule Issues

### Q: Submodules are empty after clone

Initialize the submodules:

```bash
git submodule update --init
```

For specific submodules only:

```bash
git submodule update --init src/robot_descriptions
```

### Q: Access denied to submodule

This usually means you're trying to access a private submodule without proper access.

**For open-deploy-ws:** Only public submodules should be needed. Check that:
1. You're on the correct branch
2. The submodule is listed as public in `submodules_visibility.conf`

**For fa-deploy-ws:** Verify your GitHub SSH key has access to private repos:

```bash
ssh -T git@github.com
```

### Q: Submodule conflicts during update

```bash
git submodule foreach git checkout .
git submodule update --init
```

## Build Issues

### Q: colcon build fails with missing dependency

Install dependencies via rosdep:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

### Q: numpy version conflict

Some packages require numpy < 2:

```bash
pip install 'numpy<2'
```

### Q: CMake cannot find package

Ensure ROS 2 is sourced before building:

```bash
source /opt/ros/jazzy/setup.bash
colcon build
```

### Q: Build runs out of memory

Limit parallel jobs:

```bash
colcon build --parallel-workers 2
```

Or build specific packages:

```bash
colcon build --packages-up-to <package-name>
```

## Runtime Issues

### Q: Node/topic not found

Ensure workspace is sourced:

```bash
source install/setup.bash
```

Check if the node is running:

```bash
ros2 node list
ros2 topic list
```

### Q: Controller fails to start

Check that:
1. Hardware parameter matches your setup (`mock`, `gz`, `isaac`, or real)
2. Robot parameter matches available descriptions
3. Required hardware interfaces are initialized

```bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=mock robot:=dobot_cr5
```

### Q: No communication between machines

Verify:
1. ROS Domain ID matches on both machines
2. Network connectivity exists
3. Firewall allows ROS 2 traffic

```bash
# Check domain ID
echo $ROS_DOMAIN_ID

# Test connectivity
ros2 topic list  # Should show topics from both machines
```

## CAN Interface Issues

### Q: CAN interface not found

Check if the interface exists:

```bash
ip link show
```

If the interface has a different name, rename it:

```bash
sudo ip link set can0 down
sudo ip link set can0 name <expected_name>
sudo ip link set <expected_name> up
```

### Q: CAN communication timeout

1. Verify CAN bus is properly terminated
2. Check baud rate matches robot configuration
3. Ensure no conflicting CAN traffic

## Simulation Issues

### Q: Gazebo crashes on launch

Install all Gazebo packages:

```bash
sudo apt install ros-jazzy-gz-*
```

Check GPU drivers if using hardware rendering.

### Q: Isaac Sim won't start or scripts fail

**FaSim-Isaac requires Isaac Sim 6.1 at `~/isaacsim`.**

1. Verify installation path: `ls ~/isaacsim/python.sh` — must exist
2. Verify version: Must be Isaac Sim 6.1 (not older versions)
3. If installed elsewhere, create a symlink:
   ```bash
   ln -s /your/actual/path ~/isaacsim
   ```

### Q: Isaac Sim connection fails

1. Verify Isaac Sim 6.1 is running
2. Check that the topic bridge is active
3. Ensure `hardware:=isaac` is set in launch
4. Check Domain ID matches between Isaac and ROS 2

## Network Configuration

### Q: How do I find the correct Domain ID?

The Domain ID is robot-specific. For internal deployments, consult your robot's documentation or team lead. For development with mock hardware, any ID works (default is 0).

### Q: Zenoh vs DDS?

- **DDS (default):** Works out of the box for same-network communication
- **Zenoh:** Better for cross-network, NAT traversal, or high-latency links

To use Zenoh:

```bash
sudo apt install ros-jazzy-rmw-zenoh-cpp
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
```

## Getting Help

If your issue isn't covered here:

1. Check the relevant package's README
2. Search existing GitHub issues in the repository
3. Open a new issue with:
   - Ubuntu/ROS 2 version
   - Steps to reproduce
   - Full error message
   - Relevant launch command

**Issue trackers:**
- Documentation: [fiveages-sim/docs/issues](https://github.com/fiveages-sim/docs/issues)
- Arms controller: [fiveages-sim/arms_ros2_control/issues](https://github.com/fiveages-sim/arms_ros2_control/issues)
- Descriptions: [fiveages-sim/robot_descriptions/issues](https://github.com/fiveages-sim/robot_descriptions/issues)
