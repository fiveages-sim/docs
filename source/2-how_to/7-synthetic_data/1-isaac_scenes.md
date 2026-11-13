# Isaac Scenes and USD

Synthetic datagen in this stack is an **Isaac Sim** line. Gazebo is not part of this pipeline.

Scene assets live in **FaSim-Isaac**. Robot USD files are the **robot_usds** superproject (FaSim submodule `robots/`). Environment and private project USDs sit beside that tree, not inside it.

## Prepare the workspace

Clone [FaSim-Isaac](https://github.com/fiveages-sim/FaSim-Isaac), run `./init.sh`, then `./run.sh`. The menu, flags, and first ROS 2 connection are on [Isaac Sim](../2-simulation/4-isaac_sim.md). Do not hand-assemble the tree.

The datagen example README ([`examples/IsaacSim/README.md`](https://github.com/fiveages-sim/lerobot_ros2/blob/main/examples/IsaacSim/README.md) on `main`) still lists Ubuntu 24.04, ROS 2 Jazzy, and Isaac Sim 6.0. Keep path and version in FaSim config. The FaSim fallback list (`6.2.0`, `6.1.0`, `6.0.1` in `config/fa_sim.conf`) is newer than that 6.0 line.

Open the target robot or scene USD in Isaac and run the simulation. Enable Isaac’s ROS 2 simulation-control and prim services as in the [NVIDIA Isaac ROS 2 workspace docs](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_ros.html#setup-ros-2-workspaces) linked from the example README (`/set_simulation_state`, prim service for object pose).

Workspace layout, Kit extensions, and in-process 运控: [FaSim-Isaac](../../4-reference/simulation/2-fasim_isaac.md).

## Which tree to open

| Tree | Role | Reference |
|------|------|-----------|
| `robots/` → [robot_usds](https://github.com/fiveages-sim/robot_usds) | Robot USD, including FiveAges Gen1/Gen2 gitlinks and in-tree models such as Taku | [robot_usds](../../4-reference/simulation/3-robot_usds.md) |
| `environment/fiveages_env/` → [fiveages-env-usds](https://github.com/fiveages-sim/fiveages-env-usds) | Public scenes (`static/`, `moveable/`, `articulation/`, `background/`, `tasks/`) | [Environment assets](../../4-reference/simulation/5-env_assets.md) |
| `environment/fa-project-usd/` → [fa-project-usd](https://github.com/fiveages-sim/fa-project-usd) | Private project scenes. `robot.yaml` / `task_configs/` / maps are on branch `feature/sinopec-test-tube-picking`, not on `main` | [fa-project-usd](../../4-reference/simulation/5-env_assets.md#fa-project-usd) |

If you use robot_usds **outside** FaSim, put `environment/fiveages_env` next to `robots/` so scene USDs can reference it. `fa-project-usd` is a project scene tree, not a public robot model. Product names on this page follow the public robot_usds gallery text. Keep camera rigs in the scene USD.

## Next on the pipeline

With Isaac running and ROS 2 topics/services up, motion and recording talk to the robot through **ros2_robot_interface**, orchestrated by **robot_action_composer**. Continue at [Interface and orchestration](2-orchestration.md).
