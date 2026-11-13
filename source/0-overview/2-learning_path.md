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
| Day 7 | Bring one new robot into FaSim | One robot, mock then sim |

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
1. [Install Environment](../1-getting_started/2-install_environment.md) — Ubuntu 24.04, ROS 2 Jazzy + rosdep. On a bare host: add the ROS apt source, then `ros-jazzy-desktop` / `ros-dev-tools` (fishros is optional). Workspace entry is `./init_repo.sh`, then `source install/setup.bash`.
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

### Isaac Sim (FaSim)

**FaSim** pairs NVIDIA Isaac Sim high-fidelity simulation with the same ROS 2 运控 stack as the real robot, so motion matches hardware while the sim supplies ground truth. Assets: [FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac) (one-click USD + scene pull), [robot_usds](https://github.com/fiveages-sim/robot_usds).

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
4. Connect ROS 2 using **one** of the two Isaac paths in [Isaac Sim](../2-how_to/2-simulation/4-isaac_sim.md):
   - Topic bridge, from the workspace terminal: `ros2 launch ocs2_arm_controller demo.launch.py hardware:=isaac`
   - In-process: open a USD whose ROS payload contains `ROS2ControlLaunch` and press Play. That path sets `hardware=isaac_sim` inside Isaac. It is not a second `hardware:=` on `demo.launch.py`.

**Primary sources:** [FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac), [robot_usds](https://github.com/fiveages-sim/robot_usds)

**Outcome:** Physics-based simulation with Gazebo, or FaSim (Isaac + ROS 2 运控, matching real-robot motion plus ground truth).

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
   from ros2_robot_interface import ROS2RobotInterface, ROS2RobotInterfaceConfig

   interface = ROS2RobotInterface(ROS2RobotInterfaceConfig())
   interface.connect()
   joint_state = interface.get_joint_state()
   pose = interface.left_arm_handler.get_pose()
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

These links need repository access. Without it, GitHub does not open the page. That is expected.

FA **deploy** (W1, W2, W2R, S2, S2R, dual-arm CCS) uses [fa-deploy-ws](https://github.com/fiveages-sim/fa-deploy-ws) (default branch `fa-w2`). W1/W2/S2 URDF and Gen1/Gen2 USD remotes are public; **W2R and S2R are not open**. See [FiveAges robot descriptions](../4-reference/descriptions/4-fiveages_umbrella.md).
```

Open the private checkout you were given, then follow **that repository’s README**. The shared script name is `./init_repo.sh`. Flags and robot IDs stay in that README.

| Repository | What it is | Access |
|------------|------------|--------|
| [fa-deploy-ws](https://github.com/fiveages-sim/fa-deploy-ws) | Internal workspace (`fa-w2`) | Required |
| [fa-w2r-description](https://github.com/fiveages-sim/fa-w2r-description) | W2R URDF | Required |
| [fa-s2r-description](https://github.com/fiveages-sim/fa-s2r-description) | S2R URDF | Required |
| [fa-wce3-description](https://github.com/fiveages-sim/fa-wce3-description) | Gen3 URDF | Required |
| [fiveages-gen3-robot-usds](https://github.com/fiveages-sim/fiveages-gen3-robot-usds) | Gen3 USD | Required |
| [ocs2-wbc-controller](https://github.com/fiveages-sim/ocs2-wbc-controller) | Whole-body controller | Required |
| [ocs2-humanoid](https://github.com/fiveages-sim/ocs2-humanoid) | Wheeled-arm motion library | Required |

More private descriptions, hardware interfaces, and teleop checkouts are linked on the [Repository Map](3-repo_map.md). Public W1 / W2 / S2 URDF stays on [FiveAges robot descriptions](../4-reference/descriptions/4-fiveages_umbrella.md).

**Tasks:**
1. Open [fa-deploy-ws](https://github.com/fiveages-sim/fa-deploy-ws) and run the init / quick-start scripts named in that README.
2. Follow [fa-deploy-ws Setup](../1-getting_started/4-fa_deploy_ws.md).

**Safety:** Verify in `mock_components` (or that workspace’s documented sim path) before `hardware:=real`.

## Day 7: FaSim integration exam

**Goal:** Bring **one new robot** into FaSim so Isaac and the ROS 2 运控 stack move it. Pass by taking that robot through mock, then sim, until you can see the joints move. Replaying the existing CR5 or W2 demo is only a warm-up.

**You already need** Days 0–3: `./init_repo.sh`, a launch that reaches HOLD with `hardware:=mock_components`, and FaSim `./init.sh` / `./run.sh`. Isaac Sim is installed and `ISAACSIM_DIR` is set.

Pick one robot. Add odometry, Nav2, or a dexterous hand only when this robot has them. Work through the steps below.

Procedure and file layout: [Add a Robot](../2-how_to/6-deployment/10-add_a_robot.md). Isaac start and the two connections: [Isaac Sim](../2-how_to/2-simulation/4-isaac_sim.md). Mechanism: [FaSim-Isaac](../4-reference/simulation/2-fasim_isaac.md).

### Required for every robot

1. **Description.** A `{robot}_description` package whose xacro has a `ros2_control` block. Simulation plugins come from [`simulation_hardware.xacro`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/xacro/ros2_control/simulation_hardware.xacro). `ros2 launch ocs2_arm_controller demo.launch.py robot:=<key>` (omit `hardware:=`) reaches HOLD before you open Isaac.
2. **USD.** A stage `./run.sh` can open, with one ArticulationRoot for this robot, under [robot_usds](https://github.com/fiveages-sim/robot_usds) or a project scene you can access. There is no `./run.sh --robot`.
3. **One sim connection** for those joints.
   - **Topic bridge:** `hardware:=isaac` → `TopicBasedSystem`. The xacro `joint_commands_topic` / `joint_states_topic` equal that graph’s `topicName`. The shared macro writes `/isaac/joint_command` and `/isaac/joint_states`. A robot graph may use other names (W2 topic-bridge payload: `/joint_command` and `/joint_states`). `demo.launch.py` has no namespace argument.
   - **In-process:** Play a payload that contains `ROS2ControlLaunch` (W2: [`fiveages.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/fiveages.usda)). The node sets `hardware=isaac_sim` and `isaac_prim_path`. The description xacro must accept `isaac_sim`.
4. **Controllers.** Arm or split body: `ocs2_arm_controller` (`demo` or `split_body`). Whole body only when this robot’s planner model includes the mobile base: `full_body.launch.py` and, with access, [ocs2-wbc-controller](https://github.com/fiveages-sim/ocs2-wbc-controller). Leave `infoFile` empty to keep the description default. To lock a mobile base, use `mobile_base_tcp` and `BASE_LOCK`. `full_body` together with a `fixed_base` info file has no virtual chassis joint for that lock, and arm enable can stay waiting.
5. **Motion you can see.** A small FSM home or joint target changes the same joints in Isaac.

### Only if this robot has it

| Piece | When | What to wire |
|-------|------|----------------|
| Chassis / odom | It has a mobile base | Isaac publishes `world → odom → base_*`. `robot_state_publisher` publishes the URDF tree (`base_footprint → base_link` when both exist). OCS2 `baseFrame` is that same link. One publisher per TF edge. A ROS namespace does not rename `frame_id`. |
| Gripper or hand | It has one | Launch `type` / `left_type` / `right_type`. There is no `gripper:=`. |
| Navigation | The scene drives the base on a map | `NavigationLaunch` on the USD. `map` is a path relative to the opened `env/` layer. It starts `navigation_isaac_gt.launch.py`. Composer `ros2-stack` is a separate host process. |
| Second robot | Two articulations in one stage | Each root has its own graph and `ROS2ControlLaunch` `namespace`. Topics live under `/<ns>/`. Frame names stay `world`, `odom`, `base_link`. |

### Phases

1. Mock: the demo launch above, FSM HOLD, joint names from the xacro.
2. `./run.sh`, open your USD, Play runs physics.
3. Topic bridge **or** in-process graph. `ros2 topic echo` the joint-state topic, or `ros2 control list_controllers`.
4. Command a small motion. The sim joints move. On the in-process graph, `ros2 topic hz /clock` tracks the physics step.

### What you hand in

- The description package (or branch) and the USD path you opened.
- The launch line **or** the `ROS2ControlLaunch` prim you played.
- The joint-state topic or controller list you saw, and the motion you commanded.

### Pass when you can show

- Mock HOLD, then sim Play, on **this** robot.
- Joint state or the controller state interfaces match the xacro joint names.
- A command moves those joints in Isaac.
- If the payload publishes odometry: `world → odom → base_*` from Isaac, URDF tree from `robot_state_publisher`, and no second node on the same edge.
- In-process: `/robot_description` comes from `robot_state_publisher`. The controller manager is started with robot-description publishing off.

A motion that finishes too fast is a `/clock` problem (physics-step clock versus playback tick). The FaSim reference describes that clock. It is not fixed by editing joint gains.

## Optional: Synthetic data (Isaac)

**Goal:** Understand the Isaac datagen path (not Gazebo): USD scene → `ROS2RobotInterface` → composer `task_queue` → LeRobot dataset on disk.

Follow [Synthetic Data](../2-how_to/7-synthetic_data/0-index.md) on [lerobot_ros2](https://github.com/fiveages-sim/lerobot_ros2) `main` and [robot_action_composer](https://github.com/fiveages-sim/robot_action_composer) `main`. Stop at recording/export; skip training.

## After the beginner path

Continue by **role** in [More applications](../6-more_applications/0-index.md): field commissioning (现场调试), classical algorithm (传统方案算法工程师), VLA collect / train / deploy (VLA 采训推), simulation (仿真工程师).

## Tips for Success

1. **Don't skip mock mode** — Always verify behavior in mock before simulation or real hardware
2. **Read the warnings** — The stack logs helpful messages about configuration issues
3. **Use lean branches** — `open-deploy-ws` offers `dobot-cr5`, `arx-lift2s`, and `panthera-ht`
4. **Ask questions** — File issues on the relevant repository for bugs or unclear documentation
