# How to use impedance control

On a real arm, impedance control is how the arm gives under contact. Two kinds are in use. Pick the one that matches the robot.

| Kind | Robots | Who provides compliance | What the controller commands |
|------|--------|-------------------------|------------------------------|
| **MIT-mode force / MIX** | **HighTorque** (高擎) **Panthera HT**; **ARX** (方舟无限) arms | Controller + hardware interface in MIT / `full_control` (position + velocity + effort; stiffness on the HI) | Force-capable / MIX when those interfaces are present |
| **Vendor joint impedance** | **Tianji** (天玑); **Rokae** (珞石) | Vendor stack, on the hardware interface | **Joint position** |

## 1. MIT-mode force control (Panthera HT / ARX)

Use this path on **Panthera HT** and **ARX** arms. The hardware interface runs a force-capable MIT configuration. The controller tracks the pose with that mix of position, velocity, and effort. VR teleop is one client: [VR Teleoperation](../5-teleoperation/6-vr_teleop.md).

**HighTorque Panthera HT** — [ht-ros2-control README](https://github.com/fiveages-sim/ht-ros2-control/blob/main/README.md):

- HI `control_mode:=mit` (default; the older name `full_control` is still accepted)
- The driver sends position + velocity + effort + kp/kd (`pos_vel_tqe_kp_kd`)
- Stiffness is the HI parameters `joint_kp` / `joint_kd` (rqt / `ros2 param`)
- Other documented HI modes: `effort` (torque only), `position` (position only)

**ARX arms** — [arx-ros2-control README](https://github.com/fiveages-sim/arx-ros2-control/blob/main/README.md):

- Arms use `full_control` / MIT MIX. Other `control_mode` values in xacro are ignored, with a warning
- `write()` sends position + velocity + effort
- MIT `kp` / `kd` come from HI `joint_k_gains` / `joint_d_gains`
- README mapping: OCS2 trajectory → position; OCS2 `future_input` → velocity; OCS2 effort → gravity / static feedforward torque

**Controller** — [ocs2_arm_controller README — Interface Configuration](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/README.md):

- The mode is auto-detected from the robot config
- Position-only: command `position`; state `position` + `velocity`
- Force / MIX: command `position`, `velocity`, `effort`, `kp`, and `kd` are all present. `[kp, kd]` is `default_gains` (HOME / HOLD) and `pd_gains` (OCS2), at **Startup**
- ARX documents OCS2 MIX as position + velocity + effort, with kp/kd on the HI. On HT, when kp/kd stay HI parameters, OCS2 may stay in position mode. Gravity compensation then uses `ht_gravity_compensation` or a larger `joint_kp` (same HT README)

Bring the robot up with the lean-branch `./quick_start.sh` / `hardware:=real` path on [HighTorque Panthera HT](../6-deployment/9-go_real_hardware/2-panthera_ht.md) or [ARX Lift 2S](../6-deployment/9-go_real_hardware/1-arx_lift2s.md). For the headset, follow [VR Teleoperation](../5-teleoperation/6-vr_teleop.md).

Master–slave `mode:=mit` / `effort` on Panthera HT is [Isomorphic Teleop](../5-teleoperation/7-isomorphic_teleop.md).

## 2. Vendor joint impedance (Tianji / Rokae)

Use this path on **Tianji** (天玑) and **Rokae** (珞石). The controller sends **joint position**. Joint impedance is the vendor feature on the hardware interface.

**Tianji** — [marvin-ros2-control README](https://github.com/fiveages-sim/marvin-ros2-control/blob/master/README.md):

- Command interface: joint **`position`**. State: `position`, `velocity`, `effort`
- Runtime `ctrl_mode`: `POSITION` / `JOINT_IMPEDANCE` / `CART_IMPEDANCE` / `POWER_OFF`
- Joint impedance gains: `joint_k_gains` / `joint_d_gains` (7 values). Cartesian: `cart_k_gains` / `cart_d_gains`
- Example: `ros2 param set /<hardware_node> ctrl_mode JOINT_IMPEDANCE`

**Rokae** uses the same split: the controller sends position, and compliance is the vendor hardware interface. Parameter names are in the private `rokae-ros2-control` README after access. Overview: [Hardware Interfaces](../../4-reference/hardware/0-index.md).

Internal FA robots that use Tianji / Rokae arms are in [fa-deploy-ws Setup](../../1-getting_started/4-fa_deploy_ws.md). Robot IDs and launch flags for that workspace are in its README after access.

## 3. Payload identification (负载辨识)

负载辨识 is on the Tianji / Rokae path. Run the public Tianji wizard:

:::{code-block} bash
ros2 run marvin_ros2_control tool_dyn_identify_wizard
:::

The program is [`scripts/tool_dyn_identify_wizard.py`](https://github.com/fiveages-sim/marvin-ros2-control/blob/master/scripts/tool_dyn_identify_wizard.py), installed by `CMakeLists.txt` as `tool_dyn_identify_wizard`. The banner is **机械臂负载辨识向导（工具动力学参数辨识 / CCS）**. It connects to the Marvin controller IP, collects a no-load PVT trajectory and then a loaded one, and prints the 10-D tool dynamics (`m, mx, my, mz, ixx, …`). Those values are the HI parameters `left_dyn_param` / `right_dyn_param` on the same README.

On the MIT / OCS2 path, `[kp, kd]` is `default_gains` and `pd_gains`. On-site identification for internal robots is in the private **fa-deploy-ws** README after access (the default branch is typically `fa-w2`).

## 4. Related

- [VR Teleoperation](../5-teleoperation/6-vr_teleop.md)
- [ocs2_arm_controller](../../4-reference/controllers/2-ocs2_arm_controller.md) — MIX detection, `default_gains` / `pd_gains`
- [Controller ROS 2 parameters](../../4-reference/controllers/8-ros2_parameters.md)
- [HighTorque](../../4-reference/hardware/5-ht.md) — `control_mode:=mit`, `joint_kp` / `joint_kd`
- [ARX](../../4-reference/hardware/4-arx.md) — `full_control`, `joint_k_gains` / `joint_d_gains`
- [Marvin](../../4-reference/hardware/6-marvin.md) — `JOINT_IMPEDANCE`, `left_dyn_param` / `right_dyn_param`
- [Isomorphic Teleop](../5-teleoperation/7-isomorphic_teleop.md)
