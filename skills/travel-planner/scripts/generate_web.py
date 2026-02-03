"""
Travel Planner - Web Page Generator
Generates interactive HTML travel guide pages with animations and charts.
"""

import json
from pathlib import Path
from datetime import datetime


def create_web_page(travel_data: dict, output_path: str = None) -> str:
    """
    Generate an interactive HTML travel guide page.

    Args:
        travel_data: Dictionary containing all travel information
        output_path: Optional output file path

    Returns:
        Path to generated file
    """
    html_content = build_html_content(travel_data)

    if not output_path:
        destination = travel_data.get("destination", "travel").replace(" ", "_")
        output_path = f"travel_guide_{destination}.html"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path


def build_html_content(travel_data: dict) -> str:
    """Build complete HTML content for travel guide."""

    destination = travel_data.get("destination", "旅游目的地")
    itinerary = travel_data.get("itinerary", [])
    budget = travel_data.get("budget_breakdown", {})

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{travel_data.get('title', '旅游攻略')} - {destination}</title>
    <style>
        :root {{
            --primary: #3498db;
            --secondary: #2ecc71;
            --accent: #e74c3c;
            --dark: #2c3e50;
            --light: #ecf0f1;
            --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: var(--light);
            color: var(--dark);
            line-height: 1.6;
        }}

        /* Hero Section */
        .hero {{
            background: var(--gradient);
            min-height: 60vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: white;
            position: relative;
            overflow: hidden;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>');
            animation: float 20s infinite linear;
        }}

        @keyframes float {{
            0% {{ transform: translateY(0); }}
            100% {{ transform: translateY(-100px); }}
        }}

        .hero-content {{
            position: relative;
            z-index: 1;
            padding: 2rem;
        }}

        .hero h1 {{
            font-size: 3.5rem;
            margin-bottom: 1rem;
            animation: fadeInDown 1s ease;
        }}

        .hero .subtitle {{
            font-size: 1.5rem;
            opacity: 0.9;
            animation: fadeInUp 1s ease 0.3s both;
        }}

        .hero .meta {{
            margin-top: 2rem;
            display: flex;
            gap: 2rem;
            justify-content: center;
            flex-wrap: wrap;
            animation: fadeIn 1s ease 0.6s both;
        }}

        .meta-item {{
            background: rgba(255,255,255,0.2);
            padding: 0.8rem 1.5rem;
            border-radius: 30px;
            backdrop-filter: blur(10px);
        }}

        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        /* Container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        /* Section Styles */
        .section {{
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .section:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        }}

        .section h2 {{
            color: var(--primary);
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid var(--primary);
            display: inline-block;
        }}

        /* Timeline */
        .timeline {{
            position: relative;
            padding-left: 30px;
        }}

        .timeline::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: linear-gradient(to bottom, var(--primary), var(--secondary));
            border-radius: 2px;
        }}

        .timeline-item {{
            position: relative;
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: var(--light);
            border-radius: 15px;
            transition: all 0.3s ease;
        }}

        .timeline-item:hover {{
            background: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}

        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -36px;
            top: 50%;
            transform: translateY(-50%);
            width: 16px;
            height: 16px;
            background: var(--primary);
            border-radius: 50%;
            border: 4px solid white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}

        .day-header {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }}

        .day-badge {{
            background: var(--gradient);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
        }}

        .day-date {{
            color: #666;
            font-size: 0.9rem;
        }}

        .activity-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}

        .activity-card {{
            background: white;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid var(--primary);
        }}

        .activity-card.morning {{ border-left-color: #f39c12; }}
        .activity-card.afternoon {{ border-left-color: #2ecc71; }}
        .activity-card.evening {{ border-left-color: #9b59b6; }}

        .activity-time {{
            font-size: 0.8rem;
            color: #999;
            margin-bottom: 0.3rem;
        }}

        .activity-name {{
            font-weight: bold;
            color: var(--dark);
        }}

        .activity-address {{
            font-size: 0.85rem;
            color: #666;
            margin-top: 0.3rem;
        }}

        /* Budget Chart */
        .budget-chart {{
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
            align-items: center;
        }}

        .budget-visual {{
            flex: 1;
            min-width: 250px;
        }}

        .budget-bar {{
            height: 40px;
            background: var(--light);
            border-radius: 20px;
            margin: 0.5rem 0;
            overflow: hidden;
            position: relative;
        }}

        .budget-bar-fill {{
            height: 100%;
            border-radius: 20px;
            transition: width 1s ease;
            display: flex;
            align-items: center;
            padding-left: 1rem;
            color: white;
            font-weight: bold;
            min-width: fit-content;
        }}

        .budget-legend {{
            flex: 1;
            min-width: 200px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0.5rem 0;
        }}

        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 5px;
        }}

        /* Cards Grid */
        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
        }}

        .card {{
            background: var(--light);
            border-radius: 15px;
            overflow: hidden;
            transition: transform 0.3s ease;
        }}

        .card:hover {{
            transform: translateY(-10px);
        }}

        .card-image {{
            height: 150px;
            background: var(--gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 3rem;
        }}

        .card-content {{
            padding: 1.5rem;
        }}

        .card-title {{
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
            color: var(--dark);
        }}

        .card-meta {{
            display: flex;
            gap: 1rem;
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }}

        .card-desc {{
            color: #555;
            font-size: 0.9rem;
        }}

        .rating {{
            color: #f39c12;
        }}

        /* Weather Widget */
        .weather-widget {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }}

        .weather-day {{
            text-align: center;
            padding: 1rem;
            background: var(--light);
            border-radius: 10px;
            transition: transform 0.3s ease;
        }}

        .weather-day:hover {{
            transform: scale(1.05);
        }}

        .weather-icon {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}

        .weather-temp {{
            font-size: 1.2rem;
            font-weight: bold;
            color: var(--primary);
        }}

        /* Notes List */
        .notes-list {{
            list-style: none;
        }}

        .notes-list li {{
            padding: 1rem;
            margin: 0.5rem 0;
            background: var(--light);
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .notes-list li:hover {{
            background: white;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .notes-list input[type="checkbox"] {{
            width: 20px;
            height: 20px;
            accent-color: var(--primary);
        }}

        /* Footer */
        footer {{
            text-align: center;
            padding: 3rem;
            background: var(--dark);
            color: white;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 2rem; }}
            .hero .meta {{ flex-direction: column; gap: 1rem; }}
            .budget-chart {{ flex-direction: column; }}
        }}
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <h1>{travel_data.get('title', '旅游攻略')}</h1>
            <p class="subtitle">探索 {destination} 的精彩之旅</p>
            <div class="meta">
                <div class="meta-item">📅 {travel_data.get('duration', '')}天</div>
                <div class="meta-item">👥 {travel_data.get('companions', '')}</div>
                <div class="meta-item">💰 {travel_data.get('budget', '')}元</div>
                <div class="meta-item">🎯 {travel_data.get('theme', '')}</div>
            </div>
        </div>
    </section>

    <div class="container">
        <!-- Overview -->
        <section class="section">
            <h2>📋 行程概览</h2>
            <p style="margin: 1rem 0;">
                <strong>出行时间：</strong>{travel_data.get('start_date', '')} 至 {travel_data.get('end_date', '')}
            </p>
            <p>
                <strong>目的地介绍：</strong>{travel_data.get('destination_info', {}).get('description', '')}
            </p>
        </section>

        <!-- Itinerary Timeline -->
        <section class="section">
            <h2>📅 详细行程</h2>
            <div class="timeline">
                {build_timeline_html(itinerary)}
            </div>
        </section>

        <!-- Hotels -->
        <section class="section">
            <h2>🏨 住宿推荐</h2>
            <div class="cards-grid">
                {build_hotels_html(travel_data.get('hotels', []))}
            </div>
        </section>

        <!-- Food -->
        <section class="section">
            <h2>🍜 美食推荐</h2>
            <div class="cards-grid">
                {build_food_html(travel_data.get('food_recommendations', []))}
            </div>
        </section>

        <!-- Transportation -->
        <section class="section">
            <h2>🚗 交通指南</h2>
            {build_transport_html(travel_data.get('transport_info', {}))}
        </section>

        <!-- Budget -->
        <section class="section">
            <h2>💰 预算规划</h2>
            <p style="margin-bottom: 1rem;"><strong>总预算：</strong>{budget.get('total', 0)}元</p>
            <div class="budget-chart">
                <div class="budget-visual">
                    {build_budget_bars(budget)}
                </div>
                <div class="budget-legend">
                    {build_budget_legend()}
                </div>
            </div>
        </section>

        <!-- Weather -->
        <section class="section">
            <h2>🌤️ 天气预报</h2>
            <div class="weather-widget">
                {build_weather_html(travel_data.get('weather', {}))}
            </div>
        </section>

        <!-- Notes -->
        <section class="section">
            <h2>📝 注意事项</h2>
            <ul class="notes-list">
                {build_notes_html(travel_data.get('notes', []))}
            </ul>
        </section>
    </div>

    <!-- Footer -->
    <footer>
        <p>Generated by Travel Planner</p>
        <p style="opacity: 0.7; margin-top: 0.5rem;">
            生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </p>
    </footer>

    <script>
        // Smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});

        // Animate budget bars on scroll
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.width = entry.target.dataset.width;
                }}
            }});
        }}, {{ threshold: 0.5 }});

        document.querySelectorAll('.budget-bar-fill').forEach(bar => {{
            observer.observe(bar);
        }});

        // Checkbox toggle
        document.querySelectorAll('.notes-list li').forEach(item => {{
            item.addEventListener('click', () => {{
                item.style.opacity = item.style.opacity === '0.5' ? '1' : '0.5';
            }});
        }});
    </script>
</body>
</html>"""


def build_timeline_html(itinerary: list) -> str:
    """Build HTML for itinerary timeline."""
    if not itinerary:
        return '<p>行程规划中...</p>'

    html = ""
    for i, day in enumerate(itinerary, 1):
        html += f"""
        <div class="timeline-item">
            <div class="day-header">
                <span class="day-badge">第{i}天</span>
                <span class="day-date">{day.get('date', '')}</span>
            </div>
            <div class="activity-grid">
        """

        morning = day.get("morning", {})
        if morning:
            html += f"""
            <div class="activity-card morning">
                <div class="activity-time">🌅 上午</div>
                <div class="activity-name">{morning.get('activity', '')}</div>
                <div class="activity-address">📍 {morning.get('address', 'N/A')}</div>
                <div class="activity-address">🕐 {morning.get('time', '')}</div>
            </div>
            """

        afternoon = day.get("afternoon", {})
        if afternoon:
            html += f"""
            <div class="activity-card afternoon">
                <div class="activity-time">☀️ 下午</div>
                <div class="activity-name">{afternoon.get('activity', '')}</div>
                <div class="activity-address">📍 {afternoon.get('address', 'N/A')}</div>
                <div class="activity-address">🕐 {afternoon.get('time', '')}</div>
            </div>
            """

        evening = day.get("evening", {})
        if evening:
            html += f"""
            <div class="activity-card evening">
                <div class="activity-time">🌙 晚上</div>
                <div class="activity-name">{evening.get('activity', '')}</div>
                <div class="activity-address">📍 {evening.get('address', 'N/A')}</div>
                <div class="activity-address">🕐 {evening.get('time', '')}</div>
            </div>
            """

        html += "</div></div>"

    return html


def build_hotels_html(hotels: list) -> str:
    """Build HTML for hotel cards."""
    if not hotels:
        return '<p>住宿规划中...</p>'

    html = ""
    for hotel in hotels:
        html += f"""
        <div class="card">
            <div class="card-image">🏨</div>
            <div class="card-content">
                <h3 class="card-title">{hotel.get('name', 'N/A')}</h3>
                <div class="card-meta">
                    <span class="rating">⭐ {hotel.get('rating', 'N/A')}</span>
                    <span>💰 {hotel.get('price', 'N/A')}元/晚</span>
                </div>
                <p class="card-desc">📍 {hotel.get('address', 'N/A')}</p>
                <p class="card-desc">✨ {hotel.get('features', 'N/A')}</p>
            </div>
        </div>
        """
    return html


def build_food_html(foods: list) -> str:
    """Build HTML for food cards."""
    if not foods:
        return '<p>美食推荐规划中...</p>'

    html = ""
    for i, food in enumerate(foods, 1):
        html += f"""
        <div class="card">
            <div class="card-image">🍽️</div>
            <div class="card-content">
                <h3 class="card-title">{food.get('name', 'N/A')}</h3>
                <div class="card-meta">
                    <span>🍴 {food.get('type', 'N/A')}</span>
                    <span>💰 {food.get('price_per_person', 'N/A')}元/人</span>
                </div>
                <p class="card-desc">📍 {food.get('address', 'N/A')}</p>
                <p class="card-desc">⭐ 推荐: {food.get('recommended_dishes', 'N/A')}</p>
            </div>
        </div>
        """
    return html


def build_transport_html(transport_info: dict) -> str:
    """Build HTML for transportation info."""
    if not transport_info:
        return '<p>交通指南规划中...</p>'

    getting_there = transport_info.get("getting_there", {})
    html = f"""
    <h3 style="margin: 1rem 0;">✈️ 到达方式</h3>
    <p><strong>方式：</strong>{getting_there.get('method', 'N/A')}</p>
    <p><strong>详情：</strong>{getting_there.get('details', 'N/A')}</p>
    <p><strong>预计时间：</strong>{getting_there.get('duration', 'N/A')}</p>
    <p><strong>费用：</strong>{getting_there.get('cost', 'N/A')}元</p>
    """

    local = transport_info.get("local_transport", [])
    if local:
        html += '<h3 style="margin: 1.5rem 0 0.5rem;">🚌 当地交通</h3><ul style="list-style: none;">'
        for item in local:
            html += f'<li>• <strong>{item.get("type", "")}</strong>: {item.get("description", "")}</li>'
        html += '</ul>'

    return html


def build_budget_bars(budget: dict) -> str:
    """Build HTML for budget progress bars."""
    if not budget:
        return '<p>预算规划中...</p>'

    total = budget.get("total", 1)
    categories = [
        ("交通", budget.get("transport", 0), "#3498db"),
        ("住宿", budget.get("accommodation", 0), "#2ecc71"),
        ("餐饮", budget.get("food", 0), "#f39c12"),
        ("门票", budget.get("tickets", 0), "#e74c3c"),
        ("购物", budget.get("shopping", 0), "#9b59b6"),
    ]

    html = ""
    for name, amount, color in categories:
        percentage = (amount / total * 100) if total > 0 else 0
        html += f"""
        <div class="budget-bar">
            <div class="budget-bar-fill" style="width: 0%; background: {color};"
                 data-width="{percentage}%">
                {name}: {amount}元 ({percentage:.1f}%)
            </div>
        </div>
        """
    return html


def build_budget_legend() -> str:
    """Build HTML for budget legend."""
    return """
    <div class="legend-item">
        <div class="legend-color" style="background: #3498db;"></div>
        <span>交通</span>
    </div>
    <div class="legend-item">
        <div class="legend-color" style="background: #2ecc71;"></div>
        <span>住宿</span>
    </div>
    <div class="legend-item">
        <div class="legend-color" style="background: #f39c12;"></div>
        <span>餐饮</span>
    </div>
    <div class="legend-item">
        <div class="legend-color" style="background: #e74c3c;"></div>
        <span>门票</span>
    </div>
    <div class="legend-item">
        <div class="legend-color" style="background: #9b59b6;"></div>
        <span>购物</span>
    </div>
    """


def build_weather_html(weather: dict) -> str:
    """Build HTML for weather forecast."""
    if not weather:
        return '<p>天气信息获取中...</p>'

    current = weather.get("current", {})
    forecast = weather.get("forecast", [])

    html = ""

    if current:
        html += f"""
        <div class="weather-day" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white;">
            <div class="weather-icon">☀️</div>
            <div style="font-weight: bold;">当前天气</div>
            <div class="weather-temp" style="color: white;">{current.get('temperature', 'N/A')}°C</div>
            <div>{current.get('weather', 'N/A')}</div>
        </div>
        """

    weather_icons = {"晴": "☀️", "多云": "☁️", "阴": "🌥️", "小雨": "🌦️", "中雨": "🌧️", "大雨": "⛈️"}

    for day in forecast[:5]:
        icon = weather_icons.get(day.get("day_weather", ""), "🌤️")
        html += f"""
        <div class="weather-day">
            <div class="weather-icon">{icon}</div>
            <div style="font-weight: bold;">{day.get('date', '')}</div>
            <div style="color: #666;">{day.get('week', '')}</div>
            <div class="weather-temp">{day.get('night_temp', 'N/A')}°C ~ {day.get('day_temp', 'N/A')}°C</div>
            <div style="font-size: 0.8rem; color: #999;">{day.get('day_weather', '')}</div>
        </div>
        """

    return html


def build_notes_html(notes: list) -> str:
    """Build HTML for notes/checklist."""
    if not notes:
        return '<p>注意事项规划中...</p>'

    html = ""
    for note in notes:
        html += f'<li><input type="checkbox"> <span>{note}</span></li>'
    return html


def generate_sample_travel_data() -> dict:
    """Generate sample travel data for testing."""
    from generate_word import generate_sample_travel_data
    return generate_sample_travel_data()


if __name__ == "__main__":
    sample_data = generate_sample_travel_data()
    output_file = create_web_page(sample_data)
    print(f"Generated: {output_file}")
