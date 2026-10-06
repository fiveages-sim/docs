# ros2-viser

ROS 2 3D visualization library built on Viser. **Launch it from fa-py-libraries**, not as a standalone product entry and not from lerobot_ros2.

**Repository:** [fiveages-sim/ros2-viser](https://github.com/fiveages-sim/ros2-viser)

**README:** [README.md](https://github.com/fiveages-sim/ros2-viser/blob/main/README.md)

## Purpose

- Subscribe robot URDF from `/robot_description`
- Show joint state in a Viser 3D view
- Optional FSM and gripper panels
- All ROS 2 I/O goes through **`ros2_robot_interface`** (the visualizer creates an internal `ROS2RobotInterface`)

## Primary launch (fa-py-libraries)

This is the supported operator path:

```bash
git clone https://github.com/fiveages-sim/fa-py-libraries.git
cd fa-py-libraries
./init.sh all          # Python 3.12 env; installs ros2-viser among other submodules
./run.sh viser
```

`./run.sh` with no arguments opens a menu; item 1 is `ros2-viser launch`. See [fa-py-libraries](2-fa_py_libraries.md).

lerobot_ros2 / robot_action_composer may list a PyPI extra `viser>=0.2` for grasp-generation UI. That is a **library dependency**, not the ros2-viser launcher.

## Library install (package development)

When you are working on the `ros2_viser` tree itself (from the README):

```bash
cd ros2_viser
pip install -e .
```

Requires `ros2-robot-interface`. Do not treat `pip install ros2-viser` from a random venv as the stack’s main entry.

## Embedding (README API)

Class names below match the package README (`ROS2ViserVisualizer` / `ROS2ViserConfig`). There is no `ViserVisualizer` class in this repo.

```python
from ros2_viser import ROS2ViserVisualizer, ROS2ViserConfig
import time

config = ROS2ViserConfig(
    robot_description_topic="/robot_description",
    joint_states_topic="/joint_states",
    root_node_name="/robot",
    update_rate=30.0,
)
visualizer = ROS2ViserVisualizer(config)
visualizer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    visualizer.stop()
```

Config fields documented in the README: `robot_description_topic`, `joint_states_topic`, `root_node_name`, `update_rate`, `auto_connect`, `enable_fsm_panel`, `enable_gripper_panel`.

Needs `/robot_description` and `/joint_states` publishing. Joint names must match the URDF.

## Related

- [fa-py-libraries](2-fa_py_libraries.md) — primary `./run.sh viser` launcher
- [ros2_robot_interface](1-ros2_robot_interface.md)
