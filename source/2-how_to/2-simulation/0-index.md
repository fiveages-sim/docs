# Simulation

Physics simulation with Gazebo or NVIDIA Isaac Sim.

`hardware:=mock_components` / `gz` / `isaac` are launch keys, not vendor hardware-interface packages under `hardwares/`. `isaac_sim` is set inside Isaac on the in-process path; it is not a `demo.launch.py` flag. Plugin table: [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md). Isaac topic `<param>` names: [topic_based_ros2_control](../../4-reference/hardware/1-topic_based.md).

Start Isaac and run the first checks: [Isaac Sim](4-isaac_sim.md). Mechanisms, extensions, and USD layout: [Simulation reference](../../4-reference/simulation/0-index.md).

Isaac USD → composer → LeRobot datagen is the [Synthetic Data](../7-synthetic_data/0-index.md) How-To category, not Gazebo.

```{toctree}
:maxdepth: 1

3-gazebo_sim
4-isaac_sim
```
