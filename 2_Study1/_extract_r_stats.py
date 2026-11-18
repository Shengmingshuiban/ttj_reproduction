"""步骤8：从 R 生成的 HTML 中提取 BF/ANOVA 等推断统计关键数值。"""
import re, html

f = "C:/Users/Acer/Desktop/jump/2_Study1/ttj_analyses.html"
s = open(f, encoding="utf-8", errors="ignore").read()
s = re.sub(r"<[^>]+>", " ", s)
s = html.unescape(s)
s = re.sub(r"\s+", " ", s)

for kw in ["BF", "eta", "directional", "skewness", "alpha", "p <", "p ="]:
    idxs = [m.start() for m in re.finditer(re.escape(kw), s, re.I)][:5]
    print(f"==== {kw} ({len(idxs)} hits) ====")
    for i in idxs:
        print("  ...", s[max(0, i - 100):i + 160].strip())
    print()
