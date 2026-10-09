# Configure ROS 2 controller parameters

Where controller and **hardware interface** parameters live, how to inspect them, and how this stack treats **startup vs runtime** changes. Per-parameter tables: [Controller ROS 2 parameters](../../4-reference/controllers/8-ros2_parameters.md). Hardware interface `<param>` tables are on each public driver page — [Hardware Interfaces](../../4-reference/hardware/0-index.md).

Topic lists and FSM integers stay on the controller pages — this guide is **parameters** plus the few mechanisms that several controllers share.

## Where parameters live

| Place | What it is | Typical contents |
|-------|------------|------------------|
| `{robot}_description/config/ros2_control/ros2_controllers.yaml` | Loaded by `controller_manager` (merged with `common.yaml` / `{hardware}.yaml` / EEF compose / profile `control.patch` — [robot_common_launch](../../4-reference/descriptions/2-common.md)) | Controller plugin types, `joints`, Home poses, MoveL limits, 夹爪 force keys |
| `ros2 param set` / node CLI | Live ROS 2 parameter API on a running node | Same names as YAML once the node is up |
| URDF / xacro `<ros2_control>` `<param>` | **Hardware interface** plugin arguments, not `ros2 param` | CAN device, topic names, `initialize_commands_from_state`, vendor IP — read at plugin load |
| `{robot}_description/config/ocs2/*.info` | OCS2 **task files** | `baseFrame` / `eeFrame` defaults, MPC model. **Not** ROS 2 parameters |

The **OCS2 Arm Controller** README names `config/ocs2_arm_controller.yaml`. At [arms_ros2_control `9a1da3ba`](https://github.com/fiveages-sim/arms_ros2_control/tree/9a1da3ba3747b3042866422c2269c1d49bb02f48/controller/ocs2_arm_controller/config) that folder only has `demo.rviz`. Machine values are in the description YAML (example: [`cr5_description/.../ros2_controllers.yaml`](https://github.com/fiveages-sim/robot-descriptions-dobot/blob/main/cr5_description/config/ros2_control/ros2_controllers.yaml)).

`arms_target_manager` also reads [`command/arms_target_manager/config/default.yaml`](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/config/default.yaml) or a robot `config/ocs2/target_manager.yaml`.

**Startup / Runtime** tags on the tables match the public controller READMEs in [arms_ros2_control #120](https://github.com/fiveages-sim/arms_ros2_control/pull/120) (branch commit `e1b7a147`; code pin on `main` is still [`9a1da3ba`](https://github.com/fiveages-sim/arms_ros2_control/tree/9a1da3ba3747b3042866422c2269c1d49bb02f48)). After that PR merges, the same wording is on `main`.

## Inspect running values

Controller plugins are ROS 2 nodes named after the controller. After a launch:

:::{code-block} bash
ros2 param list
ros2 param list /ocs2_arm_controller
ros2 param get /ocs2_arm_controller movel_duration
ros2 param get /left_gripper_controller force_threshold
:::

Most hardware `<param>` values do **not** appear on `ros2 param list` — they are baked into `/robot_description` when xacro runs. Some public hardware interface plugins also `declare_parameter` the same names as node params (ARX, HighTorque, Marvin, some 灵巧手); those rows are marked **Runtime** on the matching driver page — [Hardware Interfaces](../../4-reference/hardware/0-index.md). Confirm the plugin with `ros2 control list_hardware_interfaces` and the xacro under `xacro/ros2_control/`.

## Startup vs runtime

A YAML value is always applied when the controller or hardware interface plugin **starts**. Whether `ros2 param set` later changes behavior uses the same tags as the package READMEs:

| Tag | Meaning |
|-----|---------|
| **Runtime** | `ros2 param set` is picked up **without** reloading. These controllers have no generic `add_on_set_parameters_callback` for the documented keys. Home / MoveJ / waist duration / MoveL are re-read with `get_parameter` on the **next** matching state enter or command. |
| **Startup only** | Loaded in `on_init` / construction / first waist-planner create / hardware plugin `on_init`. Change the YAML or xacro and reload or restart. |
| **Unverified** | Declared, but there is no callback or clear re-read path. The READMEs in #120 mark **none** of the previously documented keys this way. |

These Runtime paths are **not** instant callbacks.

(framework-common-parameters)=
## Framework-common parameters

**Basic Joint Controller** and **OCS2 Arm Controller** both use the same ros2_control `ControllerInterface` / `controller_manager` keys. They are listed **once** here. Per-controller tables keep package-specific keys only.

**Adaptive Gripper Controller** does **not** use `joints`: it declares `joint` (singular) and binds `{joint}/position`. `arms_target_manager` is a command node, not a `ControllerInterface`.

| Parameter | Typical type / default | Meaning |
|-----------|------------------------|---------|
| `joints` | string[] | Joint names for command/state interfaces. **Startup only**. |
| `update_rate` | int (Basic Joint README example `1000`; CR5 YAML `100`) | Hz; often the `controller_manager` value. **Startup only**. |
| `command_interfaces` | string[] / `["position"]` | Command interface names. **Startup only**. OCS2 Arm also uses the set to detect position vs force/MIX — [ros2_control here](../../3-concepts/1-ros2_control_here.md). |
| `state_interfaces` | string[] / `["position", "velocity"]` | State interface names. **Startup only**. |
| `command_prefix` | string / empty | Optional prefix on command interface names. **Startup only**. |

Unload and reload the controller to change these.

## Shared mechanisms

One place for behavior that several controllers share in `libraries/arms_controller_common/`. MoveJ YAML keys are on the [Basic Joint Controller](../../4-reference/controllers/8-ros2_parameters.md) parameter table (the primary MoveJ page). **OCS2 Arm Controller** README FSM is HOME / HOLD / OCS2; it constructs `StateMoveJ` for canonical command `4` (and IK MoveL when `lina_planning` is present) but does not treat MoveJ as a README first-class mode.

运控 layering (controller vs hardware interface, 分体 vs 全身) stays on the existing pages — [Terminology](../../3-concepts/8-terminology.md), [ros2_control here](../../3-concepts/1-ros2_control_here.md), [分体控制 vs 全身控制](../../3-concepts/7-split_vs_wbc.md), [Hardware Interfaces](../../4-reference/hardware/0-index.md). The internal Feishu 运控架构图 is whiteboard-only and is not redrawn here.

### `/fsm_command` value `3`

`/fsm_command` is `std_msgs/Int32`. Canonical MOVEJ is **`4`**.

| Who is running | Meaning of `3` |
|----------------|----------------|
| Mixed OCS2 / WBC stack (分体: **OCS2 Arm Controller** + body/head **Basic Joint**; 全身: **OCS2 WBC Controller**) | **OCS2** on the arm / WBC node. Body/head **Basic Joint** instances still treat `3` as MOVEJ. |
| Standalone **Basic Joint Controller** (package demo, no OCS2 node) | **Legacy MOVEJ alias** (package README). Prefer `4`. |

Do not send `3` expecting MOVEJ on the arm / WBC controller. Full integer table: [FSM and Topics](../../3-concepts/4-fsm_and_topics.md).

(home-statehome)=
### Home (`StateHome`)

Both **Basic Joint Controller** and **OCS2 Arm Controller** use `arms_controller_common::StateHome`. Names, defaults, and **When** tags: [`arms_controller_common` README in #120](https://github.com/fiveages-sim/arms_ros2_control/blob/e1b7a147effca2f29f7cced0b2942837b096c1ff/libraries/arms_controller_common/README.md).

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `home_1` … `home_10` | from YAML (`home_1` required) | Preset configurations. **Startup only** (`StateHome::init`; not re-read). |
| `home_duration` | `3.0` | Interpolation duration (s). **Runtime** (next HOME enter or config switch). |
| `home_interpolation_type` | `"linear"` (`auto_declare` and Basic Joint README YAML) | `"tanh"` \| `"linear"` \| `"doubles"` \| `"none"` (Home has no `"servo"`). **Runtime**. |
| `home_tanh_scale` | `3.0` | tanh scale. **Runtime**. |
| `home_max_velocity` / `home_max_acceleration` / `home_max_jerk` | `2.0` / `4.0` / `20.0` | Limits. **Runtime**. In the common README; Basic Joint §3 YAML example omits them. |
| `switch_command_base` | `100` | HOME config switching. **Startup only** (constructor). |

OCS2 Arm extra slots `home_pos` / `rest_pos` stay on that controller’s table.

## Related

- [Controller ROS 2 parameters](../../4-reference/controllers/8-ros2_parameters.md)
- [Hardware Interfaces](../../4-reference/hardware/0-index.md) — per-driver `<param>` tables
- [Use Basic Joint Controller](11-basic_joint.md)
- [ros2_control in This Stack](../../3-concepts/1-ros2_control_here.md)
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
- [robot_common_launch](../../4-reference/descriptions/2-common.md) — YAML merge order
