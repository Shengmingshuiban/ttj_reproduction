"""步骤8补充：提取 α ANOVA、偏度 ANOVA 等推断统计。"""
import re, html
f = "C:/Users/Acer/Desktop/jump/2_Study1/ttj_analyses.html"
s = open(f, encoding="utf-8", errors="ignore").read()
s = re.sub(r"<[^>]+>", " ", s)
s = html.unescape(s)
s = re.sub(r"\s+", " ", s)

# α 的 ANOVA（lfm_nodeadline）
for pat in [r"aov_ez\([^)]*alpha[^)]*\)[\s\S]{0,400}",
            r"Response: alpha[\s\S]{0,300}",
            r"Skew correct[\s\S]{0,300}",
            r"BF10 for alpha[\s\S]{0,200}",
            r"ges[\s\S]{0,200}"]:
    print("=== PATTERN:", pat[:40], "===")
    for m in list(re.finditer(pat, s, re.I))[:3]:
        print("  ", m.group(0)[:400])
    print()
