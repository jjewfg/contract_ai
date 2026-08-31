\# 合同智能抽取助手



粘贴合同文本 → 自动抽取 8 个关键字段 → 输出结构化 JSON。



\- 技术栈：DeepSeek-V3 ｜ Gradio ｜ Pydantic 校验 ｜ Docker ｜ GitHub Actions CI

\- 评测：20 份合成合同字段级准确率（见 eval\_report2.md），标准答案随数据合成生成

\- CI：每次 push 自动执行 lint、语法检查与 Docker 镜像构建



\## 本地运行



pip install -r requirements.txt → 配置环境变量 SILICONFLOW\_API\_KEY → python app.py



\## Docker 运行



docker compose up --build → 浏览器打开 http://127.0.0.1:7860


**在线体验**：[魔搭创空间](https://modelscope.cn/studios/xiaoluobolyt/contract-extractor)

\## 已知限制



\- \*\*penalty 字段准确率 75%\*\*：经三方人工核对，5 份失败样本的抽取内容全部语义正确；根因是模型按 Prompt 要求逐字摘录条款（常含解约权等附加条款），而标准答案为要素摘要，对称字符相似度对这种"逐字 vs 摘要"的长度差敏感（失败样本相似度集中于 0.40\~0.47，阈值 0.5）。恪守评测纪律，不在测试集上调整阈值；v4 计划在扩充后的留出集上以"覆盖度指标 + 金额归一化"重新标定。

\- \*\*合成数据\*\*：评测集为 LLM 合成合同，已修复 2 处标签与正文漂移（ground truth 以正文为准）；未覆盖真实合同场景（中文大写金额、扫描件 OCR 等）。

\- \*\*单模型验证\*\*：仅在 DeepSeek-V3（temperature=0）上验证，跨模型稳定性未测。



