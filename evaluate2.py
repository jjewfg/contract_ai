# evaluate2.py —— 20 份合同批量抽取 + 字段级准确率评测，输出 eval_report2.md
import os, json, re, time, difflib
from datetime import datetime
from dotenv import load_dotenv
from extract import extract

load_dotenv()
NL = chr(10)

def norm_num(s):
    return sorted(re.findall(r"\d+", s or ""))

def loose_sim(a, b):
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()

def check(field, pred, gold):
    g = ("" if gold is None else str(gold)).strip()
    p = ("" if pred is None else str(pred)).strip()
    if g == "":
        return (p == ""), "gold_kong"
    if p == "":
        return False, "kong"
    if field in ("contract_type", "party_a", "party_b", "term_start", "term_end"):
        return (p == g), "exact"
    if field == "amount":
        return (norm_num(p) == norm_num(g)), "num"
    if field == "penalty":
        r = loose_sim(p, g)
        return (r >= 0.5), "sim_" + ("%.2f" % r)
    if field == "dispute_resolution":
        if "仲裁" in g:
            return ("仲裁" in p), "keyword"
        if "诉讼" in g or "法院" in g:
            return ("诉讼" in p or "法院" in p), "keyword"
        return False, "keyword"
    return False, "-"
FIELDS = ["contract_type", "party_a", "party_b", "amount", "term_start", "term_end", "penalty", "dispute_resolution"]

labels = json.load(open("labels.json", encoding="utf-8"))
print("脚本启动：待评测合同 " + str(len(labels)) + " 份", flush=True)

results = []
field_pass = {}
for f in FIELDS:
    field_pass[f] = 0
extract_fail = 0

for item in labels:
    fname = item["file"]
    gold = item["label"]
    print("评测中：" + fname, flush=True)
    try:
        text = open(os.path.join("contracts", fname), encoding="utf-8").read()
    except Exception:
        text = ""
    try:
        pred, err = extract(text)
    except Exception as e:
        pred, err = None, str(e)
    if pred is None:
        extract_fail += 1
        results.append((fname, None, err or "parse failed"))
        time.sleep(1)
        continue
    row = {}
    for f in FIELDS:
        ok, how = check(f, pred.get(f), gold.get(f, ""))
        row[f] = ok
        if ok:
            field_pass[f] += 1
    results.append((fname, row, pred))
    time.sleep(1)

n = len(labels)
lines = [
    "# 合同智能抽取助手 · 评测报告",
    "",
    "- 评测时间：" + datetime.now().strftime("%Y-%m-%d %H:%M"),
    "- 模型：DeepSeek-V3（temperature=0.1）｜样本：合成合同 " + str(n) + " 份｜字段：8 个",
    "- 抽取/解析失败：" + str(extract_fail) + " 份",
    "",
    "| 字段 | 正确 | 准确率 |",
    "|---|---|---|",
]
for f in FIELDS:
    lines.append("| " + f + " | " + str(field_pass[f]) + "/" + str(n) + " | " + ("%.0f%%" % (100.0 * field_pass[f] / n)) + " |")
overall = sum(field_pass.values()) / (n * len(FIELDS))
lines += ["", "**总体字段准确率：" + ("%.1f%%" % (100.0 * overall)) + "**", ""]
lines.append("| 文件 | 结果 |")
lines.append("|---|---|")
for fname, row, info in results:
    if row is None:
        lines.append("| " + fname + " | FAIL（" + str(info)[:60] + "） |")
    else:
        bad = []
        for f in FIELDS:
            if not row[f]:
                bad.append(f)
        lines.append("| " + fname + " | " + ("PASS 全部8字段" if not bad else "部分错误：" + ",".join(bad)) + " |")
with open("eval_report2.md", "w", encoding="utf-8") as f:
    f.write(NL.join(lines))
print("")
print("总体字段准确率：%.1f%%" % (100.0 * overall))
print("报告已写入 eval_report2.md")
