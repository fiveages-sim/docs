# lerobot_ros2

LeRobot integration for ROS 2.

**Repository:** [fiveages-sim/lerobot_ros2](https://github.com/fiveages-sim/lerobot_ros2)

## Purpose

Integrates LeRobot learning framework with ROS 2:
- Data collection
- Policy deployment
- Training pipelines

## Installation

```bash
git clone https://github.com/fiveages-sim/lerobot_ros2.git
cd lerobot_ros2
pip install -e .
```

## Features

### Data Collection

Record robot demonstrations:

```python
from lerobot_ros2 import DataCollector

collector = DataCollector(
    dataset_name="my_task",
    robot_interface=robot
)

collector.start_recording()
# ... perform demonstration ...
collector.stop_recording()
collector.save()
```

### Policy Deployment

Run trained policies:

```python
from lerobot_ros2 import PolicyRunner

runner = PolicyRunner(
    model_path="path/to/model",
    robot_interface=robot
)

runner.run()
```

## Topics

| Topic | Type | Direction | Description |
|-------|------|-----------|-------------|
| `/lerobot/episode_start` | `Empty` | Subscribe | Start episode |
| `/lerobot/episode_end` | `Empty` | Subscribe | End episode |
| `/lerobot/action` | `JointState` | Publish | Policy output |

## Dataset Format

Compatible with LeRobot HuggingFace datasets:
- Episode structure
- Observation/action format
- Metadata

## Related

- [ros2_robot_interface](1-ros2_robot_interface.md)
- [HUG](6-hug.md)
