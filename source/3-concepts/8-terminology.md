# Terminology

Chinese product names in this documentation, and the English terms they map to. Plugin class names, launch `type` / `left_type` / `right_type`, and `hardware:=` stay as code.

| Chinese | English |
|---------|---------|
| 驱动层 | Hardware Interface (ros2_control official) |
| 控制器 | Controller |
| 分体控制 | Split body |
| 全身控制 | Full body / WBC |
| 夹爪 | gripper |
| 灵巧手 | dexterous hand |
| 仿真路径 | `mock_components` / `isaac` / `gz` |

English page titles and sidebar labels use **Hardware Interface(s)** — the official ros2_control name. Chinese pages use **驱动层** for the same layer.

`mock_components`, `isaac`, and `gz` are launch / xacro keys (`hardware:=`). They are **not** vendor packages under `arms_ros2_control/hardwares/`.

## Related

- [ros2_control in This Stack](1-ros2_control_here.md)
- [Hardware Interfaces](../4-reference/hardware/0-index.md)
- [分体控制 vs 全身控制](7-split_vs_wbc.md)
- [Naming Conventions](3-naming_conventions.md)
