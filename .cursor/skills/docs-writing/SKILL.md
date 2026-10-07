---
name: docs-writing
description: >-
  Write and edit fiveages-sim/docs without fabricating APIs, scripts, or
  private-repo trees. Use when adding or changing Sphinx/MyST pages, zh_CN
  .po files, Overview / How-To / Concepts / Reference, or when tempted to
  list unverified flags. 文档撰写、不要编造、do not invent、Sphinx、sphinx-intl、
  reader-facing vs agent guidelines.
---

# Docs writing (fiveages-sim/docs)

Constraints for **authors and agents**. Put them here — **not** in reader-facing Sphinx pages.

Reader pages live under `source/`. They must sound like product documentation. Phrases such as “Do not invent…”, “This page does not invent…”, “do not treat this list as a substitute”, or “不要编造…” belong **only** in this skill (or a similar author note under Developer).

## When to use

- Adding or rewriting any `source/**/*.md`
- Updating `locale/zh_CN/LC_MESSAGES/**/*.po`
- Documenting a private repo, a launch arg, a topic, or a Cursor skill from another fiveages-sim repo

## Never invent

Do not add scripts, flags, launch arguments, package / class / topic / FSM names, conda env names, USD prim paths, skill names, or private-repo directory trees unless they are verified in a **linked** public source:

- A public README (or a cited section of one)
- `.gitmodules` / `submodules_visibility.conf`
- A launch file, xacro, or package `CMakeLists.txt` / `package.xml` you can point at
- An official branch README (`arx-lift2s`, `panthera-ht`, `dobot-cr5`)

If it is not in those sources, omit it. Prefer a link over a guessed list.

## Prefer official init scripts

Documented entry points (use the **names** from those READMEs):

| Workspace | Scripts |
|-----------|---------|
| [open-deploy-ws](https://github.com/fiveages-sim/open-deploy-ws/blob/main/README.EN.md) | `./init_repo.sh` (not recursive `git submodule update --init --recursive`) |
| Lean branches (`arx-lift2s`, `panthera-ht`, `dobot-cr5`) | `./init_repo.sh`, then `./quick_start.sh` (and `./teleop_start.sh` / `./release.sh` only if that branch README names them) |
| FaSim-Isaac | `./init.sh`, `./run.sh` |
| After `colcon build` on `main` | `source install/setup.bash` in the launch terminal (standard ROS overlay) |

Do **not** document a hand-written `~/.bashrc` `source /opt/ros/...` chain as the path. Do **not** invent a workspace `setup.bash` / env installer.

## Private repos

For `fa-deploy-ws`, FiveAges URDF remotes (`fa-*-description`, `fa-w2-components`, `fa-wce3-description`), DexCap private workspace, `ocs2_wbc_controller`, and other 404-without-access remotes:

- Tell readers to follow **that repository’s README after access**
- You may name the same **script name** as the public counterpart (`./init_repo.sh`) when that is the verified pattern
- Do **not** list `--robot`, `robot.local.yaml`, `./quick_start.sh --mock`, `fiveages_bringup`, `init-sim.sh`, conda env names, or a guessed `common/` / `arms/` / `robot/` tree

FiveAges URDF gitlinks and USD Gen labels: [robot_descriptions `.gitmodules`](https://github.com/fiveages-sim/robot_descriptions/blob/main/.gitmodules) (`main` and `feature/agilex`) and [robot_usds README](https://github.com/fiveages-sim/robot_usds/blob/main/README.md) §3.1. There is **no** public `robot-descriptions-fiveages` umbrella.

## Product facts vs writer-scolding

Keep **reader-facing product facts**:

- There is **no** `hardware:=mock`. Keys are `mock_components` / `gz` / `isaac` / `real`.
- `/fsm_command` is `std_msgs/Int32`, not strings such as `stand` / `walk`.
- Acone / AC One is **dual-arm** (双臂); Lift 2S is the **full-body** mobile manipulator. Do not call Acone arm-only / single-arm / 仅机械臂.
- Brand labels follow [robot_usds README_zh-CN.md §3.1](https://github.com/fiveages-sim/robot_usds/blob/main/README_zh-CN.md#31-中文简称与英文标识对照) (方舟无限 = ARX, never bare “Ark”; 高擎 = HighTorque / Panthera). On reader pages, use names naturally (quiet first-mention pairs such as **ARX** (方舟无限) are fine). Do not lecture “方舟无限 = ARX, not bare Ark” on every page.

Rewrite writer-scolding into a positive instruction:

| Avoid on reader pages | Prefer |
|-----------------------|--------|
| “Do not invent extra top-level scripts.” | “Top-level scripts are those listed in the open-deploy-ws README (`./init_repo.sh`, …).” |
| “This page does not invent `--robot` flags …” | “Flags and robot IDs are in the private fa-deploy-ws README after you have access.” |
| “Do not invent class names.” | “Use the plugin class from that robot’s `xacro/ros2_control/*.xacro`.” |
| “Do not invent extra … skills.” | “The `feature/agilex` skills index lists only `split-chassis-glb`.” |
| “do not treat this list as a substitute” | “Overview only; follow the linked skill / README for the full procedure.” |

“Source of truth” admonitions that **only list links** are fine. Drop bullets whose only purpose is “Do not invent X”.

## Other stack facts (do not re-invent)

- `demo.launch.py` default `robot:=cr5`, `hardware:=mock_components`
- End-effector: launch `type` / `left_type` / `right_type` (and `robot_profile`). No `gripper:=`
- Split vs full body: `split_body.launch.py` / `full_body.launch.py`
- Composer `--robot fiveages_w2` is real on robot_action_composer `ROS2_STACK.md`. It is **not** an `./init_repo.sh --robot` flag
- Description Cursor skills exist on `robot_descriptions` **`feature/agilex` only** (`split-chassis-glb`). `main` has no `.cursor/skills`
- In `open-deploy-ws` the descriptions checkout is `src/robot-descriptions/` (hyphen)
- Humanoid in this docs set = wheeled-arm (base + arms), not bipedal

## Builds after edits

```bash
make gettext
make update-po
# fill only the .po files you changed; do not run apply_zh_json on all of tmp_zh_out
make html
make html-zh_CN
python3 scripts/check_zh_coverage.py --threshold 95
python3 scripts/check_zh_mix.py
```

`make html-all` is not `.PHONY` — run `html` and `html-zh_CN` separately. Restore wrap-only unrelated `.po` from git after `update-po` if you did not mean to touch them.

zh_CN coverage must stay 100% (CI threshold 95%). Also run `python3 scripts/check_zh_mix.py` (fuzzy / leftover English — see `.cursor/skills/zh-translation-qa/SKILL.md`). Never nest `` ``` `` inside `` ```{admonition} ``; use `:::` colon fences. User-facing docs are bilingual; fill new English strings in `locale/zh_CN`.

## After a move or merge

Delete the old page. Do **not** leave a stub (“This page is merged into…”, hidden toctree for bookmarks). Checklist: `.cursor/skills/docs-remove-leftovers/SKILL.md`.

## Where this skill lives

- Primary: `.cursor/skills/docs-writing/SKILL.md` (this file)
- Optional one-line pointer for maintainers: `source/5-developer/2-docs_build.md` / `1-contributing.md`
- Do **not** add a sidebar chapter that is only “for agents”
