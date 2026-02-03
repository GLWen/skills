# wenguoli-skills - 本地 Marketplace

本目录是一个本地 (directory-sourced) Marketplace，用于存放自定义 Skills。

## 目录结构

```
/Users/wenguoli/.claude/plugins/marketplaces/wenguoli-skills/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace 配置文件
├── skills/
│   └── amap/                     # 高德地图技能
│       ├── SKILL.md               # 技能描述文档
│       ├── requirements.txt       # Python 依赖
│       ├── install/               # 安装脚本
│       ├── references/            # API 参考文档
│       └── scripts/               # 执行脚本
├── spec/                         # 技能规范文档
│   └── agent-skills-spec.md
├── template/                     # 技能模板
│   └── SKILL.md
└── README.md                      # 本文档
```

---

## 第一部分：Marketplace 配置指南

### marketplace.json

位于 `.claude-plugin/marketplace.json`，定义了 Marketplace 的元信息和包含的插件：

```json
{
  "name": "wenguoli-skills",
  "owner": {
    "name": "wenguoli",
    "email": ""
  },
  "metadata": {
    "description": "Custom skills including Amap (高德地图) geolocation services",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "amap",
      "version": "1.0.0",
      "description": "Toolkit for working with Amap (AutoNavi/高德地图) services...",
      "author": {
        "name": "wenguoli",
        "email": ""
      },
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/amap"
      ]
    }
  ]
}
```

**关键字段说明：**
- `name`: Marketplace 名称
- `plugins[]`: Marketplace 中包含的插件列表
- `plugins[].name`: 插件名称
- `plugins[].version`: **插件版本号（必需）** - 用于缓存路径（如 `/cache/wenguoli-skills/amap/1.0.0/`），缺少此字段会导致版本显示为 `unknown`
- `plugins[].description`: 插件描述
- `plugins[].author`: 插件作者信息（可选）
- `plugins[].source`: 相对于 Marketplace 根目录的源路径（通常是 `"./"`）
- `plugins[].strict`: 是否严格模式（可选）
- `plugins[].skills[]`: 相对于 Marketplace 根目录的技能路径列表

### known_marketplaces.json

需要在 `/Users/wenguoli/.claude/plugins/known_marketplaces.json` 中注册此 Marketplace：

```json
"wenguoli-skills": {
  "source": {
    "source": "directory",
    "path": "/Users/wenguoli/.claude/plugins/marketplaces/wenguoli-skills"
  },
  "installLocation": "/Users/wenguoli/.claude/plugins/marketplaces/wenguoli-skills",
  "lastUpdated": "2026-02-01T15:55:00.000Z"
}
```

### installed_plugins.json

插件安装路径应指向 Marketplace 目录（而非 cache）：

```json
"amap@wenguoli-skills": [
  {
    "scope": "user",
    "installPath": "/Users/wenguoli/.claude/plugins/marketplaces/wenguoli-skills",
    "version": "1.0.0",
    "installedAt": "2026-02-01T15:10:00.000Z",
    "lastUpdated": "2026-02-02T00:00:00.000Z"
  }
]
```

### Claude安装和卸载命令

安装

```bash
claude plugin install amap@wenguoli-skills
```

卸载

```bash
claude plugin uninstall amap
```

---

## 第二部分：编写 Skills 规范指南

### Skill 目录结构

每个 Skill 是一个包含 `SKILL.md` 文件的目录，可选包含其他资源：

```
skills/
└── my-skill/                      # Skill 目录（技能名称，全小写，中划线分隔）
    ├── SKILL.md                   # 【必需】技能描述文档
    ├── requirements.txt           # 【可选】Python 依赖（pip）
    ├── install/                   # 【可选】安装脚本
    │   └── install.sh
    ├── references/                # 【可选】API 参考文档
    │   └── api_reference.md
    ├── scripts/                   # 【可选】执行脚本
    │   ├── main.py
    │   └── utils.py
    └── templates/                 # 【可选】模板文件
        └── template.html
```

### SKILL.md 文件规范

`SKILL.md` 是 Skill 的核心描述文件，格式如下：

```markdown
---
name: skill-name              # 【必需】技能名称（全小写，中划线分隔）
description: Brief description # 【必需】简短描述，说明何时使用此技能
license: License terms        # 【可选】许可证说明
---

# Skill Title

技能详细说明、使用方法、示例和指南。
```

#### YAML Frontmatter 字段说明

| 字段 | 必需 | 说明 |
|------|------|------|
| `name` | 是 | 技能标识符，全小写，用中划线分隔单词 |
| `description` | 是 | 简短描述（1-2句话），说明技能功能和触发场景 |
| `license` | 否 | 许可证类型（如 "MIT", "Apache-2.0", "Proprietary"） |

#### description 最佳实践

description 应该包含触发关键词，便于 Claude 自动识别何时使用该技能：

```markdown
description: "Toolkit for Amap (高德地图) services. Use when users need: (1) Geocoding (address to coordinates), (2) Reverse geocoding, (3) Route planning, (4) POI search, (5) IP location, or any China map-related queries. Triggered by: '地址', '坐标', '导航', '高德地图', 'amap', etc."
```

#### SKILL.md 内容结构建议

```markdown
---
name: my-skill
description: Brief description of what this skill does
---

# Skill Name

## Overview
技能概述，说明它能做什么。

## Prerequisites
先决条件，如 API 密钥、环境配置等。

## Usage Examples
使用示例，提供常用命令或调用方式。

## Script Reference
脚本详细说明，包括参数、选项和使用方法。

## Best Practices
最佳实践建议。

## Troubleshooting
常见问题和解决方案。
```

### 触发条件设置

在 `description` 中包含触发关键词，当用户提及这些关键词时，Claude 会自动使用该 Skill：

```markdown
description: "When users mention: '地址', '经纬度', '坐标', '导航', '路线', '附近', '定位', '高德地图', 'amap', '查询', or any location-related queries in Chinese."
```

### 依赖管理

#### requirements.txt

如果 Skill 需要 Python 依赖，在根目录创建 `requirements.txt`：

```
requests>=2.28.0
pandas>=1.4.0
```

依赖会在 Skill 首次加载时自动安装。

#### install/ 目录

如果需要额外的安装步骤，在 `install/` 目录添加脚本：

```
install/
├── setup.sh          # Bash 安装脚本
└── README.md         # 安装说明
```

### 脚本组织

#### scripts/ 目录

将可执行脚本放在 `scripts/` 目录中：

```
scripts/
├── __init__.py       # 包初始化（可选）
├── main.py           # 主入口脚本
├── geocoding.py      # 地理编码功能
├── search.py         # 搜索功能
└── utils.py          # 工具函数
```

脚本应该：
- 支持 `--help` 参数显示用法
- 使用 argparse 或 click 等库处理命令行参数
- 返回结构化的输出（JSON 或格式化的文本）

#### 脚本示例

```python
#!/usr/bin/env python3
"""Geocoding script for address to coordinate conversion."""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Address to coordinates conversion")
    parser.add_argument("--address", required=True, help="Address to geocode")
    parser.add_argument("--city", help="City for better accuracy")
    args = parser.parse_args()

    # Implementation
    print(f"Geocoding: {args.address}")

if __name__ == "__main__":
    main()
```

### 参考文档

#### references/ 目录

存放 API 文档、使用指南等参考材料：

```
references/
├── api_reference.md   # API 参考
├── user_guide.md      # 用户指南
└── faq.md             # 常见问题
```

### 模板文件

#### templates/ 目录

存放可复用的模板文件：

```
templates/
├── email_template.html
├── report_template.md
└── config_template.json
```

---

## 第三部分：添加新 Skill 流程

### 步骤 1：创建 Skill 目录

在 `skills/` 目录下创建新的技能目录：

```bash
mkdir -p /Users/wenguoli/.claude/plugins/marketplaces/wenguoli-skills/skills/new-skill
mkdir -p /Users/wenguoli/.claude/plugins/marketplaces/wenguoli-skills/skills/new-skill/scripts
mkdir -p /Users/wenguoli/.claude/plugins/marketplaces/wenguoli-skills/skills/new-skill/references
```

### 步骤 2：创建 SKILL.md

在 Skill 目录创建 `SKILL.md`：

```markdown
---
name: new-skill
description: Brief description of the skill and when to use it.
---

# New Skill

Detailed description and instructions.
```

### 步骤 3：更新 marketplace.json

在 `.claude-plugin/marketplace.json` 的 `plugins[0].skills` 数组中添加：

```json
{
  "plugins": [
    {
      "name": "amap",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/amap",
        "./skills/new-skill"
      ]
    }
  ]
}
```

### 步骤 4：重启 Claude

重启 Claude CLI 使更改生效：

```bash
exit
claude
```

---

## 第四部分：官方参考资源

### Agent Skills 规范

官方规范文档：[https://agentskills.io/specification](https://agentskills.io/specification)

### 官方 Skills 示例

参考 [anthropic-agent-skills](https://github.com/anthropic/skills) 仓库获取完整示例：

| Skill | 功能 |
|-------|------|
| `docx` | Word 文档创建、编辑、分析 |
| `pdf` | PDF 文档处理 |
| `pptx` | PowerPoint 演示文稿 |
| `xlsx` | Excel 电子表格 |
| `algorithmic-art` | 算法艺术生成 |
| `webapp-testing` | Web 应用测试 |

### 官方文档

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)

---

## 附录 A：Directory-Sourced vs GitHub-Sourced

### GitHub-Sourced Marketplace（如 anthropic-agent-skills）

- **来源**: 远程 GitHub 仓库
- **Marketplace 目录**: 只是 Git 克隆副本，不是源码
- **Cache 目录**: 插件加载的**实际位置**
- **安装路径**: 指向 cache（如 `/cache/anthropic-agent-skills/example-skills/69c0b1a06741/`）
- **特点**: Cache 不会被标记为 orphaned，因为它是权威位置

### Directory-Sourced Marketplace（如 wenguoli-skills）

- **来源**: 本地目录
- **Marketplace 目录**: **就是源码本身**，是权威位置
- **Cache 目录**: 冗余的副本，不需要
- **安装路径**: 应该指向 marketplace 目录（`/marketplaces/wenguoli-skills/`）
- **特点**: Cache 会被标记为 orphaned（.orphaned_at 文件），因为 marketplace 目录才是权威来源

---

## 附录 B：常见问题

### Q: 为什么缓存路径显示为 `unknown` 而不是版本号？

A: 这是因为 `marketplace.json` 中的 plugin 定义缺少 `version` 字段。**解决方案**：在 plugin 定义中添加 `version` 字段。

### Q: 为什么会生成 `.orphaned_at` 文件？

A: 对于 Directory-sourced Marketplace，cache 中的插件副本会被标记为 orphaned。删除 cache 并将 `installPath` 指向 marketplace 即可解决。

### Q: 可以直接在 cache 目录修改代码吗？

A: 不建议。对于 Directory-sourced Marketplace，应该直接在 Marketplace 目录修改。

### Q: 如何验证 Skill 是否正确加载？

A: 在 Claude 对话中使用相关关键词触发 Skill，或查看 Skill 的 SKILL.md 中的触发条件。

### Q: requirements.txt 什么时候被安装？

A: 当 Claude 首次加载该 Skill 时，会自动安装 `requirements.txt` 中列出的依赖。

### Q: 如何调试 Skill 加载问题？

A: 检查以下内容：
1. `SKILL.md` 格式是否正确（必须包含 YAML frontmatter）
2. `marketplace.json` 中的 paths 是否正确
3. `known_marketplaces.json` 和 `installed_plugins.json` 配置是否正确
4. Skill 目录是否包含必要的文件
