# gen_data.py —— 合成 20 份合同 + 标准答案 labels.json（固定种子可复现）
import os, json, random, time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ["SILICONFLOW_API_KEY"],
                base_url="https://api.siliconflow.cn/v1")
CHAT_MODEL = "deepseek-ai/DeepSeek-V3"
NL = chr(10)
random.seed(42)

COMPANIES = ["星辰科技有限公司", "远大实业集团", "蓝海贸易有限公司", "恒信咨询有限公司",
             "绿洲食品有限公司", "天成建设有限公司", "启明软件有限公司", "华信物流有限公司"]
PERSONS = ["李明", "王芳", "张伟", "刘洋", "陈静", "赵磊", "孙婷", "周杰"]
DISPUTES = ["协商不成的，向合同签订地人民法院提起诉讼",
            "协商不成的，提交北京仲裁委员会仲裁"]

def make_profile(i):
    t = i % 4
    if t == 0:
        return {"contract_type": "劳动合同", "party_a": random.choice(COMPANIES),
                "party_b": random.choice(PERSONS),
                "amount": str(random.randint(6, 25) * 1000) + "元/月",
                "term_start": "2026-%02d-01" % random.randint(1, 12),
                "term_end": "2028-%02d-28" % random.randint(1, 12),
                "penalty": "乙方违反服务期约定的，应支付违约金" + str(random.randint(1, 5) * 5000) + "元",
                "dispute_resolution": random.choice(DISPUTES)}
    if t == 1:
        return {"contract_type": "房屋租赁合同", "party_a": random.choice(PERSONS),
                "party_b": random.choice(PERSONS),
                "amount": str(random.randint(2, 12) * 500) + "元/月",
                "term_start": "2026-%02d-01" % random.randint(1, 12),
                "term_end": "2027-%02d-28" % random.randint(1, 12),
                "penalty": "逾期支付租金超过十日的，每日按月租金的百分之一支付违约金",
                "dispute_resolution": random.choice(DISPUTES)}
    if t == 2:
        return {"contract_type": "商品买卖合同", "party_a": random.choice(COMPANIES),
                "party_b": random.choice(COMPANIES),
                "amount": str(random.randint(1, 50) * 10000) + "元",
                "term_start": "2026-%02d-10" % random.randint(1, 12),
                "term_end": "2026-%02d-20" % random.randint(1, 12),
                "penalty": "延迟交付的，每延迟一日按合同总价的千分之三支付违约金",
                "dispute_resolution": random.choice(DISPUTES)}
    return {"contract_type": "技术服务合同", "party_a": random.choice(COMPANIES),
            "party_b": random.choice(COMPANIES),
            "amount": str(random.randint(5, 80) * 10000) + "元",
            "term_start": "2026-%02d-01" % random.randint(1, 12),
            "term_end": "2027-%02d-28" % random.randint(1, 12),
            "penalty": "任一方违约的，应向守约方支付合同总额百分之十的违约金",
            "dispute_resolution": random.choice(DISPUTES)}

PROMPT = ("请根据以下要素撰写一份真实风格的中国" + "{T}" + "正文，600字左右。"
          "要求：要素信息必须全部自然融入条款；必须包含明确的违约责任条款和争议解决条款；"
          "金额、日期、名称必须与要素完全一致，不得增减改动。只输出合同正文，不要评论。" + NL +
          "甲方：{A}" + NL + "乙方：{B}" + NL + "金额：{M}" + NL +
          "起始日期：{S}" + NL + "结束日期：{E}" + NL + "违约责任要素：{P}" + NL + "争议解决要素：{D}")

def write_contract(p):
    msg = (PROMPT.replace("{T}", p["contract_type"]).replace("{A}", p["party_a"])
           .replace("{B}", p["party_b"]).replace("{M}", p["amount"])
           .replace("{S}", p["term_start"]).replace("{E}", p["term_end"])
           .replace("{P}", p["penalty"]).replace("{D}", p["dispute_resolution"]))
    r = client.chat.completions.create(model=CHAT_MODEL,
        messages=[{"role": "user", "content": msg}], temperature=0.8)
    return r.choices[0].message.content.strip()

os.makedirs("contracts", exist_ok=True)
labels = []
for i in range(1, 21):
    p = make_profile(i)
    print("生成第 %d 份（%s）..." % (i, p["contract_type"]))
    try:
        text = write_contract(p)
    except Exception as e:
        print("失败，跳过：" + str(e))
        continue
    with open("contracts/contract_%02d.txt" % i, "w", encoding="utf-8") as f:
        f.write(text)
    labels.append({"file": "contract_%02d.txt" % i, "label": p})
    time.sleep(1.2)

with open("labels.json", "w", encoding="utf-8") as f:
    json.dump(labels, f, ensure_ascii=False, indent=2)
print("完成：contracts/ 共 %d 份合同，标准答案在 labels.json" % len(labels))
