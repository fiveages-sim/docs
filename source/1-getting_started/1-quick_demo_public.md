# Quick Demo (Public Path)

This guide gets you from a **finished environment install** to a moving robot using the public `open-deploy-ws` workspace.

## Prerequisites

- Ubuntu 24.04
- ROS 2 Jazzy + rosdep already installed — do this **first**: [Install Environment](2-install_environment.md)
- Git with GitHub access

Do not hand-write `source /opt/ros/...` + workspace overlay into `~/.bashrc`. After clone, use **`./init_repo.sh`**. After `colcon build`, source that workspace’s `install/setup.bash` in the terminal you launch from (standard ROS 2 overlay; `open-deploy-ws` has no extra env script).

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

[`demo.launch.py`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/launch/demo.launch.py) defaults: `robot:=cr5`, `hardware:=mock_components`. You can omit both.

```bash
source install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py
```

There is **no** `hardware:=mock` key. See [ros2_control in This Stack](../3-concepts/1-ros2_control_here.md).

### 5. Observe the Demo

You should see:

- **RViz** (config `demo_ocs2.rviz` from the same launch)
- **`arms_target_manager`** when `enable_arms_target_manager` is `true` (launch default)
- Controller FSM starting in **HOLD** ([ocs2_arm README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/README.md))

Switch FSM with `/fsm_command` (`std_msgs/Int32`): `1` HOME, `2` HOLD, `3` OCS2 — [FSM and Topics](../3-concepts/4-fsm_and_topics.md).

Do **not** publish a stack-wide `/target_pose`. That topic is not in the OCS2 arm README or `demo.launch.py`. Branch-specific EE topics (for example `/left_target` on `panthera-ht`) are listed in that branch’s README.

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

In a new terminal, from the workspace root after a successful build:

```bash
source install/setup.bash
```

`install/setup.bash` overlays ROS. Do not add a hand-written `~/.bashrc` `source /opt/ros/...` chain as the documented path.

## Next Steps

- [Switch to different robots](../2-how_to/1-basic_operations/2-switch_robot.md)
- [Run Gazebo simulation](../2-how_to/2-simulation/3-gazebo_sim.md)
- [Connect Python interface](../2-how_to/3-programming/5-python_interface.md)

## Video Demo

```{admonition} TODO
:class: warning

Video demonstration to be added showing expected RViz output and robot motion.
```
