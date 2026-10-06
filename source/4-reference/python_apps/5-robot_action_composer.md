# robot_action_composer

Action sequence composition for robot tasks.

**Repository:** [fiveages-sim/robot_action_composer](https://github.com/fiveages-sim/robot_action_composer)

## Purpose

Compose and execute sequences of robot actions:
- Primitive actions (move, grasp)
- Conditional logic
- Looping
- Error handling

## Installation

```bash
git clone https://github.com/fiveages-sim/robot_action_composer.git
cd robot_action_composer
pip install -e .
```

## Usage

### Define Actions

```python
from robot_action_composer import ActionSequence, actions

sequence = ActionSequence([
    actions.MoveJ([0, 0, 0, 0, 0, 0]),
    actions.MoveL([0.3, 0.0, 0.4]),
    actions.GripperClose(),
    actions.MoveL([0.3, 0.0, 0.5]),
    actions.MoveL([0.3, 0.2, 0.5]),
    actions.GripperOpen(),
])
```

### Execute

```python
from ros2_robot_interface import RobotInterface

robot = RobotInterface()
robot.connect()

sequence.execute(robot)
```

## Available Actions

| Action | Description |
|--------|-------------|
| `MoveJ` | Joint space motion |
| `MoveL` | Linear Cartesian motion |
| `GripperOpen` | Open gripper |
| `GripperClose` | Close gripper |
| `Wait` | Time delay |
| `Conditional` | If/else branching |
| `Loop` | Repeat actions |

## Custom Actions

```python
from robot_action_composer import Action

class CustomAction(Action):
    def execute(self, robot):
        # Custom logic
        pass
```

## Error Handling

```python
sequence = ActionSequence([
    actions.MoveL([0.3, 0.0, 0.4]),
    actions.GripperClose(),
], on_error='retry', max_retries=3)
```

## Related

- [ros2_robot_interface](1-ros2_robot_interface.md)
- [Python Interface How-To](../../2-how_to/5-python_interface.md)
