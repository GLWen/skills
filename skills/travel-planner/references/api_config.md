# API Configuration Guide

## 高德地图 API (Amap)

### 申请步骤

1. 访问 [高德开放平台](https://lbs.amap.com/)
2. 注册/登录账号
3. 进入「控制台」→「应用管理」→「创建新应用」
4. 添加「Key」，勾选以下服务：
   - 搜索服务
   - 路线规划
   - 地理/逆地理编码
   - 天气查询
5. 复制 Web服务 API Key

### 免费额度

| 服务 | 免费调用量/日 |
|------|-------------|
| 地理编码 | 30,000 |
| 搜索 POI | 30,000 |
| 路线规划 | 30,000 |
| 天气查询 | 200,000 |

### 配置 API Key

```python
from scripts.api_config import set_api_key

# 设置高德地图 API Key
set_api_key("amap", "你的API Key")

# 验证配置
from scripts.api_config import check_api_keys
status = check_api_keys()
print(status)
```

## 环境变量方式

也可以通过环境变量配置：

```bash
export AMAP_API_KEY="你的API Key"
```

## 其他可选 API

### OpenRouteService (备选路线)
- 官网: https://openrouteservice.org/
- 免费额度: 有限制

### Amadeus (航班查询)
- 官网: https://developers.amadeus.com/
- 免费额度: 有限制
