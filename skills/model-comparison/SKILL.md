---
name: model-comparison
description: 对比分析主流大语言模型（MiniMax、GLM、DeepSeek、千问、Kimi）在代码、数学、中文、多语言、长上下文、逻辑推理、工具调用等多维度的能力表现，并生成表格、雷达图等可视化对比结果。
---

# 大模型能力对比分析

## 快速开始

当用户需要对比不同大模型能力时使用此技能。

**典型触发场景**：
- "MiniMax 和 DeepSeek 在代码生成方面哪个更强？"
- "Kimi 和千问的长上下文处理能力对比"
- "哪个模型理解上下文对意图识别更准确？"
- "帮我对比 GLM-4.7 和 qwen3-coder-plus 的数学推理能力"

## 对比能力维度

| 维度 | 说明 | 评分标准 |
|------|------|----------|
| 代码能力 | 编程任务、代码生成、调试 | 1-10分 |
| 数学推理 | 逻辑计算、公式推导 | 1-10分 |
| 中文理解 | 中文阅读理解、生成质量 | 1-10分 |
| 多语言能力 | 英文及多语言处理 | 1-10分 |
| 长上下文 | 大容量文本理解 | 1-10分 |
| 逻辑推理 | 归纳演绎、因果分析 | 1-10分 |
| 工具调用 | API调用、插件使用 | 1-10分 |
| 成本效率 | API价格、响应速度 | 1-10分 |

## 使用模式

### 模式1：单一维度对比

针对特定能力进行深入对比：
- 代码能力对比 → 读取 [BENCHMARKS.md](references/benchmarks.md) 中代码相关基准
- 数学能力对比 → 读取数学推理基准数据
- 长文本对比 → 对比上下文窗口和理解准确率

### 模式2：综合能力对比

生成多维度雷达图和综合评分：
- 运行 `scripts/generate_radar_chart.py` 生成可视化
- 运行 `scripts/generate_comparison_table.py` 生成表格

### 模式3：场景推荐

根据具体场景推荐最适合的模型：
- 代码密集型项目 → 推荐 DeepSeek / 千问
- 长文档处理 → 推荐 Kimi / 千问
- 中文内容创作 → 推荐 GLM / Kimi
- 多语言任务 → 推荐 DeepSeek / MiniMax

## 输出格式

根据用户需求选择输出形式：
- **表格对比**：`scripts/generate_comparison_table.py --format markdown`
- **雷达图**：`scripts/generate_radar_chart.py --output radar.png`
- **详细分析**：结合基准数据和实际表现撰写
- **综合评分**：加权评分模型 + 文字说明

## 模型清单

本技能支持以下模型对比：

1. **MiniMax M2.1** - MiniMax 公司开发
2. **GLM-4.7** - 智谱 AI 开发
3. **deepseek-chat** - DeepSeek 公司开发
4. **qwen3-coder-plus** - 阿里千问开发
5. **kimi-k2-thinking-turbo** - 月之暗面开发

### 详细信息

- 规格参数 → 参见 [MODEL_SPECS.md](references/model_specs.md)
- 能力指标说明 → 参见 [CAPABILITY_METRICS.md](references/capability_metrics.md)
- 基准测试结果 → 参见 [BENCHMARKS.md](references/benchmarks.md)

## 工作流程

```
1. 识别用户需求
   ↓
2. 选择对比维度（单维度/多维度）
   ↓
3. 收集相关基准数据
   ↓
4. 生成对比输出（表格/雷达图/文字）
   ↓
5. 给出推荐建议
```

## 资源说明

### scripts/
- `generate_comparison_table.py` - 生成 Markdown 表格对比
- `generate_radar_chart.py` - 生成雷达图可视化
- `analyze_capability.py` - 分析特定能力维度
- `recommend_model.py` - 基于场景推荐模型

### references/
- `model_specs.md` - 模型规格和 API 参数
- `capability_metrics.md` - 能力评估指标定义
- `benchmarks.md` - 各维度基准测试结果

### assets/
- `comparison_template.html` - HTML 对比模板
- `radar_chart_template.json` - 雷达图配置模板
