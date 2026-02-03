# Travel Guide Content Template

## 数据结构

### 必填字段

| 字段名 | 类型 | 说明 | 示例 |
|-------|------|------|------|
| `title` | string | 攻略标题 | "杭州三日游攻略" |
| `destination` | string | 目的地 | "杭州" |
| `start_date` | string | 开始日期 | "2024-03-15" |
| `end_date` | string | 结束日期 | "2024-03-17" |
| `duration` | int | 天数 | 3 |
| `companions` | string | 同行人员 | "2人情侣" |
| `budget` | float | 总预算 | 3000 |

### 选填字段

| 字段名 | 类型 | 说明 |
|-------|------|------|
| `theme` | string | 旅行主题 |
| `destination_info` | object | 目的地介绍 |
| `itinerary` | array | 每日行程 |
| `hotels` | array | 推荐酒店 |
| `food_recommendations` | array | 美食推荐 |
| `transport_info` | object | 交通信息 |
| `budget_breakdown` | object | 预算明细 |
| `notes` | array | 注意事项 |
| `weather` | object | 天气信息 |

### 详细数据结构

#### destination_info

```python
{
    "description": "杭州是中国著名的历史文化名城...",
    "highlights": ["西湖", "灵隐寺", "河坊街"],
    "best_season": "春季(3-5月)、秋季(9-11月)"
}
```

#### itinerary 每日行程

```python
{
    "date": "2024-03-15",
    "morning": {
        "activity": "西湖游船",
        "time": "9:00-12:00",
        "address": "西湖游船码头",
        "duration": "3小时",
        "tips": "建议提前网上购票"
    },
    "afternoon": {
        "activity": "灵隐寺",
        "time": "14:00-17:00",
        "address": "灵隐路法云弄1号"
    },
    "evening": {
        "activity": "河坊街夜市",
        "time": "18:30-21:00",
        "address": "河坊街"
    },
    "meals": {
        "breakfast": "酒店早餐",
        "lunch": "灵隐寺素斋",
        "dinner": "知味观"
    },
    "transport": {
        "method": "地铁+步行",
        "details": "地铁1号线到龙翔桥站"
    }
}
```

#### hotels 推荐酒店

```python
{
    "name": "杭州西子湖四季酒店",
    "address": "西湖区灵隐路5号",
    "price": 1800,
    "rating": 4.9,
    "features": ["西湖景区内", "独栋别墅", "管家服务"],
    "booking_url": "https://...",
    "phone": "0571-12345678"
}
```

#### food_recommendations 美食

```python
{
    "name": "外婆家",
    "type": "杭帮菜",
    "address": "西湖区外婆家各分店",
    "price_per_person": 80,
    "recommended_dishes": ["西湖醋鱼", "东坡肉", "龙井虾仁"],
    "average_cost": 150,
    "must_try": ["糖醋里脊"]
}
```

#### transport_info 交通

```python
{
    "getting_there": {
        "method": "高铁",
        "from": "上海虹桥",
        "to": "杭州东站",
        "duration": "45分钟",
        "cost": 73,
        "booking_tips": "建议提前1周购票"
    },
    "local_transport": [
        {"type": "地铁", "description": "支持支付宝二维码", "cost": "2元起"},
        {"type": "出租车", "description": "11元起步", "tips": "晚高峰可能拥堵"},
        {"type": "共享单车", "description": "哈啰/美团", "cost": "1.5元/30分钟"}
    ]
}
```

#### budget_breakdown 预算

```python
{
    "total": 3000,
    "transport": 500,
    "accommodation": 1200,
    "food": 600,
    "tickets": 400,
    "shopping": 200,
    "other": 100,
    "currency": "CNY"
}
```

#### notes 注意事项

```python
[
    "西湖游船建议提前在网上购票",
    "3月是杭州旅游旺季，酒店需提前预订",
    "龙井村采茶体验需提前预约"
]
```

#### weather 天气

```python
{
    "city": "杭州",
    "report_time": "2024-03-15 08:00",
    "current": {
        "weather": "多云",
        "temperature": 15,
        "humidity": 60,
        "wind_direction": "东风",
        "wind_power": "3"
    },
    "forecast": [
        {
            "date": "2024-03-15",
            "week": "周五",
            "day_weather": "多云",
            "night_weather": "晴",
            "day_temp": 18,
            "night_temp": 10
        }
    ]
}
```

## 输出示例

### 快速生成完整攻略

```python
from scripts.generate_word import create_word_document
from scripts.generate_markdown import create_markdown_document
from scripts.generate_web import create_web_page

travel_data = {
    "title": "杭州旅游攻略",
    "destination": "杭州",
    "duration": 3,
    "start_date": "2024-03-15",
    "end_date": "2024-03-17",
    "companions": "2人（情侣）",
    "budget": 3000,
    "theme": "休闲文化游",
    # ... 其他字段
}

# 生成 Word 文档
create_word_document(travel_data, "hangzhou_travel.docx")

# 生成 Markdown
create_markdown_document(travel_data, "hangzhou_travel.md")

# 生成 Web 页面
create_web_page(travel_data, "hangzhou_travel.html")
```
