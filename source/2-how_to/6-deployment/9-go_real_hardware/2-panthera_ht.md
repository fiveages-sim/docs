# HighTorque Panthera HT

**HighTorque** (高擎) is the brand. **Panthera HT** is that brand’s dual-arm **manipulator**. Workspace: `open-deploy-ws` branch `panthera-ht`. It is not ARX Lift 2S (no mobile chassis).

Brand labels follow [robot_usds README_zh-CN.md §3.1](https://github.com/fiveages-sim/robot_usds/blob/main/README_zh-CN.md#31-中文简称与英文标识对照): 高擎 = HighTorque / Panthera.

```{admonition} Source of truth
:class: important

Follow the branch README. Launch flags are those listed there.

- Chinese: [open-deploy-ws `panthera-ht` README](https://github.com/fiveages-sim/open-deploy-ws/blob/panthera-ht/README.md)
- English: [README.EN.md](https://github.com/fiveages-sim/open-deploy-ws/blob/panthera-ht/README.EN.md)
```

Robot launch name in that README is `panthera_ht`.

## Clone and init

### Field zip

README “quick deployment”: unzip (example `~/ht-deploy-ws`), then:

:::{code-block} bash
cd ~/ht-deploy-ws
./release.sh --install
source /opt/ros/jazzy/setup.bash
./quick_start.sh
:::

### Git clone (development)

:::{code-block} bash
cd ~
git clone -b panthera-ht git@github.com:fiveages-sim/open-deploy-ws.git ht-deploy-ws
cd ~/ht-deploy-ws
./init_repo.sh
:::

Then `source /opt/ros/jazzy/setup.bash` and `./quick_start.sh` to build.

## Build and launch (scripts first)

:::{code-block} bash
cd ~/ht-deploy-ws
./quick_start.sh
:::

README: **Build** (simulation vs real-hardware packages), then **Launch** (single / dual arm, simulation or real). Real hardware uses serial (`/dev/ttyACM*`); the script prompts for permissions.

Isomorphic teleop (同构遥操作) on this branch is `./teleop_start.sh` (master / slave). See [Isomorphic Teleop](../../5-teleoperation/7-isomorphic_teleop.md) and the same README section on `teleop_start.sh`. Drag teaching (拖动遥操作) is **not** a separate implemented stack.

## Optional README launch lines

Prefer the script. README equivalents:

:::{code-block} bash
source ~/ht-deploy-ws/install/setup.bash
ros2 launch robot_common_launch manipulator.launch.py robot:=panthera_ht
ros2 launch robot_common_launch manipulator.launch.py robot:=panthera_ht type:=dual
ros2 launch ocs2_arm_controller demo.launch.py robot:=panthera_ht type:=single hardware:=real
ros2 launch ocs2_arm_controller demo.launch.py robot:=panthera_ht type:=dual hardware:=real
:::

README `type:=dual` / `type:=single` is **arm topology**, not an end-effector key, and does **not** expand to `left_type` / `right_type`. Different L/R EEF keys use `left_type:=` / `right_type:=` (do not also pass `type:=`) — [robot_common_launch](../../../4-reference/descriptions/2-common.md).

Zenoh: same as other deploy hosts — `ros-jazzy-rmw-zenoh-cpp` and `RMW_IMPLEMENTATION=rmw_zenoh_cpp` (README).

## Related

- [Go to Real Hardware](0-index.md)
- [ARX Lift 2S](1-arx_lift2s.md)
- [Isomorphic Teleop](../../5-teleoperation/7-isomorphic_teleop.md)
- [open-deploy-ws setup](../../../1-getting_started/3-open_deploy_ws.md)
