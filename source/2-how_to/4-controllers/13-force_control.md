# Force control and compliance

On a real arm, use one of the two paths below so the arm can give under contact. **Payload identification (负载辨识)** belongs to the **vendor-impedance** path (Tianji / Rokae).

| Path | Robots | Who provides compliance | What the controller commands |
|------|--------|-------------------------|------------------------------|
| **MIT-mode force control** | **HighTorque** (高擎) **Panthera HT**; **ARX** (方舟无限) arms | Controller + hardware interface in MIT / `full_control` (pos + vel + effort; stiffness on the HI) | Force-capable / MIX when the interfaces allow it |
| **Vendor joint impedance** | **Tianji** (天玑); **Rokae** (珞石) | Vendor stack, exposed on the hardware interface | **Position only** |

## MIT-mode force control (Panthera HT / ARX)

Use this path on **Panthera HT** and **ARX** arms. The hardware interface must run a **force-capable** MIT configuration; the controller then tracks the pose target with that mix of position / velocity / effort. VR teleop is one client of this path: [VR Teleoperation](../5-teleoperation/6-vr_teleop.md).

**HighTorque Panthera HT** — [ht-ros2-control README](https://github.com/fiveages-sim/ht-ros2-control/blob/main/README.md):

- HI `control_mode:=mit` (default; older name `full_control` still accepted)
- The driver sends position + velocity + effort + kp/kd (`pos_vel_tqe_kp_kd`)
- Stiffness is HI parameters `joint_kp` / `joint_kd` (rqt / `ros2 param`), **not** kp/kd command interfaces
- Other documented HI modes: `effort` (torque only), `position` (position only)

**ARX arms** — [arx-ros2-control README](https://github.com/fiveages-sim/arx-ros2-control/blob/main/README.md):

- Arms support only `full_control` / MIT MIX. Other `control_mode` values in xacro are warned and ignored
- `write()` always sends position + velocity + effort
- MIT `kp` / `kd` come from HI `joint_k_gains` / `joint_d_gains` (no kp/kd command interface)
- README mapping: OCS2 trajectory → position; OCS2 `future_input` → velocity; OCS2 effort → gravity / static feedforward torque

**Controller** — [ocs2_arm_controller README — Interface Configuration](https://github.com/fiveages-sim/arms_ros2_control/blob/main/controller/ocs2_arm_controller/README.md):

- Mode is **auto-detected** from the robot config (no extra launch flag named `force:=`)
- Position-only: command `position`; state `position` + `velocity`
- Force / MIX: command `position`, `velocity`, `effort`, `kp`, `kd` all present. `[kp, kd]` is `default_gains` (HOME / HOLD) and `pd_gains` (OCS2 state), **Startup only**. The older name `force_gains` is not a parameter
- ARX documents OCS2 MIX as pos + vel + effort with kp/kd on the HI. HT notes that when kp/kd are **not** command interfaces, OCS2 may stay in position mode; gravity compensation then uses `ht_gravity_compensation` or larger `joint_kp` (same HT README)

Bring the robot up with the lean-branch `./quick_start.sh` / `hardware:=real` path on [HighTorque Panthera HT](../6-deployment/9-go_real_hardware/2-panthera_ht.md) or [ARX Lift 2S](../6-deployment/9-go_real_hardware/1-arx_lift2s.md). For the headset, follow [VR Teleoperation](../5-teleoperation/6-vr_teleop.md).

Master–slave `mode:=mit` / `effort` on Panthera HT is [Isomorphic Teleop](../5-teleoperation/7-isomorphic_teleop.md).

## Vendor joint impedance (Tianji / Rokae)

Use this path on **Tianji** (天玑) and **Rokae** (珞石). The controller only sends **joint position**. Joint impedance / compliance is the **vendor** feature, switched on the hardware interface.

**Tianji** — [marvin-ros2-control README](https://github.com/fiveages-sim/marvin-ros2-control/blob/master/README.md):

- Command interfaces: joint **`position` only**. State: `position`, `velocity`, `effort`
- Runtime `ctrl_mode`: `POSITION` / `JOINT_IMPEDANCE` / `CART_IMPEDANCE` / `POWER_OFF`
- Joint impedance gains: `joint_k_gains` / `joint_d_gains` (7 values). Cartesian: `cart_k_gains` / `cart_d_gains`
- Example: `ros2 param set /<hardware_node> ctrl_mode JOINT_IMPEDANCE`

**Rokae** — same pattern (position commands; compliance in the vendor HI). Parameter names are in the private `rokae-ros2-control` README after access. Overview: [Hardware Interfaces](../../4-reference/hardware/0-index.md).

Internal FA robots that use Tianji / Rokae arms live in [fa-deploy-ws Setup](../../1-getting_started/4-fa_deploy_ws.md). Extra robot IDs and launch flags are in that workspace README after access.

## Payload identification (负载辨识)

负载辨识 is **only** on the Tianji / Rokae (vendor impedance) path. The MIT / OCS2 side uses `default_gains` / `pd_gains` for `[kp, kd]`. It does not run this wizard.

**Public, verified Tianji wizard** (semi-automatic tool-dynamics ID on CCS): [marvin-ros2-control `scripts/tool_dyn_identify_wizard.py`](https://github.com/fiveages-sim/marvin-ros2-control/blob/master/scripts/tool_dyn_identify_wizard.py), installed as `ros2 run marvin_ros2_control tool_dyn_identify_wizard` (`CMakeLists.txt` `install(PROGRAMS … RENAME tool_dyn_identify_wizard)`).

The wizard banner is **机械臂负载辨识向导（工具动力学参数辨识 / CCS）**. It connects to the Marvin controller IP, collects no-load then loaded PVT trajectories, and prints 10-D tool dynamics (`m, mx, my, mz, ixx, …`). Those values match HI parameters `left_dyn_param` / `right_dyn_param` on the same README.

There is **no** public `open-deploy-ws` payload-ID flow. Internal on-site Tianji payload identification is in the private **fa-deploy-ws** README after access (default branch is typically `fa-w2`). Use that README’s script names — they are not listed here.

## Related

- [VR Teleoperation](../5-teleoperation/6-vr_teleop.md)
- [ocs2_arm_controller](../../4-reference/controllers/2-ocs2_arm_controller.md) — MIX detection, `default_gains` / `pd_gains`
- [Controller ROS 2 parameters](../../4-reference/controllers/8-ros2_parameters.md)
- [HighTorque](../../4-reference/hardware/5-ht.md) — `control_mode:=mit`, `joint_kp` / `joint_kd`
- [ARX](../../4-reference/hardware/4-arx.md) — `full_control`, `joint_k_gains` / `joint_d_gains`
- [Marvin](../../4-reference/hardware/6-marvin.md) — `JOINT_IMPEDANCE`, `left_dyn_param` / `right_dyn_param`
- [Isomorphic Teleop](../5-teleoperation/7-isomorphic_teleop.md)
