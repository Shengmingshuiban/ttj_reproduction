"""步骤5验证：从 executed notebook 输出与 pkl 中提取关键数值。"""
import nbformat, pickle, numpy as np, pandas as pd
from scipy.stats import skew

nb = nbformat.read("alpha_behavior.executed.ipynb", as_version=4)

def cell_stream(cells, idx):
    parts = []
    for o in cells[idx].get("outputs", []):
        if o.get("output_type") == "stream":
            parts.append(o.get("text", ""))
        elif o.get("output_type") in ("execute_result", "display_data"):
            parts.append(o.get("data", {}).get("text/plain", ""))
    return "".join(parts)

for i in (10, 11, 12, 20, 21, 23, 24, 25, 33):
    print(f"\n===== cell{i} 输出 =====")
    print(cell_stream(nb.cells, i)[:1500])

print("\n===== pkl 数据检查 =====")
with open("simulate_alpha_behavior.pkl", "rb") as f:
    data = pickle.load(f)
flat = [x for sub in data for x in sub]
df = pd.DataFrame(flat)
print("rounds:", len(data), "| 记录数:", len(df))
print("alpha 取值数:", df.alpha.nunique(), "范围:", df.alpha.min(), "-", df.alpha.max())
print("a:", sorted(df.a.unique()), "v:", sorted(df.v.unique()), "t0:", sorted(df.t0.unique()))
print("accuracy 均值:", round(df.accuracy.mean(), 4))
print("按 alpha 的 skewness_correct 均值:")
print(df.groupby("alpha").skewness_correct.mean().round(3).to_string())
