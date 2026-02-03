# Amap API Reference

Complete reference for Amap (AutoNavi/高德地图) Web Service API endpoints.

## Base URL

```
https://restapi.amap.com/v3
```

## Authentication

All API requests require an API key (`key` parameter).

### Methods to Provide API Key

1. **Environment variable (recommended)**: Set `AMAP_API_KEY`
2. **Interactive prompt**: Scripts will prompt if environment variable is not set

```bash
export AMAP_API_KEY=your_api_key_here
```

## API Endpoints

### 1. Geocoding API (地址解析)

**Endpoint**: `/geocode/geo`

**Purpose**: Convert structured address to geographic coordinates.

**Parameters**:
- `address` (required): Address string to geocode
- `city` (optional): City name to improve accuracy
- `key` (required): API key

**Request Example**:
```
GET https://restapi.amap.com/v3/geocode/geo?address=北京市朝阳区阜通东大街6号&city=北京市&key=YOUR_KEY
```

**Response Format**:
```json
{
  "status": "1",
  "info": "OK",
  "infocode": "10000",
  "geocodes": [
    {
      "formatted_address": "北京市朝阳区阜通东大街6号",
      "province": "北京市",
      "city": "北京市",
      "district": "朝阳区",
      "street": "阜通东大街",
      "number": "6号",
      "location": "116.481485,39.990464",
      "level": "门牌"
    }
  ]
}
```

---

### 2. Reverse Geocoding API (逆地址解析)

**Endpoint**: `/geocode/regeo`

**Purpose**: Convert coordinates to structured address.

**Parameters**:
- `location` (required): Coordinate string "longitude,latitude"
- `extensions` (optional): `base` (default) or `all` for detailed info
- `key` (required): API key

**Request Example**:
```
GET https://restapi.amap.com/v3/geocode/regeo?location=116.481485,39.990464&extensions=base&key=YOUR_KEY
```

**Response Format**:
```json
{
  "status": "1",
  "info": "OK",
  "infocode": "10000",
  "regeocode": {
    "formatted_address": "北京市朝阳区阜通东大街6号",
    "addressComponent": {
      "province": "北京市",
      "city": "北京市",
      "district": "朝阳区",
      "street": "阜通东大街",
      "streetNumber": "6号"
    }
  }
}
```

---

### 3. Driving Route Planning (驾车路径规划)

**Endpoint**: `/direction/driving`

**Purpose**: Plan driving route between two points.

**Parameters**:
- `origin` (required): Start coordinate "lon,lat"
- `destination` (required): End coordinate "lon,lat"
- `strategy` (optional): Route strategy (0-10, default 0)
  - 0: Speed priority
  - 1: Cost priority
  - 2: Distance priority
- `key` (required): API key

**Request Example**:
```
GET https://restapi.amap.com/v3/direction/driving?origin=116.481485,39.990464&destination=121.473701,31.230416&key=YOUR_KEY
```

**Response Format**:
```json
{
  "status": "1",
  "info": "OK",
  "infocode": "10000",
  "route": {
    "paths": [
      {
        "distance": "1200000",
        "duration": "43200",
        "tolls": "150",
        "toll_distance": "50000",
        "steps": [...]
      }
    ]
  }
}
```

---

### 4. Walking Route Planning (步行路径规划)

**Endpoint**: `/direction/walking`

**Purpose**: Plan walking route between two points.

**Parameters**: Same as driving API

**Request Example**:
```
GET https://restapi.amap.com/v3/direction/walking?origin=116.481485,39.990464&destination=116.485485,39.990464&key=YOUR_KEY
```

---

### 5. Cycling Route Planning (骑行路径规划)

**Endpoint**: `/direction/bicycling`

**Purpose**: Plan cycling route between two points.

**Parameters**: Same as driving API

**Request Example**:
```
GET https://restapi.amap.com/v3/direction/bicycling?origin=116.481485,39.990464&destination=116.485485,39.990464&key=YOUR_KEY
```

---

### 6. Transit Route Planning (公交路径规划)

**Endpoint**: `/direction/transit/integrated`

**Purpose**: Plan public transit route (bus, subway, etc.) between two points.

**Parameters**:
- `origin` (required): Start coordinate "lon,lat"
- `destination` (required): End coordinate "lon,lat"
- `city` (optional): City name (default: 全国)
- `cityd` (optional): Destination city name
- `key` (required): API key

**Request Example**:
```
GET https://restapi.amap.com/v3/direction/transit/integrated?origin=116.481485,39.990464&destination=116.485485,39.990464&city=北京市&key=YOUR_KEY
```

**Response Format**:
```json
{
  "status": "1",
  "info": "OK",
  "infocode": "10000",
  "route": {
    "transits": [
      {
        "duration": "3600",
        "distance": "15000",
        "cost": "5.0",
        "segments": [...]
      }
    ]
  }
}
```

---

### 7. POI Search (关键字搜索)

**Endpoint**: `/place/text`

**Purpose**: Search for Points of Interest by keywords.

**Parameters**:
- `keywords` (required): Search keywords
- `city` (required): City name
- `location` (optional): Center coordinate "lon,lat"
- `radius` (optional): Search radius in meters (default: 3000)
- `offset` (optional): Pagination offset (default: 0)
- `page` (optional): Page number (default: 1)
- `key` (required): API key

**Request Example**:
```
GET https://restapi.amap.com/v3/place/text?keywords=餐厅&city=北京市&location=116.481485,39.990464&radius=1000&key=YOUR_KEY
```

**Response Format**:
```json
{
  "status": "1",
  "info": "OK",
  "infocode": "10000",
  "count": "10",
  "pois": [
    {
      "id": "B000A85BAA",
      "name": "肯德基",
      "type": "餐饮服务;快餐服务",
      "address": "阜通东大街6号院1号楼",
      "location": "116.481485,39.990464",
      "tel": "010-64301234",
      "distance": "100"
    }
  ]
}
```

---

### 8. IP Location (IP定位)

**Endpoint**: `/ip`

**Purpose**: Get geographic location from IP address.

**Parameters**:
- `ip` (required): IP address
- `key` (required): API key

**Request Example**:
```
GET https://restapi.amap.com/v3/ip?ip=114.114.114.114&key=YOUR_KEY
```

**Response Format**:
```json
{
  "status": "1",
  "info": "OK",
  "infocode": "10000",
  "province": "北京",
  "city": "北京",
  "ip": "114.114.114.114",
  "rectangle": "116.0119343,39.66127144;116.7829835,40.2164962"
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 10000 | 请求正常 |
| 10001 | key不正确或过期 |
| 10002 | 没有权限使用相应的服务或请求接口的路径拼写错误 |
| 10003 | 访问已超出日访问限额 |
| 10004 | 单位时间内访问过于频繁 |
| 10005 | IP白名单限制，检查请求服务器IP是否在白名单内 |
| 10006 | 域名不合法，使用的协议、http/https错误 |
| 10007 | 权限不足，服务被禁用或未开通 |
| 20000 | 请求参数非法 |
| 20001 | 缺少必填参数 |
| 20002 | 请求协议非法 |
| 20003 | 其他未知错误 |
| 30000 | 配额超限 |
| 40000 | 服务异常 |

## Rate Limits

- **Daily quota**: 300,000 requests/day for individual accounts
- **QPS limit**: 100 requests/second for most services
- **Exceeding limits**: Returns error code 10003 (daily) or 10004 (QPS)

## Usage Quotas by Service

| Service | Daily Quota | QPS |
|---------|-------------|-----|
| Geocoding | 300,000 | 100 |
| Reverse Geocoding | 300,000 | 100 |
| Driving Route | 300,000 | 100 |
| Walking Route | 300,000 | 100 |
| Cycling Route | 300,000 | 100 |
| Transit Route | 300,000 | 100 |
| POI Search | 300,000 | 100 |
| IP Location | 300,000 | 100 |

## Best Practices

1. **Batch requests**: When processing multiple locations, batch requests where possible
2. **Cache results**: Cache frequently accessed locations to reduce API calls
3. **Retry logic**: Implement exponential backoff for network errors
4. **Error handling**: Always check `status` and `infocode` in responses
5. **Rate limiting**: Respect rate limits to avoid being blocked
6. **Use city parameter**: Always provide city parameter for geocoding to improve accuracy

## Official Documentation

For the most up-to-date documentation, visit:
- [Amap Web Service API](https://lbs.amap.com/api/webservice/summary)
- [Amap Console](https://console.amap.com/)
