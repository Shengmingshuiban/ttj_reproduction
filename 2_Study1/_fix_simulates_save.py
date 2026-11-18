"""步骤4补充修复3：恢复被作者注释掉的 simulates 写文件行（可重复运行）。
- cell 73：作者源码中 all_sim_data.to_csv(simulates_path, index=False) 被注释，
  只打印 "Saved" 却不写文件。作者本地因仓库自带 simulates 故未暴露。
- 我们清空了执行路径强制真跑，必须恢复该写文件行，cell 75 才能读到。
- 去掉行首 '#' 即可，完全符合作者原意，不改变模拟逻辑。
"""
import nbformat

SRC_DIR = "C:/Users/Acer/Desktop/jump/time_to_jump-main/3_simulators"
DST_DIR = "C:/Users/Acer/Desktop/jump/2_Study1"
name = "param_estim_no_deadline.ipynb"
cell_idx = 73
expected = [1, 7, 33, 36, 73]

src = nbformat.read(f"{SRC_DIR}/{name}", as_version=4)
dst = nbformat.read(f"{DST_DIR}/{name}", as_version=4)
cell_src = dst.cells[cell_idx].source

COMMENTED = "                #all_sim_data.to_csv(simulates_path, index=False)"
FIXED = "                all_sim_data.to_csv(simulates_path, index=False)"

if FIXED in cell_src:
    print(f"SKIP {name}: cell{cell_idx} 写文件行已恢复")
else:
    assert cell_src.count(COMMENTED) == 1, f"未找到唯一注释行，实际 {cell_src.count(COMMENTED)}"
    cell_src = cell_src.replace(COMMENTED, FIXED)
    dst.cells[cell_idx].source = cell_src
    nbformat.validate(dst)
    nbformat.write(dst, f"{DST_DIR}/{name}")
    print(f"FIX  {name}: cell{cell_idx} to_csv 写文件行已恢复")

check = nbformat.read(f"{DST_DIR}/{name}", as_version=4)
diffs = [i for i, (a, b) in enumerate(zip(src.cells, check.cells))
         if a.source != b.source or a.cell_type != b.cell_type or a.get("metadata") != b.get("metadata")]
assert diffs == expected, f"差异应为 {expected}，实际 {diffs}"
print(f"  OK  {name}: 差异={diffs}")
print("ALL DONE")
