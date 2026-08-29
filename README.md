\# 合同智能抽取助手



粘贴合同文本 → 自动抽取 8 个关键字段 → 输出结构化 JSON。



\- 技术栈：DeepSeek-V3 ｜ Gradio ｜ Pydantic 校验 ｜ Docker ｜ GitHub Actions CI

\- 评测：20 份合成合同字段级准确率（见 eval\_report2.md），标准答案随数据合成生成

\- CI：每次 push 自动执行 lint、语法检查与 Docker 镜像构建



\## 本地运行



pip install -r requirements.txt → 配置环境变量 SILICONFLOW\_API\_KEY → python app.py



\## Docker 运行



docker compose up --build → 浏览器打开 http://127.0.0.1:7860



