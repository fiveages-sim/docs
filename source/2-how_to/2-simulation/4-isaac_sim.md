# Isaac Sim

Open a robot in NVIDIA Isaac Sim and drive it with the same ROS 2 stack you use on the real machine.

FaSim-Isaac holds the assets and installs the OmniGraph extensions. Run `./init.sh`, then `./run.sh` or `./run_headless.sh`. You choose the robot by opening its USD. There is no `./run.sh --robot`. The Isaac path and version are in `config/fa_sim.conf`, with a machine override in `config/fa_sim.local.conf`.

Connect ROS 2 in one of two ways. Use one of them for a given stage. These are description hardware keys, not the FaSim Kit extensions.

| What you start | Plugin | What moves the joints |
|----------------|--------|------------------------|
| `hardware:=isaac` | `topic_based_ros2_control/TopicBasedSystem` | OmniGraph joint topics |
| Play on an in-process `ROS2ControlLaunch` | `isaacsim_ros2_control/IsaacSimSystem` (`hardware=isaac_sim` inside the node) | The controller manager inside the Isaac process |

`isaac_sim` is the hardware interface for that in-process controller. It is not a second robot. A swerve chassis uses a different node, `SwerveController`, which is not a hardware key. Mechanism, parameters, and clock/TF: [FaSim-Isaac reference](../../4-reference/simulation/2-fasim_isaac.md).

## Before you start

- Isaac Sim is installed, the GPU driver matches it, and `ISAACSIM_DIR` points at that install (`~/isaacsim` unless you set another path).
- A ROS 2 Jazzy workspace already builds this robot: `open-deploy-ws`, or [fa-deploy-ws](https://github.com/fiveages-sim/fa-deploy-ws) once you can open that repository.
- The topic bridge needs `topic_based_ros2_control` in that workspace. The in-process graph and a swerve graph both need `./init.sh` operation 5 (the FaSim extensions) and a restart of Isaac. The in-process path also needs a description xacro that accepts `hardware` `isaac_sim`.

(start-fasim)=

## Start FaSim

:::{code-block} bash
git clone git@github.com:fiveages-sim/FaSim-Isaac.git
cd FaSim-Isaac
./init.sh
./run.sh
:::

`./init.sh` asks you to ([README](https://github.com/fiveages-sim/FaSim-Isaac/blob/main/README.md)):

1. Check out the submodules you select (`.gitmodules` and `submodules_visibility.conf`). Public entries start checked. Private entries, including [fa-project-usd](https://github.com/fiveages-sim/fa-project-usd) and [labutopia-usd](https://github.com/fiveages-sim/labutopia-usd), stay unchecked until you can open them. A later run only adds what you check. Current public versus private rows: [robot_usds](../../4-reference/simulation/3-robot_usds.md) and [Environment assets](../../4-reference/simulation/5-env_assets.md).
2. Update submodules you already checked out (`./init.sh --update`). This does not pull the FaSim repository itself.
3. Download ArtVIP into `environment/ArtVIP/` (`tools/artvip_kitchen.py`).
4. Optionally add an Isaac ROS 2 Jazzy overlay under `isaac_jazzy_ws/`. The menu asks GitHub for stable tags. If that query fails, `config/fa_sim.conf` falls back to `6.2.0`, `6.1.0`, and `6.0.1`. Override with `ISAAC_SIM_VERSION=… ./init.sh`.
5. Install the FaSim extensions into this Isaac (`exts/fasim.steering.nodes`, `exts/fasim.ros2.nodes`) and quiet the script warnings. Run this again after you reinstall Isaac, then restart Isaac so the extensions load. What each extension does: [FaSim Kit extensions](../../4-reference/simulation/2-fasim_isaac.md#fasim-kit-extensions).

`./run.sh` shows the saved backend, then asks PhysX or Newton, CPU governor, and which ROS 2 workspace to source. `./run_headless.sh` is the same menu for Headless Streaming. Non-interactive examples from the README:

:::{code-block} bash
./run.sh -y --physics physx --cpu auto --ros-ws ~/ros2_ws
./run_headless.sh -y --physics physx --instance 0
./run.sh --asset-region china
./run.sh --kit-profile none
:::

`config/fa_sim.conf` kit profiles (`--kit-profile` / `--list-kit-profiles`): `none`, `newton-physx-min`, `newton-physx`, `physx-compat`, `physx-compat-full`. `--asset-region` is `none`, `us`, or `china`. Copy `config/fa_sim.local.template.conf` to `config/fa_sim.local.conf` for a machine override. When `RMW_IMPLEMENTATION=rmw_zenoh_cpp`, `./run.sh` starts a Zenoh router and stops it on exit.

Open the robot USD under `robots/` (robot_usds) or a scene under `environment/`. Operation 5 must already be done before a stage that uses `ROS2ControlLaunch` or `SwerveController`.

(topic-bridge)=

## Topic bridge (`hardware:=isaac`)

In another terminal, after the workspace overlay:

:::{code-block} bash
source ~/open-deploy-ws/install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone hardware:=isaac
:::

`robot:=` is the description key (`<key>_description`). `demo.launch.py` has no namespace argument. Do not append `namespace:=…` on this launch.

The shared macro [`simulation_hardware.xacro`](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/xacro/ros2_control/simulation_hardware.xacro) sets:

- `joint_commands_topic` = `/isaac/joint_command`
- `joint_states_topic` = `/isaac/joint_states`

Those strings have to match the OmniGraph `topicName` on this robot. W2’s topic-bridge payload [`W2/payloads/ROS/ros2.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/ros2.usda) publishes `/joint_command` and `/joint_states` instead. If the two sides differ, change the xacro `<param>` or the graph until `ros2 topic echo` shows the same `sensor_msgs/JointState` names the controller is using. Plugin parameters: [topic_based_ros2_control](../../4-reference/hardware/1-topic_based.md).

`use_sim_time` follows `hardware` (`isaac` → true) unless you pass `use_sim_time:=true` or `false`.

Check:

:::{code-block} bash
ros2 topic echo /isaac/joint_states --once
# or the topicName this USD actually publishes
:::

A joint command on the matching command topic moves the articulation. There is no stack-wide `/target_pose`.

## In-process hardware interface (`isaac_sim`)

Use this when the USD contains `fasim.ros2.nodes.ROS2ControlLaunch`. W2’s in-process payload is [`W2/payloads/ROS/fiveages.usda`](https://github.com/fiveages-sim/fiveages-gen2-robot-usds/blob/main/W2/payloads/ROS/fiveages.usda). Press Play. The node calls `emit_control`, which sets `hardware=isaac_sim`, passes the ArticulationRoot as `isaac_prim_path`, and starts the controller manager inside Isaac.

The description package still has to exist. Its ros2_control xacro includes `simulation_hardware_plugin` for `isaac_sim` ([robot_common_launch README](https://github.com/fiveages-sim/robot-descriptions-common/blob/main/robot_common_launch/README.md)). Graph inputs, CppAD cache, and `infoFile`: [ROS 2 Control extension](../../4-reference/simulation/2-fasim_isaac.md#ros-2-control-extension). An empty `robot` reads the USD `Robot` variant. That string is the description package stem.

After Play, check:

:::{code-block} bash
ros2 control list_controllers
ros2 topic echo /joint_states --once
ros2 topic hz /clock
:::

`/joint_states` here is the controller’s `joint_state_broadcaster`, not the topic-bridge pair. `/clock` should tick near the physics rate. Arm degrees of freedom are not also bridged on `/isaac/joint_command`.

`namespace` on the graph (empty for one robot) is how a second articulation gets `/<ns>/controller_manager`. It is not a `demo.launch.py` argument. Frame ids stay `world`, `odom`, and `base_link` / `base_footprint`. See [TF](../../4-reference/simulation/2-fasim_isaac.md#tf).

Whole-body mode (`mode` `full_body`) loads `ocs2_wbc_controller`. That package is already in the GitHub Release deb `ros-jazzy-arms-ros2-control`. Choose `d` for arms in `./init_repo.sh`, or run `./scripts/install_core_debs.sh --only arms`. Cloning [ocs2-wbc-controller](https://github.com/fiveages-sim/ocs2-wbc-controller) is how you read or edit the source. To hold a mobile base, keep the description’s `mobile_base_tcp` info and send `BASE_LOCK`. A `full_body` graph whose `infoFile` points at a `fixed_base` info file has no virtual chassis joint for that lock, and arm enable can stay in `WAITING_FOR_ENABLE_POLICY`.

If the opened USD uses `SwerveController` (Linkhou S2 or Taku chassis graphs), that is the [swerve extension](../../4-reference/simulation/2-fasim_isaac.md#swerve-extension), not this hardware key. After Play, publish a `geometry_msgs/Twist` on the graph’s subscribe topic and check that steer joints move in position and wheel joints in velocity.

## What to open

| Tree | Content |
|------|---------|
| `robots/` → [robot_usds](https://github.com/fiveages-sim/robot_usds) | Robot USD. Folder map: [robot_usds](../../4-reference/simulation/3-robot_usds.md) |
| `environment/fiveages_env/` | Public scenes |
| `environment/fa-project-usd/` → [fa-project-usd](https://github.com/fiveages-sim/fa-project-usd) | Project scenes (private; needs access) |
| `environment/artvip-usd/` | ArtVIP components |

Scene trees and project layout: [Environment assets](../../4-reference/simulation/5-env_assets.md).

(when-it-fails)=

## When it fails

**Isaac does not start.** `ISAACSIM_DIR` must contain the launchers named in `config/fa_sim.conf` (`isaac-sim.sh`, `isaac-sim.newton.sh`, `isaac-sim.streaming.sh`, `isaac-sim.newton.streaming.sh`). `nvidia-smi` shows a GPU. Logs: `~/.nvidia-omniverse/logs/`.

**Play starts, but no ROS 2 topics appear.** The domain id and `RMW_IMPLEMENTATION` match the workspace you sourced. For the topic bridge, the graph `topicName` matches the xacro. For the in-process graph, operation 5 is installed and Isaac was restarted, and the stage’s `ROS` variant is the fiveages payload rather than the topic-bridge payload. For a swerve graph, the `SwerveController` node type must be available (same operation 5 and restart).

**A motion finishes much too fast.** On the in-process payload, `/clock` comes from the on-demand `ROS_Clock` graph (`OnPhysicsStep`). That is how W2 `fiveages.usda` is already wired. The topic-bridge `ros2.usda` still publishes the clock from `OnPlaybackTick`. Fix the clock before you edit joint gains. The mechanism is on the [FaSim-Isaac Clock](../../4-reference/simulation/2-fasim_isaac.md#clock) section.

## Next

- [FaSim-Isaac reference](../../4-reference/simulation/2-fasim_isaac.md)
- [Add a Robot](../6-deployment/10-add_a_robot.md) and the [Day 7 exam](../../0-overview/2-learning_path.md#day-7-bring-one-new-robot-into-fasim)
- [Synthetic Data](../7-synthetic_data/0-index.md)
