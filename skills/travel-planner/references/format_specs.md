# Output Format Specifications

## Word Document (.docx)

### 规格

| 属性 | 值 |
|-----|-----|
| 页面尺寸 | A4 |
| 边距 | 2.54cm (1英寸) |
| 字体 | 宋体/微软雅黑 |
| 字号 | 正文 12pt，标题 16-24pt |
| 行距 | 1.5倍行距 |

### 章节结构

1. 封面（标题、副标题）
2. 目录
3. 行程概览
4. 目的地信息
5. 详细行程（按天）
6. 住宿推荐
7. 美食推荐
8. 交通指南
9. 预算规划
10. 注意事项
11. 天气预报
12. 页脚（生成时间）

## Markdown Document (.md)

### 语法规范

- 标题使用 `#` 到 `######`
- 列表使用 `-` 或 `1.`
- 表格使用 `|` 分隔
- 链接使用 `[text](url)`
- 图片使用 `![alt](path)`

### 推荐扩展

- `.md` - 标准 Markdown
- `.mdx` - 支持 React 组件（用于静态站）

## Web Page (.html)

### 技术规格

| 属性 | 值 |
|-----|-----|
| HTML 版本 | HTML5 |
| CSS 框架 | 原生 CSS + Flexbox + Grid |
| JavaScript | ES6+ |
| 响应式 | 支持移动端 (≤768px) |

### 组件

- Hero 区域（标题、封面图）
- 时间线（行程展示）
- 卡片网格（酒店、美食）
- 进度条（预算展示）
- 天气预报组件
- 交互式复选框（注意事项）

### 动画效果

- 页面滚动动画
- 卡片悬停效果
- 预算条加载动画
- 平滑滚动导航

### 浏览器兼容性

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 文件命名规范

```
travel_guide_[目的地]_[开始日期].[扩展名]

# 示例
travel_guide_hangzhou_20240315.docx
travel_guide_hangzhou_20240315.md
travel_guide_hangzhou_20240315.html
```

## 编码要求

- 字符编码: UTF-8
- 换行符: LF (Unix)
