# FaSim-Isaac

NVIDIA Isaac Sim workspace for FiveAges Sim: robot and scene USD, an optional Isaac ROS 2 Jazzy overlay, and the extensions that start 运控 inside Sim.

**Repository:** [fiveages-sim/FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac) `main` (`3606dc89`, 2026-11-13). In-process ros2_control landed on `main` in [#7](https://github.com/fiveages-sim/FaSim-Isaac/pull/7) (`1a4193a3`). `feature/ros2-control-node` has since diverged (Replicator capture under `exts/fasim.replicator.sdg` is on that branch, not on `main`).

**README:** [README.md](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/README.md)

How to start Sim and which launch to use: [Isaac Sim](../../2-how_to/2-simulation/4-isaac_sim.md).

## Two hardware interfaces

| Key | Where it is set | Plugin | Joint I/O |
|-----|-----------------|--------|-----------|
| `isaac` | `ros2 launch … hardware:=isaac` | `topic_based_ros2_control/TopicBasedSystem` | `sensor_msgs/JointState` topics |
| `isaac_sim` | `emit_control` inside `ROS2ControlLaunch` (not a `demo.launch.py` flag) | `isaacsim_ros2_control/IsaacSimSystem` | In-process articulation |

Shared xacro: [`simulation_hardware.xacro`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/xacro/ros2_control/simulation_hardware.xacro). `hardware:=isaac` writes `/isaac/joint_command` and `/isaac/joint_states`. `hardware:=isaac_sim` writes `<param name="prim_path">` from launch `isaac_prim_path` (ArticulationRoot). [`robot_common_launch` README](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/README.md) lists both keys. `use_sim_time` is true for `gz`, `isaac`, and `isaac_sim` unless the launch argument is explicitly `true` or `false` ([`launch_arg_utils.py`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/robot_common_launch/common/launch_arg_utils.py)).

A robot xacro that whitelists `validated_hardware_type` must include `isaac_sim` or that xacro fails on purpose.

`{hardware}.yaml` overlays merge only when the file exists. `load_robot_config` order is common → type yaml → `{variant}.yaml` → end-effector compose → `{hardware}.yaml` → `control.patch` ([`robot_utils.py`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/robot_common_launch/common/robot_utils.py)). Hardware overlay runs after compose so a later compose pass does not drop gripper keys from `isaac.yaml` ([robot-descriptions-common #41](https://github.com/fiveages-sim/robot-descriptions-common/pull/41)). `isaac_sim` can reuse `isaac.yaml`; emit passes `hardware_yaml=isaac`. A file named `isaac_sim.yaml` is loaded when the launch hardware string is `isaac_sim`.

### Topic names are per robot

The shared macro’s `/isaac/joint_*` pair is the topic-bridge default (Acone uses that macro). W2’s topic-bridge graph publishes `/joint_command` and `/joint_states` ([`ros2.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/ros2.usda)). The xacro `<param>` and the graph `topicName` are the same strings. `demo.launch.py` does not take a namespace that rewrites them.

In-process W2 ([`fiveages.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/fiveages.usda)) does not bridge body or arm `JointState` topics. The controller manager owns those degrees of freedom. Chassis `cmd_vel` / `odom` stay on the child ROS graph.

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

`emit_control` builds one xacro URDF and pins both the controller manager and `/robot_description` to it. `Ros2ControlManager.setup` is called with `publish_robot_description=False`, so the manager does not publish that topic again. `robot_state_publisher` (host process) publishes `/robot_description` and the URDF TF tree. If that process does not start, a latched `fasim_robot_description` publisher is the fallback. Resource Manager therefore loads the description once.

That xacro path is also why Play does not synthesize a fresh URDF from the stage on every start: the node reuses the description xacro and only falls back to USD synthesis for an unexpected prim.

### CppAD cache

`ocs2_arm_controller` declares `recompile_libraries` with default **true** when `task.info` does not set `recompileLibraries` ([`CtrlComponent.h`](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/include/ocs2_arm_controller/control/CtrlComponent.h)). The library folder is `${OCS2_PLANNING_URDF_DIR:-/tmp}/ocs2_ros2/<robot>/ocs2/<content-hash>`.

`emit_control` then sets `recompile_libraries: false` on the **main** controller only: `ocs2_arm_controller` for `demo` / `split_body`, `ocs2_wbc_controller` for `full_body`. That force applies to the in-process `isaac_sim` path. A topic-bridge `hardware:=isaac` launch does not run `emit_control`, so it keeps the controller default (true unless that robot’s info or YAML already says false).

Reusing the xacro URDF and reusing the CppAD cache are the two startup shortcuts for a simulated robot that runs 运控 inside Isaac.

### `infoFile` and `BASE_LOCK`

`infoFile` overrides `info_file_name` on the main controller. `fixed_base_tcp` drops the virtual chassis degrees of freedom (`manipulatorModelType` 0) so whole-body planning is body and arms.

`emit_control` warns when `mode` is `full_body` and the override name contains `fixed_base`: the planner has `basePlan=0`, so a runtime `BASE_LOCK` has nothing to constrain, and the arm enable policy can stay in `WAITING_FOR_ENABLE_POLICY`. Locking the base uses `mobile_base_tcp` plus `BASE_LOCK`.

Whole-body control needs [ocs2-wbc-controller](https://github.com/fiveages-sim/ocs2-wbc-controller) (private; open it after access).

## Clock

In-process W2 publishes `/clock` from a separate on-demand graph `ROS_Clock`: `evaluationMode=OnDemand`, `pipelineStage=pipelineStageOnDemand`, `OnPhysicsStep` → `PublishClock`, `IsaacReadSimulationTime` with `resetOnStop=1` ([`fiveages.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/fiveages.usda)). `OnPhysicsStep` does not run in the automatic `ROS_Control` graph, so the clock graph stays beside it. `ROS_Control` still uses `OnPlaybackTick` to start `ROS2ControlLaunch` once.

The topic-bridge payload on the same robot ([`ros2.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/ros2.usda)) still drives `PublishClock` from `OnPlaybackTick` and sets `resetOnStop=0`.

`/clock` is the controller’s time base when `use_sim_time` is true. A render-frame clock advances several physics steps in one tick, so a timed move finishes early. The repair is the physics-step clock, not a joint-parameter change. The same `ROS_Clock` pattern is what new fiveages in-process payloads follow; this page verifies it on W2. Odometry graphs keep their own `ReadSimTime` (`resetOnStop=1`) so `odom` stamps stay valid. Camera prims belong on the scene payload, not on this clock graph.

`arms_target_manager`, when the node spawns it, is a host process with `use_sim_time:=false` so markers are not tied to the physics step.

## TF

Isaac’s odometry graph publishes `world → odom → base_*` and `/odom`. It does not publish the whole URDF tree. `robot_state_publisher` publishes `base_footprint → base_link` (when both links exist) and the arm tree, including fixed frames such as `right_eef`.

W2’s in-process ArticulationRoot is `base_link` (`/FiveAges_W2/base_link`). The odometry chain on that payload is `world → odom → base_footprint`; `robot_state_publisher` publishes `base_footprint → base_link`. OCS2 `baseFrame` is the same link the planner’s `task.info` names. `base_footprint` is the ground link; `base_link` may sit above it. Two publishers on one edge fight. A standing model with no `base_footprint` uses `base_link` for that chain. Confirm the link in that robot’s USD and `task.info` before copying the W2 names.

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

[fa-project-usd](https://github.com/fiveages-sim/fa-project-usd) is private. On `main`, a project is `scene.usd(a)`, `objects/`, and runnable `env/` ([README](https://github.com/fiveages-sim/fa-project-usd/blob/main/README.md)).

Orchestration files next to those scenes (`robot.yaml`, `task_configs/`, `maps/` or `map/`) are on branch `feature/sinopec-test-tube-picking`, which is ahead of `main` and not merged (compared 2026-11-13). Three projects on that branch have this layout: `Fiveages/2026-11 Standard Moving Boxes`, `Siemens/2026-06 Wind Turbine Blade Detection`, and `Aimbo/2026-04 Bosch German&Poland POC`. Open the branch after you have access. The public entry for running a project directory is [lerobot_ros2 `examples/IsaacSim/README.md`](https://github.com/fiveages-sim/lerobot_ros2/blob/main/examples/IsaacSim/README.md) (`motion-generation` with `LEROBOT_ROOT` set). Camera rigs stay in the scene USD.

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
