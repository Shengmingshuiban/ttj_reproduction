"""步骤3：向两个 notebook 的 cell1 开头插入种子=42 代码块。
- 只改 cell1 的 source 开头，其它 cell / 元数据一律不动。
- 用 nbformat 读写，保证仍是合法 .ipynb。
"""
import copy
import nbformat

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

SRC_DIR = "C:/Users/Acer/Desktop/jump/time_to_jump-main/1_introduction"
DST_DIR = "C:/Users/Acer/Desktop/jump/moni"
NOTEBOOKS = ["alpha_behavior.ipynb", "density_sample_paths.ipynb"]

for name in NOTEBOOKS:
    src = nbformat.read(f"{SRC_DIR}/{name}", as_version=4)
    dst = nbformat.read(f"{DST_DIR}/{name}", as_version=4)
    original_cell1 = dst.cells[1].source

    # 只在 cell1 开头插入种子块
    dst.cells[1].source = SEED_BLOCK + original_cell1
    nbformat.validate(dst)
    nbformat.write(dst, f"{DST_DIR}/{name}")

    # 语义校验：除 cell1 外，所有 cell 与源文件完全一致；cell1 = 种子块 + 原文
    check = nbformat.read(f"{DST_DIR}/{name}", as_version=4)
    assert len(check.cells) == len(src.cells), f"{name}: cell 数不一致"
    diffs = []
    for i, (a, b) in enumerate(zip(src.cells, check.cells)):
        if a.source != b.source:
            diffs.append(i)
        # 其它字段（cell_type / metadata / outputs / execution_count）也应一致
        if a.cell_type != b.cell_type or a.get("metadata") != b.get("metadata"):
            diffs.append(f"{i}:meta")
    assert diffs == [1], f"{name}: 差异 cell 应为 [1]，实际 {diffs}"
    assert check.cells[1].source == SEED_BLOCK + src.cells[1].source
    print(f"OK  {name}: cell 数={len(check.cells)}, 仅 cell1 新增种子块 ({len(SEED_BLOCK)} 字符)")

print("ALL DONE")
