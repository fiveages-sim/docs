# wuji-retargeting

Hand motion retargeting for Wuji hands.

**Repository:** [fiveages-sim/wuji-retargeting](https://github.com/fiveages-sim/wuji-retargeting)

## Purpose

Retargets hand motion between different hand models:
- Human to robot
- Robot to robot
- Mirror operations

## Installation

```bash
git clone https://github.com/fiveages-sim/wuji-retargeting.git
cd wuji-retargeting
pip install -e .
```

## Usage

```python
from wuji_retargeting import Retargeter

retargeter = Retargeter(
    source_model="human_hand",
    target_model="wuji_hand2"
)

robot_joints = retargeter.retarget(human_joints)
```

## Configuration

```yaml
retargeting:
  source:
    model: human_hand
    joint_names: [...]
  
  target:
    model: wuji_hand2
    joint_names: [...]
  
  mapping:
    # Joint correspondence
    human_thumb_mcp: wuji_thumb_1
    human_thumb_pip: wuji_thumb_2
    # ...
```

## SDK Preference

For best results, prefer wuji-sdk for direct hand control where available.

## Related

- [wuji_glove_teleop](../teleop/5-wuji_glove.md)
- [wuji-ros2-control](../teleop/7-wuji_hand_hi.md)
