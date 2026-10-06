# Architecture

This page describes the layered architecture of the FiveAges Sim ecosystem and how components depend on each other.

## Layer Diagram

```{mermaid}
flowchart TB
  subgraph entry [Entry Workspaces]
    ODW["open-deploy-ws<br/>public quick-start"]
    FDW["fa-deploy-ws<br/>private FA robots"]
    DCW["dexcap_teleop_ws<br/>DexCap teleop"]
    FAI["FaSim-Isaac<br/>Isaac asset + jazzy_ws"]
  end

  subgraph L1 [L1 Descriptions]
    RD["robot_descriptions<br/>public umbrella"]
    RDC["robot-descriptions-common"]
    RDF["robot-descriptions-fiveages<br/>private umbrella"]
    BRAND["brand desc:<br/>dobot / arx / galbot / ht / quadruped<br/>tianji / rokae / ubtech / …"]
  end

  subgraph L2 [L2 Hardware Interfaces]
    HI["*-ros2-control<br/>public + private HIs<br/>nested under arms_ros2_control"]
  end

  subgraph L3 [L3 Controllers + MPC]
    ARMS["arms_ros2_control<br/>ocs2_arm / teleop / gripper"]
    WBC["ocs2-wbc-controller<br/>private"]
    OH["ocs2-humanoid / ocs2_wheel_humanoid<br/>private"]
    OCS2["legubiao/ocs2_ros2<br/>deb ros-jazzy-ocs2"]
  end

  subgraph L4 [L4 Simulation]
    GZ["Gazebo Harmonic<br/>via arms launches"]
    USD["robot_usds + gitmodules<br/>Gen1/2/3 · Galbot · Ubtech"]
    ENV["FaSim: fiveages-env-usds<br/>+ fa-project-usd sibling"]
  end

  subgraph L5 [L5 Teleop / Apps / Python]
    PY["fa-py-libraries<br/>interface · viser · vr_pose_publisher"]
    TEL["drag / DexCap / wuji glove / vive / teleop-joint-mapper"]
    APP["lerobot_ros2 · robot_action_composer · HUG"]
  end

  ODW --> ARMS
  ODW --> RD
  ODW --> OCS2
  FDW --> RDF
  FDW --> ARMS
  FDW --> OCS2
  RD --> RDC
  RD --> BRAND
  RDF --> BRAND
  ARMS --> HI
  ARMS --> WBC
  ARMS --> OH
  ARMS --> OCS2
  FAI --> USD
  FAI --> ENV
  ARMS --> GZ
  ARMS --> USD
  PY --> ARMS
  TEL --> ARMS
  APP --> PY
  DCW --> TEL
```

## Layer Descriptions

### Entry Workspaces

These are the starting points for building and running the stack:

| Workspace | Purpose | Visibility |
|-----------|---------|------------|
| `open-deploy-ws` | Public quick-start with mock/sim demos | Public |
| `fa-deploy-ws` | Internal workspace for FA robots | Private |
| `dexcap_teleop_ws` | DexCap teleoperation deployment | Private |
| `FaSim-Isaac` | Isaac Sim assets and optional jazzy_ws | Public |

### L1: Descriptions

Robot descriptions define the URDF/xacro models, visual meshes, and ros2_control hardware configurations:

- **robot_descriptions** — Public umbrella that aggregates brand-specific packages
- **robot-descriptions-common** — Shared grippers, hands, sensors, and launch utilities
- **robot-descriptions-fiveages** — Private umbrella for FA humanoids
- **Brand packages** — Per-vendor descriptions (dobot, arx, galbot, etc.)

### L2: Hardware Interfaces

ROS 2 control plugins that communicate with physical or simulated hardware:

- Public HIs: `arx-ros2-control`, `dobot-cr-ros2-control`, `unitree-ros2-control`, etc.
- Private HIs: `rokae-ros2-control`, `eyou-ros2-control`, `wuji-ros2-control`, etc.

### L3: Controllers + MPC

Motion planning and control algorithms:

- **arms_ros2_control** — Main controller package with OCS2 arm controller, gripper, and teleop plugins
- **ocs2_ros2** — OCS2 MPC library (GitHub Release `.deb`: `ros-jazzy-ocs2`)
- **ocs2-wbc-controller** — Whole-body control for humanoids (private)
- **ocs2-humanoid** — Wheel-humanoid specific library (private)

### L4: Simulation

Simulation backends and assets:

- **Gazebo Harmonic** — Integrated via launch files in `arms_ros2_control`
- **robot_usds** — USD assets for Isaac Sim (Gen1/2/3, Galbot, Ubtech)
- **FaSim environments** — Scene assets via `fiveages-env-usds` and `fa-project-usd`

### L5: Teleop / Apps / Python

High-level applications and teleoperation:

- **fa-py-libraries** — Python utilities including ros2_robot_interface, viser, vr_pose_publisher
- **Teleop systems** — drag teaching, DexCap, wuji glove, vive tracker
- **Applications** — lerobot_ros2, robot_action_composer, HUG

## Dependency Rule of Thumb

:::{code-block} none
Descriptions (URDF + ros2_control YAML)
    ↓
Hardware Interface plugins
    ↓
Controllers (arm MPC / WBC)
    ↓
Simulation backends OR Real hardware
    ↓
Teleop / Apps (same topic/FSM contracts)
:::

When adding a new robot:
1. Create or extend a description package
2. Ensure the hardware interface plugin exists
3. Configure the controller parameters
4. Test in mock → simulation → real hardware
