# Claude Skill 开发指南 - 高德地图技能

本文档记录了高德地图技能的目录结构、安装教程和使用方法，供后续开发其他技能时参考。

---

## 目录结构

```
amap/
├── SKILL.md              # 技能描述文件（必需）
├── requirements.txt      # Python 依赖
├── install/              # 安装文档（本文件）
├── references/           # 参考文档
│   ├── api_reference.md # API 参考文档
│   └── use.md           # 使用文档
└── scripts/              # 脚本目录
    ├── __init__.py       # 共享工具函数
    ├── geocoding.py      # 地址解析脚本
    ├── path_planning.py  # 路径规划脚本
    ├── poi_search.py     # POI 搜索脚本
    └── ip_location.py    # IP 定位脚本
```

### 文件说明

| 文件/目录 | 说明 | 是否必需 |
|-----------|------|----------|
| `SKILL.md` | 技能定义文件，包含 name、description 和使用说明 | ✅ 必需 |
| `requirements.txt` | Python 依赖包列表 | ⚠️ 如有 Python 脚本则必需 |
| `scripts/__init__.py` | 共享工具函数（API Key 获取、请求构建等） | ✅ 如有多个脚本则推荐 |
| `scripts/*.py` | 各功能脚本文件 | ✅ 核心功能必需 |

---

## 安装教程

### 1. 目录结构准备

在插件根目录下创建以下结构：

```
wenguoli-skills/
├── 1.0.0/
│   ├── .claude-plugin/
│   │   ├── marketplace.json  # 插件元数据
│   │   └── .orphaned_at      # 删除此文件以激活
│   └── skills/
│       └── amap/
│           ├── SKILL.md
│           ├── requirements.txt
│           └── scripts/
```

### 2. 创建 marketplace.json

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
      "description": "Toolkit for working with Amap (AutoNavi/高德地图) services including geocoding, reverse geocoding, path planning, POI search, and IP location lookup",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/amap"
      ]
    }
  ]
}
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 注册插件到 Claude

编辑 `~/.claude/plugins/installed_plugins.json`，添加插件注册：

```json
{
  "version": 2,
  "plugins": {
    "amap@wenguoli-skills": [
      {
        "scope": "user",
        "installPath": "/Users/wenguoli/.claude/plugins/cache/wenguoli-skills/1.0.0",
        "version": "1.0.0",
        "installedAt": "2026-02-01T15:10:00.000Z",
        "lastUpdated": "2026-02-01T15:10:00.000Z"
      }
    ]
  }
}
```

### 5. 激活插件

```bash
# 删除孤儿标记
rm ~/.claude/plugins/cache/wenguoli-skills/1.0.0/.claude-plugin/.orphaned_at
```

### 6. 设置环境变量（如需要）

```bash
export AMAP_API_KEY=your_api_key_here
```

---

## SKILL.md 格式说明

```markdown
---
name: amap
description: 技能描述，说明触发条件和使用场景
---

# 技能名称

技能详细介绍...

## 功能列表

- 功能 1
- 功能 2
```

### Description 字段规范

描述应包含以下信息：
- 技能功能概述
- 触发条件（何时使用）
- 关键词列表

**示例：**
```markdown
description: 高德地图服务工具包，支持地址解析、逆地址解析、路径规划、POI搜索和IP定位。当Claude需要处理以下任务时使用： (1) 将地址转换为经纬度，(2) 将经纬度转换为地址，(3) 规划路线和导航，(4) 搜索兴趣点如餐厅、酒店、加油站，(5) 通过IP地址获取位置，(6) 计算位置之间的距离，或任何涉及中国地图、位置服务或高德地图API的任务。当用户提到："地址"、"经纬度"、"坐标"、"导航"、"路线"、"附近"、"定位"、"高德地图"、"amap"、"查询"、"北京"、"上海"或任何中文位置/地理相关查询时触发
```

---

## scripts/__init__.py 设计规范

### 核心功能

`__init__.py` 应包含所有脚本共享的工具函数：

```python
"""
技能共享工具模块
"""

import os
import getpass
from typing import Optional

# API 基础 URL
API_BASE_URL = "https://api.example.com/v3"


def get_api_key() -> str:
    """从环境变量获取 API Key，未设置则提示输入"""
    api_key = os.environ.get('API_KEY')
    if api_key:
        return api_key
    print("API_KEY environment variable not found.")
    api_key = getpass.getpass("Please enter your API key: ")
    if not api_key:
        raise ValueError("API key cannot be empty")
    return api_key


def build_api_url(endpoint: str, params: dict) -> str:
    """构建 API URL 并添加查询参数"""
    from urllib.parse import urlencode
    return f"{API_BASE_URL}{endpoint}?{urlencode(params)}"


def make_api_request(url: str, api_key: str, timeout: int = 10) -> dict:
    """发送 API 请求并处理错误"""
    import requests

    if '?' in url:
        url = f"{url}&key={api_key}"
    else:
        url = f"{url}?key={api_key}"

    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    # 检查 API 错误状态
    if data.get('status') != '1':
        error_code = data.get('infocode', 'UNKNOWN')
        error_msg = data.get('info', 'Unknown error')
        raise ValueError(f"API Error [{error_code}]: {error_msg}")

    return data


def parse_coordinates(location: str) -> Optional[tuple[float, float]]:
    """解析位置字符串为坐标"""
    try:
        parts = location.split(',')
        if len(parts) == 2:
            lon = float(parts[0].strip())
            lat = float(parts[1].strip())
            return (lon, lat)
    except (ValueError, AttributeError):
        pass
    return None
```

---

## 脚本编写规范

### 1. 脚本头部模板

```python
#!/usr/bin/env python3
"""
功能名称脚本

简要描述功能。

Usage:
    # 使用示例 1
    python scripts/script.py --param value

    # 使用示例 2
    python scripts/script.py --option "value"
"""

import argparse
import sys
from typing import Optional

# 添加 scripts 目录到导入路径
sys.path.insert(0, __file__.rsplit('/', 1)[0])

from __init__ import (
    get_api_key,
    build_api_url,
    make_api_request
)
```

### 2. 函数定义规范

```python
def function_name(param1: str, param2: Optional[int] = None,
                   api_key: Optional[str] = None) -> dict:
    """
    函数描述。

    Args:
        param1: 参数说明
        param2: 可选参数说明
        api_key: API key（如为 None 将从环境获取）

    Returns:
        返回值说明

    Raises:
        ValueError: 参数错误时的异常说明
    """
    if api_key is None:
        api_key = get_api_key()

    params = {
        'param1': param1
    }
    if param2 is not None:
        params['param2'] = param2

    url = build_api_url('/endpoint', params)
    data = make_api_request(url, api_key)

    return data
```

### 3. 命令行参数规范

```python
def main():
    parser = argparse.ArgumentParser(
        description='功能描述',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 示例 1
  python scripts/script.py --param value

  # 示例 2
  python scripts/script.py --option "value"
        """
    )

    parser.add_argument('--required-param', type=str, required=True,
                        help='必需参数说明')
    parser.add_argument('--optional-param', type=str,
                        help='可选参数说明')
    parser.add_argument('--flag-param', action='store_true',
                        help='标志参数说明')

    args = parser.parse_args()

    try:
        result = function_name(args.required_param, args.optional_param)
        print(format_result(result))

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### 4. 输出格式化

```python
def format_result(data: dict, limit: int = 10) -> str:
    """
    格式化输出结果。

    Args:
        data: API 返回数据
        limit: 最大显示数量

    Returns:
        格式化的字符串
    """
    output = []
    output.append("Header:")
    output.append("=" * 50)

    for item in data.get('items', [])[:limit]:
        name = item.get('name', 'N/A')
        output.append(f"- {name}")

    return '\n'.join(output)
```

---

## 使用示例

### 地址解析

```bash
python scripts/geocoding.py --address "北京市朝阳区阜通东大街6号"
```

### 路径规划

```bash
# 步行路线
python scripts/path_planning.py --origin "北京市天安门" --destination "北京市王府井" --mode walking

# 驾车路线
python scripts/path_planning.py --origin "116.482086,39.990496" --destination "116.410544,39.909836" --mode driving

# 公交路线
python scripts/path_planning.py --origin "北京市天安门" --destination "北京市王府井" --mode transit
```

### POI 搜索

```bash
python scripts/poi_search.py --keywords "餐厅" --city "北京市" --radius 1000
```

---

## 测试检查清单

开发完成后，请确保以下功能测试通过：

| 功能项 | 测试命令 | 预期结果 |
|--------|----------|----------|
| 依赖安装 | `pip install -r requirements.txt` | 成功安装，无错误 |
| 地址解析 | `geocoding.py --address "地址"` | 返回坐标 |
| 逆地址解析 | `geocoding.py --lon X --lat Y` | 返回地址 |
| 路径规划 | `path_planning.py --orgin A --dest B --mode driving` | 返回路线 |
| POI 搜索 | `poi_search.py --keywords "餐厅" --city "北京"` | 返回结果列表 |
| 错误处理 | 不带 API Key 运行 | 提示输入 API Key |
| 帮助文档 | `--help` 参数 | 显示完整帮助信息 |

---

## 常见问题

### 1. 导入错误

**问题：** `ImportError: cannot import name 'xxx' from '__init__'`

**解决：** 确保所有共享函数在 `__init__.py` 中定义，且函数名拼写正确。

### 2. API Key 未设置

**问题：** 提示 API Key 为空

**解决：**
```bash
export API_KEY=your_key_here
```

### 3. 类型比较错误

**问题：** `'>' not supported between instances of 'str' and 'int'`

**解决：** 对 API 返回的数据进行类型转换：
```python
count = int(data.get('count', 0))
```

### 4. 插件未生效

**问题：** 技能未出现在可用技能列表中

**解决：**
1. 检查 `installed_plugins.json` 是否正确配置
2. 删除 `.claude-plugin/.orphaned_at` 文件
3. 重启 Claude

---

## 参考资源

- Claude Skills 文档
- 高德地图开放平台：https://console.amap.com
- Python argparse 模块：https://docs.python.org/3/library/argparse.html

---

## 更新日志

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-02-01 | 初始版本，支持地址解析、路径规划、POI 搜索、IP 定位 |
