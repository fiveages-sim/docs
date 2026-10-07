# Submodules Visibility

How `open-deploy-ws` decides which **nested** submodules to init.

```{admonition} Source of truth
:class: important

[`submodules_visibility.conf`](https://github.com/fiveages-sim/open-deploy-ws/blob/main/submodules_visibility.conf) and [`./init_repo.sh`](https://github.com/fiveages-sim/open-deploy-ws/blob/main/init_repo.sh). Format is pipe-separated, not INI.
```

## Format

Each data line: `parent_dir|relative_path|public` or `private`. Blank lines and `#` comments are ignored.

From the current file (examples, not the full list):

:::{code-block} none
src/robot-descriptions|common|public
src/robot-descriptions|manipulator/Dobot|public
src/robot-descriptions|manipulator/ARX|public
src/robot-descriptions|manipulator/Tianji|private
src/arms_ros2_control|controller/ocs2_wbc_controller|private
src/arms_ros2_control|libraries/ocs2_humanoid|private
src/arms_ros2_control|libraries/lina_planning|private
:::

Hardware-interface nested lines in that file are **commented out** (they are not active visibility rows).

## What `./init_repo.sh` does

From the [open-deploy-ws README](https://github.com/fiveages-sim/open-deploy-ws/blob/main/README.EN.md):

1. **Nested visibility:** `public` (external) or `private` (needs internal GitHub access). This only affects nested modules **inside** each repo.
2. **Core module mode:** per module `d` (GitHub Release `.deb`) or `s` (source). Top-level `ocs2_ros2`, `arms_ros2_control`, and `robot-descriptions/common` are initialized when you pick **source**.

Then the script inits nested modules according to visibility (skipped if the parent or common is deb), checks out configured branches, runs `rosdep` on source paths, and installs chosen debs.

Do **not** `git submodule update --init --recursive` as the primary path.

## Public vs private (this file)

| Nested path (examples) | Visibility |
|------------------------|------------|
| `robot-descriptions` `common`, `manipulator/Dobot`, `manipulator/ARX`, `quadruped`, `humanoid/Galbot` | `public` |
| `manipulator/Tianji`, `manipulator/Rokae`, FiveAges `fiveages_w*` descriptions, `humanoid/Ubtech` | `private` |
| `arms_ros2_control` `ocs2_wbc_controller`, `ocs2_humanoid`, `lina_planning` | `private` |

If you need private nested modules, use a workspace/README that documents private access (`fa-deploy-ws`). This page does not invent that repo’s extra flags.

## Adding a nested submodule (contributors)

1. Add it to the **parent** `.gitmodules` (Git INI).
2. Add one pipe line to `submodules_visibility.conf`.
3. Test with `./init_repo.sh` on a clean clone.

## Related

- [Workspace Layout](2-workspace_layout.md)
- [Source vs Deb](5-source_vs_deb.md)
