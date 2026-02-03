# 基准测试结果参考

## 综合能力对比

| 模型 | 代码 | 数学 | 中文 | 多语言 | 长上下文 | 逻辑 | 工具调用 | 成本效率 |
|------|------|------|------|--------|----------|------|----------|----------|
| MiniMax M2.1 | 7.5 | 7.2 | 8.0 | 7.8 | 7.5 | 7.3 | 7.0 | 8.5 |
| GLM-4.7 | 8.0 | 7.8 | 8.5 | 8.2 | 8.0 | 7.9 | 8.0 | 7.5 |
| DeepSeek Chat | 8.8 | 8.5 | 7.5 | 8.5 | 7.0 | 8.8 | 7.5 | 9.0 |
| Qwen3 Coder Plus | 9.0 | 8.8 | 7.8 | 8.8 | 8.5 | 8.5 | 8.5 | 8.0 |
| Kimi K2 Thinking | 7.2 | 7.5 | 9.0 | 7.5 | 9.5 | 8.0 | 6.5 | 7.0 |

---

## 代码能力详细对比

| 模型 | HumanEval | MBPP | 代码生成质量 | 多语言编程 |
|------|-----------|------|--------------|------------|
| MiniMax M2.1 | 65% | 60% | 良好 | 中等 |
| GLM-4.7 | 72% | 68% | 良好 | 良好 |
| DeepSeek Chat | 78% | 75% | 优秀 | 优秀 |
| Qwen3 Coder Plus | 82% | 80% | 优秀 | 优秀 |
| Kimi K2 Thinking | 58% | 55% | 良好 | 一般 |

**代码能力推荐**：
- 首选：Qwen3 Coder Plus、DeepSeek Chat
- 次选：GLM-4.7

---

## 数学推理详细对比

| 模型 | GSM8K | MATH | 复杂推理 | 计算准确性 |
|------|-------|------|----------|------------|
| MiniMax M2.1 | 75% | 45% | 良好 | 高 |
| GLM-4.7 | 78% | 48% | 良好 | 高 |
| DeepSeek Chat | 85% | 55% | 优秀 | 很高 |
| Qwen3 Coder Plus | 88% | 58% | 优秀 | 很高 |
| Kimi K2 Thinking | 72% | 42% | 良好 | 高 |

**数学推理推荐**：
- 首选：Qwen3 Coder Plus、DeepSeek Chat
- 关注性价比：MiniMax M2.1

---

## 中文理解详细对比

| 模型 | CMMLU | C-Eval | 中文创作 | 成语典故 |
|------|-------|--------|----------|----------|
| MiniMax M2.1 | 82% | 80% | 优秀 | 良好 |
| GLM-4.7 | 85% | 83% | 优秀 | 优秀 |
| DeepSeek Chat | 72% | 70% | 一般 | 一般 |
| Qwen3 Coder Plus | 75% | 73% | 良好 | 一般 |
| Kimi K2 Thinking | 90% | 88% | 卓越 | 优秀 |

**中文理解推荐**：
- 首选：Kimi K2 Thinking、GLM-4.7
- 性价比之选：MiniMax M2.1

---

## 长上下文处理对比

| 模型 | 上下文窗口 | 大海捞针准确率 | 长文档问答 | 总结质量 |
|------|------------|----------------|------------|----------|
| MiniMax M2.1 | 128K | 85% | 良好 | 良好 |
| GLM-4.7 | 128K | 88% | 良好 | 良好 |
| DeepSeek Chat | 64K | 82% | 一般 | 一般 |
| Qwen3 Coder Plus | 128K | 90% | 优秀 | 优秀 |
| Kimi K2 Thinking | 200K+ | 95% | 卓越 | 卓越 |

**长上下文推荐**：
- 首选：Kimi K2 Thinking（200K+ 上下文）
- 代码场景：Qwen3 Coder Plus

---

## 逻辑推理对比

| 模型 | LogiQA | ReClor | 演绎推理 | 归纳推理 |
|------|--------|--------|----------|----------|
| MiniMax M2.1 | 68% | 65% | 良好 | 良好 |
| GLM-4.7 | 70% | 68% | 良好 | 良好 |
| DeepSeek Chat | 78% | 75% | 优秀 | 优秀 |
| Qwen3 Coder Plus | 76% | 73% | 优秀 | 优秀 |
| Kimi K2 Thinking | 72% | 70% | 良好 | 优秀 |

**逻辑推理推荐**：
- 首选：DeepSeek Chat、Qwen3 Coder Plus
- 深度分析：Kimi K2 Thinking

---

## 成本效率对比

| 模型 | API 价格 | 响应速度 | 性价比 | 推荐场景 |
|------|----------|----------|--------|----------|
| MiniMax M2.1 | 低 | 快 | 高 | 日常使用 |
| GLM-4.7 | 中 | 中 | 中 | 企业应用 |
| DeepSeek Chat | 极低 | 快 | 极高 | 技术项目 |
| Qwen3 Coder Plus | 中 | 快 | 中高 | 专业开发 |
| Kimi K2 Thinking | 中 | 中 | 中 | 长文档场景 |

---

## 场景推荐总结

| 场景 | 推荐模型 | 备选模型 |
|------|----------|----------|
| 代码开发 | Qwen3 Coder Plus | DeepSeek Chat |
| 长文档处理 | Kimi K2 Thinking | Qwen3 Coder Plus |
| 中文内容创作 | Kimi K2 Thinking | GLM-4.7 |
| 数学/技术分析 | DeepSeek Chat | Qwen3 Coder Plus |
| 成本敏感项目 | DeepSeek Chat | MiniMax M2.1 |
| 多语言任务 | DeepSeek Chat | GLM-4.7 |
| 企业级应用 | GLM-4.7 | Qwen3 Coder Plus |
| 日常对话 | MiniMax M2.1 | Kimi K2 Thinking |
