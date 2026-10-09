# Introduction

Stack-specific notes. Concrete names come from repository READMEs / launch / xacro — not a generic ROS 2 textbook.

## Topics Covered

- [ros2_control Here](1-ros2_control_here.md) — `hardware:=` → `ros2_control_hardware_type`; Acone plugin table
- [Workspace Layout](2-workspace_layout.md) — `open-deploy-ws` tree and `./init_repo.sh`
- [Naming Conventions](3-naming_conventions.md) — Launch `robot` / EEF `type` / `left_type` / `right_type` (not `gripper:=`); `hardware` values
- [FSM and Topics](4-fsm_and_topics.md) — `std_msgs/Int32` `/fsm_command`; Topic vs Action vs Service; WBC body/head + `/mode_command`
- [分体控制 vs 全身控制](7-split_vs_wbc.md) — 分体控制 (`split_body.launch.py`, OCS2 Arm + Basic Joint) vs 全身控制 (`full_body.launch.py`, OCS2 WBC)
- [Source vs Deb](5-source_vs_deb.md) — GitHub Release `.deb` vs source via `./init_repo.sh`
- [Submodules Visibility](6-submodules_visibility.md) — `parent|path|public|private` and init

## Related Sections

- [Reference](../4-reference/descriptions/0-index.md) — Package pages
- [How-To Guides](../2-how_to/0-index.md)
