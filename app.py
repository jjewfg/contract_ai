# app.py —— 合同智能抽取助手（Gradio 界面）
import os, json
from dotenv import load_dotenv
import gradio as gr
from extract import extract

load_dotenv()

def run_extract(text):
    if not text or not text.strip():
        return None, None
    result, err = extract(text)
    if result is None:
        return {"error": "抽取失败：" + str(err)}, None
    with open("extraction_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        print(nl)
    return result, "extraction_result.json"

EXAMPLE = ""
for p in ["contracts/contract_01.txt", "contract_01.txt"]:
    try:
        EXAMPLE = open(p, encoding="utf-8").read()
        break
    except Exception:
        pass


demo = gr.Interface(
    fn=run_extract,
    inputs=gr.Textbox(lines=18, label="粘贴合同正文"),
    outputs=[gr.JSON(label="结构化抽取结果"), gr.File(label="下载 JSON")],
    title="合同智能抽取助手",
    description="粘贴合同文本，自动抽取 8 个关键字段并输出结构化 JSON（LLM 抽取 + Pydantic 校验 + 失败重试）",
    examples=[[EXAMPLE]] if EXAMPLE else None,
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
