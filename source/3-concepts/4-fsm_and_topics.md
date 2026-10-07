# FSM and Topics

Finite-state machines in this stack live in [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control). Shared primitives are in `libraries/arms_controller_common/` (`StateHome`, `StateHold`, `StateMoveJ`, `FSMCommandPublisher`).

```{admonition} Source of truth
:class: important

`/fsm_command` is **`std_msgs/Int32`**, not `String`. There is no documented `/mode_command`, `/fsm_state` String, or wheeled-arm `stand` / `walk` / `arm_teleop` contract. Per-controller topics: the controller pages and package READMEs.
```

## `/fsm_command` (`std_msgs/Int32`)

`FSMCommandPublisher` publishes `std_msgs/Int32` on `/fsm_command`. Header values: `1` HOME, `2` HOLD, `3` OCS2, `4` MOVEJ (`100` switches HOME pose).

Exact transitions depend on the **running controller**:

| Controller | States | Commands |
|------------|--------|----------|
| [basic_joint_controller](../4-reference/controllers/7-basic_joint_controller.md) | Home / Hold / MoveJ | README: `1` HOME, `2` HOLD, `4` MOVEJ (canonical); `3` is a legacy MOVEJ alias, and means **OCS2** on mixed OCS2/WBC stacks |
| [ocs2_arm_controller](../4-reference/controllers/2-ocs2_arm_controller.md) | HOME / OCS2 / HOLD | README: `1` HOME, `2` HOLD, `3` OCS2 on `/control_input`; starts in HOLD; OCS2 returns only to HOLD |
| [ocs2_wbc_controller](../4-reference/controllers/3-ocs2_wbc.md) | Whole-body stack | Private package; do not invent states here |

:::{code-block} bash
ros2 topic pub --once /fsm_command std_msgs/msg/Int32 "data: 2"   # HOLD
:::

## 分体控制 vs 全身控制

| Mode | Chinese | What runs | Launch |
|------|---------|-----------|--------|
| **Split** | 分体控制 | Arm MPC ([ocs2_arm_controller](../4-reference/controllers/2-ocs2_arm_controller.md)) + body/head (and typically hands) via [basic_joint_controller](../4-reference/controllers/7-basic_joint_controller.md) | `ros2 launch ocs2_arm_controller split_body.launch.py` (`launch_mode` `split_body`) |
| **Whole-body** | 全身控制 | Unified [ocs2_wbc_controller](../4-reference/controllers/3-ocs2_wbc.md) (`ocs2_wheel_humanoid`) | `ros2 launch ocs2_arm_controller full_body.launch.py` (`launch_mode` `full_body`) when the config type is `ocs2_wbc_controller/Ocs2WbcController` |

Do not describe teleop as a separate FSM state. Implemented teleop is the isomorphic path — [Isomorphic Teleop](../2-how_to/7-isomorphic_teleop.md) — not a `/teleop/left_ee_pose` contract on this page.

## Related

- [basic_joint_controller](../4-reference/controllers/7-basic_joint_controller.md)
- [ocs2_arm_controller](../4-reference/controllers/2-ocs2_arm_controller.md)
- [ocs2-wbc-controller](../4-reference/controllers/3-ocs2_wbc.md)
- [Controllers reference](../4-reference/controllers/0-index.md)
