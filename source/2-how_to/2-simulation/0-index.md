# Simulation

The default physics simulation path is NVIDIA Isaac Sim (FaSim). Start Isaac and run the first checks: [Isaac Sim](4-isaac_sim.md). To view and control the robot in a browser while Sim is running, start Viser first: [Start Viser](../3-programming/5-python_interface.md#start-viser). Mechanisms, extensions, and USD layout: [Simulation reference](../../4-reference/simulation/0-index.md).

`hardware:=mock_components` / `gz` / `isaac` are launch keys, not vendor hardware-interface packages under `hardwares/`. `isaac_sim` is set inside Isaac on the in-process path; it is not a `demo.launch.py` flag. Plugin table: [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md). Isaac topic `<param>` names: [topic_based_ros2_control](../../4-reference/hardware/1-topic_based.md).

Gazebo remains available as an alternative backend: [Gazebo Simulation](3-gazebo_sim.md).

Isaac USD → composer → LeRobot datagen is the [Synthetic Data](../7-synthetic_data/0-index.md) How-To category, not Gazebo.

```{toctree}
:maxdepth: 1

4-isaac_sim
3-gazebo_sim
```
