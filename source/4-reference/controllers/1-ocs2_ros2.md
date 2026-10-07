# ocs2_ros2

OCS2 (Optimal Control for Switched Systems) ROS 2 port.

**Repository:** [legubiao/ocs2_ros2](https://github.com/legubiao/ocs2_ros2) (branch: `ros2`)

## Purpose

OCS2 is a Model Predictive Control (MPC) library providing:
- Real-time trajectory optimization
- Constraint handling
- Multiple robot support (arms, mobile bases, quadrupeds)

## Installation

OCS2 is **not** in the ROS apt index. Install (or switch source ↔ deb) through the deploy workspace:

:::{code-block} bash
cd ~/open-deploy-ws   # or fa-deploy-ws
./init_repo.sh
# 1) init: choose d (deb) or s (source) for OCS2
# 2) 切换模块安装方式 — change an existing OCS2 path
# 3) ./scripts/install_core_debs.sh --only ocs2
# 4) ./scripts/uninstall_core_debs.sh --only ocs2
:::

Default in `open-deploy-ws` is OCS2=`d` (GitHub Release `.deb` via `scripts/install_core_debs.sh`). Then `colcon build`.

:::{admonition} Manual fallback
:class: note

Without a deploy workspace: download `ros-jazzy-ocs2_*_<arch>.deb` from [ocs2_ros2 Releases](https://github.com/legubiao/ocs2_ros2/releases) and `sudo dpkg -i`. For source, clone branch `ros2` into `src/` and `colcon build --packages-up-to ocs2`.
:::

## Usage

OCS2 is typically used through higher-level controllers like `ocs2_arm_controller`. Direct usage:

### Include in Package

```text
find_package(ocs2_core REQUIRED)
find_package(ocs2_mpc REQUIRED)
find_package(ocs2_robotic_tools REQUIRED)

target_link_libraries(my_controller
  ocs2_core::ocs2_core
  ocs2_mpc::ocs2_mpc
)
```

## Examples

The repository includes example packages:

| Example | Description |
|---------|-------------|
| `ocs2_double_integrator` | Simple 1D system |
| `ocs2_cartpole` | Classic control example |
| `ocs2_ballbot` | Mobile robot example |
| `ocs2_mobile_manipulator` | Arm + base |
| `ocs2_legged_robot` | Quadruped |

### Run Double Integrator Example

```bash
ros2 launch ocs2_double_integrator double_integrator.launch.py
```

## Key Concepts

### MPC Problem

OCS2 solves optimal control problems:

- **State**: Robot configuration (positions, velocities)
- **Input**: Control commands
- **Cost**: Tracking error + control effort
- **Constraints**: Joint limits, collision avoidance

### DDP Solver

Uses Differential Dynamic Programming:
- Forward pass: Simulate trajectory
- Backward pass: Compute optimal gains
- Iterate until convergence

### Real-time Operation

The MPC runs in a separate thread:
- Configurable update rate
- Latest solution always available
- Handles timing variations

## Configuration

### MPC Parameters

```yaml
mpc:
  dt: 0.01           # MPC timestep
  horizon: 1.0       # Prediction horizon (seconds)
  iterations: 1      # DDP iterations per update
```

### Task Configuration

```yaml
task:
  targetTrackingWeight: [100, 100, 100, 10, 10, 10]  # Position, orientation
  inputWeight: [1, 1, 1, 1, 1, 1]                     # Control effort
```

## Related Packages

| Package | Purpose |
|---------|---------|
| `ocs2_core` | Core algorithms |
| `ocs2_mpc` | MPC implementation |
| `ocs2_robotic_tools` | Robot utilities |
| `ocs2_pinocchio_interface` | Pinocchio integration |

## References

- [OCS2 Documentation](https://leggedrobotics.github.io/ocs2/)
- [Original OCS2 Repository](https://github.com/leggedrobotics/ocs2)
