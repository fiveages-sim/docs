# Newcomer Learning Path

This guide provides a structured day-by-day approach to learning the FiveAges Sim ecosystem. Follow it sequentially to build understanding from fundamentals to advanced topics.

## Overview

| Stage | Goal | Time Estimate |
|-------|------|---------------|
| Day 0 | Map the stack | 1-2 hours reading |
| Day 1 | First motion in sim | 2-4 hours |
| Day 2 | Switch robots | 1-2 hours |
| Day 3 | Gazebo / Isaac | 2-4 hours |
| Day 4 | Python interface | 2-3 hours |
| Day 5 | Teleoperation | 2-4 hours |
| Day 6 | Real hardware | Varies |
| Day 7+ | Add a robot | Project-dependent |

```{admonition} Real Hardware for External Users
:class: tip

**ARX Lift 2S** is the full-body ARX (方舟无限) mobile manipulator (including chassis). **Acone** / **AC One** is **dual-arm**, not Lift 2S. **HighTorque Panthera HT** (高擎) is a dual-arm manipulator. Prefer the dedicated how-to pages. You don't need internal access for those `open-deploy-ws` branches.
```

## Day 0: Map the Stack

**Goal:** Understand the ecosystem structure and choose your entry path.

**Tasks:**
1. Read this [Overview](0-index.md) section
2. Study the [Architecture](1-architecture.md) diagram
3. Decide: Public path (`open-deploy-ws`) or Internal path (`fa-deploy-ws`)
4. Review the [Repository Map](3-repo_map.md)

**Outcome:** You can explain the five layers and know which workspace to start with.

## Day 1: First Motion in Simulation

**Goal:** Install the environment, then run a robot demo (`hardware` default `mock_components`).

**Tasks:**
1. [Install Environment](../1-getting_started/2-install_environment.md) — Ubuntu 24.04, ROS 2 Jazzy + rosdep (open-deploy-ws README: fishros / `ros-jazzy-desktop`). Workspace entry is `./init_repo.sh`, then `source install/setup.bash`.
2. Clone `open-deploy-ws` and run the official init script:
   ```bash
   git clone https://github.com/fiveages-sim/open-deploy-ws.git
   cd open-deploy-ws
   ./init_repo.sh
   ```
3. Build the workspace:
   ```bash
   colcon build --symlink-install
   ```
4. Launch the demo (defaults: `robot:=cr5`, `hardware:=mock_components` — omit both; there is no `hardware:=mock`):
   ```bash
   source install/setup.bash
   ros2 launch ocs2_arm_controller demo.launch.py
   ```

**Primary sources:** [open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws), [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control)

**Outcome:** RViz opens with the OCS2 demo; FSM starts in HOLD. See [Quick Demo](../1-getting_started/1-quick_demo_public.md).

## Day 2: Switch Robots

**Goal:** Change the robot model and understand the description system.

**Tasks:**
1. Prefer `./init_repo.sh` so nested modules under `src/robot-descriptions/` match `submodules_visibility.conf` (do not recursive-init).
2. Rebuild the packages you need, then `source install/setup.bash`.
3. Launch with the new robot (omit `hardware:=` to keep `mock_components`):
   ```bash
   ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone
   ```
   `arx_acone` is **Acone** (dual-arm), not Lift 2S. Full-body ARX Lift 2S uses the `arx-lift2s` branch scripts — see [ARX Lift 2S](../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md).

**Primary sources:** [robot_descriptions](https://github.com/fiveages-sim/robot_descriptions), brand-specific READMEs

**Outcome:** You can switch between Dobot CR5, Acone (dual-arm), Galbot, etc.

## Day 3: Gazebo and Isaac Simulation

**Goal:** Run physics simulation instead of mock hardware.

### Gazebo Harmonic

```bash
# Install Gazebo packages (if not already)
sudo apt install ros-jazzy-gz-*

# Launch with Gazebo
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz
```

### Isaac Sim

```{admonition} FaSim-Isaac scripts
:class: warning

Use **FaSim-Isaac** `./init.sh` then `./run.sh`. Default Isaac path is `ISAACSIM_DIR` (`~/isaacsim`); override in `config/fa_sim.local.conf`. Version for the optional ROS 2 workspace comes from the init menu (fallback list in `config/fa_sim.conf`), not a hardcoded minor version in these docs.
```

1. Install NVIDIA Isaac Sim (default directory `~/isaacsim`, or set `ISAACSIM_DIR`).
2. Clone and initialize FaSim-Isaac:
   ```bash
   git clone git@github.com:fiveages-sim/FaSim-Isaac.git
   cd FaSim-Isaac
   ./init.sh
   ```
3. Start Isaac (`./run.sh` menu: PhysX / Newton / Headless Streaming):
   ```bash
   ./run.sh
   ```
4. In another terminal, launch the ROS 2 side with Isaac hardware:
   ```bash
   ros2 launch ocs2_arm_controller demo.launch.py hardware:=isaac
   ```

**Primary sources:** [FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac), [robot_usds](https://github.com/fiveages-sim/robot_usds)

**Outcome:** Physics-based simulation with Gazebo or Isaac Sim.

## Day 4: Python Interface

**Goal:** Control the robot programmatically.

**Tasks:**
1. Install fa-py-libraries:
   ```bash
   cd ~/
   git clone https://github.com/fiveages-sim/fa-py-libraries.git
   cd fa-py-libraries
   ./init.sh all    # Python 3.12 env; installs ros2_robot_interface and related submodules
   ```
2. Write a simple script:
   ```python
   from ros2_robot_interface import RobotInterface
   
   robot = RobotInterface()
   robot.connect()
   robot.move_j([0.0, -0.5, 0.5, 0.0, 0.0, 0.0])
   robot.gripper_close()
   ```

**Primary sources:** [fa-py-libraries](https://github.com/fiveages-sim/fa-py-libraries), [ros2_robot_interface](https://github.com/fiveages-sim/ros2_robot_interface)

**Outcome:** You can script robot motions in Python.

## Day 5: Teleoperation

**Goal:** Control the robot via VR or isomorphic teleop.

### VR Teleoperation

**Supported headsets:** Pico Enterprise (recommended; USB 网络共享, Enterprise App), Pico consumer (different App), and Meta Quest. Backends: WebXR (`./run.sh vr`) or XRoboToolkit (`./run.sh vr-xrt`).

```bash
cd fa-py-libraries
./run.sh vr
```

```{admonition} Pico Enterprise vs consumer
:class: tip

Pico **Enterprise** and Pico **consumer** are different SKUs: Enterprise supports USB 网络共享 and uses a **different App**. Install the App that matches the headset edition.
```

### Isomorphic Teleop (HighTorque Panthera HT)

Master–slave **isomorphic teleop** (同构遥操作). On the `panthera-ht` branch, real-robot teleop is `./teleop_start.sh` — see [HighTorque Panthera HT](../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md). Mock (package README):

```bash
ros2 launch drag_teleop_controller drag_teleop_controller.launch.py \
  role:=master hardware:=mock_components
ros2 launch drag_teleop_controller drag_teleop_controller.launch.py \
  role:=slave hardware:=mock_components
```

**Primary sources:** VR pose publisher, [drag_teleop_controller](https://github.com/fiveages-sim/drag_teleop_controller)

**Outcome:** Real-time control via VR headset or master–slave isomorphic teleop.

## Day 6: Real Hardware

**Goal:** Deploy to physical robots.

### Public Path (ARX Lift 2S, Acone, HighTorque Panthera HT)

Use the matching **branch README** and `./quick_start.sh`. **Acone** / **AC One** is **dual-arm**; **Lift 2S** is the full-body platform.

- **[ARX Lift 2S](../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md)** — full-body including chassis: `git clone -b arx-lift2s …` then `./init_repo.sh` / `./quick_start.sh`
- **Acone** / **AC One** — **dual-arm**; same `arx-lift2s` workspace, pick ACone in `quick_start` for co-debug
- **[HighTorque Panthera HT](../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md)** — dual-arm: `git clone -b panthera-ht …` then `./init_repo.sh` / `./quick_start.sh`

### Internal Path (FA Robots)

```{admonition} Internal Access Required
:class: warning

FA robots (W2, W2R, S2, S2R, dual-arm CCS) require access to `fa-deploy-ws`. Contact your team lead for repository access and hardware allocation.
```

**Tasks:**
1. Clone `fa-deploy-ws` and run the init / quick-start scripts named in **that repository’s README** (not public). Flags and robot IDs are documented only there.
2. Follow [fa-deploy-ws Setup](../1-getting_started/4-fa_deploy_ws.md).

**Safety:** Verify in `mock_components` (or that workspace’s documented sim path) before `hardware:=real`.

## Day 7+: Add a Robot

**Goal:** Integrate a new robot into the ecosystem.

**Tasks:**
1. Create a description package with URDF/xacro
2. Add ros2_control hardware interface YAML
3. Configure OCS2 controller parameters
4. Test progression: mock → simulation → real hardware

See the [Developer Guide](../5-developer/0-index.md) for detailed instructions.

## Optional: Synthetic data (Isaac)

**Goal:** Understand the Isaac datagen path (not Gazebo): USD scene → `ROS2RobotInterface` → composer `task_queue` → LeRobot dataset on disk.

Follow [Synthetic Data](../2-how_to/7-synthetic_data/0-index.md). Documented composer/lerobot branches are `feature/dex-grasp-generator` and `feature/sim-grasp-datagen`. Stop at recording/export; skip training.

## Tips for Success

1. **Don't skip mock mode** — Always verify behavior in mock before simulation or real hardware
2. **Read the warnings** — The stack logs helpful messages about configuration issues
3. **Use lean branches** — `open-deploy-ws` offers `dobot-cr5`, `arx-lift2s`, and `panthera-ht`
4. **Ask questions** — File issues on the relevant repository for bugs or unclear documentation
