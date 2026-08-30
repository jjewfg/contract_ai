# 合同智能抽取助手 · 评测报告

- 评测时间：2026-08-30 21:08
- 模型：DeepSeek-V3（temperature=0.1）｜样本：合成合同 20 份｜字段：8 个
- 抽取/解析失败：0 份

| 字段 | 正确 | 准确率 |
|---|---|---|
| contract_type | 20/20 | 100% |
| party_a | 20/20 | 100% |
| party_b | 20/20 | 100% |
| amount | 20/20 | 100% |
| term_start | 20/20 | 100% |
| term_end | 20/20 | 100% |
| penalty | 15/20 | 75% |
| dispute_resolution | 20/20 | 100% |

**总体字段准确率：96.9%**

| 文件 | 结果 |
|---|---|
| contract_01.txt | PASS 全部8字段 |
| contract_02.txt | 部分错误：penalty |
| contract_03.txt | PASS 全部8字段 |
| contract_04.txt | PASS 全部8字段 |
| contract_05.txt | PASS 全部8字段 |
| contract_06.txt | PASS 全部8字段 |
| contract_07.txt | 部分错误：penalty |
| contract_08.txt | PASS 全部8字段 |
| contract_09.txt | PASS 全部8字段 |
| contract_10.txt | 部分错误：penalty |
| contract_11.txt | 部分错误：penalty |
| contract_12.txt | PASS 全部8字段 |
| contract_13.txt | PASS 全部8字段 |
| contract_14.txt | PASS 全部8字段 |
| contract_15.txt | 部分错误：penalty |
| contract_16.txt | PASS 全部8字段 |
| contract_17.txt | PASS 全部8字段 |
| contract_18.txt | PASS 全部8字段 |
| contract_19.txt | PASS 全部8字段 |
| contract_20.txt | PASS 全部8字段 |