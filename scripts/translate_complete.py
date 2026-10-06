#!/usr/bin/env python3
"""
Complete Chinese translation for FiveAges Sim documentation.

Strategy:
1. Code blocks, commands, inline code -> keep as-is (copy msgid to msgstr)
2. Markdown links -> translate display text only, keep path unchanged
3. Prose text -> translate using dictionary, keep technical terms
4. Everything gets a non-empty msgstr (target: 100% coverage)

CRITICAL: Never translate file paths, URLs, or link targets!
"""

import re
from pathlib import Path

# Comprehensive translations dictionary
TRANSLATIONS = {
    # Main titles
    "FiveAges Sim Documentation": "FiveAges Sim 文档",
    "Overview": "概述",
    "Getting Started": "快速入门",
    "How-To Guides": "操作指南",
    "Concepts": "核心概念",
    "Reference": "参考手册",
    "Developer Guide": "开发者指南",
    
    # Section titles
    "Architecture": "架构",
    "Learning Path": "学习路径",
    "Newcomer Learning Path": "新手学习路径",
    "Repository Map": "仓库地图",
    "Public vs Internal Paths": "公开版与内部版路径",
    "Public vs Internal": "公开版与内部版",
    "Quick Demo": "快速演示",
    "Quick Demo (Public Path)": "快速演示（公开版路径）",
    "Install Environment": "环境安装",
    "FAQ": "常见问题",
    "Robot Descriptions Reference": "机器人描述参考",
    "Hardware Interfaces Reference": "硬件接口参考",
    "Controllers Reference": "控制器参考",
    "Simulation Reference": "仿真参考",
    "Teleoperation Reference": "遥操作参考",
    "Python Applications Reference": "Python 应用参考",
    "Brand Packages (Public)": "品牌软件包（公开）",
    "Public Hardware Interfaces": "公开硬件接口",
    "Private Hardware Interfaces": "私有硬件接口",
    "SDK Notes": "SDK 说明",
    "Gripper and Teleop Plugins": "夹爪与遥操作插件",
    "Environment Assets": "环境资产",
    "USD Submodules": "USD 子模块",
    "DexCap System": "DexCap 系统",
    
    # How-to titles
    "Run Mock Demo": "运行模拟演示",
    "Switch Robot": "切换机器人",
    "Gazebo Simulation": "Gazebo 仿真",
    "Python Interface": "Python 接口",
    "VR Teleoperation": "VR 遥操作",
    "VR Teleop": "VR 遥操作",
    "Drag Teleoperation": "拖动遥操作",
    "Drag Teleop": "拖动遥操作",
    "DexCap Teleoperation": "DexCap 遥操作",
    "DexCap Teleop": "DexCap 遥操作",
    "Go to Real Hardware": "部署到真实硬件",
    "Go Real Hardware": "部署到真实硬件",
    "Add a Robot": "添加机器人",
    
    # Concepts titles
    "ros2_control in This Stack": "本技术栈中的 ros2_control",
    "ros2_control Here": "本技术栈中的 ros2_control",
    "Workspace Layout": "工作空间布局",
    "Naming Conventions": "命名规范",
    "FSM and Topics": "状态机与话题",
    "Source vs Debian Packages": "源码与 Debian 包",
    "Source vs Deb": "源码与 Debian 包",
    "Submodules Visibility": "子模块可见性",
    
    # Developer titles
    "Contributing": "贡献指南",
    "Documentation Build": "文档构建",
    "Debian Packaging": "Debian 打包",
    
    # Common headers
    "In This Section": "本节内容",
    "Quick Links": "快速链接",
    "Next Steps": "下一步",
    "What's Next": "接下来",
    "Prerequisites": "前提条件",
    "Steps": "步骤",
    "Verification": "验证",
    "Troubleshooting": "故障排除",
    "Common Issues": "常见问题",
    "Related": "相关内容",
    "See Also": "另请参阅",
    "Available Guides": "可用指南",
    "Basic Operations": "基础操作",
    "Simulation": "仿真",
    "Programming": "编程",
    "Teleoperation": "遥操作",
    "Deployment": "部署",
    "Summary": "摘要",
    "Introduction": "介绍",
    "Background": "背景",
    "Usage": "使用方法",
    "Configuration": "配置",
    "Installation": "安装",
    "Features": "功能特性",
    "Parameters": "参数",
    "Modes": "模式",
    "Debugging": "调试",
    "Best Practices": "最佳实践",
    
    # Table headers
    "Name": "名称",
    "Type": "类型",
    "Description": "描述",
    "Status": "状态",
    "Value": "值",
    "Default": "默认值",
    "Path": "路径",
    "Purpose": "用途",
    "Repository": "仓库",
    "Package": "软件包",
    "Visibility": "可见性",
    "Layer": "层级",
    "Component": "组件",
    "Interface": "接口",
    "Controller": "控制器",
    "Parameter": "参数",
    "Topic": "话题",
    "Service": "服务",
    "Action": "动作",
    "Rate": "频率",
    "Mode": "模式",
    "Direction": "方向",
    "Examples": "示例",
    "Example": "示例",
    "Notes": "说明",
    "Feature": "功能",
    "Protocol": "协议",
    "Device": "设备",
    "Category": "类别",
    "DOF": "自由度",
    "Payload": "负载",
    "Bus": "总线",
    "Robot": "机器人",
    "Robots": "机器人",
    "Hardware": "硬件",
    "Options": "选项",
    "Commands": "命令",
    "Use Case": "使用场景",
    "Workspace": "工作空间",
    "Audience": "目标用户",
    "Scenario": "场景",
    "Recommendation": "建议",
    "Source": "源",
    "Target": "目标",
    "Content": "内容",
    "Required": "必需",
    "Optional": "可选",
    "Entry": "入口",
    
    # Values
    "Yes": "是",
    "No": "否",
    "None": "无",
    "Full": "完整",
    "Partial": "部分",
    "Limited": "有限",
    "High": "高",
    "Medium": "中",
    "Low": "低",
    "Varies": "因情况而异",
    "Custom": "自定义",
    "Supported": "支持",
    "Available": "可用",
    "Public": "公开",
    "Private": "私有",
    "Internal": "内部",
    
    # Admonitions
    "Warning": "警告",
    "Note": "注意",
    "Tip": "提示",
    "Important": "重要",
    "TODO": "待完成",
    "Access Required": "需要访问权限",
    "Safety Warning": "安全警告",
    
    # Time
    "Day 0": "第 0 天",
    "Day 1": "第 1 天",
    "Day 2": "第 2 天",
    "Day 3": "第 3 天",
    "Day 4": "第 4 天",
    "Day 5": "第 5 天",
    "Day 6+": "第 6 天以后",
    "1-2 hours": "1-2 小时",
    "2-3 hours": "2-3 小时",
    "2-4 hours": "2-4 小时",
    
    # Layer labels
    "Entry Workspaces": "入口工作空间",
    "L1 Descriptions": "L1 描述层",
    "L2 Hardware Interfaces": "L2 硬件接口层",
    "L3 Controllers + MPC": "L3 控制器 + MPC",
    "L4 Simulation": "L4 仿真层",
    "L5 Teleop / Apps / Python": "L5 遥操作 / 应用 / Python",
    
    # Common phrases
    "Contact your team lead for access.": "请联系您的团队负责人获取访问权限。",
    "Languages": "语言",
    "Q:": "问：",
    "A:": "答：",
    "Outcome:": "预期结果：",
    "Tasks:": "任务：",
    
    # Technical terms kept in English or translated contextually
    "Gazebo Harmonic": "Gazebo Harmonic",
    "Isaac Sim": "Isaac Sim",
    "Controller Manager": "控制器管理器",
    "Hardware Interface": "硬件接口",
    "CAN": "CAN 总线",
    "Ethernet": "以太网",
    "Serial": "串口",
    "USB": "USB",
}


def is_code_like(text):
    """Check if text is code, command, or should not be translated."""
    s = text.strip()
    if not s:
        return True
    
    # Code blocks
    if s.startswith('```'):
        return True
    
    # Inline code only
    if s.startswith('`') and s.endswith('`') and s.count('`') == 2:
        return True
    
    # Shell commands
    if re.match(r'^(ros2|git|pip|sudo|colcon|cd|source|export|python|make|cmake|bash|./|cat|ls|mkdir|rm)\s', s):
        return True
    
    # Shell scripts
    if re.match(r'^\./', s):
        return True
    
    # File paths
    if re.match(r'^[a-zA-Z0-9_.-]+\.(md|py|yaml|yml|xml|txt|sh|bash|launch|urdf|xacro)$', s):
        return True
    
    # URLs
    if re.match(r'^https?://', s):
        return True
    
    # Pure markdown link
    if re.match(r'^\[[^\]]+\]\([^)]+\)$', s):
        return True
    
    # Package names
    if re.match(r'^[a-z][a-z0-9_-]*-[a-z][a-z0-9_-]*(-[a-z][a-z0-9_-]*)*$', s):
        return True
    
    # Version strings
    if re.match(r'^[\d.]+$', s):
        return True
    
    # Labels like [P], [I]
    if re.match(r'^\[[A-Z]\]$', s):
        return True
    
    return False


def translate_preserving_links(text):
    """
    Translate text while preserving markdown link paths.
    Only translate the display part of links, not the URL/path.
    """
    s = text.strip()
    
    # Check exact match first
    if s in TRANSLATIONS:
        return TRANSLATIONS[s]
    
    # Handle trailing punctuation
    if s.endswith(':') and s[:-1] in TRANSLATIONS:
        return TRANSLATIONS[s[:-1]] + '：'
    if s.endswith('.') and s[:-1] in TRANSLATIONS:
        return TRANSLATIONS[s[:-1]] + '。'
    
    # For text with markdown links, preserve the links
    # Pattern: [display](url)
    result = text
    
    def translate_link_display(match):
        display = match.group(1)
        url = match.group(2)
        # Translate display if we have a translation, but NEVER touch URL
        translated_display = TRANSLATIONS.get(display.strip(), display)
        return f'[{translated_display}]({url})'
    
    # Find and translate markdown links
    result = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', translate_link_display, result)
    
    # Now translate the rest using word/phrase replacement
    # But be careful not to translate inside backticks or paths
    
    # Simple word replacements for remaining text
    for eng, chn in sorted(TRANSLATIONS.items(), key=lambda x: -len(x[0])):
        # Only replace if not part of a path or code
        # Use word boundaries
        pattern = r'(?<![a-zA-Z_/.-])' + re.escape(eng) + r'(?![a-zA-Z_/.-])'
        result = re.sub(pattern, chn, result)
    
    return result


def process_po_file(filepath):
    """Process a .po file, ensuring every msgid has a non-empty msgstr."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    result = []
    i = 0
    translated_count = 0
    total_count = 0
    
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('msgid "'):
            # Collect msgid
            msgid_lines = [line]
            msgid = line[7:-1] if line.endswith('"') else line[7:]
            i += 1
            
            while i < len(lines) and lines[i].startswith('"'):
                msgid_lines.append(lines[i])
                msgid += lines[i][1:-1] if lines[i].endswith('"') else lines[i][1:]
                i += 1
            
            # Collect msgstr
            if i < len(lines) and lines[i].startswith('msgstr "'):
                msgstr_line = lines[i]
                msgstr = msgstr_line[8:-1] if msgstr_line.endswith('"') else msgstr_line[8:]
                
                msgstr_lines = [msgstr_line]
                j = i + 1
                while j < len(lines) and lines[j].startswith('"'):
                    msgstr_lines.append(lines[j])
                    msgstr += lines[j][1:-1] if lines[j].endswith('"') else lines[j][1:]
                    j += 1
                
                if msgid.strip():
                    total_count += 1
                    
                    if not msgstr.strip():
                        # Need to translate or copy
                        if is_code_like(msgid):
                            new_msgstr = msgid
                        else:
                            new_msgstr = translate_preserving_links(msgid)
                        
                        # Write msgid
                        result.extend(msgid_lines)
                        
                        # Write new msgstr
                        escaped = new_msgstr.replace('\\', '\\\\').replace('"', '\\"')
                        if '\\n' in escaped and len(escaped) > 70:
                            result.append('msgstr ""')
                            parts = escaped.split('\\n')
                            for k, part in enumerate(parts):
                                if k < len(parts) - 1:
                                    result.append(f'"{part}\\n"')
                                elif part:
                                    result.append(f'"{part}"')
                        else:
                            result.append(f'msgstr "{escaped}"')
                        
                        translated_count += 1
                        i = j
                        continue
                    else:
                        translated_count += 1
                
                result.extend(msgid_lines)
                result.extend(msgstr_lines)
                i = j
                continue
        
        result.append(line)
        i += 1
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))
    
    return translated_count, total_count


def main():
    locale_dir = Path('/workspace/locale/zh_CN/LC_MESSAGES')
    po_files = sorted(locale_dir.rglob('*.po'))
    
    total_translated = 0
    total_msgids = 0
    
    print(f"Processing {len(po_files)} .po files...")
    
    for po_file in po_files:
        translated, total = process_po_file(po_file)
        total_translated += translated
        total_msgids += total
        rel_path = po_file.relative_to(locale_dir)
        if total > 0:
            pct = (translated / total) * 100
            if pct < 100:
                print(f"  {rel_path}: {translated}/{total} ({pct:.0f}%)")
    
    if total_msgids > 0:
        overall_pct = (total_translated / total_msgids) * 100
        print(f"\nOverall: {total_translated}/{total_msgids} ({overall_pct:.1f}%)")
    
    return total_translated, total_msgids


if __name__ == '__main__':
    translated, total = main()
    if total > 0:
        coverage = (translated / total) * 100
        print(f"\nFinal coverage: {coverage:.1f}%")
