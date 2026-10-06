# Isaac Sim

Run robot demos with NVIDIA Isaac Sim for high-fidelity simulation.

## Prerequisites

- NVIDIA GPU (RTX recommended)
- NVIDIA Omniverse Launcher installed
- Isaac Sim installed via Omniverse
- ROS 2 Jazzy workspace

## Steps

### 1. Clone FaSim-Isaac

```bash
cd ~/
git clone https://github.com/fiveages-sim/FaSim-Isaac.git
cd FaSim-Isaac
```

### 2. Initialize

```bash
./init.sh
```

This initializes:
- `robot_usds` submodule (USD robot assets)
- Environment assets
- Configuration files

### 3. Start Isaac Sim

```bash
./run.sh
```

This launches Isaac Sim with the configured scene.

### 4. Launch ROS 2 Side

In a new terminal:

```bash
source /opt/ros/jazzy/setup.bash
source ~/open-deploy-ws/install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py hardware:=isaac
```

### 5. Verify Connection

Check topics are bridged:

```bash
ros2 topic list
# Should see /joint_states, /target_pose, etc.
```

## USD Assets

FaSim-Isaac uses USD (Universal Scene Description) assets from `robot_usds`:

| Path | Content |
|------|---------|
| `humanoid/FiveAges/Gen1` | Gen1 humanoid USD |
| `humanoid/FiveAges/Gen2` | Gen2 humanoid USD |
| `humanoid/FiveAges/Gen3` | Gen3 humanoid USD |
| `humanoid/Galbot` | Galbot mobile manipulator |
| `humanoid/Ubtech` | Ubtech humanoid |

See [robot_usds reference](../4-reference/simulation/3-robot_usds.md) for details.

## Environment Assets

Scene environments are loaded from:
- `fiveages-env-usds` — Public environment assets
- `fa-project-usd` — Internal project-specific scenes (private)

## Hardware Interface

The `hardware:=isaac` parameter uses the topic-based hardware interface that bridges Isaac Sim physics to ROS 2 control.

## Switching Robots

```bash
# Edit FaSim-Isaac config or use command line
./run.sh --robot galbot

# Corresponding ROS 2 launch
ros2 launch ocs2_arm_controller demo.launch.py robot:=galbot hardware:=isaac
```

## Headless Mode

For training or CI:

```bash
./run.sh --headless
```

## Verification

- Isaac Sim window shows robot in scene
- ROS 2 topics from Isaac appear in `ros2 topic list`
- Robot responds to joint commands
- Sensor data (if configured) publishes to ROS 2

## Troubleshooting

### Isaac Sim fails to launch

1. Check Omniverse Launcher for updates
2. Verify GPU drivers: `nvidia-smi`
3. Check Isaac Sim logs in `~/.nvidia-omniverse/logs/`

### No ROS 2 topics

1. Verify the ROS 2 bridge extension is enabled in Isaac Sim
2. Check domain ID matches between Isaac and ROS 2
3. Restart Isaac Sim and the bridge

### USD asset not found

```bash
cd FaSim-Isaac
git submodule update --init --recursive
```

### Simulation runs slowly

- Reduce rendering quality in Isaac Sim settings
- Use headless mode for non-visual testing
- Check GPU memory usage

## Next Steps

- [robot_usds reference](../4-reference/simulation/3-robot_usds.md)
- [FaSim-Isaac reference](../4-reference/simulation/2-fasim_isaac.md)
