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
└── README.md                      # 本文档
```

## 配置文件说明

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

## Claude安装和卸载命令

安装

```bash
claude plugin install amap@wenguoli-skills
```

卸载

```bash
claude plugin uninstall amap
```



## 如何添加新的 Skill

### 步骤 1：创建 Skill 目录

在 `skills/` 目录下创建新的技能目录：

```bash
mkdir -p /Users/wenguoli/.claude/plugins/marketplaces/wenguoli-skills/skills/new-skill
```

### 步骤 2：创建必要文件

在新的技能目录中创建：
- `SKILL.md` - 技能描述文档（必须包含 YAML frontmatter）
- `requirements.txt` - Python 依赖（如果需要）
- `install/` - 安装脚本（可选）
- `references/` - 参考文档（可选）
- `scripts/` - 执行脚本（可选）

**SKILL.md 示例：**

```markdown
---
name: new-skill
description: 简短描述，说明何时应该使用此技能
---

# New Skill

详细描述技能的功能、用法和示例。
```

### 步骤 3：更新 marketplace.json

在 `.claude-plugin/marketplace.json` 的 `plugins[0].skills` 数组中添加新技能：

```json
{
  "plugins": [
    {
      "name": "amap",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/amap",
        "./skills/new-skill"  // 新添加的技能
      ]
    }
  ]
}
```

### 步骤 4：更新 known_marketplaces.json 的 lastUpdated

```json
"wenguoli-skills": {
  ...
  "lastUpdated": "2026-02-02T00:00:00.000Z"  // 更新为当前时间
}
```

### 步骤 5：重启 Claude

重启 Claude 以使更改生效。

## Directory-Sourced vs GitHub-Sourced Marketplaces

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

## Installed vs Marketplaces 的区别

在 `/plugin` 命令中，有两个不同的区域：

### Marketplaces 区域

显示**所有已注册的 Marketplace**，无论是否安装了其中的插件。Marketplace 注册在 `known_marketplaces.json` 中：

| Marketplace | 来源类型 | 说明 |
|-------------|----------|------|
| anthropic-agent-skills | GitHub | 远程仓库克隆 |
| claude-plugins-official | GitHub | 远程仓库克隆 |
| wenguoli-skills | Directory | 本地目录源 |

### Installed 区域

显示**已安装的具体插件**，插件注册在 `installed_plugins.json` 中：

| 插件 | Marketplace | 安装路径 |
|------|-------------|----------|
| document-skills | anthropic-agent-skills | `/cache/.../document-skills/...` |
| example-skills | anthropic-agent-skills | `/cache/.../example-skills/...` |
| pyright-lsp | claude-plugins-official | `/cache/.../pyright-lsp/1.0.0` |
| amap | wenguoli-skills | `/marketplaces/wenguoli-skills/` |

### 为什么 amap 在 Installed 列表中看不到？

这个问题可能有以下原因：

1. **显示刷新问题**: `/plugin` 命令的输出可能缓存了旧数据，但实际 `installed_plugins.json` 中确实有 `amap@wenguoli-skills` 的记录

2. **安装路径类型不同**:
   - GitHub-sourced 的插件，安装路径指向 `/cache/...`
   - Directory-sourced 的插件，安装路径指向 `/marketplaces/...`
   - CLI 可能根据路径类型对插件有不同的显示逻辑

3. **市场加载 vs 插件安装**:
   - Directory-sourced marketplace 的插件可能被系统视为"始终从 marketplace 直接加载"
   - 不需要"安装"步骤，因此可能不显示在 Installed 列表中

**验证插件是否可用**:

```bash
# 检查 installed_plugins.json 是否包含插件
cat /Users/wenguoli/.claude/plugins/installed_plugins.json | grep amap

# 检查技能是否被加载
# 在 Claude 对话中尝试使用 amap 技能
```

## 常见问题

### Q: 为什么缓存路径显示为 `unknown` 而不是版本号？

A: 这是因为 `marketplace.json` 中的 plugin 定义缺少 `version` 字段。**解决方案**：在 plugin 定义中添加 `version` 字段：

```json
{
  "plugins": [
    {
      "name": "amap",
      "version": "1.0.0",  // 必须添加此字段
      "description": "...",
      "author": {
        "name": "wenguoli",
        "email": ""
      },
      ...
    }
  ]
}
```

修复后，缓存路径将从 `/cache/wenguoli-skills/amap/unknown/` 变为 `/cache/wenguoli-skills/amap/1.0.0/`。

### Q: 为什么会生成 `.orphaned_at` 文件？

A: 对于 Directory-sourced Marketplace，cache 中的插件副本会被标记为 orphaned，因为 Marketplace 目录本身就是权威来源。删除 cache 并将 `installPath` 指向 marketplace 即可解决。

### Q: 可以直接在 cache 目录修改代码吗？

A: 不建议。对于 Directory-sourced Marketplace，应该直接在 `/marketplaces/wenguoli-skills/` 目录修改。

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
