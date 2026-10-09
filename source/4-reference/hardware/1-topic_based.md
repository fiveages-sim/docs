# topic_based_ros2_control

In-tree under `arms_ros2_control/hardwares/` (not a nested gitmodule). ROS 2 topic hardware interface used when `hardware:=isaac` (Acone xacro: `/isaac/joint_command`, `/isaac/joint_states`).

**Plugin:** `topic_based_ros2_control/TopicBasedSystem`. No `declare_parameter` and no `on_set_parameters`.

**README:** [topic_based_ros2_control](https://github.com/fiveages-sim/arms_ros2_control/blob/d50933d6862ad35ec7633ef522a134924827b115/hardwares/topic_based_ros2_control/README.md). Source: [`topic_based_system.cpp`](https://github.com/fiveages-sim/arms_ros2_control/blob/d50933d6862ad35ec7633ef522a134924827b115/hardwares/topic_based_ros2_control/src/topic_based_system.cpp) at [`d50933d`](https://github.com/fiveages-sim/arms_ros2_control/tree/d50933d6862ad35ec7633ef522a134924827b115).

How to read **Startup only** / **Runtime**: [Hardware Interfaces](0-index.md#how-to-read-the-tables). Isaac Sim: [Isaac Sim](../../2-how_to/2-simulation/4-isaac_sim.md).

:::{code-block} xml
<ros2_control name="my_system" type="system">
  <hardware>
    <plugin>topic_based_ros2_control/TopicBasedSystem</plugin>
    <param name="joint_commands_topic">/robot_joint_commands</param>
    <param name="joint_states_topic">/robot_joint_states</param>
    <param name="initialize_commands_from_state">true</param>
  </hardware>
</ros2_control>
:::

## Parameters

All rows in this table are **Startup only**.

| Parameter | Type / default | Meaning |
|---|---|---|
| `joint_commands_topic` | `"/robot_joint_commands"` | Command `sensor_msgs/JointState` topic |
| `joint_states_topic` | `"/robot_joint_states"` | State `sensor_msgs/JointState` topic |
| `initialize_commands_from_state` | `true` (README: recommended for real hardware) | `true`: first received state becomes the command. `false`: use state_interface `initial_value` |
| `trigger_joint_command_threshold` | `1e-5` | Skip publish when command vs state is below this delta; `-1` always send |
| `sum_wrapped_joint_states` | `false` | `true`: unwrap ±2π (Isaac-style wrapping) |
| `joint_name_prefix` | `""` | Strip this prefix from hardware joint names when matching topic names |
| `initial_value` | per `state_interface` | Used when `initialize_commands_from_state` is `false` |
| `mimic` | per joint | Name of the joint to mimic |
| `multiplier` | `1` | Mimic scale |
