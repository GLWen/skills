## 目录结构
```bash
amap/
├── SKILL.md                      # 技能主文档
├── requirements.txt              # Python依赖
├── scripts/                      # 可执行脚本
│   ├── __init__.py               # 共享工具模块（API密钥管理）
│   ├── geocoding.py              # 地址解析/逆地址解析
│   ├── path_planning.py          # 路径规划（驾车/步行/骑行/公交）
│   ├── poi_search.py             # POI搜索
│   └── ip_location.py            # IP定位
└── references/
    └── api_reference.md          # 完整的API参考文档
```

主要特性
API密钥管理（两种方式）
1. 环境变量（推荐）：设置 AMAP_API_KEY 环境变量
2. 交互式输入：如果环境变量未配置，脚本会提示用户输入
支持的功能

脚本	功能	示例
geocoding.py	地址转坐标 / 坐标转地址	python scripts/geocoding.py --address "北京市朝阳区阜通东大街6号"
path_planning.py	路径规划（4种模式）	python scripts/path_planning.py --origin "北京市" --destination "上海市" --mode driving
poi_search.py	POI搜索	python scripts/poi_search.py --keywords "餐厅" --city "北京市" --radius 2000
ip_location.py	IP定位	python scripts/ip_location.py --ip 8.8.8.8

## 使用示例
```bash
# 设置API密钥（推荐）
export AMAP_API_KEY=your_api_key_here

# 地址解析
python scripts/geocoding.py --address "北京市朝阳区阜通东大街6号" --city "北京市"

# 逆地址解析
python scripts/geocoding.py --longitude 116.481485 --latitude 39.990464

# 驾车路径规划
python scripts/path_planning.py --origin "北京市" --destination "上海市" --mode driving

# POI搜索
python scripts/poi_search.py --keywords "餐厅" --city "北京市" --radius 1000

# IP定位
python scripts/ip_location.py --ip 114.114.114.114
```