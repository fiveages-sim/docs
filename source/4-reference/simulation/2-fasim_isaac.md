# FaSim-Isaac

FaSim-Isaac is the Isaac Sim workspace for this stack. It holds robot and scene USD, can install an optional Isaac ROS 2 Jazzy overlay, and installs two OmniGraph extensions: one starts 运控 inside Sim, and one computes swerve (舵轮) commands for a chassis. It is not only a launcher for opening a USD.

Use the [Isaac Sim How-To](../../2-how_to/2-simulation/4-isaac_sim.md) to install, start Sim, pick a launch, and run the first checks. This page explains the hardware keys, the two Kit extensions, and why a joint topic, a clock, or a TF edge behaves the way it does.

**Repository:** [fiveages-sim/FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac) `main` (`3606dc89`, 2026-11-13). In-process ros2_control is on `main` ([#7](https://github.com/fiveages-sim/FaSim-Isaac/pull/7), `1a4193a3`). The swerve extension is also on `main`. Replicator capture (`exts/fasim.replicator.sdg`) is on `feature/ros2-control-node`, not on `main`.

**README:** [README.md](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/README.md)

(fasim-hardware-interfaces)=

## Hardware keys `isaac` and `isaac_sim`

These keys are ros2_control hardware interfaces in the robot description xacro. They are not the FaSim Kit extensions below, and they are not a second robot body. One stage uses one of them.

`isaac` is the topic bridge you pass on a ROS 2 launch. `isaac_sim` is set inside Isaac when Play starts the in-process node. It is not a `demo.launch.py` flag.

| Key | Where it is set | Plugin | Joint I/O |
|-----|-----------------|--------|-----------|
| `isaac` | `ros2 launch … hardware:=isaac` | `topic_based_ros2_control/TopicBasedSystem` | `sensor_msgs/JointState` topics |
| `isaac_sim` | `emit_control` inside `ROS2ControlLaunch` | `isaacsim_ros2_control/IsaacSimSystem` | The articulation in the Isaac process |

Both keys are in the shared [`simulation_hardware.xacro`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/xacro/ros2_control/simulation_hardware.xacro) and in the [`robot_common_launch` README](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/README.md). `hardware:=isaac` writes `/isaac/joint_command` and `/isaac/joint_states`. `hardware:=isaac_sim` writes `<param name="prim_path">` from the launch argument `isaac_prim_path`, which is the ArticulationRoot. `use_sim_time` is true for `gz`, `isaac`, and `isaac_sim` unless you pass the launch argument as `true` or `false` ([`launch_arg_utils.py`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/robot_common_launch/common/launch_arg_utils.py)).

If a robot xacro whitelists `validated_hardware_type`, include `isaac_sim`. Otherwise that xacro fails on purpose when the in-process node starts.

`{hardware}.yaml` is merged only when the file exists. `load_robot_config` applies files in this order: common, type yaml, `{variant}.yaml`, end-effector compose, `{hardware}.yaml`, then `control.patch` ([`robot_utils.py`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/robot_common_launch/common/robot_utils.py)). The hardware file comes after compose so a later compose pass does not drop gripper keys from `isaac.yaml` ([robot-descriptions-common #41](https://github.com/fiveages-sim/robot-descriptions-common/pull/41)). `isaac_sim` can reuse `isaac.yaml`. `emit_control` passes `hardware_yaml=isaac`. A file named `isaac_sim.yaml` is loaded when the launch hardware string is `isaac_sim`.

### Topic names follow the robot

The shared macro’s `/isaac/joint_*` pair is the topic-bridge default. Acone uses that macro. W2’s topic-bridge graph publishes `/joint_command` and `/joint_states` ([`ros2.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/ros2.usda)). The xacro `<param>` and the graph `topicName` are the same strings. `demo.launch.py` has no namespace argument that rewrites them.

In-process W2 ([`fiveages.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/fiveages.usda)) does not bridge body or arm `JointState` topics. The controller manager owns those joints. Chassis `cmd_vel` and `odom` stay on the child ROS graph.

(fasim-kit-extensions)=

## FaSim Kit extensions

`./init.sh` operation 5 installs two extensions into this Isaac (`ISAACSIM_DIR`, default `~/isaacsim`). The script symlinks `exts/<name>` into `extsUser/` and adds the extension to the full, Newton, and streaming kit files. Reinstall Isaac, then run operation 5 again. Restart a running Isaac so the extensions load.

The two extensions have different entry points. Do not treat a `SwerveController` graph as a ros2_control hardware key, and do not treat `ROS2ControlLaunch` as `hardware:=isaac`.

| Extension | OmniGraph nodes | What it is for |
|-----------|-----------------|----------------|
| `exts/fasim.ros2.nodes` | `ROS2ControlLaunch`, `NavigationLaunch` | Start the in-process controller manager (`hardware=isaac_sim`) and, optionally, host Nav2 |
| `exts/fasim.steering.nodes` | `SwerveController` | Turn a planar twist into steer-position and wheel-velocity commands for a four-wheel swerve chassis |

(fasim-ros2-control)=

## ROS 2 Control extension

`fasim.ros2.nodes` is the in-process 运控 entry. After Play, `OgnROS2ControlLaunch` ([`OgnROS2ControlLaunch.ogn`](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/exts/fasim.ros2.nodes/fasim/ros2/nodes/ogn/python/nodes/OgnROS2ControlLaunch.ogn)) runs once and calls `emit_control`. That path sets `hardware=isaac_sim`, passes the ArticulationRoot as `isaac_prim_path`, and starts Isaac’s ControllerManager in the same process. Examples on this path include G1D, G1, and W2. W2’s in-process payload is [`W2/payloads/ROS/fiveages.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/fiveages.usda).

This is not the topic-bridge path. A stage that only uses `hardware:=isaac` does not go through this node.

### `ROS2ControlLaunch` inputs

| Input | Role |
|-------|------|
| `targetPrim` | One ArticulationRoot, or a parent that contains exactly one |
| `robot` | Description stem (`unitree_g1d`, `fiveages_w2`). Empty reads the USD `Robot` variant |
| `mode` | `demo`, `split_body`, or `full_body` |
| `type` | `robot_common_launch` end-effector key. Empty reads EE variants on the stage |
| `namespace` | Controller manager namespace. Empty is the global `/controller_manager` |
| `infoFile` | OCS2 `.info` basename. Empty keeps the description default |
| `useSimTime` | Forced true for `isaac_sim` (needs `/clock`) |
| `publishRobotDescription` | Latch the same xacro on `/robot_description` (default true) |
| `profile` | Optional robot profile YAML path |
| `enableGripper` | Same as `robot_common_launch` `enable_gripper` |
| `rosSetup` | Path to `install/setup.bash`. Empty: first non-`/opt/ros` install on `AMENT_PREFIX_PATH` |
| `enableArmsTargetManager` | Spawn `arms_target_manager` as a host process (default true) |
| `arms` | `robot_common_launch` arms xacro key. Empty keeps the description default |

`emit_control` builds one xacro URDF and points both the controller manager and `/robot_description` at it. `Ros2ControlManager.setup` is called with `publish_robot_description=False`, so the manager does not publish that topic a second time. `robot_state_publisher` on the host publishes `/robot_description` and the URDF TF tree. If that process does not start, a latched `fasim_robot_description` publisher is the fallback. The resource manager therefore loads the description once.

Play does not rebuild a URDF from the stage on every start. The node reuses the description xacro, and it falls back to synthesizing a URDF from the USD only for an unexpected prim.

### CppAD cache

`ocs2_arm_controller` declares `recompile_libraries` with default true when `task.info` does not set `recompileLibraries` ([`CtrlComponent.h`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/include/ocs2_arm_controller/control/CtrlComponent.h)). The library folder is `${OCS2_PLANNING_URDF_DIR:-/tmp}/ocs2_ros2/<robot>/ocs2/<content-hash>`.

On the in-process path, `emit_control` then sets `recompile_libraries: false` on the main controller only: `ocs2_arm_controller` for `demo` and `split_body`, `ocs2_wbc_controller` for `full_body`. A topic-bridge launch (`hardware:=isaac`) does not run `emit_control`, so it keeps the controller default. That default stays true unless that robot’s info file or YAML already says false.

A simulated robot that runs 运控 inside Isaac starts faster for two reasons: the node reuses the description xacro, and it reuses this CppAD cache.

### `infoFile` and `BASE_LOCK`

`infoFile` overrides `info_file_name` on the main controller. `fixed_base_tcp` drops the virtual chassis degrees of freedom (`manipulatorModelType` 0), so whole-body planning covers the body and the arms.

`emit_control` warns when `mode` is `full_body` and the override name contains `fixed_base`. The planner then has `basePlan=0`, so a runtime `BASE_LOCK` has nothing to constrain, and arm enable can stay in `WAITING_FOR_ENABLE_POLICY`. Lock the base with `mobile_base_tcp` and `BASE_LOCK`.

`full_body` loads `ocs2_wbc_controller` from the GitHub Release package `ros-jazzy-arms-ros2-control` (`./init_repo.sh` with arms set to `d`, or `./scripts/install_core_debs.sh --only arms`). The same package contains `ocs2_humanoid` and `lina_planning`. It is not an apt package, and it is not `ros-jazzy-arms-ros2-control-full`. Open [ocs2-wbc-controller](https://github.com/fiveages-sim/ocs2-wbc-controller) when you need to read or change the source. You can run the controller from the deb without that private source checkout.

### Add a robot to the in-process path

1. The `{robot}_description` xacro includes `simulation_hardware_plugin` for `isaac_sim`, or lists `isaac_sim` in `validated_hardware_type` if that robot uses a whitelist.
2. The USD has one ArticulationRoot and a payload that contains `ROS2ControlLaunch`. Set `targetPrim`, `robot` or the `Robot` variant, and `mode`.
3. Operation 5 is installed and Isaac was restarted. The ROS variant on the stage is the in-process payload, not the topic-bridge payload.
4. Press Play, then check as in the [How-To](../../2-how_to/2-simulation/4-isaac_sim.md#in-process-hardware-interface-isaac_sim).

### What you should see

`ros2 control list_controllers` lists the controllers for that `mode`. `/joint_states` is the controller’s `joint_state_broadcaster`, not the topic-bridge `/isaac/joint_*` pair. `/clock` ticks near the physics rate (see [Clock](#clock)). A command moves the articulation in the viewport. Arm degrees of freedom are not also bridged on `/isaac/joint_command`.

(fasim-swerve)=

## Swerve extension

`fasim.steering.nodes` provides `fasim.steering.nodes.SwerveController` ([`OgnSwerveController.ogn`](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/exts/fasim.steering.nodes/fasim/steering/nodes/ogn/python/nodes/OgnSwerveController.ogn), kinematics in [`swerve.py`](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/exts/fasim.steering.nodes/fasim/steering/nodes/swerve.py)). It is an OmniGraph node, not a ros2_control hardware interface. A ScriptNode used to hold the same kinematics in module globals, which made Isaac disable every Action Graph until the user opted in. This node keeps state on the instance instead.

It reads a planar twist in the body frame and writes two arrays, in the same wheel order: front-left, rear-left, rear-right, front-right (`fl`, `rl`, `rr`, `fr`).

- `Steer_Position_Command` and `Steer_Joints` — steer angles, in radians, sent as position commands
- `Wheel_Velocity_Command` and `Wheel_Joints` — wheel velocity commands, sent as velocity commands

The two command types go to two `isaacsim.core.nodes.IsaacArticulationController` nodes. Do not wire steer angles as wheel velocities, or the other way around.

`Desired_Linear_Velocity_X` / `Y` are forward and lateral speed in metres per second. `Desired_Angular_Velocity` is yaw rate in radians per second. Wheel positions in the profiles are body-frame `(x, y)` in metres, with `x` forward and `y` left. Inverse kinematics use `vx_total = vx - ω y_i` and `vy_total = vy + ω x_i`.

`linearGain` scales wheel speed after the inverse kinematics. `angularGain` scales yaw rate before it. `flipVelocityScale` (clamped to `[0, 1]`) scales wheel speed for one frame when the equivalent steer solution flips sign. `simTime` is unused; it remains so existing Taku graph connections still resolve.

The node accepts only two profiles. An unknown `profile` raises `ValueError`. There is no separate profile YAML.

| `profile` | Steer joints | Drive (wheel) joints | Wheel `(x, y)` (m) | Stop and command behaviour |
|-----------|----------------|----------------------|--------------------|----------------------------|
| `linkhou_s2_v1` (OGN default) | `fl_steer_joint`, `rl_steer_joint`, `rr_steer_joint`, `fr_steer_joint` | `fl_wheel_joint`, `rl_wheel_joint`, `rr_wheel_joint`, `fr_wheel_joint` | `(0.23072, 0.21738)`, `(-0.22928, 0.21738)`, `(-0.23072, -0.21738)`, `(0.22928, -0.21738)` | When both linear speed and yaw rate are below `0.0001`, steer commands snap to zero and wheel speeds go to zero |
| `taku` | `agv_left_front_steering_joint`, `agv_left_back_steering_joint`, `agv_right_back_steering_joint`, `agv_right_front_steering_joint` | `agv_left_front_rotate_joint`, `agv_left_back_rotate_joint`, `agv_right_back_rotate_joint`, `agv_right_front_rotate_joint` | `(0.2745, 0.2045)`, `(-0.2745, 0.2045)`, `(-0.2745, -0.2045)`, `(0.2745, -0.2045)` | On stop, steer holds; steer slew is limited to 180°/s; wheel speed is scaled down until the steer error is small (full speed at 8°, zero at 35°). `msgCount` must keep changing: if it is unchanged for 0.25 s, the last twist is dropped. Linear deadband 0.02 m/s, yaw deadband 0.05 rad/s. Flip choice uses a 20° hysteresis. `deltaSeconds` is the playback frame dt (values `≤ 1e-6` or `> 0.1` fall back to `1/60`) |

### Graph wiring on current assets

Both example graphs tick from `OnPlaybackTick`, subscribe to a `geometry_msgs/Twist` with `ROS2SubscribeTwist`, break out linear `x`/`y` and angular `z`, and run `SwerveController`. Linear velocity is passed through `OgnIsaacScaleToFromStageUnit`.

- Linkhou S2: [`mobile_base/Linkhou/S2_V1/payloads/ROS/ros2.usda`](https://github.com/fiveages-sim/robot_usds/blob/main/mobile_base/Linkhou/S2_V1/payloads/ROS/ros2.usda), graph `ROS_Steering_Controller`, `profile` `linkhou_s2_v1`. `linearGain` is 14.28, `angularGain` is 1.04. The ArticulationRoot target is `</Linkhou_S2_V1>`. Joint name arrays come from the node outputs `Steer_Joints` and `Wheel_Joints`. The `ROS2SubscribeTwist` `topicName` attribute is present in that USDA but has no value; confirm the topic on the opened stage before you publish.
- Taku: [`humanoid/Dyna/Taku/components/Taku_Chassis/payloads/Graph/enable.usda`](https://github.com/fiveages-sim/robot_usds/blob/main/humanoid/Dyna/Taku/components/Taku_Chassis/payloads/Graph/enable.usda), graph `steering_wheel_controller`, `profile` `taku`. `topicName` is `/cmd_vel`. `linearGain` is 16, `flipVelocityScale` is 0.15, `angularGain` is 1. `deltaSeconds` comes from `OnPlaybackTick`, `msgCount` from a Counter on the subscriber `execOut`, and `simTime` from `IsaacReadSimulationTime` (the node does not use that last input). The ArticulationRoot target is `</Taku_Chassis/base_link>`. The two `IsaacArticulationController` nodes list the steer and drive joint names explicitly, in the same `fl`, `rl`, `rr`, `fr` order as the profile.

OGN defaults, if a graph leaves them unset, are `linearGain` 50, `angularGain` 1, and `flipVelocityScale` 0.35.

### Add a swerve chassis

A new chassis is not configured by pointing `profile` at a file. Add a profile in [`swerve.py`](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/exts/fasim.steering.nodes/fasim/steering/nodes/swerve.py): wheel `(x, y)`, steer and drive joint names, and the stop behaviour that chassis needs. List the token in the OGN `allowedTokens`. Copy a graph from Linkhou S2 or Taku: subscribe a twist, set `profile`, and connect steer positions and wheel velocities to two `IsaacArticulationController` nodes on the ArticulationRoot. Joint names on those controllers, or on the node outputs, must match the USD and the profile, in `fl`, `rl`, `rr`, `fr` order. Install operation 5 and restart Isaac so `SwerveController` is available.

### What you should see

After Play, a `geometry_msgs/Twist` on the graph’s subscribe topic moves the chassis. Steer joints follow `Steer_Position_Command`; wheel joints follow `Wheel_Velocity_Command`. On Linkhou S2, a zero command snaps the steer joints to zero. On Taku, the steer joints hold, and a stale command (no new `msgCount` for 0.25 s) stops the wheels. If the node type is missing, operation 5 was not installed or Isaac was not restarted.

(fasim-clock)=

## Clock

In-process W2 publishes `/clock` from a separate on-demand graph `ROS_Clock`: `evaluationMode=OnDemand`, `pipelineStage=pipelineStageOnDemand`, `OnPhysicsStep` → `PublishClock`, `IsaacReadSimulationTime` with `resetOnStop=1` ([`fiveages.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/fiveages.usda)). `OnPhysicsStep` does not run in the automatic `ROS_Control` graph, so the clock graph stays beside it. `ROS_Control` still uses `OnPlaybackTick` to start `ROS2ControlLaunch` once.

The topic-bridge payload on the same robot ([`ros2.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/ros2.usda)) still drives `PublishClock` from `OnPlaybackTick` and sets `resetOnStop=0`.

`/clock` is the controller’s time base when `use_sim_time` is true. A clock that ticks once per rendered frame jumps several physics steps, so a timed move finishes early. Use the physics-step clock. Changing joint gains does not fix that. New in-process payloads follow the same `ROS_Clock` pattern. This page checks it on W2. Odometry graphs keep their own `ReadSimTime` (`resetOnStop=1`) so `odom` stamps stay valid. Put cameras on the scene payload, not on this clock graph.

`arms_target_manager`, when the node spawns it, is a host process with `use_sim_time:=false` so markers are not tied to the physics step.

(fasim-tf)=

## TF

Isaac’s odometry graph publishes `world → odom → base_*` and `/odom`. It does not publish the whole URDF tree. `robot_state_publisher` publishes `base_footprint → base_link` (when both links exist) and the arm tree, including fixed frames such as `right_eef`.

On in-process W2 the ArticulationRoot is `base_link` (`/FiveAges_W2/base_link`). That payload’s odometry chain is `world → odom → base_footprint`, and `robot_state_publisher` publishes `base_footprint → base_link`. OCS2 `baseFrame` is the link named in that planner’s `task.info`. `base_footprint` sits on the ground. `base_link` can sit above it. Two publishers on one edge fight. A standing model with no `base_footprint` uses `base_link` for that chain. Read the link names in the robot’s USD and `task.info` before you copy the W2 names.

### Several robots

One ArticulationRoot, one `ROS2ControlLaunch`, and one controller manager per robot. Isolation is the graph `namespace` plus relative topic names (`cmd_vel`, `fsm_command`, `robot_description`). `/clock` stays global.

A ROS namespace remaps topics (`/<ns>/tf`, `/<ns>/tf_static`). It does not prefix `frame_id`. Each tree still has frames named `world`, `odom`, and `base_link`. `world → odom` is that robot’s latched spawn pose on **its** `/<ns>/tf`, not a rewritten frame called `g1d/world`. RViz listens to `/tf` unless you remap it, for example:

:::{code-block} bash
ros2 run tf2_ros tf2_echo world base_link --ros-args \
  -r /tf:=/<ns>/tf -r /tf_static:=/<ns>/tf_static
:::

`<ns>` is the string on that graph’s `namespace` input, not a `demo.launch.py` argument. A stage with one graph and one controller manager per robot has been run.

(fasim-navigation)=

## Navigation

`NavigationLaunch` ([`OgnNavigationLaunch.ogn`](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/exts/fasim.ros2.nodes/fasim/ros2/nodes/ogn/python/nodes/OgnNavigationLaunch.ogn)) starts `ros2 launch robot_common_launch navigation_isaac_gt.launch.py` on Play when `enabled` is true. W2’s fiveages graph leaves `enabled` false.

`map` and `paramsFile` are paths relative to the opened stage root, so an `env/` layer can point at `../../maps/<name>/map.yaml` stored in the same [fa-project-usd](https://github.com/fiveages-sim/fa-project-usd) project. The node does not call composer `ros2-stack`. Default `nav2Profile` is `map_only`. `publishMapWorldTf` defaults true (map drawn in USD world). `publishMapOdomTf` defaults false because odometry comes from Isaac.

Where those map files and `robot.yaml` currently live: [Environment assets](5-env_assets.md#fa-project-usd).

(fasim-layout)=

## Layout

:::{code-block} none
FaSim-Isaac/
├── init.sh
├── run.sh
├── run_headless.sh
├── config/                         # fa_sim.conf + optional fa_sim.local.conf
├── exts/fasim.ros2.nodes/          # ROS2ControlLaunch, NavigationLaunch
├── exts/fasim.steering.nodes/      # SwerveController
├── tools/audit_mimic_joint_drives.py
├── robots/                         # → robot_usds
└── environment/
    ├── fiveages_env/
    ├── fa-project-usd/             # private
    ├── artvip-usd/
    └── labutopia-usd/              # private
:::

Submodule URLs: [`.gitmodules`](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/.gitmodules). Visibility: `submodules_visibility.conf`. Robot tree: [robot_usds](3-robot_usds.md). Scene trees: [Environment assets](5-env_assets.md).

## Mimic joints

`tools/audit_mimic_joint_drives.py` reports mimic joints that have no drive. Assets that already use `PhysxMimicJointAPI` or `NewtonMimicAPI` should not gain a second drive: the solver already enforces the mimic, and a drive at `targetPosition=0` fights it. `--apply` is for a mimic that has neither PhysX nor Newton mimic API.

## Related

- [Isaac Sim how-to](../../2-how_to/2-simulation/4-isaac_sim.md)
- [robot_usds](3-robot_usds.md)
- [Environment assets](5-env_assets.md)
- [topic_based_ros2_control](../hardware/1-topic_based.md)
- [robot_common_launch](../descriptions/2-common.md)
- [lerobot_ros2](../python_apps/4-lerobot_ros2.md)
