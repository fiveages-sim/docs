# Newcomer Learning Path

This guide provides a structured day-by-day approach to learning the FiveAges Sim ecosystem. Follow it sequentially to build understanding from fundamentals to advanced topics.

## Overview

| Stage | Goal | Time Estimate |
|-------|------|---------------|
| Day 0 | Map the stack | 1-2 hours reading |
| Day 1 | First motion in sim | 2-4 hours |
| Day 2 | Switch robots | 1-2 hours |
| Day 3 | fa-py-libraries and Viser | 2-3 hours |
| Day 4 | Isaac Sim | 2-4 hours |
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

After this launch, the clip below shows the effect in RViz (a single arm): drag the end-effector target, adjust joints with the JointControlPanel sliders, and use HOME to reset. It does not show the terminal or the launch command, so it is not a complete startup recording, and it is not Isaac physics verification.

```{raw} html
<video controls preload="metadata" width="100%">
  <source src="../_static/videos/day1-first-motion-rviz-single-arm.mp4" type="video/mp4">
</video>
```

**Primary sources:** [open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws), [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control)

**Outcome:** RViz opens with the OCS2 demo; FSM starts in HOLD. See [Quick Demo](../1-getting_started/1-quick_demo_public.md).

## Day 2: Switch Robots

**Goal:** Change the robot model and understand the description system.

**Tasks:**
1. Prefer `./init_repo.sh` so nested modules under `src/robot-descriptions/` match `submodules_visibility.conf` (do not recursive-init).
2. Rebuild the packages you need, then `source install/setup.bash`.
3. Launch one of the robots below. Omit `hardware:=`; the launch default is `mock_components`.

### ARX Lift 2S

Use the `arx-lift2s` branch of `open-deploy-ws` for this robot, not the Day 1 default tree. Clone and `./init_repo.sh` are on [ARX Lift 2S](../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md).

```bash
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift2s
```

`arx_lift2s` is **ARX Lift 2S** (方舟无限), the full-body mobile manipulator (arms, lift, and chassis). It is not **Acone** / **AC One** (`arx_acone`, dual-arm). `full_body.launch.py` starts `ocs2_wbc_controller`, which ships in the `ros-jazzy-arms-ros2-control` deb.

This clip shows operating the ARX Lift 2S (方舟无限 Lift 2S, a dual-arm mobile manipulator) in RViz: drag the left and right end-effector interactive markers, then use the right-click menu to send the end-effector pose; both arms follow the targets. The clip has no terminal or launch commands.

```{raw} html
<video controls preload="metadata" width="100%">
  <source src="../_static/videos/day2-arx-lift2s.mp4" type="video/mp4">
</video>
```

### FiveAges W2 with xhand1

W2 is a FiveAges wheeled-arm robot. Its URDF is public ([fa-w2-description](https://github.com/fiveages-sim/fa-w2-description)); the usual workspace is [fa-deploy-ws](https://github.com/fiveages-sim/fa-deploy-ws) (default branch `fa-w2`). See [FiveAges robot descriptions](../4-reference/descriptions/4-fiveages_umbrella.md) and [fa-deploy-ws Setup](../1-getting_started/4-fa_deploy_ws.md).

```bash
ros2 launch ocs2_arm_controller full_body.launch.py robot:=fiveages_w2 type:=xhand1
```

This clip is a W2 with xhand1 operation demo: in RViz, drag the dual-arm end-effector targets, reset both arms, and adjust the head joints with JointControlPanel.

```{raw} html
<video controls preload="metadata" width="100%">
  <source src="../_static/videos/day2-fiveages-w2-xhand1.mp4" type="video/mp4">
</video>
```

**Primary sources:** [robot_descriptions](https://github.com/fiveages-sim/robot_descriptions), brand-specific READMEs

**Outcome:** You have switched from the Day 1 CR5 `demo.launch.py` to a `full_body.launch.py` robot, for example ARX Lift 2S or FiveAges W2 with xhand1.

## Day 3: fa-py-libraries and Viser

**Goal:** Install fa-py-libraries and open Viser in a browser, so you can see the robot and send basic commands before you start Isaac Sim.

Viser is the browser 3D view and control page from [ros2-viser](https://github.com/fiveages-sim/ros2-viser). Launch it from **fa-py-libraries**, not as a standalone product and not from lerobot_ros2.

**Tasks:**

1. Keep a robot demo from Day 1 or Day 2 running. The ros2-viser README asks you to start the control stack first; `/robot_description` must be available.
2. Install fa-py-libraries (Python 3.12 env; this also installs `ros2_robot_interface` and `ros2-viser`):
   ```bash
   git clone https://github.com/fiveages-sim/fa-py-libraries.git
   cd fa-py-libraries
   ./init.sh all
   ```
3. Start Viser from that repository:
   ```bash
   ./run.sh viser
   ```
   `./run.sh` with no arguments opens a menu; item 1 is `ros2-viser launch`. The command runs `ros2-viser/launch.py`.
4. In a browser, open the URL that Viser prints in the terminal (`访问 URL`). The same output shows the host and port; this launch has no separate host/port flag. You can also scan the QR code it prints.
5. The page starts as an empty scene. If only one robot is present, it loads automatically. If there are several, pick one under “选择命名空间”. If the robot comes up later, click “刷新命名空间列表”.
6. Confirm the model is visible. For a first control check: use HOME / HOLD on the state panel; switch to OCS2 and drag the end-effector handles; or switch to MOVEJ, move the joint sliders, and send the target. On a mobile base such as G1-D, `launch.py` sets the visualization frame to `world`; you can also choose `map` or `odom` on the page so the model and the handles share the same ground.

Do not copy the rest of the Python API here. Full Viser UI: [ros2-viser](../4-reference/python_apps/3-ros2_viser.md). Writing scripts with `ROS2RobotInterface`: [Python Interface](../2-how_to/3-programming/5-python_interface.md).

**Primary sources:** [fa-py-libraries](https://github.com/fiveages-sim/fa-py-libraries), [ros2-viser](https://github.com/fiveages-sim/ros2-viser)

**Outcome:** You can open Viser in a browser, see the robot, and use the page to move it while a demo is running.

## Day 4: Isaac Sim

**Goal:** Run physics simulation in Isaac Sim (FaSim), instead of mock hardware. This is the default simulation path.

**FaSim** pairs NVIDIA Isaac Sim with the same ROS 2 运控 stack as the real robot. Follow [Isaac Sim](../2-how_to/2-simulation/4-isaac_sim.md): clone [FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac), run `./init.sh`, then `./run.sh`, and connect with **one** of the two paths on that page (`hardware:=isaac`, or Play on a `ROS2ControlLaunch` payload). Default Isaac path is `ISAACSIM_DIR` (`~/isaacsim`); override in `config/fa_sim.local.conf`.

Start Viser the way you did on Day 3, after the Isaac / ROS 2 stack is up, so you can view and control the robot in the browser: [Start Viser](../2-how_to/3-programming/5-python_interface.md#start-viser).

This clip is a G1-D demonstration of full-body control in Isaac Sim. On the Viser web control interface, drag the dual-arm end-effector targets and move the chassis in rotation and translation; G1-D in Isaac Sim moves with it. Start Viser as in [Start Viser](../2-how_to/3-programming/5-python_interface.md#start-viser) after the stack is up.

```{raw} html
<video controls preload="metadata" width="100%">
  <source src="../_static/videos/isaac-g1d-full-body-mobile.mp4" type="video/mp4">
</video>
```

The same clip, and the rest of the Isaac Sim steps, are on [G1-D full-body control and chassis motion](../2-how_to/2-simulation/4-isaac_sim.md#g1-d-full-body-control-and-chassis-motion).

What the two connections and the Kit extensions do: [FaSim-Isaac](../4-reference/simulation/2-fasim_isaac.md). Assets: [robot_usds](../4-reference/simulation/3-robot_usds.md), [Environment assets](../4-reference/simulation/5-env_assets.md).

**Primary sources:** [FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac), [robot_usds](https://github.com/fiveages-sim/robot_usds)

**Outcome:** You can start FaSim and see the robot move in Isaac Sim with the same ROS 2 运控 as the real robot, plus simulation ground truth.

### Gazebo (alternative)

If you need Gazebo Harmonic instead, follow [Gazebo Simulation](../2-how_to/2-simulation/3-gazebo_sim.md):

```bash
# Install Gazebo packages (if not already)
sudo apt install ros-jazzy-gz-*

# Launch with Gazebo
ros2 launch ocs2_arm_controller demo.launch.py hardware:=gz
```

## Day 5: Teleoperation

**Goal:** Start with VR or a game controller, then know what the other input methods are for.

Keep the robot stack from Days 1–4 running. Teleop only publishes targets or assist events into that stack; it does not replace it.

Inputs in this stack have different jobs: **end-effector pose** (VR controllers, Vive Tracker, DexCap exoskeleton arms), **joint-space following** (isomorphic teleop), **fingers / grippers** (VR triggers, Wuji gloves, DexCap gloves), and **enable / pause / FSM assists** (some VR buttons, the joystick enable switch, the foot pedal).

### Start here: VR

**What it is for.** Drive the arms from the headset controllers’ end-effector pose. Triggers operate the gripper or hand. Buttons handle FSM, pause, and — on 全身 — some arm enable/disable assists. Use this path when you have a Pico or Quest headset.

**Minimum steps.** Follow [VR Teleoperation](../2-how_to/5-teleoperation/6-vr_teleop.md). You need fa-py-libraries from Day 3, `enable_vr: true` in the description’s `config/ocs2/target_manager.yaml` (most robots default off), and a network to the headset. Then:

```bash
cd ~/fa-py-libraries
./run.sh vr
```

Open the URL shown in the headset browser (WebXR). For the lower-latency XRoboToolkit path, use `./run.sh vr-xrt-service` then `./run.sh vr-xrt` as on that page. Pico **Enterprise** is the preferred Pico SKU (USB 网络共享, and a **different App** from Pico consumer).

**What you should see.** The arms follow the VR controllers, and you can change FSM and the gripper from the controller buttons.

### Start here: game controller (joystick)

**What it is for.** A gamepad or joystick, without a headset, to command arm velocity (`control_input` → `/left_target/twist` and `/right_target/twist`) and, in chassis mode, `/cmd_vel`. Use this path when you only have a game controller.

**Minimum steps.** With the robot stack already running, follow [Joystick teleop](../2-how_to/5-teleoperation/9-joystick_teleop.md):

```bash
ros2 launch arms_teleop joystick_teleop.launch.py
```

Joystick control starts disabled; press the right stick to enable it (package README). Most mapped gamepads use the generic SDL layout automatically.

**What you should see.** After you enable the controller, stick motion changes the arm target, or the chassis in chassis mode.

### Other methods

These are additional ways to supply pose, finger, or assist signals. Use the linked pages for setup; this day does not walk through them.

- **Isomorphic teleop** (同构遥操作) — Master–slave joint following on HighTorque Panthera HT, not end-effector pose. On the `panthera-ht` branch, real-robot teleop is `./teleop_start.sh`: [HighTorque Panthera HT](../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md), [Isomorphic Teleop](../2-how_to/5-teleoperation/7-isomorphic_teleop.md).
- **DexCap exoskeleton and gloves** (internal) — The exoskeleton measures waist and arm joints; the gloves measure finger joints. Combined arm + hand teleop: [DexCap Teleoperation](../2-how_to/5-teleoperation/8-dexcap_teleop.md).
- **VR gesture / hand tracking** — The current `./run.sh vr` path starts **controller** mode. This docs set does not document a launch entry that turns on VR gesture or hand-tracking recognition.
- **Wuji gloves** (internal) — Finger and hand joint teleop, with optional Vive Tracker for arm pose: [wuji_glove_teleop](../4-reference/teleop/5-wuji_glove.md).
- **Foot pedal** — An assist, not a complete teleop setup. `foot_pedal_teleop` in `arms_teleop` publishes events on `/teleop/controller_state` (FSM up/down, arm enable, STORAGE/UPDATE, mirror). It does not replace VR or the game controller: [Joystick teleop](../2-how_to/5-teleoperation/9-joystick_teleop.md#foot-pedal-assist-only).
- **Vive Tracker** (internal) — SteamVR **Vive Tracker** poses mapped to arm end-effector targets (`vive_tracker_teleop`). That is the name used in the package and in these docs; it is not documented as “Valve Tracker”: [Vive Tracker](../4-reference/teleop/6-vive_tracker.md).

**Primary sources:** [VR Teleoperation](../2-how_to/5-teleoperation/6-vr_teleop.md), [arms_teleop README](https://github.com/fiveages-sim/arms_ros2_control/blob/main/command/arms_teleop/README.md)

**Outcome:** You can run either the VR path or the game-controller path, and you can tell which of the other devices is for pose, fingers, or enable/pause assists.

## Day 6: Real Hardware

**Goal:** Deploy to physical robots.

### Public Path (ARX Lift 2S, Acone, HighTorque Panthera HT)

Use the matching **branch README** and `./quick_start.sh`. **Acone** / **AC One** is **dual-arm**; **Lift 2S** is the full-body platform.

- **[ARX Lift 2S](../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md)** — full-body including chassis: `git clone -b arx-lift2s …` then `./init_repo.sh` / `./quick_start.sh`
- **Acone** / **AC One** — **dual-arm**; same `arx-lift2s` workspace, pick ACone in `quick_start` for co-debug
- **[HighTorque Panthera HT](../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md)** — dual-arm: `git clone -b panthera-ht …` then `./init_repo.sh` / `./quick_start.sh`

### Internal path (FiveAges robots)

FiveAges robots (W1, W2, W2R, S2, S2R, and the dual-arm CCS) use [fa-deploy-ws](https://github.com/fiveages-sim/fa-deploy-ws), default branch `fa-w2`. W1, W2, and S2 URDF, plus the Gen1 and Gen2 USD remotes, are public. W2R and S2R are not. The description map is [FiveAges robot descriptions](../4-reference/descriptions/4-fiveages_umbrella.md).

Open the checkout you were given and follow that repository’s README. The script name shared with the public workspace is `./init_repo.sh`.

GitHub hides a private repository from anyone without access. That does not block every binary.

| Repository | Use it for | Access |
|------------|------------|--------|
| [fa-deploy-ws](https://github.com/fiveages-sim/fa-deploy-ws) | The internal workspace (`fa-w2`) | Clone and follow its README |
| [fa-w2r-description](https://github.com/fiveages-sim/fa-w2r-description) | W2R URDF | Read or change that description |
| [fa-s2r-description](https://github.com/fiveages-sim/fa-s2r-description) | S2R URDF | Read or change that description |
| [ocs2-wbc-controller](https://github.com/fiveages-sim/ocs2-wbc-controller) | Whole-body controller source | Read or change the source |
| [ocs2-humanoid](https://github.com/fiveages-sim/ocs2-humanoid) | Wheeled-arm motion library source | Read or change the source |

You can run whole-body control without those two source checkouts. The standard GitHub Release package `ros-jazzy-arms-ros2-control` already contains `ocs2_wbc_controller`, `ocs2_humanoid`, and `lina_planning` ([arms deb notes](https://github.com/fiveages-sim/arms_ros2_control/blob/main/README.deb.md)). In `open-deploy-ws` or `fa-deploy-ws`, choose `d` for arms in `./init_repo.sh`, or run `./scripts/install_core_debs.sh --only arms`. The script installs that standard package. It does not install `ros-jazzy-arms-ros2-control-full`, and the package is not on Ubuntu or ROS apt. Private descriptions, other hardware interfaces, and teleop trees are separate repositories. They stay on the [Repository Map](3-repo_map.md). Public W1, W2, and S2 URDF stays on [FiveAges robot descriptions](../4-reference/descriptions/4-fiveages_umbrella.md).

**Tasks:**

1. Open [fa-deploy-ws](https://github.com/fiveages-sim/fa-deploy-ws) and run the init and quick-start scripts named in that README.
2. Follow [fa-deploy-ws Setup](../1-getting_started/4-fa_deploy_ws.md).

**Safety:** Prove the motion in `mock_components`, or in the sim path that workspace documents, before you set `hardware:=real`.

(day-7-bring-one-new-robot-into-fasim)=
## Day 7: Bring one new robot into FaSim

**Goal:** Independently connect a robot that is not already a demo, so Isaac and the ROS 2 stack move it. This is the exam, not a walkthrough of CR5 or W2. You are done when a command moves that robot in the viewport and you can hand in the items below.

**Before you start.** Finish Days 0–4. You can reach HOLD with `hardware:=mock_components`, Viser opens in the browser, Isaac Sim is installed, `ISAACSIM_DIR` is set, and you have run FaSim `./init.sh` and `./run.sh`.

Package layout: [Add a Robot](../2-how_to/6-deployment/10-add_a_robot.md). Start Sim and choose a connection: [Isaac Sim](../2-how_to/2-simulation/4-isaac_sim.md). In-process inputs, swerve chassis graphs, clock, and TF: [FaSim-Isaac](../4-reference/simulation/2-fasim_isaac.md).

### Build these four pieces

1. **A description.** Add a `{robot}_description` package whose xacro includes a `ros2_control` block. Simulation plugins come from [`simulation_hardware.xacro`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/xacro/ros2_control/simulation_hardware.xacro). Before you open Isaac, `ros2 launch ocs2_arm_controller demo.launch.py robot:=<key>` reaches HOLD. Leave `hardware` at the default.

2. **A USD stage.** `./run.sh` opens it, and the stage has one ArticulationRoot for this robot. Put it under [robot_usds](../4-reference/simulation/3-robot_usds.md), or in a project scene you can open. There is no `./run.sh --robot`.

3. **One connection for those joints.** Use the topic bridge *or* the in-process graph, as in [Isaac Sim](../2-how_to/2-simulation/4-isaac_sim.md). For `isaac_sim`, the xacro must accept that hardware key, and the payload must contain `ROS2ControlLaunch` ([ROS 2 Control extension](../4-reference/simulation/2-fasim_isaac.md#ros-2-control-extension)). On a four-wheel swerve chassis such as Linkhou S2 or Taku, the steer and drive joints are commanded by `SwerveController`, not by that hardware key ([Swerve extension](../4-reference/simulation/2-fasim_isaac.md#swerve-extension)).

4. **Controllers that match the body.** An arm, or a split-body robot, uses `ocs2_arm_controller` (`demo` or `split_body`). A planner model that includes the mobile base uses `full_body.launch.py` and `ocs2_wbc_controller`. That controller is already in the `ros-jazzy-arms-ros2-control` deb from Day 6. Cloning [ocs2-wbc-controller](https://github.com/fiveages-sim/ocs2-wbc-controller) is how you read or edit the source. Leave `infoFile` empty to keep the description default. Lock a mobile base with the `mobile_base_tcp` info file and `BASE_LOCK`. `full_body` together with a `fixed_base` info file has no virtual chassis joint for that lock, and arm enable can stay in `WAITING_FOR_ENABLE_POLICY`.

### Work in this order

1. In mock, the launch above reaches HOLD, and the joint names match the xacro.
2. Run `./run.sh`, open your USD, and press Play so physics runs.
3. Connect with the topic bridge or the in-process graph. Read the joint-state topic with `ros2 topic echo`, or run `ros2 control list_controllers`.
4. Send a small joint target. The same joints move in Isaac. On the in-process graph, `ros2 topic hz /clock` follows the physics step.

### What you hand in

- The description package, or the branch, and the USD path you opened.
- The launch line, or the `ROS2ControlLaunch` prim you played (and the swerve graph, if you used one).
- The joint-state topic or the controller list, and the motion you sent.
- A short note of known limits, plus steps another person can replay, and a demo recording.

### How you know it works

Check the functions that belong to the robot you chose: joint control, chassis motion, end effector, and sensor data. For a wheeled robot, show that the base drives; for a robot with a dexterous hand, show that the hand opens and closes.

**Joints.** Mock reaches HOLD, Play runs, and the joint names in the state topic or in `ros2 control list_controllers` match the xacro. A command moves those joints in the viewport.

**Base.** Follow the [TF](../4-reference/simulation/2-fasim_isaac.md#tf) and, if the robot drives on a map, [Navigation](../4-reference/simulation/2-fasim_isaac.md#navigation) sections. A ROS namespace does not rename `frame_id`. Composer `ros2-stack` is a separate process on the host.

**End effector.** The launch arguments `type`, `left_type`, or `right_type` name this gripper or hand, and you can see it open or close. There is no `gripper:=` argument.

**Sensors.** While Play is running, the camera or lidar topics from the scene are publishing. Camera rigs stay on the scene USD.

If a timed motion finishes much too fast, check `/clock` against [Clock](../4-reference/simulation/2-fasim_isaac.md#clock) before you edit joint gains.

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
