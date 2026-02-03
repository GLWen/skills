---
name: amap
description: 高德地图服务工具包，支持地址解析、逆地址解析、路径规划、POI搜索和IP定位。当Claude需要处理以下任务时使用： (1) 将地址转换为经纬度（地址转经纬度/地理编码），(2) 将经纬度转换为地址（经纬度转地址/逆地理编码），(3) 规划路线和导航（路径规划/导航/驾车路线/步行路线/骑行路线/公交路线），(4) 搜索兴趣点如餐厅、酒店、加油站（POI搜索/查找附近的餐厅/酒店/加油站/兴趣点），(5) 通过IP地址获取位置（IP定位），(6) 计算位置之间的距离（距离计算），或任何涉及中国地图、位置服务或高德地图API的任务。当用户提到："地址"、"经纬度"、"坐标"、"导航"、"路线"、"附近"、"定位"、"高德地图"、"amap"、"查询"、"北京"、"上海"或任何中文位置/地理相关查询时触发
---

# 高德地图 (Amap)

与高德地图服务交互的工具包。提供地址解析、路径规划、POI搜索和位置服务的脚本。

## API Key 配置

此技能需要高德地图API密钥。支持两种方法：

1. **环境变量（推荐）**: 设置 `AMAP_API_KEY` 环境变量
2. **交互式提示**: 如果未设置环境变量，脚本会提示输入API密钥

设置环境变量：
```bash
export AMAP_API_KEY=your_api_key_here
```

## 可用脚本

使用 `--help` 参数查看完整用法：

- `scripts/geocoding.py` - 地址与坐标相互转换
- `scripts/path_planning.py` - 路径规划（驾车、步行、骑行、公交）
- `scripts/poi_search.py` - 在指定位置搜索兴趣点
- `scripts/ip_location.py` - IP地址转位置

## 快速开始示例

### 地址解析（地址 → 坐标）

```bash
python scripts/geocoding.py --address "北京市朝阳区阜通东大街6号"
```

### 逆地址解析（坐标 → 地址）

```bash
python scripts/geocoding.py --longitude 116.481485 --latitude 39.990464
```

### 驾车路线规划

```bash
python scripts/path_planning.py --origin "北京市" --destination "上海市" --mode driving
```

### 步行路线规划

```bash
python scripts/path_planning.py --origin "北京市天安门" --destination "北京市王府井" --mode walking
```

### POI搜索

```bash
python scripts/poi_search.py --keywords "餐厅" --city "北京市" --radius 1000
```

### IP定位

```bash
python scripts/ip_location.py --ip 8.8.8.8
```

## 脚本详情

### geocoding.py

处理地址到坐标的转换以及坐标到地址的转换。

**参数：**
- `--address`: 要解析的地址字符串（用于正向地理编码）
- `--longitude`: 经度（用于逆地理编码）
- `--latitude`: 纬度（用于逆地理编码）
- `--city`: 城市名称以提高精度（可选）

**示例：**
```bash
# 正向地理编码
python scripts/geocoding.py --address "北京市朝阳区阜通东大街6号" --city "北京市"

# 逆地理编码
python scripts/geocoding.py --longitude 116.481485 --latitude 39.990464
```

### path_planning.py

使用不同交通方式规划两个位置之间的路线。

**参数：**
- `--origin`: 起点地址或坐标（格式："经度,纬度"）
- `--destination`: 终点地址或坐标（格式："经度,纬度"）
- `--mode`: 交通方式：`driving`（驾车）、`walking`（步行）、`cycling`（骑行）、`transit`（公交）

**示例：**
```bash
# 地址到地址
python scripts/path_planning.py --origin "北京市" --destination "上海市" --mode driving

# 坐标到坐标
python scripts/path_planning.py --origin "116.481485,39.990464" --destination "121.473701,31.230416" --mode driving

# 地址到坐标
python scripts/path_planning.py --origin "北京市" --destination "121.473701,31.230416" --mode driving
```

### poi_search.py

在指定位置附近搜索兴趣点。

**参数：**
- `--keywords`: 搜索关键词
- `--city`: 城市名称（必需）
- `--longitude`: 中心经度（可选，默认为城市中心）
- `--latitude`: 中心纬度（可选，默认为城市中心）
- `--radius`: 搜索半径（米，默认1000）

**示例：**
```bash
# 在城市中心附近搜索
python scripts/poi_search.py --keywords "餐厅" --city "北京市" --radius 2000

# 在指定坐标附近搜索
python scripts/poi_search.py --keywords "加油站" --longitude 116.481485 --latitude 39.990464 --city "北京市" --radius 500
```

### ip_location.py

将IP地址转换为其地理位置。

**参数：**
- `--ip`: 要定位的IP地址

**示例：**
```bash
python scripts/ip_location.py --ip 8.8.8.8
```

## 错误处理

脚本处理常见错误：

- **缺少API密钥**: 如果未设置 `AMAP_API_KEY`，会交互式提示输入API密钥
- **无效参数**: 提供清晰的错误消息和正确用法
- **API错误**: 显示高德地图API的错误代码和消息
- **网络问题**: 超时和重试处理

## API参考

请参阅 `references/api_reference.md` 获取完整的高德地图API文档，包括：
- 所有可用的API端点
- 参数说明
- 响应格式
- 错误代码
- 速率限制
- 使用配额

## 最佳实践

1. **将API密钥设置为环境变量**，以便重复使用，避免重复输入
2. **使用city参数**进行地理编码，以提高常见地址名称的精度
3. **批量请求**，在处理多个位置时
4. **缓存结果**，对于频繁访问的位置
5. **优雅地处理错误**，并为网络问题实现重试逻辑
