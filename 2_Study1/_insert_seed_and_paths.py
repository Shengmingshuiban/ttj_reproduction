"""步骤3：生成 4 份 Study 1 干净 notebook。
- 只改两处：cell1 开头插入固定种子块；常量 cell 改 PRESIM_PATH 一行为 "."。
- 其余 cell / 元数据一律不动，用 nbformat 读写保证仍是合法 .ipynb。
- 断言：与源文件的差异 cell 索引精确为预期集合。
"""
import copy
import nbformat

SRC_DIR = "C:/Users/Acer/Desktop/jump/time_to_jump-main/3_simulators"
DST_DIR = "C:/Users/Acer/Desktop/jump/2_Study1"

# 与 1_moni/_insert_seed.py 完全相同的种子块（SEED=42，含 C 库双路径播种）
SEED_BLOCK = """# ===== 复现固定随机种子（仅新增，不改动原有代码）=====
SEED = 42
import ctypes as _ctypes
import random as _random
import numpy as _np
_np.random.seed(SEED)      # 控制 numpy 与 scipy.stats 的随机数
_random.seed(SEED)         # 控制标准库 random
# Cython 扩展以 MSVC /MD 编译，其 rand() 来自 Universal CRT (ucrtbase.dll)。
# 必须显式给该 CRT 播种，才能让 C 噪声可复现（msvcrt.dll 是另一套独立状态）。
_c_seeded = False
for _dll in ("ucrtbase.dll", "msvcrt.dll", "vcruntime140.dll"):
    try:
        _ctypes.CDLL(_dll).srand(SEED)
        _c_seeded = True
        break
    except Exception:
        pass
if not _c_seeded:
    try:
        _ctypes.CDLL(None).srand(SEED)
        _c_seeded = True
    except Exception:
        pass
print("RNG seeded:", SEED, "| C-libc seeded:", _c_seeded)
# ====================================================

"""

OLD = 'PRESIM_PATH = "/media/administrator/Expansion/"'
NEW = 'PRESIM_PATH = "."'

# (文件名, 路径常量所在 cell 索引, 期望差异集合)
TASKS = [
    ("param_estim_no_deadline.ipynb", 7, [1, 7]),
    ("param_estim_deadline.ipynb", 7, [1, 7]),
    ("model_comp_no_deadline.ipynb", 4, [1, 4]),
    ("model_comp_deadline.ipynb", 4, [1, 4]),
]

for name, path_cell, expected in TASKS:
    src = nbformat.read(f"{SRC_DIR}/{name}", as_version=4)
    dst = nbformat.read(f"{DST_DIR}/{name}", as_version=4)

    original_cell1 = dst.cells[1].source
    original_path_cell = dst.cells[path_cell].source
    assert OLD in original_path_cell, f"{name}: cell{path_cell} 未找到 PRESIM_PATH 原值"

    # 改动1：cell1 开头插入种子块
    dst.cells[1].source = SEED_BLOCK + original_cell1
    # 改动2：常量 cell 只替换 PRESIM_PATH 一行
    dst.cells[path_cell].source = original_path_cell.replace(OLD, NEW)

    nbformat.validate(dst)
    nbformat.write(dst, f"{DST_DIR}/{name}")

    # ---- 严格校验 ----
    check = nbformat.read(f"{DST_DIR}/{name}", as_version=4)
    assert len(check.cells) == len(src.cells), f"{name}: cell 数不一致"
    diffs = []
    for i, (a, b) in enumerate(zip(src.cells, check.cells)):
        if a.source != b.source or a.cell_type != b.cell_type or a.get("metadata") != b.get("metadata"):
            diffs.append(i)
    assert diffs == expected, f"{name}: 差异 cell 应为 {expected}，实际 {diffs}"

    # cell1 = 种子块 + 源文
    assert check.cells[1].source == SEED_BLOCK + src.cells[1].source, f"{name}: cell1 非预期"
    # 路径 cell：除 PRESIM_PATH 一行外逐字相同
    assert check.cells[path_cell].source == src.cells[path_cell].source.replace(OLD, NEW), \
        f"{name}: cell{path_cell} 非预期"
    # 其余 cell 逐字相同
    for i, (a, b) in enumerate(zip(src.cells, check.cells)):
        if i not in expected:
            assert a.source == b.source, f"{name}: 非预期地改动了 cell{i}"

    print(f"OK  {name}: cell 数={len(check.cells)}, 差异={diffs}, "
          f"cell1 +{len(SEED_BLOCK)}字符, cell{path_cell} PRESIM_PATH->'.'")

print("ALL DONE")
