# 分体控制 vs 全身控制

Two real launch paths in [ocs2_arm_controller](https://github.com/fiveages-sim/arms_ros2_control/tree/main/controller/ocs2_arm_controller/launch), also offered as **split body** / **full body** in the [open-deploy-ws `arx-lift2s` README](https://github.com/fiveages-sim/open-deploy-ws/blob/arx-lift2s/README.EN.md).

| | **分体控制** (split) | **全身控制** (whole-body) |
|--|----------------------|---------------------------|
| Meaning | Arms and body/head (and typically hands) run as **separate** controllers | One **unified** whole-body MPC controller |
| Arm / body | [ocs2_arm_controller](../4-reference/controllers/2-ocs2_arm_controller.md) + [basic_joint_controller](../4-reference/controllers/7-basic_joint_controller.md) (`setup_body_controllers` for `body` and `head`) | [ocs2_wbc_controller](../4-reference/controllers/3-ocs2_wbc.md) using `ocs2_wheel_humanoid` |
| Launch | `ros2 launch ocs2_arm_controller split_body.launch.py` (`launch_mode` `split_body`) | `ros2 launch ocs2_arm_controller full_body.launch.py` (`launch_mode` `full_body`) when the robot config type is `ocs2_wbc_controller/Ocs2WbcController` |
| Lift2S menu | `./quick_start.sh` → Launch → Lift2S → **split body** | same menu → **full body** |

Do not treat `split_body.launch.py` as whole-body control. There is no public README that lists a standalone `ros2 launch ocs2_wbc_controller …` entry; `full_body.launch.py` is the in-tree loader.

## Packages (do not invent)

- **basic_joint_controller** — joint FSM Home / Hold / MoveJ; `/fsm_command` is `std_msgs/Int32`. How-to: [Use basic_joint_controller](../2-how_to/11-basic_joint.md).
- **ocs2_arm_controller** — arm MPC FSM HOME / OCS2 / HOLD (package README).
- **ocs2_wbc_controller** — private submodule; whole-body MPC. This docs set does not invent its states or topics.

FSM command values: [FSM and Topics](4-fsm_and_topics.md). Controllers index: [Controllers reference](../4-reference/controllers/0-index.md).
