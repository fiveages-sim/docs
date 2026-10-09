# Field commissioning

For on-site engineers who unpack a workspace, bring up the robot, and run teleop or a browser view.

## 1. Deploy from a field zip (deploy-ws)

Public lean branches document a **zip** path: unzip, then `./release.sh --install`, then `./quick_start.sh`. Descriptions stay as source; controllers and the driver layer come from `.deb`.

1. [Go to Real Hardware](../2-how_to/6-deployment/9-go_real_hardware/0-index.md) — safety, robot table, which branch to use.
2. [ARX Lift 2S](../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md) — field zip, then `./quick_start.sh` (split body / full body).
3. [HighTorque Panthera HT](../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md) — field zip (`~/ht-deploy-ws` example), `./release.sh --install`, `./quick_start.sh`.

Git clone + `./init_repo.sh` is the development path on the same pages. Extra flags and robot IDs for **fa-deploy-ws** are only in that workspace’s README after access: [fa-deploy-ws Setup](../1-getting_started/4-fa_deploy_ws.md).

## 2. Deploy fa-py-libraries (zip or git)

On-site Python tools (interface, Viser, VR) come from [fa-py-libraries](../4-reference/python_apps/2-fa_py_libraries.md).

- Git: `git clone` then `./init.sh all` (Python 3.12 env).
- Field zip: the [fa-py-libraries README](https://github.com/fiveages-sim/fa-py-libraries/blob/main/README.md) documents `./release.sh` (`--package-no-git` is the smaller zip). After unzip: `./init.sh install` (and the optional XRoboToolkit `./init.sh` lines only if you use that VR backend).

Then launch with `./run.sh` or a direct subcommand from that README.

## 3. Start VR teleop

1. [VR Teleop](../2-how_to/5-teleoperation/6-vr_teleop.md) — Pico Enterprise vs consumer, WebXR (`./run.sh vr`) vs XRoboToolkit (`./run.sh vr-xrt`).
2. Same commands are listed on [fa-py-libraries](../4-reference/python_apps/2-fa_py_libraries.md).

The robot stack (deploy-ws `./quick_start.sh` or the launch on the how-to) must already be running. Headset SKU notes stay on the VR page.

## 4. Start Viser (browser view)

1. Bring up the robot so `/robot_description` and `/joint_states` are published.
2. From fa-py-libraries: `./run.sh viser` — [ros2-viser](../4-reference/python_apps/3-ros2_viser.md), [fa-py-libraries](../4-reference/python_apps/2-fa_py_libraries.md).

Viser is a **browser** 3D view. The ros2-viser README also documents optional **FSM** and **gripper** panels (`enable_fsm_panel` / `enable_gripper_panel`, default on). There is no separate “phone app” or host/port flag in this docs set; open the Viser page the library prints, including from another device on the same network if that URL is reachable.

## Related

- [Install Environment](../1-getting_started/2-install_environment.md)
- [open-deploy-ws Setup](../1-getting_started/3-open_deploy_ws.md)
- [FSM and Topics](../3-concepts/4-fsm_and_topics.md) — `/fsm_command` is `std_msgs/Int32`
- [Configure ROS 2 controller parameters](../2-how_to/4-controllers/12-ros2_parameters.md) — YAML vs runtime `ros2 param`
