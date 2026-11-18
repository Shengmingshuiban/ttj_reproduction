"""最小修复：仅把 moni 副本中 cell14 的一处 bug 行改掉。
np.mean() 不接受 bias 参数（应为 skew 的写法误粘贴）。
改动：np.mean(RTs_incorrect, bias=False) -> np.mean(RTs_incorrect)
其余任何代码/元数据一律不动。
"""
import nbformat

path = "C:/Users/Acer/Desktop/jump/moni/alpha_behavior.ipynb"
src_path = "C:/Users/Acer/Desktop/jump/time_to_jump-main/1_introduction/alpha_behavior.ipynb"

nb = nbformat.read(path, as_version=4)
src = nbformat.read(src_path, as_version=4)

OLD = "np.mean(RTs_incorrect, bias=False)"
NEW = "np.mean(RTs_incorrect)"

cell = nb.cells[14].source
assert cell.count(OLD) == 1, f"期望恰好 1 处，实际 {cell.count(OLD)}"
nb.cells[14].source = cell.replace(OLD, NEW)
nbformat.validate(nb)
nbformat.write(nb, path)

# 校验：与源文件相比，差异应仅为 (a) 种子块 (b) 这一行 bug 修复
check = nbformat.read(path, as_version=4)
assert len(check.cells) == len(src.cells) == 34
diff_cells = [i for i in range(34) if check.cells[i].source != src.cells[i].source]
assert diff_cells == [1, 14], f"差异 cell 应为 [1,14]，实际 {diff_cells}"
# cell14 除该行外完全一致
exp14 = src.cells[14].source.replace(OLD, NEW)
assert check.cells[14].source == exp14
print("OK: cell1=种子块, cell14=仅删除多余的 bias=False, 其余 32 个 cell 与源文件逐字一致")
