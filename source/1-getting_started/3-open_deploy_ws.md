# open-deploy-ws Setup

Detailed setup guide for the public `open-deploy-ws` workspace.

## Repository Overview

**URL:** [https://github.com/fiveages-sim/open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws)

`open-deploy-ws` is the public entry point for the FiveAges Sim ecosystem. It provides:

- Pre-configured submodule structure
- Public-only visibility by default
- Lean branches for minimal builds
- GitHub Release `.deb` integration for OCS2 (and optionally common / arms)

Finish [Install Environment](2-install_environment.md) first (ROS apt source → Jazzy + rosdep). Then use **`./init_repo.sh`**. After `colcon build`, `source install/setup.bash` in the launch terminal.

## Cloning

```bash
git clone https://github.com/fiveages-sim/open-deploy-ws.git
cd open-deploy-ws
```

The top-level clone can use HTTPS. Nested remotes in [`.gitmodules`](https://github.com/fiveages-sim/open-deploy-ws/blob/main/.gitmodules) are still `git@github.com:…` (same for nested `.gitmodules` in `arms_ros2_control` and `robot_descriptions`).

### SSH remotes vs HTTPS / `gh`

Machines without an `ssh` binary or GitHub SSH keys fail submodule fetch with `error: cannot run ssh: No such file or directory`.

`git config url.https://github.com/.insteadOf git@github.com:` **alone is not enough** for `git submodule update`. Nested repos read their own `.gitmodules` and invoke `ssh` directly.

The `init_repo.sh` in [open-deploy-ws#8](https://github.com/fiveages-sim/open-deploy-ws/pull/8) rewrites GitHub `git@` URLs in `.gitmodules` to HTTPS, runs `submodule sync` / `update`, then restores `.gitmodules` (so the working tree is not left dirty). That path runs when `ssh` is missing, when public mode has no usable key, or when you pass `--https` / `OPEN_DEPLOY_GIT_HTTPS=1`. After #8 merges — or once you pull an `init_repo.sh` that has these flags — prefer:

:::{code-block} bash
./init_repo.sh --public --ocs2=deb --arms=source --common=source
# force HTTPS even if ssh exists:
./init_repo.sh --public --https --ocs2=deb --arms=source --common=source
:::

`./init_repo.sh --help` lists the rest. Hosts that already have SSH keys (especially for private nested modules) keep the original SSH URLs unless `--https` is set.

**Older `init_repo.sh` (no `--https` / no CLI flags):** clone public remotes over HTTPS, or `gh repo clone <org/name>` with GitHub CLI auth:

:::{code-block} bash
# after the HTTPS clone of open-deploy-ws — matches init defaults (ocs2=deb, arms/common=source)
git clone https://github.com/fiveages-sim/arms_ros2_control.git src/arms_ros2_control
git clone https://github.com/fiveages-sim/robot_descriptions.git src/robot-descriptions
git clone https://github.com/fiveages-sim/robot-descriptions-common.git src/robot-descriptions/common
./scripts/install_core_debs.sh --only ocs2
:::

For **Taku**, clone descriptions on `feature/agilex` instead of the default `main` (see [Taku / `feature/agilex`](#taku--featureagilex)).

## Initialization

```bash
./init_repo.sh
```

With no arguments the menu is interactive (`read` prompts: public/private, then per-module `d`/`s`). What the script does (open-deploy-ws README):

| Menu | Role |
|------|------|
| **1) 初始化工作空间（推荐）** | Nested visibility (`public` / `private`), then per-module `d` (GitHub Release `.deb`) or `s` (source). Then submodule sync, `rosdep install` on source paths, and install chosen debs. |
| **2) 切换模块安装方式** | Switch source ↔ deb for a module (OCS2, arms, common). Cleans conflicting source or uninstalls the matching deb, then re-syncs. |
| **3) 仅安装/更新核心 deb** | Skip Git. `./scripts/install_core_debs.sh --only ocs2` (or `common`, `arms`, comma-separated). |
| **4) 卸载核心 deb** | `./scripts/uninstall_core_debs.sh --only ocs2` |
| **5) 仅运行 rosdep** | `rosdep install --from-paths src --ignore-src -r -y` — no Git, no debs |

You still **colcon-build** after init. Do not start with `git submodule update --init --recursive`; the script already initializes the modules you selected.

### Core module options (OCS2, arms, common)

When prompted (`d=deb`, `s=source`; Enter accepts the default):

| Option | Description | When to Use |
|--------|-------------|-------------|
| `d` | GitHub Release `.deb` | Quick start; no need to build that module from source |
| `s` | Source build | Development, debugging, or contributing |

Defaults in `open-deploy-ws`: OCS2=`d`, arms=`s`, common=`s`. Deb mode does **not** install from packages.ros.org.

### CI / non-interactive init

The CLI is in [open-deploy-ws#8](https://github.com/fiveages-sim/open-deploy-ws/pull/8) (not on `main` until that PR merges). After you pull an `init_repo.sh` that has these flags, a container or CI job with no TTY can run:

```bash
./init_repo.sh --public --ocs2=deb --arms=source --common=source
```

Defaults match the interactive menu: `public`, ocs2=deb, arms=source, common=source. Passing `--public`, `--private`, or any module flag skips keyboard prompts. `./init_repo.sh --help` lists flow switches (`--init`, `--switch`, `--deb-only`, `--rosdep`, …).

| Flag | Environment variable | Meaning |
|------|----------------------|---------|
| `--public` / `--private` | `OPEN_DEPLOY_VISIBILITY` | Nested visibility |
| `--ocs2=deb\|source` | `OPEN_DEPLOY_OCS2` | ocs2 install mode |
| `--arms=deb\|source` | `OPEN_DEPLOY_ARMS` | arms install mode |
| `--common=deb\|source` | `OPEN_DEPLOY_COMMON` | common install mode |
| `--https` | `OPEN_DEPLOY_GIT_HTTPS=1` | Force HTTPS for GitHub submodules |
| `-y` / `--yes` | `OPEN_DEPLOY_YES=1` | Auto-confirm source-tree cleanup |

Command-line flags override the matching env vars.

**Older `init_repo.sh` (interactive only):** use the HTTPS / `gh` public clone fallback above, then `colcon build`. Do not pipe menu answers as the primary path.

### Lean Branches

For a single product, clone the matching branch (README directory names). Use a lean branch when you only need that robot’s packages (smaller clone). **Taku has no lean `open-deploy-ws` branch** — stay on `main` and switch descriptions to `feature/agilex`.

:::{code-block} bash
# Dobot CR5
git clone -b dobot-cr5 git@github.com:fiveages-sim/open-deploy-ws.git dobot_cr5_ws
# ARX Lift 2S (full-body). Acone (dual-arm) is co-debug in this workspace, not a separate platform.
git clone -b arx-lift2s git@github.com:fiveages-sim/open-deploy-ws.git lift2s-ws
# HighTorque Panthera HT
git clone -b panthera-ht git@github.com:fiveages-sim/open-deploy-ws.git ht-deploy-ws
:::

The [open-deploy-ws README](https://github.com/fiveages-sim/open-deploy-ws/blob/main/README.EN.md) also lists `arx-acone`. Then `./init_repo.sh` and `./quick_start.sh` as in that branch’s README. See [ARX Lift 2S](../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md) and [HighTorque Panthera HT](../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md).

## Directory Structure

After initialization:

From the [open-deploy-ws README](https://github.com/fiveages-sim/open-deploy-ws/blob/main/README.EN.md) (hyphen, not `robot_descriptions`):

:::{code-block} none
open-deploy-ws/
├── src/
│   ├── arms_ros2_control/     # controllers / commands / hardware interfaces / shared libs
│   ├── robot-descriptions/    # common / manipulator / humanoid
│   └── ocs2_ros2/             # only if that module is installed as source
├── init_repo.sh
├── submodules_visibility.conf
├── deb_versions.conf
└── scripts/
:::

## Taku / `feature/agilex`

[`open-deploy-ws` `.gitmodules`](https://github.com/fiveages-sim/open-deploy-ws/blob/main/.gitmodules) pins `src/robot-descriptions` to **`main`**. **Taku is not on `main`.**

The in-tree package lives at [`humanoid/Dyna/taku_description`](https://github.com/fiveages-sim/robot_descriptions/tree/feature/agilex/humanoid/Dyna/taku_description) on **`feature/agilex`** ([package README](https://github.com/fiveages-sim/robot_descriptions/blob/feature/agilex/humanoid/Dyna/taku_description/README.md)). After a normal init (or the HTTPS clone of `robot_descriptions` on `main`):

:::{code-block} bash
cd src/robot-descriptions
git fetch origin
git checkout feature/agilex
# common is required (sensor_models / robot_common_launch)
git clone https://github.com/fiveages-sim/robot-descriptions-common.git common
# or, if SSH works: git submodule update --init common
:::

If you are starting from a clean HTTPS tree, clone descriptions on that branch in one step: `git clone -b feature/agilex https://github.com/fiveages-sim/robot_descriptions.git src/robot-descriptions`.

Verified launch keys from that package README (`robot:=taku` → `taku_description`):

:::{code-block} bash
colcon build --packages-up-to taku_description sensor_models --symlink-install
source install/setup.bash
ros2 launch robot_common_launch humanoid.launch.py robot:=taku
:::

Mock demo with the same `robot:=` key (after descriptions on `feature/agilex`):

:::{code-block} bash
colcon build --packages-up-to ocs2_arm_controller taku_description
source install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=taku hardware:=mock_components enable_gripper:=false
:::

In RViz, set **Fixed Frame** to **`base_link`** (or the coincident `base_footprint`). OCS2 `baseFrame` / markers use `base_link`. There is **no** `hardware:=mock` — the default key is `mock_components`. `hardware:=gz` may need a GPU; mock + RViz is the default verify path.

`ocs2_arm_controller demo.launch.py` uses the same `robot:=<key>` → `{key}_description` lookup. Taku ships `config/ocs2/` and a ros2_control yaml that names `ocs2_arm_controller`, so `robot:=taku` is the same convention — not a special-cased flag.

The description is **inferred** (public Dyna kinematics; not official Dyna specs). That is stated in the package README.

## Empty private directories and `COLCON_IGNORE`

In **public** mode, `./init_repo.sh` skips private nested modules listed in [`submodules_visibility.conf`](https://github.com/fiveages-sim/open-deploy-ws/blob/main/submodules_visibility.conf). Under `src/arms_ros2_control` those placeholders stay empty, including:

- `controller/ocs2_wbc_controller`
- `libraries/lina_planning`
- `libraries/ocs2_humanoid`

Empty private / uninitialized hardware dirs can make `colcon build` fail (colcon still walks them).

The `init_repo.sh` in [open-deploy-ws#8](https://github.com/fiveages-sim/open-deploy-ws/pull/8) writes `COLCON_IGNORE` on uninitialized nested paths (including `hardwares/*` and private visibility entries). A later private init removes that marker before clone. After #8 merges — or once you pull that script — you do not need to `touch` these by hand.

**Older `init_repo.sh`:** drop a `COLCON_IGNORE` file in each empty private dir:

:::{code-block} bash
touch src/arms_ros2_control/controller/ocs2_wbc_controller/COLCON_IGNORE
touch src/arms_ros2_control/libraries/lina_planning/COLCON_IGNORE
touch src/arms_ros2_control/libraries/ocs2_humanoid/COLCON_IGNORE
:::

Other empty nested submodule dirs under `arms_ros2_control` (uninited hardware interfaces) get the same treatment if colcon errors on that path: `touch <empty-dir>/COLCON_IGNORE`.

## Building

`./init_repo.sh` already runs `rosdep install` on source paths. You still need to colcon-build:

```bash
colcon build --symlink-install
```

Then `source install/setup.bash` in the terminal you launch from. The README does not install a workspace env script besides `./init_repo.sh`.

### Partial Build

Build only specific packages:

```bash
# Just descriptions
colcon build --packages-select robot-descriptions-dobot

# Up to a specific package
colcon build --packages-up-to ocs2_arm_controller
```

## Supported Robots

| Robot | Description Package | Hardware Interface | Notes |
|-------|--------------------|--------------------|-------|
| Dobot CR5 | robot-descriptions-dobot | dobot-cr-ros2-control | `dobot-cr5` branch |
| ARX X5 | robot-descriptions-arx | arx-ros2-control | Co-debug in `arx-lift2s` |
| **Acone** / **AC One** | robot-descriptions-arx | arx-ros2-control | **Dual-arm** (not Lift 2S) |
| **ARX Lift 2S** | robot-descriptions-arx | arx-ros2-control | **Full-body** (arms + lift + chassis); branch `arx-lift2s` |
| Galbot | robot-descriptions-galbot | (varies) | Simulation-oriented |
| **HighTorque Panthera HT** | `panthera_ht_description` | ht-ros2-control | Dual-arm; branch `panthera-ht`; umbrella path `manipulator/HighTorque/panthera_ht_description` |
| **Taku** (Dyna / DVT1) | `taku_description` | mock / gz / isaac in package xacro | In-tree on `robot_descriptions` **`feature/agilex`** at `humanoid/Dyna/taku_description`; `robot:=taku` on `humanoid.launch.py` |
| Quadruped | robot-descriptions-quadruped | unitree-ros2-control | Simulation-oriented |

```{admonition} Real Hardware Deployment
:class: tip

**ARX Lift 2S** (方舟无限) is the full-body mobile manipulator. **Acone** / **AC One** is **dual-arm**. **HighTorque Panthera HT** (高擎) is a dual-arm manipulator. See [ARX Lift 2S](../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md), [HighTorque Panthera HT](../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md), and [Go to Real Hardware](../2-how_to/6-deployment/9-go_real_hardware/0-index.md).
```

## Launch Examples

### Mock Hardware Demo

```bash
source install/setup.bash
ros2 launch ocs2_arm_controller demo.launch.py
```

`demo.launch.py` defaults: `robot:=cr5`, `hardware:=mock_components`. There is **no** `hardware:=mock`.

### With Specific Robot

```bash
# Acone (dual-arm, not Lift 2S). Omit hardware:= to keep mock_components.
ros2 launch ocs2_arm_controller demo.launch.py robot:=arx_acone

# Taku (descriptions on feature/agilex). RViz Fixed Frame: base_link (or base_footprint).
ros2 launch ocs2_arm_controller demo.launch.py robot:=taku hardware:=mock_components enable_gripper:=false
```

Taku visualize path (package README): `ros2 launch robot_common_launch humanoid.launch.py robot:=taku`. See [Taku / `feature/agilex`](#taku--featureagilex) for the build and Fixed Frame notes.

### End-effector (`type`)

Not `gripper:=`. Symmetric: `type:=<eef_key>`. Different L/R: `left_type:=` / `right_type:=` together (**do not pass `type:=`** then). Profile `defaults.end_effectors` is used when `use_profile_eef:=true` (default). See [robot_common_launch](../4-reference/descriptions/2-common.md).

:::{code-block} bash
ros2 launch ocs2_arm_controller demo.launch.py \
  robot:=<robot_name> \
  use_profile_eef:=false \
  left_type:=rg75 right_type:=linkerhand_o7
:::

## Adding Robot Descriptions

To add a new robot to your workspace:

Prefer `./init_repo.sh` so nested modules under `src/robot-descriptions/` match `submodules_visibility.conf`. Do not `git submodule update --init --recursive`. Then `colcon build` the packages you need.

## Submodule Management

Prefer `./init_repo.sh` (menu 1 or 2) over a recursive submodule init. Check status with `git submodule status`. To update a specific source tree you already initialized, pull that module then rebuild.

## GitHub Release `.deb` vs Source Matrix

| Component | GitHub Release `.deb` | Source Path |
|-----------|----------------------|-------------|
| OCS2 | `ros-jazzy-ocs2` ([releases](https://github.com/legubiao/ocs2_ros2/releases)) | `src/ocs2_ros2` |
| Common descriptions | `ros-jazzy-robot-descriptions-common` ([releases](https://github.com/fiveages-sim/robot-descriptions-common/releases)) | `src/robot-descriptions/common` |
| arms_ros2_control | `ros-jazzy-arms-ros2-control` (optional; [releases](https://github.com/fiveages-sim/arms_ros2_control/releases)) | `src/arms_ros2_control` |

Check `deb_versions.conf` for the GitHub repos and release tags used by `scripts/install_core_debs.sh`. These packages are not in the ROS apt index.

## Common Issues

### Submodules Empty

Re-run `./init_repo.sh` (menu 1). Do not use `git submodule update --init --recursive` as the primary recovery path.

### `cannot run ssh` / Access Denied to Submodule

`.gitmodules` URLs are SSH. `insteadOf` HTTPS rewrite alone does not fix `git submodule update`. After [open-deploy-ws#8](https://github.com/fiveages-sim/open-deploy-ws/pull/8) (or once you pull that `init_repo.sh`), the script rewrites `.gitmodules` to HTTPS for the fetch and restores it afterwards — use `--https` / `OPEN_DEPLOY_GIT_HTTPS=1` to force that. Older scripts: HTTPS / `gh` clone fallback above.

Some nested modules are private. In `open-deploy-ws`, only public nested modules should be required. If you see access errors:

1. Check you're on the correct branch (not accidentally on a private branch)
2. Verify the submodule is listed as public in `submodules_visibility.conf`
3. For empty private dirs that break colcon on an older init, add `COLCON_IGNORE` as above

### Build Fails with numpy

```bash
pip install 'numpy<2'
```

### CAN Interface Rename Needed

For CAN-based robots, you may need to rename the interface:

```bash
sudo ip link set can0 down
sudo ip link set can0 name <expected_name>
sudo ip link set <expected_name> up
```

## Next Steps

- [Run mock demo](../2-how_to/1-basic_operations/1-run_mock_demo.md)
- [Switch robots](../2-how_to/1-basic_operations/2-switch_robot.md)
- [ARX Lift 2S](../2-how_to/6-deployment/9-go_real_hardware/1-arx_lift2s.md)
- [HighTorque Panthera HT](../2-how_to/6-deployment/9-go_real_hardware/2-panthera_ht.md)
- [Gazebo simulation](../2-how_to/2-simulation/3-gazebo_sim.md)
