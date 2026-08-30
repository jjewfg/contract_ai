# diagnose.py —— 三方对照：标签 vs 模型抽取 vs 正文原文
import json
from extract import extract

NAMES = ["contract_02.txt", "contract_06.txt", "contract_10.txt"]
labels = json.load(open("labels.json", encoding="utf-8"))
for n in NAMES:
    gold = next(x["label"] for x in labels if x["file"] == n)
    text = open("contracts/" + n, encoding="utf-8").read()
    pred, err = extract(text)
    p = pred or {}
    print("== " + n)
    print("  标签  :", gold.get("term_start"), "→", gold.get("term_end"))
    print("  模型  :", p.get("term_start"), "→", p.get("term_end"))
    print("  正文含年份的行:")
    for line in text.split(chr(10)):
        if "2026" in line or "2027" in line or "2028" in line:
            print("   |", line.strip()[:70])
    print("")
