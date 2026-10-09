# Configure ROS 2 controller parameters

Where controller and hardware-interface parameters live, how to inspect them, and how this stack treats **startup vs runtime** changes. Per-parameter tables: [Controller ROS 2 parameters](../../4-reference/controllers/8-ros2_parameters.md) and [Hardware interface parameters](../../4-reference/hardware/4-ros2_parameters.md).

Topic lists and FSM integers stay on the existing controller pages — this guide is **parameters only**.

## Where parameters live

| Place | What it is | Typical contents |
|-------|------------|------------------|
| `{robot}_description/config/ros2_control/ros2_controllers.yaml` | Loaded by `controller_manager` (merged with `common.yaml` / `{hardware}.yaml` / EEF compose / profile `control.patch` — [robot_common_launch](../../4-reference/descriptions/2-common.md)) | Controller plugin types, `joints`, Home poses, MoveL limits, gripper force keys |
| `ros2 param set` / node CLI | Live ROS 2 parameter API on a running node | Same names as YAML once the node is up |
| URDF / xacro `<ros2_control>` `<param>` | Hardware **plugin** arguments, not `ros2 param` | CAN device, topic names, `initialize_commands_from_state`, vendor IP |
| `{robot}_description/config/ocs2/*.info` | OCS2 **task files** | `baseFrame` / `eeFrame` defaults, MPC model. **Not** ROS 2 parameters |

The `ocs2_arm_controller` README names `config/ocs2_arm_controller.yaml`. At [arms_ros2_control `9a1da3ba`](https://github.com/fiveages-sim/arms_ros2_control/tree/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/ocs2_arm_controller/config) that folder only has `demo.rviz`. Machine values are in the description YAML (example: [`cr5_description/.../ros2_controllers.yaml`](https://github.com/fiveages-sim/robot-descriptions-dobot/blob/main/cr5_description/config/ros2_control/ros2_controllers.yaml)).

`arms_target_manager` also reads [`command/arms_target_manager/config/default.yaml`](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/config/default.yaml) or a robot `config/ocs2/target_manager.yaml`.

## Inspect running values

Controller plugins are ROS 2 nodes named after the controller. After a launch:

:::{code-block} bash
ros2 param list
ros2 param list /ocs2_arm_controller
ros2 param get /ocs2_arm_controller movel_duration
ros2 param get /left_gripper_controller force_threshold
:::

Hardware `<param>` values do **not** appear on `ros2 param list`. They are baked into `/robot_description` when xacro runs. Confirm the plugin with `ros2 control list_hardware_interfaces` and the xacro under `xacro/ros2_control/`.

## Startup vs runtime (what is verified)

A value in YAML is always applied when the controller or hardware plugin **starts**. Whether `ros2 param set` later changes behavior is recorded only when a source or README says so:

| Mark on the reference tables | Meaning |
|------------------------------|---------|
| **Runtime (callback)** | `add_on_set_parameters_callback` writes the new value into live fields |
| **Runtime (README)** | Package README states a hot update (this stack: `movel_duration` as the example) |
| **Startup only (README)** | README states a restart is required (`base_frame` / `left_ee_frame` / `right_ee_frame`) |
| **Startup (plugin load)** | URDF / xacro `<param>` read in hardware `on_init` — change the xacro and restart |
| **未核实（启动时加载；运行时是否可改未在源码中确认）** | Declared and read at init (or re-read without a documented callback). **Not** marked dynamic |

Verified runtime on `ocs2_arm_controller` at the same pin: `hardware_latency`, `traj_record_dir`, `traj_record_enabled`, `rt_timing_enabled` (`CtrlComponent::on_parameter_change`), plus the `movel_*` family that `PoseBasedReferenceManager::updateParam()` re-reads and that the `arms_target_manager` README treats like `movel_duration`.

Everything else on the tables, including `basic_joint_controller` and `adaptive_gripper_controller` keys, is **未核实** unless a footnote says otherwise.

## Related

- [Controller ROS 2 parameters](../../4-reference/controllers/8-ros2_parameters.md)
- [Hardware interface parameters](../../4-reference/hardware/4-ros2_parameters.md)
- [Use basic_joint_controller](11-basic_joint.md)
- [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md)
- [robot_common_launch](../../4-reference/descriptions/2-common.md) — YAML merge order
