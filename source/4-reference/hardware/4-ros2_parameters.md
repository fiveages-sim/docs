# Hardware interface parameters

ros2_control **hardware plugin** arguments. These are URDF / xacro `<param>` entries under `<ros2_control><hardware>`, loaded in the plugin `on_init`. They are **not** the same API as `ros2 param list` on a controller node.

How the launch `hardware:=` key selects a plugin: [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md). How to inspect controllers vs hardware: [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md).

The in-tree [`hardwares/README.md`](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/hardwares/README.md) is **build-only** (`colcon build --packages-up-to …`). Parameter names live in each hardware-interface README and in the robot xacro.

## topic_based_ros2_control

Public plugin used when `hardware:=isaac` (Acone xacro: `/isaac/joint_command`, `/isaac/joint_states`). README: [topic_based_ros2_control](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/hardwares/topic_based_ros2_control/README.md). Source pin: [`9a1da3ba` `topic_based_system.cpp`](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/hardwares/topic_based_ros2_control/src/topic_based_system.cpp).

Plugin class: `topic_based_ros2_control/TopicBasedSystem`.

README example:

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

| Parameter | README / source default | Meaning | Startup / runtime |
|-----------|-------------------------|---------|-------------------|
| `joint_commands_topic` | `"/robot_joint_commands"` | Command `sensor_msgs/JointState` topic | Startup (plugin load) |
| `joint_states_topic` | `"/robot_joint_states"` | State `sensor_msgs/JointState` topic | Startup (plugin load) |
| `initialize_commands_from_state` | `true` (README: recommended for real hardware) | `true`: first received state becomes the command (avoids a jump). `false`: use state_interface `initial_value` | Startup (plugin load) |
| `trigger_joint_command_threshold` | `1e-5` (source; not in README) | Skip publish when command vs state is below this delta | Startup (plugin load) |
| `sum_wrapped_joint_states` | `"false"` (source; not in README) | `"true"`: unwrap ±2π (Isaac-style wrapping) | Startup (plugin load) |
| `joint_name_prefix` | `""` (source; not in README) | Strip this prefix from hardware joint names when matching topic names | Startup (plugin load) |

Per-joint `initial_value` on a `state_interface` is used when `initialize_commands_from_state` is `false`. Joint `mimic` / `multiplier` are standard ros2_control joint parameters read at the same `on_init`.

Change any of these by editing the xacro (or the overlay that generates it) and **restarting** the hardware. There is no `on_set_parameters` path in this plugin.

Isaac Sim: [Isaac Sim](../../2-how_to/2-simulation/4-isaac_sim.md).

## Other public hardware interfaces

Vendor plugins and the `<param>` names already listed on [Public hardware interfaces](1-public_hi.md) (for example ARX `can_interface`, Dobot `robot_ip` / `robot_port`, HighTorque `serial_port`, Modbus `serial_port` / `baudrate`). Those pages are the parameter lists. They are xacro `<param>` values at plugin load — same **Startup (plugin load)** rule as above.

Use the plugin class from that robot’s `xacro/ros2_control/*.xacro`.

## Private hardware interfaces

[Private hardware interfaces](2-private_hi.md) names the private packages (Rokae, Eyou, iNex, Wuji, DexCap, Fairino). Configuration keys, IP/serial layouts, and SDK env vars are in **that repository’s README after access**. This page does not list undocumented private SDK parameters.

SDK build notes: [SDK Notes](3-sdk_notes.md).

## OCS2 `.info` files

`{robot}_description/config/ocs2/*.info` (and the generated library under `config/ocs2/generated`) are **OCS2 task / model files**, not ROS 2 parameters. The controller ROS param `info_file_name` (default `task`) only chooses which `.info` to load at startup — [Controller ROS 2 parameters](../controllers/8-ros2_parameters.md).

## Related

- [Configure ROS 2 controller parameters](../../2-how_to/4-controllers/12-ros2_parameters.md)
- [Public hardware interfaces](1-public_hi.md)
- [Private hardware interfaces](2-private_hi.md)
- [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md)
