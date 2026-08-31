# 合同智能抽取助手

> 粘贴合同文本 → 自动抽取 8 个关键字段 → 输出结构化 JSON，可直接对接下游系统。

![CI](https://github.com/jjewfg/contract_ai/actions/workflows/ci.yml/badge.svg)

**在线体验**：[魔搭创空间](https://modelscope.cn/studios/xiaoluobolyt/contract-extractor)

## 解决什么问题

法务/商务场景中，人工读一份合同并提取关键要素（类型、甲乙方、金额、履约期间、违约条款、争议解决方式）平均要 5~10 分钟。本项目用 LLM 把这一过程压到秒级，并用评测体系保证输出质量**可量化、可复现**。

## 核心特性

- **结构化输出管线**：Prompt 约束 JSON schema → null 清洗 → Pydantic 强类型校验 → 失败重试，四道关保证下游拿到的数据干净可用
- **字段级评测体系**：20 份合成合同 × 8 字段，按字段特性分级设计匹配策略（精确匹配 / 数字集合 / 相似度 / 关键词判定）
- **可复现评测**：temperature=0，同输入同输出，每轮数字可归因
- **容器化交付**：Dockerfile + compose，GitHub CI 云端、本地、魔搭三端验证"一次构建，哪都能跑"
- **自动化质量门**：每次 push 自动执行 lint、语法检查与 Docker 镜像构建

## 评测结果

| 版本 | 总体字段准确率 | 关键改动 |
|---|---|---|
| v1 | 76.9% | 基线（含评测器匹配冤案 + null 整份连坐） |
| v3 | **96.9%** | 评测器改关键词判定、null 清洗、ground truth 以正文为准、temperature=0 |

7/8 字段 100%，penalty 75% 为指标局限（详见下方已知限制）。
完整调试推理链见 **[EVAL_DEBUG_REPORT.md](EVAL_DEBUG_REPORT.md)**，全部踩坑记录见 **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**。

## 快速开始

本地运行：

```bash
pip install -r requirements.txt
# 配置环境变量 SILICONFLOW_API_KEY
python app.py
```

Docker 运行：

```bash
docker compose up --build
# 浏览器打开 http://127.0.0.1:7860
```

## 技术栈

Python / Gradio / Pydantic / Docker / GitHub Actions / DeepSeek-V3

## 已知限制

- **penalty 字段准确率 75%**：经三方人工核对，5 份失败样本的抽取内容全部语义正确；根因是模型按 Prompt 要求逐字摘录条款（常含解约权等附加条款），而标准答案为要素摘要，对称字符相似度对这种"逐字 vs 摘要"的长度差敏感（失败样本相似度集中于 0.40~0.47，阈值 0.5）。恪守评测纪律，不在测试集上调整阈值；v4 计划在扩充后的留出集上以"覆盖度指标 + 金额归一化"重新标定。
- **合成数据**：评测集为 LLM 合成合同，已修复 2 处标签与正文漂移（ground truth 以正文为准）；未覆盖真实合同场景（中文大写金额、扫描件 OCR 等）。
- **单模型验证**：仅在 DeepSeek-V3（temperature=0）上验证，跨模型稳定性未测。
