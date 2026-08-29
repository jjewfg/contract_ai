# extract.py —— 合同结构化抽取：JSON 输出 + Pydantic 校验 + 失败重试
import os, json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError

load_dotenv()
client = OpenAI(api_key=os.environ["SILICONFLOW_API_KEY"],
                base_url="https://api.siliconflow.cn/v1")
CHAT_MODEL = "deepseek-ai/DeepSeek-V3"
NL = chr(10)
FIELDS = ("contract_type（只能取：劳动合同/房屋租赁合同/商品买卖合同/技术服务合同），"
          "party_a（甲方名称，原样保留），party_b（乙方名称，原样保留），"
          "amount（金额，如：5000元/月 或 100000元），"
          "term_start（起始日期，格式YYYY-MM-DD），term_end（结束日期，格式YYYY-MM-DD），"
          "penalty（违约责任条款原文摘要，50字以内），dispute_resolution（争议解决方式：诉讼 或 仲裁）")

PROMPT = ("你是合同信息抽取引擎。从下面的合同正文中抽取指定字段。规则：" + NL +
          "1) 只输出一个JSON对象，不要输出任何解释、不要用markdown代码块；" + NL +
          "2) 字段必须包含：" + FIELDS + NL +
          "3) 合同中没有的信息填 null，禁止编造。" + NL +
          "合同正文：" + NL)

class ContractInfo(BaseModel):
    contract_type: str
    party_a: str = ""
    party_b: str = ""
    amount: str = ""
    term_start: str = ""
    term_end: str = ""
    penalty: str = ""
    dispute_resolution: str = ""

def extract_once(text):
    r = client.chat.completions.create(model=CHAT_MODEL,
        messages=[{"role": "user", "content": PROMPT + text}],
        temperature=0.1)
    return r.choices[0].message.content.strip()

def extract(text, max_retry=1):
    for attempt in range(max_retry + 1):
        raw = extract_once(text)
        raw = raw.replace("```json", "").replace("```", "").strip()
        try:
            data = json.loads(raw)
            return ContractInfo(**data).model_dump(), None
        except (json.JSONDecodeError, ValidationError, TypeError) as e:
            err = str(e)[:200]
    return None, err

if __name__ == "__main__":
    text = open("contracts/contract_01.txt", encoding="utf-8").read()
    result, err = extract(text)
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("抽取失败：" + str(err))
