# ros2-viser

Web-based 3D visualization using Viser.

**Repository:** [fiveages-sim/ros2-viser](https://github.com/fiveages-sim/ros2-viser)

## Purpose

Web visualization for ROS 2:
- 3D robot model
- Joint state display
- Target markers
- Browser accessible

## Installation

```bash
pip install ros2-viser
```

Or via fa-py-libraries:

```bash
cd fa-py-libraries
pip install -e .
```

## Usage

### Basic

```python
from ros2_viser import ViserVisualizer

viz = ViserVisualizer()
viz.start()

print(f"Open browser: {viz.get_url()}")
```

### With Robot

```python
from ros2_viser import ViserVisualizer
from ros2_robot_interface import RobotInterface

robot = RobotInterface()
robot.connect()

viz = ViserVisualizer()
viz.set_robot_model("dobot_cr5")
viz.start()

# Visualization updates automatically from /joint_states
```

## Features

### Robot Visualization

- URDF model rendering
- Real-time joint updates
- Link highlighting

### Markers

- Target pose markers
- Trajectory preview
- Custom markers

### UI Elements

- Joint sliders
- Mode selector
- Status display

## Configuration

```python
viz = ViserVisualizer(
    host="0.0.0.0",
    port=8080,
    urdf_path="/path/to/robot.urdf"
)
```

## Web Interface

Access via browser:
- Desktop: `http://localhost:8080`
- Mobile: `http://<host-ip>:8080`
- VR: WebXR compatible

## Related

- [fa-py-libraries](2-fa_py_libraries.md)
