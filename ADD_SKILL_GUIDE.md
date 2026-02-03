# 新增 Skills 操作清单

每次添加新技能时，需要更新以下文件和配置。

---

## 一、必需更新文件

### 1. marketplace.json

**文件位置**: `.claude-plugin/marketplace.json`

**更新内容**: 在 `plugins` 数组中添加新插件配置（每个 skill 独立一个 plugin）

```json
{
  "plugins": [
    {
      "name": "amap",
      "version": "1.0.0",
      "description": "高德地图服务工具包，支持地址解析、逆地址解析、路径规划、POI搜索和IP定位",
      "author": {
        "name": "wenguoli",
        "email": "15160333779@163.com"
      },
      "source": "./skills/amap",
      "strict": false
    },
    {
      "name": "new-skill",
      "version": "1.0.0",
      "description": "新技能功能描述",
      "author": {
        "name": "wenguoli",
        "email": "15160333779@163.com"
      },
      "source": "./skills/new-skill",
      "strict": false
    }
  ]
}
```

**注意**: 每个 skill 独立一个 plugin，`source` 指向对应技能目录。

---

## 二、README.md 可选更新

**文件位置**: `README.md`

根据需要更新以下章节：

### 2.1 目录结构

更新 `skills/` 部分：

```markdown
├── skills/
│   ├── amap/                     # 高德地图技能
│   ├── model-comparison/         # 大模型能力对比技能
│   └── new-skill/                # 新技能名称（简短描述）
```

### 2.2 技能清单表格

在官方参考资源章节更新表格：

```markdown
| Skill | 功能 |
|-------|------|
| `amap` | 高德地图服务 |
| `model-comparison` | 大模型能力对比分析 |
| `new-skill` | 新技能功能说明 |
```

---

## 三、目录结构示例

新技能目录结构建议：

```
skills/new-skill/
├── SKILL.md              # 【必需】技能描述文档
├── requirements.txt      # 【可选】Python 依赖
├── scripts/              # 【可选】执行脚本
│   └── main.py
├── references/           # 【可选】参考文档
│   └── README.md
└── assets/              # 【可选】静态资源
```

---

## 四、SKILL.md 模板

```markdown
---
name: new-skill
description: 简短描述，说明技能功能和触发场景
license: MIT
---

# 技能名称

## Overview
技能概述。

## Usage
使用示例。

## Dependencies
依赖说明（如果有 requirements.txt）。

## Scripts
脚本说明。
```

---

## 五、完整操作步骤

| 步骤 | 操作 | 文件 |
|------|------|------|
| 1 | 创建技能目录 | `skills/new-skill/` |
| 2 | 创建 SKILL.md | `skills/new-skill/SKILL.md` |
| 3 | 更新 marketplace.json（添加独立 plugin） | `.claude-plugin/marketplace.json` |
| 4 | (可选) 更新 README.md | `README.md` |

---

## 六、验证方法

1. 重启 Claude CLI
2. 使用技能相关关键词触发测试
3. 检查 `claude plugin list` 显示正常
