# FaSim-Isaac

FaSim-Isaac is the Isaac Sim workspace: robot and scene USD, an optional Isaac ROS 2 Jazzy overlay, and the extensions that start 运控 inside Sim.

Use this page when you need to see why a joint topic, a clock, or a TF edge behaves the way it does. To start Sim and pick a launch, follow [Isaac Sim](../../2-how_to/2-simulation/4-isaac_sim.md).

**Repository:** [fiveages-sim/FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac) `main` (`3606dc89`, 2026-11-13). In-process ros2_control is on `main` ([#7](https://github.com/fiveages-sim/FaSim-Isaac/pull/7), `1a4193a3`). Replicator capture (`exts/fasim.replicator.sdg`) is on `feature/ros2-control-node`, not on `main`.

**README:** [README.md](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/README.md)

## Two hardware interfaces

One stage uses one of these. `isaac` is the topic bridge you pass on a ROS 2 launch. `isaac_sim` is set inside Isaac when Play starts the in-process node. It is not a `demo.launch.py` flag, and it is not a second robot body.

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

## In-process launch

`OgnROS2ControlLaunch` ([`OgnROS2ControlLaunch.ogn`](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/exts/fasim.ros2.nodes/fasim/ros2/nodes/ogn/python/nodes/OgnROS2ControlLaunch.ogn)) runs once after Play:

| Input | Role |
|-------|------|
| `targetPrim` | One ArticulationRoot |
| `robot` | Description stem (`unitree_g1d`, `fiveages_w2`). Empty reads the USD `Robot` variant |
| `mode` | `demo`, `split_body`, or `full_body` |
| `type` | `robot_common_launch` end-effector key. Empty reads EE variants on the stage |
| `namespace` | Controller manager namespace. Empty is the global `/controller_manager` |
| `infoFile` | OCS2 `.info` basename. Empty keeps the description default |
| `useSimTime` | Forced true for `isaac_sim` (needs `/clock`) |
| `publishRobotDescription` | Latch the same xacro on `/robot_description` (default true) |

`emit_control` builds one xacro URDF and points both the controller manager and `/robot_description` at it. `Ros2ControlManager.setup` is called with `publish_robot_description=False`, so the manager does not publish that topic a second time. `robot_state_publisher` on the host publishes `/robot_description` and the URDF TF tree. If that process does not start, a latched `fasim_robot_description` publisher is the fallback. The resource manager therefore loads the description once.

Play does not rebuild a URDF from the stage on every start. The node reuses the description xacro, and it falls back to synthesizing a URDF from the USD only for an unexpected prim.

### CppAD cache

`ocs2_arm_controller` declares `recompile_libraries` with default true when `task.info` does not set `recompileLibraries` ([`CtrlComponent.h`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/include/ocs2_arm_controller/control/CtrlComponent.h)). The library folder is `${OCS2_PLANNING_URDF_DIR:-/tmp}/ocs2_ros2/<robot>/ocs2/<content-hash>`.

On the in-process path, `emit_control` then sets `recompile_libraries: false` on the main controller only: `ocs2_arm_controller` for `demo` and `split_body`, `ocs2_wbc_controller` for `full_body`. A topic-bridge launch (`hardware:=isaac`) does not run `emit_control`, so it keeps the controller default. That default stays true unless that robot’s info file or YAML already says false.

A simulated robot that runs 运控 inside Isaac starts faster for two reasons: the node reuses the description xacro, and it reuses this CppAD cache.

### `infoFile` and `BASE_LOCK`

`infoFile` overrides `info_file_name` on the main controller. `fixed_base_tcp` drops the virtual chassis degrees of freedom (`manipulatorModelType` 0), so whole-body planning covers the body and the arms.

`emit_control` warns when `mode` is `full_body` and the override name contains `fixed_base`. The planner then has `basePlan=0`, so a runtime `BASE_LOCK` has nothing to constrain, and arm enable can stay in `WAITING_FOR_ENABLE_POLICY`. Lock the base with `mobile_base_tcp` and `BASE_LOCK`.

`full_body` loads `ocs2_wbc_controller` from the GitHub Release package `ros-jazzy-arms-ros2-control` (`./init_repo.sh` with arms set to `d`, or `./scripts/install_core_debs.sh --only arms`). The same package contains `ocs2_humanoid` and `lina_planning`. It is not an apt package, and it is not `ros-jazzy-arms-ros2-control-full`. Open [ocs2-wbc-controller](https://github.com/fiveages-sim/ocs2-wbc-controller) when you need to read or change the source.

## Clock

In-process W2 publishes `/clock` from a separate on-demand graph `ROS_Clock`: `evaluationMode=OnDemand`, `pipelineStage=pipelineStageOnDemand`, `OnPhysicsStep` → `PublishClock`, `IsaacReadSimulationTime` with `resetOnStop=1` ([`fiveages.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/fiveages.usda)). `OnPhysicsStep` does not run in the automatic `ROS_Control` graph, so the clock graph stays beside it. `ROS_Control` still uses `OnPlaybackTick` to start `ROS2ControlLaunch` once.

The topic-bridge payload on the same robot ([`ros2.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/ros2.usda)) still drives `PublishClock` from `OnPlaybackTick` and sets `resetOnStop=0`.

`/clock` is the controller’s time base when `use_sim_time` is true. A clock that ticks once per rendered frame jumps several physics steps, so a timed move finishes early. Use the physics-step clock. Changing joint gains does not fix that. New in-process payloads follow the same `ROS_Clock` pattern. This page checks it on W2. Odometry graphs keep their own `ReadSimTime` (`resetOnStop=1`) so `odom` stamps stay valid. Put cameras on the scene payload, not on this clock graph.

`arms_target_manager`, when the node spawns it, is a host process with `use_sim_time:=false` so markers are not tied to the physics step.

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

## Navigation

`NavigationLaunch` ([`OgnNavigationLaunch.ogn`](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/exts/fasim.ros2.nodes/fasim/ros2/nodes/ogn/python/nodes/OgnNavigationLaunch.ogn)) starts `ros2 launch robot_common_launch navigation_isaac_gt.launch.py` on Play when `enabled` is true. W2’s fiveages graph leaves `enabled` false.

`map` and `paramsFile` are paths relative to the opened stage root, so an `env/` layer can point at `../../maps/<name>/map.yaml` stored in the same [fa-project-usd](https://github.com/fiveages-sim/fa-project-usd) project. The node does not call composer `ros2-stack`. Default `nav2Profile` is `map_only`. `publishMapWorldTf` defaults true (map drawn in USD world). `publishMapOdomTf` defaults false because odometry comes from Isaac.

## Project scenes

[fa-project-usd](https://github.com/fiveages-sim/fa-project-usd) is a private repository. On `main`, a project is `scene.usd(a)`, `objects/`, and a runnable `env/` ([README](https://github.com/fiveages-sim/fa-project-usd/blob/main/README.md)).

The files the orchestrator reads next to those scenes (`robot.yaml`, `task_configs/`, and `maps/` or `map/`) are on branch `feature/sinopec-test-tube-picking`. That branch was ahead of `main` and not merged when these pages were checked on 2026-11-13. Three projects there use this layout: `Fiveages/2026-11 Standard Moving Boxes`, `Siemens/2026-06 Wind Turbine Blade Detection`, and `Aimbo/2026-04 Bosch German&Poland POC`. You need access to open the branch. The public way to run a project directory is [lerobot_ros2 `examples/IsaacSim/README.md`](https://github.com/fiveages-sim/lerobot_ros2/blob/main/examples/IsaacSim/README.md): `motion-generation` with `LEROBOT_ROOT` set. Keep camera rigs in the scene USD.

## Layout

:::{code-block} none
FaSim-Isaac/
├── init.sh
├── run.sh
├── run_headless.sh
├── config/                         # fa_sim.conf + optional fa_sim.local.conf
├── exts/fasim.ros2.nodes/          # ROS2ControlLaunch, NavigationLaunch
├── exts/fasim.steering.nodes/      # swerve graph node
├── tools/audit_mimic_joint_drives.py
├── robots/                         # → robot_usds
└── environment/
    ├── fiveages_env/
    ├── fa-project-usd/             # private
    ├── artvip-usd/
    └── labutopia-usd/
:::

Submodule URLs: [`.gitmodules`](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/.gitmodules). Visibility: `submodules_visibility.conf`.

## Mimic joints

`tools/audit_mimic_joint_drives.py` reports mimic joints that have no drive. Assets that already use `PhysxMimicJointAPI` or `NewtonMimicAPI` should not gain a second drive: the solver already enforces the mimic, and a drive at `targetPosition=0` fights it. `--apply` is for a mimic that has neither PhysX nor Newton mimic API.

## Related

- [Isaac Sim how-to](../../2-how_to/2-simulation/4-isaac_sim.md)
- [topic_based_ros2_control](../hardware/1-topic_based.md)
- [robot_common_launch](../descriptions/2-common.md)
- [lerobot_ros2](../python_apps/4-lerobot_ros2.md)
- [Environment assets](5-env_assets.md)
