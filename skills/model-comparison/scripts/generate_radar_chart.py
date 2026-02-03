#!/usr/bin/env python3
"""
大模型能力雷达图生成器
使用 matplotlib 生成多维度能力雷达图
"""

import json
import math
import sys

# 模型能力数据
MODEL_CAPABILITIES = {
    "MiniMax M2.1": {
        "代码能力": 7.5,
        "数学推理": 7.2,
        "中文理解": 8.0,
        "多语言能力": 7.8,
        "长上下文": 7.5,
        "逻辑推理": 7.3,
        "工具调用": 7.0,
        "成本效率": 8.5,
    },
    "GLM-4.7": {
        "代码能力": 8.0,
        "数学推理": 7.8,
        "中文理解": 8.5,
        "多语言能力": 8.2,
        "长上下文": 8.0,
        "逻辑推理": 7.9,
        "工具调用": 8.0,
        "成本效率": 7.5,
    },
    "deepseek-chat": {
        "代码能力": 8.8,
        "数学推理": 8.5,
        "中文理解": 7.5,
        "多语言能力": 8.5,
        "长上下文": 7.0,
        "逻辑推理": 8.8,
        "工具调用": 7.5,
        "成本效率": 9.0,
    },
    "qwen3-coder-plus": {
        "代码能力": 9.0,
        "数学推理": 8.8,
        "中文理解": 7.8,
        "多语言能力": 8.8,
        "长上下文": 8.5,
        "逻辑推理": 8.5,
        "工具调用": 8.5,
        "成本效率": 8.0,
    },
    "kimi-k2-thinking-turbo": {
        "代码能力": 7.2,
        "数学推理": 7.5,
        "中文理解": 9.0,
        "多语言能力": 7.5,
        "长上下文": 9.5,
        "逻辑推理": 8.0,
        "工具调用": 6.5,
        "成本效率": 7.0,
    },
}

CAPABILITY_DIMENSIONS = [
    "代码能力",
    "数学推理",
    "中文理解",
    "多语言能力",
    "长上下文",
    "逻辑推理",
    "工具调用",
    "成本效率",
]

# 颜色配置
COLORS = {
    "MiniMax M2.1": "#3B82F6",
    "GLM-4.7": "#10B981",
    "deepseek-chat": "#EF4444",
    "qwen3-coder-plus": "#F59E0B",
    "kimi-k2-thinking-turbo": "#8B5CF6",
}


def generate_radar_config(selected_models: list = None) -> dict:
    """生成雷达图配置 JSON"""
    if selected_models is None:
        selected_models = list(MODEL_CAPABILITIES.keys())

    config = {
        "title": "大模型多维度能力对比",
        "dimensions": CAPABILITY_DIMENSIONS,
        "maxScore": 10,
        "models": [],
    }

    for model in selected_models:
        if model in MODEL_CAPABILITIES:
            config["models"].append({
                "name": model,
                "color": COLORS.get(model, "#666666"),
                "scores": [MODEL_CAPABILITIES[model].get(dim, 0) for dim in CAPABILITY_DIMENSIONS]
            })

    return config


def generate_html_radar_chart(config: dict) -> str:
    """生成 HTML 雷达图（使用 Chart.js）"""
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>大模型能力对比雷达图</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; max-width: 900px; margin: 0 auto; }
        h1 { text-align: center; color: #333; }
        .chart-container { position: relative; height: 600px; margin: 20px auto; }
        .legend { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-top: 20px; }
        .legend-item { display: flex; align-items: center; gap: 8px; }
        .color-box { width: 16px; height: 16px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>大模型多维度能力对比</h1>
    <div class="chart-container">
        <canvas id="radarChart"></canvas>
    </div>
    <div class="legend">
'''

    # 添加图例
    for model in config["models"]:
        html += f'''        <div class="legend-item">
            <div class="color-box" style="background-color: {model['color']}"></div>
            <span>{model['name']}</span>
        </div>
'''

    html += '''    </div>
    <script>
        const ctx = document.getElementById('radarChart').getContext('2d');
        const data = {
            labels: ''' + json.dumps(config["dimensions"], ensure_ascii=False) + ''',
            datasets: [
'''

    # 添加每个模型的数据集
    for i, model in enumerate(config["models"]):
        if i > 0:
            html += ",\n"
        html += f'''                {{
                    label: '{model["name"]}',
                    data: {json.dumps(model["scores"])},
                    backgroundColor: '{model["color"]}40',
                    borderColor: '{model["color"]}',
                    borderWidth: 2,
                    pointBackgroundColor: '{model["color"]}',
                }}
'''

    html += '''            ]
        };

        const config = {
            type: 'radar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: ''' + str(config["maxScore"]) + ''',
                        ticks: {
                            stepSize: 2,
                            font: { size: 12 }
                        },
                        pointLabels: {
                            font: { size: 14 }
                        }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        };

        new Chart(ctx, config);
    </script>
</body>
</html>'''

    return html


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="生成大模型能力雷达图")
    parser.add_argument("--models", nargs="+", help="指定要对比的模型")
    parser.add_argument("--output", "-o", default="radar_chart.html", help="输出文件路径")
    parser.add_argument("--format", choices=["html", "json"], default="html", help="输出格式")

    args = parser.parse_args()

    selected_models = args.models

    if args.format == "json":
        config = generate_radar_config(selected_models)
        print(json.dumps(config, indent=2, ensure_ascii=False))
    else:
        config = generate_radar_config(selected_models)
        html = generate_html_radar_chart(config)

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"雷达图已生成：{args.output}")
        print(f"对比模型：{', '.join(config['models'][m]['name'] for m in range(len(config['models'])))}")


if __name__ == "__main__":
    main()
