# Isaac Sim

Run robot demos with NVIDIA Isaac Sim for high-fidelity simulation.

```{admonition} Required Version and Path
:class: warning

FaSim-Isaac requires **Isaac Sim 6.1** installed at **`~/isaacsim`**. The run scripts assume this exact path. Other versions or paths will not work without modifying the scripts.
```

## Prerequisites

- **Isaac Sim 6.1 binary** installed at `~/isaacsim`
- NVIDIA GPU (RTX recommended)
- NVIDIA drivers compatible with Isaac Sim 6.1
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

This launches Isaac Sim with the configured scene. The script expects Isaac Sim 6.1 at `~/isaacsim`.

:::{admonition} Path Verification
:class: tip

Verify your installation path before running:

```bash
ls ~/isaacsim/python.sh
```

If this file doesn't exist, either install Isaac Sim 6.1 to `~/isaacsim` or create a symlink.
:::

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

1. **Verify installation path**: `ls ~/isaacsim/python.sh` — must exist
2. **Check version**: Ensure you have Isaac Sim 6.1 (not older versions)
3. Verify GPU drivers: `nvidia-smi`
4. Check Isaac Sim logs in `~/.nvidia-omniverse/logs/`

### Wrong Isaac Sim path

If Isaac Sim is installed elsewhere, create a symlink:
```bash
ln -s /path/to/your/isaacsim ~/isaacsim
```

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
