"""
Travel Planner - Markdown Document Generator
Generates Markdown travel guide documents.
"""

from datetime import datetime
from pathlib import Path


def create_markdown_document(travel_data: dict, output_path: str = None) -> str:
    """
    Generate a Markdown document from travel planning data.

    Args:
        travel_data: Dictionary containing all travel information
        output_path: Optional output file path

    Returns:
        Path to generated file
    """
    lines = []

    # Title
    lines.append(f"# {travel_data.get('title', '旅游攻略')}")
    lines.append("")
    lines.append(f"**目的地**: {travel_data.get('destination', '')}  ")
    f"**行程天数**: {travel_data.get('duration', '')}天  "
    lines.append(f"**出行时间**: {travel_data.get('start_date', '')} - {travel_data.get('end_date', '')}  ")
    lines.append(f"**同行人员**: {travel_data.get('companions', '')}  ")
    lines.append(f"**总预算**: {travel_data.get('budget', '')}元  ")
    lines.append(f"**旅行主题**: {travel_data.get('theme', '')}")
    lines.append("")

    # Table of Contents
    lines.append("## 目录")
    lines.append("")
    lines.append("- [1. 行程概览](#1-行程概览)")
    lines.append("- [2. 目的地信息](#2-目的地信息)")
    lines.append("- [3. 详细行程](#3-详细行程)")
    lines.append("- [4. 住宿推荐](#4-住宿推荐)")
    lines.append("- [5. 美食推荐](#5-美食推荐)")
    lines.append("- [6. 交通指南](#6-交通指南)")
    lines.append("- [7. 预算规划](#7-预算规划)")
    lines.append("- [8. 注意事项](#8-注意事项)")
    lines.append("- [9. 天气预报](#9-天气预报)")
    lines.append("")

    # Section 1: Overview
    lines.append("## 1. 行程概览")
    lines.append("")
    lines.append(f"| 项目 | 内容 |")
    lines.append("|:---|:---|")
    lines.append(f"| 出行天数 | {travel_data.get('duration', 'N/A')}天 |")
    lines.append(f"| 同行人员 | {travel_data.get('companions', 'N/A')} |")
    lines.append(f"| 总预算 | {travel_data.get('budget', 'N/A')}元 |")
    lines.append(f"| 旅行主题 | {travel_data.get('theme', 'N/A')} |")
    lines.append("")

    # Section 2: Destination Info
    lines.append("## 2. 目的地信息")
    lines.append("")
    dest_info = travel_data.get("destination_info", {})
    if dest_info:
        lines.append(dest_info.get("description", ""))
    lines.append("")

    # Section 3: Itinerary
    lines.append("## 3. 详细行程")
    lines.append("")
    itinerary = travel_data.get("itinerary", [])
    if itinerary:
        for i, day in enumerate(itinerary, 1):
            lines.append(f"### 第{i}天: {day.get('date', f'Day {i}')}")
            lines.append("")

            morning = day.get("morning", {})
            if morning:
                lines.append(f"**上午**: {morning.get('activity', '')}")
                lines.append(f"- 时间: {morning.get('time', '')}")
                lines.append(f"- 地址: {morning.get('address', 'N/A')}")
                lines.append("")

            afternoon = day.get("afternoon", {})
            if afternoon:
                lines.append(f"**下午**: {afternoon.get('activity', '')}")
                lines.append(f"- 时间: {afternoon.get('time', '')}")
                lines.append(f"- 地址: {afternoon.get('address', 'N/A')}")
                lines.append("")

            evening = day.get("evening", {})
            if evening:
                lines.append(f"**晚上**: {evening.get('activity', '')}")
                lines.append(f"- 时间: {evening.get('time', '')}")
                lines.append(f"- 地址: {evening.get('address', 'N/A')}")
                lines.append("")

            meals = day.get("meals", {})
            if meals:
                lines.append("**用餐**:")
                lines.append(f"- 早餐: {meals.get('breakfast', '自理')}")
                lines.append(f"- 午餐: {meals.get('lunch', '自理')}")
                lines.append(f"- 晚餐: {meals.get('dinner', '自理')}")
                lines.append("")

            transport = day.get("transport", {})
            if transport:
                lines.append(f"**交通**: {transport.get('method', '')} - {transport.get('details', '')}")
                lines.append("")

    # Section 4: Hotels
    lines.append("## 4. 住宿推荐")
    lines.append("")
    hotels = travel_data.get("hotels", [])
    if hotels:
        for i, hotel in enumerate(hotels, 1):
            lines.append(f"### 推荐{i}: {hotel.get('name', 'N/A')}")
            lines.append("")
            lines.append(f"- **地址**: {hotel.get('address', 'N/A')}")
            lines.append(f"- **价格**: {hotel.get('price', 'N/A')}元/晚")
            lines.append(f"- **评分**: {hotel.get('rating', 'N/A')}分")
            lines.append(f"- **特色**: {hotel.get('features', 'N/A')}")
            lines.append("")
    else:
        lines.append("住宿规划中...")
        lines.append("")

    # Section 5: Food
    lines.append("## 5. 美食推荐")
    lines.append("")
    foods = travel_data.get("food_recommendations", [])
    if foods:
        for i, food in enumerate(foods, 1):
            lines.append(f"### {i}. {food.get('name', 'N/A')}")
            lines.append("")
            lines.append(f"- **类型**: {food.get('type', 'N/A')}")
            lines.append(f"- **地址**: {food.get('address', 'N/A')}")
            lines.append(f"- **人均**: {food.get('price_per_person', 'N/A')}元")
            lines.append(f"- **推荐菜**: {food.get('recommended_dishes', 'N/A')}")
            lines.append("")
    else:
        lines.append("美食推荐规划中...")
        lines.append("")

    # Section 6: Transportation
    lines.append("## 6. 交通指南")
    lines.append("")
    transport_info = travel_data.get("transport_info", {})
    if transport_info:
        getting_there = transport_info.get("getting_there", {})
        lines.append("### 到达方式")
        lines.append("")
        lines.append(f"- **方式**: {getting_there.get('method', 'N/A')}")
        lines.append(f"- **详情**: {getting_there.get('details', 'N/A')}")
        lines.append(f"- **预计时间**: {getting_there.get('duration', 'N/A')}")
        lines.append(f"- **费用**: {getting_there.get('cost', 'N/A')}元")
        lines.append("")

        local = transport_info.get("local_transport", [])
        if local:
            lines.append("### 当地交通")
            lines.append("")
            for item in local:
                lines.append(f"- **{item.get('type', '')}**: {item.get('description', '')}")
            lines.append("")
    else:
        lines.append("交通指南规划中...")
        lines.append("")

    # Section 7: Budget
    lines.append("## 7. 预算规划")
    lines.append("")
    budget = travel_data.get("budget_breakdown", {})
    if budget:
        lines.append(f"**总预算**: {budget.get('total', 'N/A')}元")
        lines.append("")
        lines.append("| 类别 | 预算金额 |")
        lines.append("|:---|:---:|")
        lines.append(f"| 交通 | {budget.get('transport', 0)}元 |")
        lines.append(f"| 住宿 | {budget.get('accommodation', 0)}元 |")
        lines.append(f"| 餐饮 | {budget.get('food', 0)}元 |")
        lines.append(f"| 门票 | {budget.get('tickets', 0)}元 |")
        lines.append(f"| 购物 | {budget.get('shopping', 0)}元 |")
        lines.append(f"| 其他 | {budget.get('other', 0)}元 |")
        lines.append("")
    else:
        lines.append("预算规划中...")
        lines.append("")

    # Section 8: Notes
    lines.append("## 8. 注意事项")
    lines.append("")
    notes = travel_data.get("notes", [])
    if notes:
        for note in notes:
            lines.append(f"- [ ] {note}")
        lines.append("")
    else:
        lines.append("注意事项规划中...")
        lines.append("")

    # Section 9: Weather
    lines.append("## 9. 天气预报")
    lines.append("")
    weather = travel_data.get("weather", {})
    if weather:
        lines.append(f"**目的地**: {weather.get('city', 'N/A')}")
        lines.append("")

        current = weather.get("current", {})
        if current:
            lines.append("### 当前天气")
            lines.append("")
            lines.append(f"- 天气: {current.get('weather', 'N/A')}")
            lines.append(f"- 温度: {current.get('temperature', 'N/A')}°C")
            lines.append(f"- 湿度: {current.get('humidity', 'N/A')}%")
            lines.append(f"- 风向: {current.get('wind_direction', 'N/A')} {current.get('wind_power', 'N/A')}级")
            lines.append("")

        forecast = weather.get("forecast", [])
        if forecast:
            lines.append("### 天气预报")
            lines.append("")
            lines.append("| 日期 | 星期 | 白天 | 夜间 | 温度 |")
            lines.append("|:---|:---|:---|:---|:---:|")
            for day in forecast:
                lines.append(f"| {day.get('date', '')} | {day.get('week', '')} | "
                           f"{day.get('day_weather', '')} | {day.get('night_weather', '')} | "
                           f"{day.get('night_temp', 'N/A')}°C ~ {day.get('day_temp', 'N/A')}°C |")
            lines.append("")
    else:
        lines.append("天气信息获取中...")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Travel Planner*")

    # Join lines
    content = "\n".join(lines)

    # Save
    if not output_path:
        destination = travel_data.get("destination", "travel").replace(" ", "_")
        start_date = travel_data.get("start_date", "").replace("-", "")
        output_path = f"travel_guide_{destination}_{start_date}.md"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_path


def generate_sample_travel_data() -> dict:
    """Generate sample travel data for testing."""
    from generate_word import generate_sample_travel_data
    return generate_sample_travel_data()


if __name__ == "__main__":
    sample_data = generate_sample_travel_data()
    output_file = create_markdown_document(sample_data)
    print(f"Generated: {output_file}")
