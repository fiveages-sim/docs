# Add a Robot

Integrate a new robot into the FiveAges Sim ecosystem.

## Overview

Adding a robot requires:
1. Description package (URDF/xacro + ros2_control config)
2. Hardware interface plugin (if not existing)
3. Controller configuration
4. Testing progression: mock → simulation → real

## Step 1: Create Description Package

### Package Structure

:::{code-block} none
robot_description_newrobot/
├── CMakeLists.txt
├── package.xml
├── urdf/
│   ├── newrobot.urdf.xacro
│   └── newrobot.ros2_control.xacro
├── meshes/
│   ├── visual/
│   └── collision/
├── config/
│   └── ocs2_arm_config.yaml
└── launch/
    └── display.launch.py
:::

### URDF/Xacro

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="newrobot">
  
  <!-- Include ros2_control -->
  <xacro:include filename="$(find robot_description_newrobot)/urdf/newrobot.ros2_control.xacro"/>
  
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <mesh filename="package://robot_description_newrobot/meshes/visual/base.stl"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <mesh filename="package://robot_description_newrobot/meshes/collision/base.stl"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
    </inertial>
  </link>
  
  <!-- Joints and links... -->
  
</robot>
```

### ros2_control Configuration

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
  
  <xacro:macro name="newrobot_ros2_control" params="hardware_type">
    <ros2_control name="NewRobotSystem" type="system">
      
      <xacro:if value="${hardware_type == 'mock'}">
        <hardware>
          <plugin>mock_components/GenericSystem</plugin>
        </hardware>
      </xacro:if>
      
      <xacro:if value="${hardware_type == 'gz'}">
        <hardware>
          <plugin>gz_ros2_control/GazeboSimSystem</plugin>
        </hardware>
      </xacro:if>
      
      <xacro:if value="${hardware_type == 'real'}">
        <hardware>
          <plugin>newrobot_ros2_control/NewRobotHardwareInterface</plugin>
          <param name="device">can0</param>
        </hardware>
      </xacro:if>
      
      <joint name="joint_1">
        <command_interface name="position"/>
        <state_interface name="position"/>
        <state_interface name="velocity"/>
      </joint>
      <!-- More joints... -->
      
    </ros2_control>
  </xacro:macro>
  
</robot>
```

## Step 2: Hardware Interface (if needed)

If using an existing interface (CAN, Modbus, etc.), skip this step.

### Plugin Structure

```cpp
// newrobot_hardware_interface.hpp
class NewRobotHardwareInterface : public hardware_interface::SystemInterface
{
public:
  CallbackReturn on_init(const hardware_interface::HardwareInfo & info) override;
  CallbackReturn on_configure(const rclcpp_lifecycle::State & previous_state) override;
  CallbackReturn on_activate(const rclcpp_lifecycle::State & previous_state) override;
  CallbackReturn on_deactivate(const rclcpp_lifecycle::State & previous_state) override;
  
  std::vector<hardware_interface::StateInterface> export_state_interfaces() override;
  std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;
  
  return_type read(const rclcpp::Time & time, const rclcpp::Duration & period) override;
  return_type write(const rclcpp::Time & time, const rclcpp::Duration & period) override;
};
```

## Step 3: Controller Configuration

### OCS2 Arm Config

```yaml
# config/ocs2_arm_config.yaml
arm:
  dof: 6
  joint_names:
    - joint_1
    - joint_2
    - joint_3
    - joint_4
    - joint_5
    - joint_6

  joint_limits:
    position:
      lower: [-3.14, -2.0, -2.5, -3.14, -2.0, -3.14]
      upper: [3.14, 2.0, 2.5, 3.14, 2.0, 3.14]
    velocity: [2.0, 2.0, 2.0, 2.5, 2.5, 2.5]
    effort: [100, 100, 80, 50, 50, 30]

mpc:
  dt: 0.01
  horizon: 1.0
  # MPC tuning parameters...
```

## Step 4: Test Progression

### Mock Testing

```bash
# Verify URDF
check_urdf newrobot.urdf

# Display in RViz
ros2 launch robot_description_newrobot display.launch.py

# Mock demo
ros2 launch ocs2_arm_controller demo.launch.py robot:=newrobot hardware:=mock
```

### Gazebo Testing

```bash
ros2 launch ocs2_arm_controller demo.launch.py robot:=newrobot hardware:=gz
```

### Real Hardware Testing

```bash
# Follow the go_real_hardware guide
ros2 launch ocs2_arm_controller demo.launch.py robot:=newrobot hardware:=real
```

## Step 5: Integration

### Add to robot_descriptions

1. Create package in appropriate location
2. Add as submodule to `robot_descriptions`
3. Update visibility configuration
4. Create PR

### Document

Create or update:
- Package README
- Launch file documentation
- Hardware-specific notes

## Checklist

- [ ] URDF parses without errors
- [ ] Meshes display correctly in RViz
- [ ] ros2_control configuration valid
- [ ] Mock hardware demo works
- [ ] Gazebo simulation works (if applicable)
- [ ] Real hardware works (if applicable)
- [ ] OCS2 controller tracks targets
- [ ] Package builds cleanly
- [ ] README documents usage

## Common Issues

### URDF errors

:::{code-block} bash
# Check for syntax errors
check_urdf <(xacro newrobot.urdf.xacro)
:::

### Controller fails to start

- Verify joint names match between URDF and config
- Check ros2_control hardware plugin is found
- Review controller manager logs

### Motion incorrect

- Verify joint axis directions
- Check joint limits match physical robot
- Verify inertia parameters

## Next Steps

- [ros2_control here](../3-concepts/1-ros2_control_here.md) — Understand the control architecture
- [Developer guide](../5-developer/0-index.md) — Contributing guidelines
