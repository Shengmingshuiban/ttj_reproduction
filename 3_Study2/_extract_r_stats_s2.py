"""步骤7：从渲染后的 HTML 结构化提取 Study 2 核对统计量。
- 只读 HTML，输出 _extracted_stats_s2.txt（供人工核对与写文档使用）。
- 不改动任何源数据/结果文件。
"""
import re
import html as htmlmod

HTML_PATH = "C:/Users/Acer/Desktop/jump/3_Study2/ttj_analyses_s2.html"
OUT_PATH = "C:/Users/Acer/Desktop/jump/3_Study2/_extracted_stats_s2.txt"

raw = open(HTML_PATH, "rb").read().decode("utf-8", errors="ignore")

def clean(x):
    x = htmlmod.unescape(x)
    x = re.sub(r"<U\+([0-9A-Fa-f]+)>", lambda m: chr(int(m.group(1), 16)), x)
    return re.sub(r"<[^>]+>", "", x).strip()

def parse_table(tb):
    rows = []
    for r in re.findall(r"<tr.*?</tr>", tb, re.S):
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S)
        rows.append([clean(x) for x in cells])
    return rows

tables = [parse_table(tb) for tb in re.findall(r"<table.*?</table>", raw, re.S)]

lines = []
def emit(s=""):
    lines.append(s)

emit("Study 2 复现 —— 从 ttj_analyses_s2.html 提取的统计量")
emit("=" * 60)

names = {
    0: "行为描述（分亮度 s0=暗/s1=亮，net 估计用）",
    7: "参数组间比较（附录版，含显著性标记）",
    8: "参数组间比较（完整版，含 p 值）",
    9: "主文表 maintext_table（Control vs Explicit Deadline）",
}
for i in [0, 7, 8, 9]:
    emit()
    emit(f"===== TABLE {i}: {names[i]} =====")
    for row in tables[i]:
        emit(" | ".join(row))

# 定向假设 BF10
t = htmlmod.unescape(re.sub(r"<[^>]+>", " ", raw))
t = re.sub(r"<U\+([0-9A-Fa-f]+)>", lambda m: chr(int(m.group(1), 16)), t)
t = re.sub(r"\s+", " ", t)
i = t.find("Directional Hypothesis")
emit()
emit("===== 定向假设 alpha_control > alpha_explicit =====")
if i >= 0:
    seg = t[i:i + 1000]
    m_bf = re.search(r"condition\s+##\s+(\d+)", seg) or re.search(r"condition\s+(\d{4,})", seg)
    m_p = re.search(r"Proportion consistent:\s*([\d.]+)", seg)
    emit("BF10 (directional): " + (m_bf.group(1) if m_bf else "N/A"))
    emit("Proportion consistent: " + (m_p.group(1) if m_p else "N/A"))

open(OUT_PATH, "w", encoding="utf-8").write("\n".join(lines))
print("WROTE", OUT_PATH)
print("\n".join(lines))
