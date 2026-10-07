# VLA collect / train / deploy

For teams that collect motion data (VR or sim), then train and deploy a VLA-style policy. This page is a **collection and stack** path. Training and policy serving are not documented here yet.

## 1. Collect with VR teleop

1. Bring up the robot (mock, sim, or real) from [Go to Real Hardware](../2-how_to/6-deployment/9-go_real_hardware/0-index.md) or [Run Mock Demo](../2-how_to/1-basic_operations/1-run_mock_demo.md).
2. [VR Teleop](../2-how_to/5-teleoperation/6-vr_teleop.md) — `./run.sh vr` or `./run.sh vr-xrt` from [fa-py-libraries](../4-reference/python_apps/2-fa_py_libraries.md).
3. Optional bags: the fa-py-libraries README lists `./run.sh vr-record` / `./run.sh vr-playback` for `/teleop/*`.

Pico Enterprise vs consumer stays on the VR how-to.

## 2. Whole-body control with waist

Whole-body here is **全身控制** (`full_body.launch.py` / Lift 2S **full body**), not a separate waist-only product.

1. [分体控制 vs 全身控制](../3-concepts/7-split_vs_wbc.md) — `split_body.launch.py` vs `full_body.launch.py`.
2. [ARX Lift 2S](../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md) — `./quick_start.sh` menu: **full body**.
3. [ocs2_wbc_controller](../4-reference/controllers/3-ocs2_wbc.md) — private submodule; public loader is `full_body.launch.py`. Topics and FSM values: that package README after access.
4. Waist **joint** commands on the split / `basic_joint_controller` side: [basic_joint_controller](../4-reference/controllers/7-basic_joint_controller.md) (`waist_lifting_*`, `waist_turning_command`). How-to: [Use basic_joint_controller](../2-how_to/4-controllers/11-basic_joint.md).

Internal FA wheeled-arm humanoids: [fa-deploy-ws Setup](../1-getting_started/4-fa_deploy_ws.md) after access.

## 3. Arm force control and load identification

There is **no** dedicated force-control or **load-identification** how-to in this docs set (no load-ID CLI, no identified-inertia file format).

Closest verified pages:

- [ocs2_arm_controller](../4-reference/controllers/2-ocs2_arm_controller.md) — YAML `force_gains`; control mode is position-only vs force/`MIX` when `position`, `velocity`, `effort`, `kp`, `kd` are all present.
- [Isomorphic Teleop](../2-how_to/5-teleoperation/7-isomorphic_teleop.md) — `mode`: `position` / `mit` / `effort`; master `feedback` includes `effort` (HighTorque Panthera HT).
- Hardware plugins: [Public hardware interfaces](../4-reference/hardware/1-public_hi.md).

For parameters not listed there, use the package README linked from those pages.

## 4. Sim collection (optional)

Isaac USD → interface → composer → LeRobot **record/export** (not training): [Synthetic Data](../2-how_to/7-synthetic_data/0-index.md).

[LeRobot Record and Export](../2-how_to/7-synthetic_data/3-record_export.md) stops at the dataset on disk.

## Not in this docs set yet

- VLA **training** (optimizer, dataset mix, checkpoint format)
- VLA **deploy / inference** on the robot (policy node, runtime flags)

When those land, they should get their own How-To. Until then, collect with the paths above and keep training in the project that owns the model.
