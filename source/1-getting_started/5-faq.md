# FAQ

Frequently asked questions and common troubleshooting solutions.

## Installation Issues

### Q: `apt` cannot find `python3-colcon-common-extensions` / `python3-rosdep` / `python3-vcstool`

Those packages are in the ROS 2 apt index, not stock Ubuntu. On a bare 24.04 host or container, add the ROS key + Noble ROS 2 source, then `apt update`, **before** installing them. Full order: [Install Environment](2-install_environment.md). fishros is an optional shortcut, not the only path.

### Q: rosdep init fails with "already initialized"

This is normal if you've used ROS 2 before. Just run update:

```bash
rosdep update
```

### Q: Package not found after apt install

This applies to packages that **are** in the ROS apt index (for example `ros-jazzy-desktop`) after the ROS 2 apt source exists. After ROS is installed, clone a deploy workspace and run `./init_repo.sh`, then `source install/setup.bash` after `colcon build`.

```bash
sudo apt update
```

### Q: OCS2 `.deb` not found via apt

OCS2 is **not** published to ROS 2 / Ubuntu apt software sources. `sudo apt install ros-jazzy-ocs2` will not find it.

**Primary path:** in `open-deploy-ws` / `fa-deploy-ws`, run `./init_repo.sh`. Choose `d` for OCS2 (menu 1), switch source ↔ deb with menu **2**, or install/update with menu **3** (`./scripts/install_core_debs.sh --only ocs2`).

To build from source, choose `s` during init (or menu 2).

:::{admonition} Manual fallback
:class: note

Download the matching asset from [ocs2_ros2 Releases](https://github.com/legubiao/ocs2_ros2/releases) and `sudo dpkg -i ros-jazzy-ocs2_*.deb` only if you are not using a deploy workspace.
:::

## Submodule Issues

### Q: Submodules are empty after clone

In `open-deploy-ws` / `fa-deploy-ws`, re-run `./init_repo.sh` (menu 1). In FaSim-Isaac / fa-py-libraries / lerobot_ros2, re-run that repo’s `./init.sh` (or `./init.sh all`). Do not start with a recursive `git submodule update --init --recursive`.

### Q: `error: cannot run ssh: No such file or directory`

[`.gitmodules`](https://github.com/fiveages-sim/open-deploy-ws/blob/main/.gitmodules) uses `git@github.com:…`. `git config url.https://github.com/.insteadOf git@github.com:` alone does **not** fix `git submodule update` (nested repos read their own `.gitmodules` and call `ssh`). Current `./init_repo.sh` on `main` temporarily rewrites those URLs to HTTPS. Force with `--https` / `OPEN_DEPLOY_GIT_HTTPS=1`. Steps: [open-deploy-ws Setup](3-open_deploy_ws.md).

### Q: How do I run `init_repo.sh` in CI / a container (no TTY)?

On current open-deploy-ws `main`:

```bash
./init_repo.sh --public --ocs2=deb --arms=source --common=source
```

Same defaults as the interactive menu. Also: `--https` / `OPEN_DEPLOY_GIT_HTTPS=1`, `-y` / `--yes`, and env `OPEN_DEPLOY_VISIBILITY`, `OPEN_DEPLOY_OCS2`, `OPEN_DEPLOY_ARMS`, `OPEN_DEPLOY_COMMON`. `./init_repo.sh --help` lists the rest. If your checkout predates these flags, pull `main`.

### Q: Access denied to submodule

This usually means you're trying to access a private submodule without proper access, or the remote is still SSH and this machine has no key.

**For open-deploy-ws:** Only public submodules should be needed. Check that:
1. You're on the correct branch
2. The submodule is listed as public in `submodules_visibility.conf`
3. You have `ssh` + a key, or you passed `--https` / `OPEN_DEPLOY_GIT_HTTPS=1`

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

### Q: colcon fails on an empty directory under `arms_ros2_control`

Public init leaves private nested modules empty (`controller/ocs2_wbc_controller`, `libraries/lina_planning`, `libraries/ocs2_humanoid`, and uninitialized `hardwares/*`). Current public-mode `./init_repo.sh` writes `COLCON_IGNORE` on those empty dirs. If colcon still walks one (old checkout), pull `main` and re-run init, or `touch <empty-dir>/COLCON_IGNORE`. Details: [open-deploy-ws Setup](3-open_deploy_ws.md).

### Q: Where is Taku?

On `robot_descriptions` branch **`feature/agilex`** at `humanoid/Dyna/taku_description` — not on the default `main` submodule pin. Launch: `ros2 launch robot_common_launch humanoid.launch.py robot:=taku` ([package README](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/humanoid/Dyna/taku_description/README.md)). There is no lean `open-deploy-ws` Taku branch. Checkout steps: [open-deploy-ws Setup](3-open_deploy_ws.md).

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

Build from a workspace that already ran `./init_repo.sh`. If `ros2` / `colcon` is missing, finish [Install Environment](2-install_environment.md) first. After a successful build, `source install/setup.bash` in the launch terminal.

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
1. Hardware parameter matches your setup (`mock_components`, `gz`, `isaac`, or `real` — there is no `hardware:=mock`)
2. Robot parameter matches a `{key}_description` package
3. Required hardware interfaces are initialized

```bash
ros2 launch ocs2_arm_controller demo.launch.py
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

Use **FaSim-Isaac** `./init.sh` / `./run.sh`. Default Isaac path is `ISAACSIM_DIR` (`~/isaacsim` unless overridden in `config/fa_sim.local.conf`). Version for the optional Isaac ROS 2 workspace comes from the `./init.sh` operation 2 menu (GitHub tags; fallback in `config/fa_sim.conf`: `6.0.1` / `6.0.0` / `5.1.0`) — do not assume a single hardcoded minor version.

1. Confirm the directory in `ISAACSIM_DIR` exists and contains the launch scripts named in `config/fa_sim.conf` (`isaac-sim.sh`, …)
2. Copy `config/fa_sim.local.template.conf` → `config/fa_sim.local.conf` if Isaac is not at `~/isaacsim`
3. Re-run `./run.sh` and pick PhysX / Newton / Headless Streaming from the menu (`./run.sh` has no `--headless` / `--robot` flags)

### Q: Isaac Sim connection fails

1. Verify Isaac Sim is running (`./run.sh` from FaSim-Isaac)
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
