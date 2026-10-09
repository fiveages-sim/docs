# Controllers

**Basic Joint Controller** joint-position FSM (HOME / HOLD / MOVEJ). `/fsm_command` is `std_msgs/Int32` — on mixed OCS2/WBC stacks `3` means **OCS2**; canonical MOVEJ is `4`.

Parameter YAML, `ros2 param` inspection, and Startup vs Runtime: [Configure ROS 2 controller parameters](12-ros2_parameters.md). Tables: [Controller ROS 2 parameters](../../4-reference/controllers/8-ros2_parameters.md).

```{toctree}
:maxdepth: 1

11-basic_joint
12-ros2_parameters
```
