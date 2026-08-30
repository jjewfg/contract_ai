# diagnose2.py —— penalty 专项：5 份失败合同的三方对照 + 相似度
import json, difflib
from extract import extract

NAMES = ["contract_02.txt", "contract_07.txt", "contract_10.txt", "contract_11.txt", "contract_15.txt"]
labels = json.load(open("labels.json", encoding="utf-8"))
for n in NAMES:
    gold = next(x["label"] for x in labels if x["file"] == n)
    text = open("contracts/" + n, encoding="utf-8").read()
    pred, err = extract(text)
    p = (pred or {}).get("penalty", "")
    g = gold.get("penalty", "")
    r = difflib.SequenceMatcher(None, p, g).ratio() if (p and g) else 0.0
    print("== " + n + "  相似度=%.2f" % r)
    print("  标签:", g)
    print("  抽取:", p)
    print("")
