# Repository Map

This page lists all repositories in the FiveAges Sim ecosystem, organized by architectural layer.

## Legend

- **[P]** = Public repository
- **[I]** = Private/internal repository
- **[X]** = External repository (not in fiveages-sim org)

## Entry Workspaces

| Repository | Visibility | Purpose |
|------------|------------|---------|
| [open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws) | [P] | Public quick-start workspace |
| fa-deploy-ws | [I] | Internal deployment for FA robots |
| dexcap_teleop_ws | [I] | DexCap teleoperation workspace |
| [FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac) | [P] | Isaac Sim assets and jazzy_ws |

## L1: Descriptions

### Umbrella Repositories

| Repository | Visibility | Purpose |
|------------|------------|---------|
| [robot_descriptions](https://github.com/fiveages-sim/robot_descriptions) | [P] | Public umbrella for all descriptions |
| [robot-descriptions-common](https://github.com/fiveages-sim/robot-descriptions-common) | [P] | Shared grippers, hands, sensors |
| robot-descriptions-fiveages | [I] | Private umbrella for FA robots |

### Brand-Specific (Public)

| Repository | Visibility | Robots |
|------------|------------|--------|
| [robot-descriptions-dobot](https://github.com/fiveages-sim/robot-descriptions-dobot) | [P] | Dobot CR series |
| [robot-descriptions-arx](https://github.com/fiveages-sim/robot-descriptions-arx) | [P] | ARX X5, ACone, Lift2S |
| [robot-descriptions-galbot](https://github.com/fiveages-sim/robot-descriptions-galbot) | [P] | Galbot mobile manipulators |
| [robot-descriptions-ht](https://github.com/fiveages-sim/robot-descriptions-ht) | [P] | HT Panthera |
| [robot-descriptions-quadruped](https://github.com/fiveages-sim/robot-descriptions-quadruped) | [P] | Quadruped robots |

### Brand-Specific (Private)

| Repository | Visibility | Robots |
|------------|------------|--------|
| robot-descriptions-tianji | [I] | Tianji M6, M6S, M20S |
| robot-descriptions-rokae | [I] | Rokae arms |
| robot-descriptions-fairino | [I] | Fairino arms |
| robot-descriptions-gento | [I] | Gento robots |
| robot-descriptions-ubtech | [I] | Ubtech humanoids |
| agibot-g2-description | [I] | Agibot G2 |
| fa-w2-description | [I] | FA W2 humanoid |
| fa-w2r-description | [I] | FA W2R humanoid |
| fa-s2-description | [I] | FA S2 humanoid |
| fa-s2r-description | [I] | FA S2R humanoid |
| fa-w2-components | [I] | Shared W2 components |

## L2: Hardware Interfaces

### Public

| Repository | Visibility | Hardware |
|------------|------------|----------|
| [arx-ros2-control](https://github.com/fiveages-sim/arx-ros2-control) | [P] | ARX CAN interface |
| [dobot-cr-ros2-control](https://github.com/fiveages-sim/dobot-cr-ros2-control) | [P] | Dobot TCP interface |
| [unitree-ros2-control](https://github.com/fiveages-sim/unitree-ros2-control) | [P] | Unitree SDK2 |
| [ht-ros2-control](https://github.com/fiveages-sim/ht-ros2-control) | [P] | HT Panthera serial |
| [marvin-ros2-control](https://github.com/fiveages-sim/marvin-ros2-control) | [P] | Tianji + EE matrix |
| [modbus-ros2-control](https://github.com/fiveages-sim/modbus-ros2-control) | [P] | RS485 grippers |
| [can-ros2-control](https://github.com/fiveages-sim/can-ros2-control) | [P] | CAN/CANFD hands |
| [juxie-ros2-control](https://github.com/fiveages-sim/juxie-ros2-control) | [P] | JX CAN FD |

### Private

| Repository | Visibility | Hardware |
|------------|------------|----------|
| rokae-ros2-control | [I] | Rokae arms |
| eyou-ros2-control | [I] | CANopen harmonic |
| eyou_canfd_ros2_control | [I] | CAN FD PHU |
| inex-ros2-control | [I] | iNexus + LinkerHand |
| wuji-ros2-control | [I] | Wuji Hand2 Ethernet |
| dexcap-ros2-control | [I] | DexCap V4 |
| fairino-ros2-control | [I] | Fairino SDK |

## L3: Controllers

| Repository | Visibility | Purpose |
|------------|------------|---------|
| [arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control) | [P] | OCS2 arm controller, teleop plugins |
| [legubiao/ocs2_ros2](https://github.com/legubiao/ocs2_ros2) | [X] | OCS2 MPC library (branch: ros2) |
| ocs2-wbc-controller | [I] | Whole-body control |
| ocs2-humanoid | [I] | Wheel-humanoid library |
| lina_planning | [I] | Trajectory primitives |

## L4: Simulation

| Repository | Visibility | Purpose |
|------------|------------|---------|
| [robot_usds](https://github.com/fiveages-sim/robot_usds) | [P] | Isaac USD superproject |
| [galbot-usds](https://github.com/fiveages-sim/galbot-usds) | [P] | Galbot USD assets |
| [fiveages-env-usds](https://github.com/fiveages-sim/fiveages-env-usds) | [P] | Environment USD assets |
| fiveages-gen1-robot-usds | [I] | Gen1 USD |
| fiveages-gen2-robot-usds | [I] | Gen2 USD |
| fiveages-gen3-robot-usds | [I] | Gen3 USD |
| fa-project-usd | [I] | FaSim project assets |

## L5: Teleop and Applications

### Teleop

| Repository | Visibility | Purpose |
|------------|------------|---------|
| [drag_teleop_controller](https://github.com/fiveages-sim/drag_teleop_controller) | [P] | Drag teaching |
| vr_pose_publisher | [I] | VR pose bridge |
| teleop-joint-mapper | [I] | DexCap→M6 mapper |
| wuji_glove_teleop | [I] | Glove teleoperation |
| vive_tracker_teleop | [I] | Vive tracker EE pose |

### Python Libraries

| Repository | Visibility | Purpose |
|------------|------------|---------|
| [fa-py-libraries](https://github.com/fiveages-sim/fa-py-libraries) | [P] | Python utilities umbrella |
| [ros2_robot_interface](https://github.com/fiveages-sim/ros2_robot_interface) | [P] | High-level robot API |
| [ros2-viser](https://github.com/fiveages-sim/ros2-viser) | [P] | Viser visualization |
| [lerobot_ros2](https://github.com/fiveages-sim/lerobot_ros2) | [P] | LeRobot ↔ ROS 2 monorepo |
| [robot_action_composer](https://github.com/fiveages-sim/robot_action_composer) | [P] | Task-queue YAML / motion generation |
| [wuji-retargeting](https://github.com/fiveages-sim/wuji-retargeting) | [P] | Hand retargeting |
| HUG | [I] | Grasp inference |

## Excluded from This Documentation

The following repositories are **not** documented here:

- `arms_moveit` — MoveIt PoC, not actively maintained
- `maniskill_models` — ManiSkill PoC, not actively maintained
- `.github` — Organization configuration
- Navigation/data repositories: `internnav_w2`, `LightNav-0_W2`, `data-collector-platform`, `internnav_arx_lift2s`
- Stale private repositories: `vla_http_bridge`, `Discoverse_socket`, `fiveages_descriptions`, `ACT_socket`, `act_Discoverse_connector`, `robocasa`, `lerobot-sim2real-so101`, `marvin-usds`, `ubtech-ros2-control`
