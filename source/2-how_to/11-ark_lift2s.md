# Ark / Lift 2s

**Ark (方舟)** is **Lift 2s**: the full-body platform (arms **plus** lift axis and **mobile base / chassis**), not an arm-only robot.

**Acone** is the **arm portion** of the same stack (manipulator only). It is not the Lift 2s platform. The `arx-lift2s` workspace can launch Acone from `quick_start` for co-debug; the product focus of that branch is Lift 2s.

```{admonition} Source of truth
:class: important

Follow the branch README. Do not invent extra launch flags.

- Chinese: [open-deploy-ws `arx-lift2s` README](https://github.com/fiveages-sim/open-deploy-ws/blob/arx-lift2s/README.md)
- English: [README.EN.md](https://github.com/fiveages-sim/open-deploy-ws/blob/arx-lift2s/README.EN.md)
```

## Clone and init

From the README (directory name `lift2s-ws` is the example):

:::{code-block} bash
cd ~
git clone -b arx-lift2s git@github.com:fiveages-sim/open-deploy-ws.git lift2s-ws
cd ~/lift2s-ws
./init_repo.sh
:::

Field zip (README): unzip, then `./release.sh --install`, then `./quick_start.sh`. Descriptions stay as source; controllers / hardware interface come from `.deb`.

## Build and launch (scripts first)

Primary path is `./quick_start.sh` (scenario build + Lift2S split/full body, simulation or real):

:::{code-block} bash
cd ~/lift2s-ws
./quick_start.sh
:::

README menu:

1. **Build** — simulation packages, or real-hardware packages (includes `arx_ros2_control`)
2. **Launch** — choose **Lift2S**, then **split body** or **full body**, then simulation (`mock_components`) or **real hardware**

CAN (README): left/right arms `can1` / `can3`; no network IP. Lift axis defaults to `hybrid` (change to `soft_p` in `quick_start`).

X5 / R5 / **ACone** / Lift / X7S in the same menu are `robot-descriptions-arx` models for **co-debug**. Pick **ACone** only when you want the **arm**, not the full Lift 2s chassis.

## Optional README launch lines

Prefer the script. These are the README’s optional equivalents for **Lift2S**:

:::{code-block} bash
source ~/lift2s-ws/install/setup.bash
# Visualization
ros2 launch robot_common_launch manipulator.launch.py robot:=arx_lift2s
# Split body / full body (add hardware:=real for the robot)
ros2 launch ocs2_arm_controller split_body.launch.py robot:=arx_lift2s
ros2 launch ocs2_arm_controller full_body.launch.py robot:=arx_lift2s
:::

Zenoh: README asks for `sudo apt install ros-jazzy-rmw-zenoh-cpp` and `export RMW_IMPLEMENTATION=rmw_zenoh_cpp` on the deploy host.

## Related

- [Go to Real Hardware](9-go_real_hardware.md)
- [Panthera HT](12-panthera_ht.md)
- [open-deploy-ws setup](../1-getting_started/3-open_deploy_ws.md)
