# Isaac Sim

Run robot demos with NVIDIA Isaac Sim for high-fidelity simulation.

Use **FaSim-Isaac** `./init.sh` and `./run.sh`. Path and version live in that repo’s config; CLI flags are those named in its README.

## Prerequisites

- NVIDIA Isaac Sim binary installed (GPU + matching NVIDIA drivers)
- ROS 2 Jazzy workspace
- Default Isaac directory: `ISAACSIM_DIR` (`~/isaacsim` unless you override it)

## Steps

### 1. Clone FaSim-Isaac

:::{code-block} bash
cd ~/
git clone git@github.com:fiveages-sim/FaSim-Isaac.git
cd FaSim-Isaac
:::

### 2. Initialize

:::{code-block} bash
./init.sh
:::

What the script does (FaSim README):

1. **Operation 1** — initialize submodules listed in `.gitmodules` / `submodules_visibility.conf` (`public` selected by default; `private` needs access). Re-runs are additive.
2. **Operation 2** — optional **Isaac ROS 2 Jazzy workspace**: version menu queries GitHub stable tags (fallback list in `config/fa_sim.conf` currently `6.0.1` / `6.0.0` / `5.1.0`). Override with `ISAAC_SIM_VERSION=… ./init.sh`.

### 3. Start Isaac Sim

:::{code-block} bash
./run.sh
:::

What the script does: optional CPU governor, optional Zenoh router if `RMW_IMPLEMENTATION=rmw_zenoh_cpp`, then an interactive menu — **PhysX** / **Newton** / **Headless Streaming**. There is no `./run.sh --robot` or `./run.sh --headless`.

Path/version overrides: copy `config/fa_sim.local.template.conf` → `config/fa_sim.local.conf` and set `ISAACSIM_DIR` / `ISAAC_SIM_DEFAULT_VERSION`. Env also works: `ISAACSIM_DIR=/path ./run.sh`.

### 4. Launch ROS 2 Side

In a new terminal:

:::{code-block} bash
source ~/open-deploy-ws/install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=isaac
:::

Pass `robot:=…` on this ROS 2 launch as usual. Robot USD selection is done by opening the asset under FaSim `robots/` (robot_usds) in Isaac — not a FaSim `run.sh` flag.

### 5. Verify Connection

:::{code-block} bash
ros2 topic list
:::

Acone `hardware:=isaac` uses `topic_based_ros2_control/TopicBasedSystem` with `/isaac/joint_command` and `/isaac/joint_states` ([xacro](https://github.com/fiveages-sim/robot-descriptions-arx/blob/main/arx_acone_description/xacro/ros2_control/robot.xacro)). Do not expect a stack-wide `/target_pose`.

## USD Assets

FaSim-Isaac uses USD (Universal Scene Description) assets from `robot_usds`:

| Path | Content |
|------|---------|
| `humanoid/FiveAges/Gen1` | Gen1 wheeled-arm USD |
| `humanoid/FiveAges/Gen2` | Gen2 wheeled-arm USD |
| `humanoid/FiveAges/Gen3` | Gen3 wheeled-arm USD |
| `humanoid/Galbot` | Galbot mobile manipulator |
| `humanoid/Ubtech` | Ubtech humanoid |

See [robot_usds reference](../../4-reference/simulation/3-robot_usds.md) for details.

## Environment Assets

Scene environments are loaded from:
- `fiveages-env-usds` — Public environment assets
- `fa-project-usd` — Internal project-specific scenes (private)

Open the scene USD in Isaac. There is no `./run.sh --env`.

## Hardware Interface

The `hardware:=isaac` parameter uses the topic-based hardware interface that bridges Isaac Sim physics to ROS 2 control. Plugin `<param>` names (`joint_commands_topic`, `initialize_commands_from_state`, …): [topic_based_ros2_control](../../4-reference/hardware/1-topic_based.md).

## Verification

- Isaac Sim window (or Headless Streaming) is running from `./run.sh`
- ROS 2 topics from Isaac appear in `ros2 topic list`
- Robot responds to joint commands
- Sensor data (if configured) publishes to ROS 2

## Troubleshooting

### Isaac Sim fails to launch

1. Confirm `ISAACSIM_DIR` (default `~/isaacsim`) contains the launch scripts named in `config/fa_sim.conf` (`isaac-sim.sh`, `isaac-sim.newton.sh`, `isaac-sim.streaming.sh`)
2. Set `ISAACSIM_DIR` in `config/fa_sim.local.conf` if Isaac is not at `~/isaacsim`
3. Verify GPU drivers: `nvidia-smi`
4. Check Isaac Sim logs in `~/.nvidia-omniverse/logs/`

### No ROS 2 topics

1. Verify the ROS 2 bridge extension is enabled in Isaac Sim
2. Check domain ID matches between Isaac and ROS 2
3. Restart `./run.sh` and the ROS 2 launch

### USD asset not found

Re-run `./init.sh` operation 1 and select the needed submodules (including `robots`).

### Simulation runs slowly

- Reduce rendering quality in Isaac Sim settings
- Use `./run.sh` menu **Headless Streaming** for non-visual testing
- Check GPU memory usage

## Next Steps

- [robot_usds reference](../../4-reference/simulation/3-robot_usds.md)
- [FaSim-Isaac reference](../../4-reference/simulation/2-fasim_isaac.md)
- [Synthetic Data](../7-synthetic_data/0-index.md) — datagen pipeline on Isaac (not Gazebo)
