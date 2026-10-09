# 分体控制 vs 全身控制

Two real launch paths in [ocs2_arm_controller](https://github.com/fiveages-sim/arms_ros2_control/tree/main/controller/ocs2_arm_controller/launch), also offered as **split body** / **full body** in the [open-deploy-ws `arx-lift2s` README](https://github.com/fiveages-sim/open-deploy-ws/blob/arx-lift2s/README.EN.md).

| | **分体控制** (Split Body) | **全身控制** (Full Body) |
|--|--------------------------|-------------------------|
| Meaning | Arms and body/head (and typically dexterous hands) run as **separate** controllers | One **unified** whole-body MPC controller |
| Arm / body | [OCS2 Arm Controller](../4-reference/controllers/2-ocs2_arm_controller.md) + [Basic Joint Controller](../4-reference/controllers/7-basic_joint_controller.md) (`setup_body_controllers` for `body` and `head`) | [OCS2 WBC Controller](../4-reference/controllers/3-ocs2_wbc.md) using `ocs2_wheel_humanoid` |
| Launch | `ros2 launch ocs2_arm_controller split_body.launch.py` (`launch_mode` `split_body`) | `ros2 launch ocs2_arm_controller full_body.launch.py` (`launch_mode` `full_body`) when the robot config type is `ocs2_wbc_controller/Ocs2WbcController` |
| Lift2S menu | `./quick_start.sh` → Launch → Lift2S → **split body** | same menu → **full body** |

`split_body.launch.py` is the 分体控制 (Split Body) path. 全身控制 uses `full_body.launch.py` (there is no public standalone `ros2 launch ocs2_wbc_controller …` entry).

## Packages

- **Basic Joint Controller** (`basic_joint_controller`) — joint FSM HOME / HOLD / MOVEJ; `/fsm_command` is `std_msgs/Int32`. How-to: [Use Basic Joint Controller](../2-how_to/4-controllers/11-basic_joint.md).
- **OCS2 Arm Controller** (`ocs2_arm_controller`) — arm MPC FSM HOME / OCS2 / HOLD (package README).
- **OCS2 WBC Controller** (`ocs2_wbc_controller`) — private submodule; 全身控制. States and topics are in that package README after access.

FSM command values, Action / Service tables, and WBC Cartesian topics: [FSM and Topics](4-fsm_and_topics.md). Controllers index: [Controllers reference](../4-reference/controllers/0-index.md).

`/body_target*`, `/head_target*`, `/mode_command`, and `WbcCurrentState` need **`ocs2_wbc_controller`** and that robot’s 全身 launch/config. Default mock demos (`demo.launch.py`) and 分体 do **not** imply those features are present; capability bits are machine-dependent. Public Taku mock uses `split_body.launch.py robot:=taku`; `full_body.launch.py robot:=taku` still needs the private `ocs2_wbc_controller` submodule (shipping `config/ocs2/fixed_base_tcp.info` is not enough).
