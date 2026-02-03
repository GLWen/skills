#!/usr/bin/env python3
"""
大模型推荐工具
根据用户场景需求推荐最适合的模型
"""

import json

# 模型特性映射
MODEL_FEATURES = {
    "MiniMax M2.1": {
        "strengths": ["中文理解", "成本效率", "多语言能力"],
        "weaknesses": ["工具调用", "长上下文"],
        "best_for": ["日常对话", "文本处理", "成本敏感场景"],
        "context_window": "128K",
        "pricing": "低",
    },
    "GLM-4.7": {
        "strengths": ["中文理解", "代码能力", "工具调用"],
        "weaknesses": ["成本效率"],
        "best_for": ["企业应用", "中文内容创作", "多任务处理"],
        "context_window": "128K",
        "pricing": "中",
    },
    "deepseek-chat": {
        "strengths": ["代码能力", "数学推理", "逻辑推理", "成本效率"],
        "weaknesses": ["中文理解", "长上下文"],
        "best_for": ["代码开发", "技术分析", "成本敏感的技术项目"],
        "context_window": "64K",
        "pricing": "极低",
    },
    "qwen3-coder-plus": {
        "strengths": ["代码能力", "数学推理", "长上下文", "工具调用"],
        "weaknesses": ["中文理解"],
        "best_for": ["代码开发", "复杂推理", "长文档处理"],
        "context_window": "128K",
        "pricing": "中",
    },
    "kimi-k2-thinking-turbo": {
        "strengths": ["中文理解", "长上下文", "逻辑推理"],
        "weaknesses": ["工具调用", "成本效率"],
        "best_for": ["长文档理解", "中文创作", "深度分析"],
        "context_window": "200K+",
        "pricing": "中",
    },
}

# 场景需求映射
SCENARIO_REQUIREMENTS = {
    "代码密集型项目": ["代码能力", "数学推理", "工具调用"],
    "长文档处理": ["长上下文", "逻辑推理", "中文理解"],
    "中文内容创作": ["中文理解", "多语言能力"],
    "多语言任务": ["多语言能力", "中文理解"],
    "成本敏感场景": ["成本效率"],
    "技术分析": ["逻辑推理", "数学推理", "代码能力"],
    "企业应用": ["工具调用", "中文理解", "成本效率"],
    "日常对话": ["中文理解", "成本效率"],
}


def calculate_match_score(model: str, requirements: list) -> dict:
    """计算模型与需求的匹配度"""
    features = MODEL_FEATURES.get(model, {})
    strengths = features.get("strengths", [])
    scores = []

    for req in requirements:
        if req in strengths:
            scores.append(10)
        elif req in features.get("weaknesses", []):
            scores.append(3)
        else:
            scores.append(6)

    return {
        "model": model,
        "avg_score": sum(scores) / len(scores) if scores else 0,
        "matched": sum(1 for s in scores if s >= 8),
        "details": dict(zip(requirements, scores)),
    }


def recommend_for_scenario(scenario: str, top_n: int = 3) -> list:
    """根据场景推荐模型"""
    requirements = SCENARIO_REQUIREMENTS.get(scenario, ["代码能力", "中文理解"])

    results = []
    for model in MODEL_FEATURES:
        score_info = calculate_match_score(model, requirements)
        results.append(score_info)

    # 按匹配度排序
    results.sort(key=lambda x: (x["avg_score"], x["matched"]), reverse=True)

    return results[:top_n]


def interactive_recommend():
    """交互式推荐"""
    print("=== 大模型智能推荐 ===\n")

    print("可用场景：")
    for i, scenario in enumerate(SCENARIO_REQUIREMENTS.keys(), 1):
        print(f"  {i}. {scenario}")
    print("  0. 自定义需求")

    try:
        choice = input("\n请选择场景（输入编号）：").strip()

        if choice == "0":
            requirements = input("请输入需求关键词（空格分隔，如：代码能力 中文理解）：").split()
            if not requirements:
                print("未输入有效需求")
                return
        else:
            scenarios = list(SCENARIO_REQUIREMENTS.keys())
            if choice.isdigit() and 1 <= int(choice) <= len(scenarios):
                scenario = scenarios[int(choice) - 1]
                requirements = SCENARIO_REQUIREMENTS[scenario]
                print(f"\n选择场景：{scenario}")
                print(f"需求维度：{', '.join(requirements)}")
            else:
                print("无效选择")
                return

        print("\n推荐结果：\n")
        recommendations = recommend_for_scenario(requirements[0] if isinstance(requirements[0], str) else "", len(MODEL_FEATURES))

        for i, rec in enumerate(recommendations, 1):
            model = rec["model"]
            features = MODEL_FEATURES[model]
            print(f"{i}. {model}（匹配度：{rec['avg_score']:.1f}/10）")
            print(f"   优势：{', '.join(features['strengths'])}")
            print(f"   适用：{', '.join(features['best_for'])}")
            print(f"   上下文：{features['context_window']} | 定价：{features['pricing']}")
            print()

    except KeyboardInterrupt:
        print("\n已取消")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # 命令行模式
        scenario = " ".join(sys.argv[1:])
        results = recommend_for_scenario(scenario)

        print(f"场景：{scenario}\n")
        for i, rec in enumerate(results, 1):
            print(f"{i}. {rec['model']} - 匹配度：{rec['avg_score']:.1f}/10")
    else:
        # 交互模式
        interactive_recommend()
