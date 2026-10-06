# HUG

Human grasp inference for manipulation.

```{admonition} Access Required
:class: warning

This package requires private repository access.
```

**Repository:** HUG (private)

## Purpose

Grasp inference from human demonstrations:
- Grasp pose prediction
- Object manipulation
- Learning from observation

## Installation

HUG is a submodule of lerobot_ros2:

```bash
cd lerobot_ros2
git submodule update --init HUG
cd HUG
uv sync  # or pip install -e .
```

## Usage

```python
from hug import GraspInference

model = GraspInference.load("path/to/model")
grasp_pose = model.predict(rgb_image, depth_image)
```

## Integration

Used with lerobot_ros2 for:
- Data collection with grasp labels
- Policy training
- Deployment

## Notes

- No training secrets in public docs
- Model weights separate from code
- See internal documentation for training

## Related

- [lerobot_ros2](4-lerobot_ros2.md)
