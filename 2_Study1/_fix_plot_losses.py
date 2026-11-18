"""步骤4补充修复（稳健版，可重复运行）：给加载 checkpoint 场景下的训练损失绘图加容错。
- 背景：从 checkpoint 加载会跳过训练，loss_history 为空，
  bf.diagnostics.plot_losses(get_plottable()) 抛 AttributeError。
- 该绘图行 savefig 已被作者注释、无后续引用，对结果/图表零影响。
- 只改各 notebook 训练 cell 内这一行，包成 try/except；其余一律不动。
- 幂等：若已修复则跳过。最终断言差异 cell 精确为预期集合。
"""
import nbformat

SRC_DIR = "C:/Users/Acer/Desktop/jump/time_to_jump-main/3_simulators"
DST_DIR = "C:/Users/Acer/Desktop/jump/2_Study1"

# 支持两种变量名写法：param 用 f=，model_comp 用 diag_plot=
TMPL = "{indent}{var} = bf.diagnostics.plot_losses(trainer.loss_history.get_plottable(), moving_average=True)"

def make_old(indent, var):
    return TMPL.format(indent=indent, var=var)

def make_new(indent, var):
    return (f"{indent}try:\n"
            f"{indent}    {var} = bf.diagnostics.plot_losses(trainer.loss_history.get_plottable(), moving_average=True)\n"
            f"{indent}except Exception:\n"
            f"{indent}    pass  # 从 checkpoint 加载时无训练曲线，跳过（对结果无影响）")

TASKS = [
    ("param_estim_no_deadline.ipynb", 33, "f", [1, 7, 33]),
    ("param_estim_deadline.ipynb", 33, "f", [1, 7, 33]),
    ("model_comp_no_deadline.ipynb", 17, "diag_plot", [1, 4, 17]),
    ("model_comp_deadline.ipynb", 16, "diag_plot", [1, 4, 16]),
]

for name, train_cell, var, expected in TASKS:
    src = nbformat.read(f"{SRC_DIR}/{name}", as_version=4)
    dst = nbformat.read(f"{DST_DIR}/{name}", as_version=4)
    cell_src = dst.cells[train_cell].source

    # 找到目标行及其缩进（源文件里是 4 空格缩进）
    old_line = make_old("    ", var)
    already = ("    try:\n" in cell_src and "从 checkpoint 加载时无训练曲线" in cell_src)

    if already:
        print(f"SKIP {name}: 已修复，跳过")
    else:
        assert cell_src.count(old_line) == 1, \
            f"{name}: cell{train_cell} 未找到唯一目标行 {var}，实际 {cell_src.count(old_line)}"
        cell_src = cell_src.replace(old_line, make_new("    ", var))
        dst.cells[train_cell].source = cell_src
        nbformat.validate(dst)
        nbformat.write(dst, f"{DST_DIR}/{name}")
        print(f"FIX  {name}: cell{train_cell} 已加 try/except 容错 ({var})")

    # 最终校验差异集合
    check = nbformat.read(f"{DST_DIR}/{name}", as_version=4)
    diffs = [i for i, (a, b) in enumerate(zip(src.cells, check.cells))
             if a.source != b.source or a.cell_type != b.cell_type or a.get("metadata") != b.get("metadata")]
    assert diffs == expected, f"{name}: 差异应为 {expected}，实际 {diffs}"
    assert "从 checkpoint 加载时无训练曲线" in check.cells[train_cell].source, \
        f"{name}: cell{train_cell} 容错未生效"
    print(f"  OK  {name}: 差异={diffs}，容错已生效")

print("ALL DONE")
