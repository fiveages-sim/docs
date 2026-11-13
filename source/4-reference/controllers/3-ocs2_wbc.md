# OCS2 WBC Controller

Whole-body MPC — **全身控制** (`ocs2_wbc_controller`) — for wheeled dual-arm robots, using `ocs2_wheel_humanoid`.

```{admonition} Run the deb, clone the source to edit it
:class: note

You can run `ocs2_wbc_controller` without opening the private repository. It ships in the GitHub Release package `ros-jazzy-arms-ros2-control`, together with `ocs2_humanoid` and `lina_planning` ([arms deb notes](https://github.com/fiveages-sim/arms_ros2_control/blob/main/README.deb.md)). In `open-deploy-ws` or `fa-deploy-ws`, choose `d` for arms in `./init_repo.sh`, or run `./scripts/install_core_debs.sh --only arms`. That script installs the standard package. It does not install `ros-jazzy-arms-ros2-control-full`, and the package is not on Ubuntu or ROS apt.

[ocs2-wbc-controller](https://github.com/fiveages-sim/ocs2-wbc-controller) is the source checkout under `controller/ocs2_wbc_controller` in [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control). Open it when you need to read or change the source. Topics and FSM values that are only written in that README stay there. The public loader is `full_body.launch.py`.
```

## Role

- Unified **全身控制** stack: one `ocs2_wbc_controller` instead of arm MPC plus separate body/head joint controllers
- Motion library: `ocs2_wheel_humanoid` (see [ocs2-humanoid](4-ocs2_humanoid.md))

Contrast with **分体控制**: [OCS2 Arm Controller](2-ocs2_arm_controller.md) + [Basic Joint Controller](7-basic_joint_controller.md) via `split_body.launch.py`.

## Launch (from `ocs2_arm_controller`)

There is no public README listing a `ros2 launch ocs2_wbc_controller …` entry point. The in-tree path that loads this controller is:

:::{code-block} bash
ros2 launch ocs2_arm_controller full_body.launch.py robot:=<robot>
:::

`full_body.launch.py` (`launch_mode` `full_body`) spawns `ocs2_wbc_controller` when the robot’s `controller_manager` type is `ocs2_wbc_controller/Ocs2WbcController`.

The same file declares `type` and `create_robot_profile_launch_arguments()` (`left_type` / `right_type`, `use_profile_eef`). End-effectors: [OCS2 Arm Controller](2-ocs2_arm_controller.md) and [robot_common_launch](../descriptions/2-common.md). Planning URDF is the same xacro path (`planning_urdf_path`); static `urdf/{robot}_{robot_type}.urdf` lookup was removed.

`split_body.launch.py` is the split (分体) path; whole-body control uses `full_body.launch.py`.

## Public command surface

Extra FSM states stay in the private package README after access. From public sources, 全身 uses:

- Cartesian body / head: `/body_target*`, `/head_target*` ([arms_target_manager](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_target_manager/README.md))
- `/mode_command` (`std_msgs/String`) and `/ocs2_wbc_controller/current_state` (`WbcCurrentState`)
- Shared action / service types: [`arms_ros2_control_msgs` README](https://github.com/fiveages-sim/arms_ros2_control/blob/9a1da3ba3747b3042866422c2269c1d49bb02f48/command/arms_ros2_control_msgs/README.md)

:::{admonition} Whole-body (WBC) availability
:class: warning

These topics need `ocs2_wbc_controller` and that robot’s 全身 launch and config. `demo.launch.py` and 分体 (`split_body.launch.py`) do not start them. Capability bits (`WbcCapability`) depend on the robot. Public Taku mock uses `split_body.launch.py robot:=taku` (arm MPC, body and head basic controllers, and grippers). `full_body.launch.py robot:=taku` needs `ocs2_wbc_controller` from the `ros-jazzy-arms-ros2-control` deb, or from a source checkout. Shipping `config/ocs2/fixed_base_tcp.info` is not enough. With that config and the controller installed, Taku full-body default `headMode` is `HEAD_GAZE` (gaze on `head_camera_mid_optical_frame`), and `target_manager.yaml` has `enable_head_control: false`. Head 6D tracking (`HEAD_TRACKING`) is there when `head_tracking_ee_enabled` is true. Taku’s body-relative rest is around x≈−0.21, not Bot2 `[0, 0.25]`. Full tables: [FSM and Topics](../../3-concepts/4-fsm_and_topics.md).
:::

## Related

- [Controller ROS 2 parameters](8-ros2_parameters.md) — public overlay keys; full list is the private package README
- [OCS2 Arm Controller](2-ocs2_arm_controller.md) — 分体控制 / `split_body.launch.py`
- [Basic Joint Controller](7-basic_joint_controller.md)
- [ocs2-humanoid](4-ocs2_humanoid.md) — `ocs2_wheel_humanoid`
- [FSM and Topics](../../3-concepts/4-fsm_and_topics.md)
- [ros2_robot_interface](../python_apps/1-ros2_robot_interface.md)
- [分体控制 vs 全身控制](../../3-concepts/7-split_vs_wbc.md)
