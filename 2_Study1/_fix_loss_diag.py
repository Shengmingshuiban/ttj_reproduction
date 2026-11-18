"""步骤4补充修复2：给所有 loss_history 诊断 cell 加容错（可重复运行）。
- cell 33/17/16 的 plot_losses 行：已在 _fix_plot_losses.py 处理。
- cell 36（param 系列）的 loss 收敛检查：trainer.loss_history.get_plottable()
  在 checkpoint 加载时为空 dict，无 .shape/.tail/Loss 列，故报错。
- 该 cell 纯打印诊断、不产出文件、后续不依赖其变量，整体包 try/except 跳过。
- 幂等 + 严格断言差异集合。
"""
import nbformat

SRC_DIR = "C:/Users/Acer/Desktop/jump/time_to_jump-main/3_simulators"
DST_DIR = "C:/Users/Acer/Desktop/jump/2_Study1"

MARK = "从 checkpoint 加载时无训练曲线"

# (文件, 诊断cell索引, 该cell原文首行, 最终期望差异集合)
TASKS = [
    ("param_estim_no_deadline.ipynb", 36, "for network in range(NUM_ENSEMBLE_MEMBERS):", [1, 7, 33, 36]),
    ("param_estim_deadline.ipynb", 36, "for network in range(NUM_ENSEMBLE_MEMBERS):", [1, 7, 33, 36]),
]

for name, cell_idx, first_line, expected in TASKS:
    src = nbformat.read(f"{SRC_DIR}/{name}", as_version=4)
    dst = nbformat.read(f"{DST_DIR}/{name}", as_version=4)
    cell_src = dst.cells[cell_idx].source

    if MARK in cell_src and "try:" in cell_src:
        print(f"SKIP {name}: cell{cell_idx} 已修复")
    else:
        assert cell_src.startswith(first_line), f"{name}: cell{cell_idx} 首行不符"
        lines = cell_src.split("\n")
        indented = "\n".join("    " + ln if ln.strip() else ln for ln in lines)
        new_src = (
            "try:  # 从 checkpoint 加载时无训练曲线，跳过 loss 诊断（对结果无影响）\n"
            + indented
            + "\nexcept Exception:\n"
            + "    pass"
        )
        dst.cells[cell_idx].source = new_src
        nbformat.validate(dst)
        nbformat.write(dst, f"{DST_DIR}/{name}")
        print(f"FIX  {name}: cell{cell_idx} 已整体加 try/except 容错")

    check = nbformat.read(f"{DST_DIR}/{name}", as_version=4)
    diffs = [i for i, (a, b) in enumerate(zip(src.cells, check.cells))
             if a.source != b.source or a.cell_type != b.cell_type or a.get("metadata") != b.get("metadata")]
    assert diffs == expected, f"{name}: 差异应为 {expected}，实际 {diffs}"
    print(f"  OK  {name}: 差异={diffs}")

print("ALL DONE")
