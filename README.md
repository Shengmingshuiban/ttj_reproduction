# Reproduction of "Time to jump" (Liss et al., 2026)

本仓库是 **Liss, von Krause, Elsemüller, Hunsmann, & Lerche (2026)** 发表于 *Cognitive Psychology* 的论文
**"Time to jump: Exploring the distribution of noise in evidence accumulation as a function of time pressure"**
（*Cognitive Psychology*, 167, 101836）的独立复现。

> 原作者仓库：<https://github.com/jvliss/time_to_jump>
> 论文 DOI 见期刊页面；原始数据、作者训练权重与参考结果请从上述原仓库获取（本仓库不重复托管）。

---

## 1. 研究问题与复现范围

论文研究**时间压力如何改变证据累积过程中噪声分布的 Lévy 稳定性参数 α**。
本复现覆盖论文的**一个模拟 + 两个实验**，共三个模块：

| 模块 | 对应论文章节 | 内容 |
|---|---|---|
| `1_moni/` | 2. Simulation | 参数网格模拟（567 组合 × 400 试次），验证 α 塑造 RT 偏度 |
| `2_Study1/` | 3. Study 1 | 字母–数字辨别任务（N=317），三级时间压力 |
| `3_Study2/` | 4. Study 2 | 亮度辨别任务（N=160），跨任务验证 |

---

## 2. 核心结果对照（复现 vs 论文）

### Study 1（net1, simple LFM, 主分析）

| 指标 | accuracy | implicit deadline | explicit deadline | 论文 |
|---|---|---|---|---|
| **α** | **1.646** | **1.251** | **1.136** | 1.65 / 1.25 / 1.14 |
| 正确 RT 偏度 | 1.45 | 0.96 | −0.07 | 1.45 / 0.96 / −0.07 |
| 正确 RT (ms) | 495.78 | 404.76 | 378.07 | 同 |
| 正确率 | .96 | .87 | .83 | 同 |

- 简单 LFM 后验模型概率（PMP）：**0.495 / 0.875 / 0.936**，三条件均最高（四模型中）。
- α 方向性 BF₁₀ = **7.92×10⁵⁷**（论文 8.49×10⁵⁷，差异为蒙特卡洛随机波动）。
- net2 交叉验证 α：1.644 / 1.293 / 1.182（同样单调下降）。

### Study 1 额外分析（建模 timeout，仅 explicit 条件）

| 参数 | 主分析（timeout 删除） | 额外分析（timeout 编码为 0） | 论文 |
|---|---|---|---|
| LFM α | 1.136 | **1.298** | 1.14 → 1.30 |
| DM 漂移率 v0 | −3.504 | −2.810（幅度降约 20%） | 降约 20% |

### Study 2（net1, full LFM）

| 参数 | control | explicit deadline | 论文 |
|---|---|---|---|
| **α** | **1.80** | **1.72** | 1.80 → 1.72 |
| 阈距 a | 1.36 | 0.52 | 同 |

α：t = 6.70, d = 1.06, BF₁₀ = 2.43×10⁷（论文 6.65 / 1.05 / 1.91×10⁷）。

### Simulation（1_moni）

α 与正确 RT 偏度相关 **r = 0.37, p < .001**（论文 r ≈ .40）；分 α 偏度均值 1.250 → 1.776 单调上升；近对称分布仅在低 α 出现（α=1 时 3.7%，α=2 时 0%）。

---

## 3. 复现策略（重要）

- **加载作者已训练的 BayesFlow checkpoint 直接推断，不重训 250 epochs**（经导师许可）。
  - 因此执行版 notebook 中 `Initialized empty loss history`，**本次复现不产生新的训练 loss**；干净版所见 loss 曲线为作者原始训练的历史输出。
- **统一随机种子 42**：numpy/scipy 与 Cython 内核所用的 UCRT 双重播种（`ucrtbase.dll.srand(42)`），保证可复现。这是唯一影响数值的改动。
- 其余改动均为**保真最小适配**：预模拟路径改为本机、loss 绘图容错、恢复 `simulates` 写盘、Rmd `root_path` 路径。模型函数、噪声核与超参数**未改动**（MD5 一致）。
- 详细改动清单见各模块 `结论_中文.md` 与 `数值核对表.md`。

---

## 4. 目录结构

```
.
├── 1_moni/                     # 模拟模块（论文 §2）
│   ├── alpha_behavior.ipynb / .executed.ipynb
│   ├── density_sample_paths.ipynb / .executed.ipynb
│   ├── simulate_alpha_behavior.pkl
│   ├── *.png                   # 4 张复现图
│   ├── _*.py                   # 种子/校验/留痕脚本
│   └── 结论_中文.md
├── 2_Study1/                   # 研究一（论文 §3）
│   ├── *.ipynb / *.executed.ipynb
│   ├── estimates_param_estim/  # 参数估计 CSV（8 个）
│   ├── estimates_model_comp/   # 模型比较 PMP CSV（4 个）
│   ├── figures/                # 64 张复现图
│   ├── ttj_analyses.Rmd / .html
│   ├── _*.py, _step*.log
│   └── 结论_中文.md / 数值核对表.md
├── 3_Study2/                   # 研究二（论文 §4）
│   ├── *.ipynb / *.executed.ipynb
│   ├── estimates_param_estim/  # 参数估计 CSV（2 个）
│   ├── figures/                # 7 张复现图
│   ├── ttj_analyses_s2.Rmd / .html
│   ├── _*.py, _step*.log
│   └── 结论_中文.md / 数值核对表.md
├── README.md
├── NOTICE
├── LICENSE                     # 作者代码 MIT
└── LICENSE_DATA                # 作者数据/估计 CC BY 4.0
```

**未包含在本仓库**（体积大、版权或为原作者资产，见 `.gitignore`）：
`time_to_jump-main/`（作者源仓库）、论文 PDF（Elsevier 版权）、`*/data/`（原始数据）、
`*/validation_files/`（SBC 中间 pkl）、`*/_reference_estimates/`（作者参考结果）、
`*/checkpoint_*/`（作者训练权重）、`simulates_*/`（可再生成）、`*/3_simulators/`（符号链接容器，复跑时重建）、
`*workbuddy*/` 与 `.workbuddy/`（工作日志与工具目录）。

上传后实际纳入版本控制的文件约 **161 个、合计约 101MB**，最大单文件为 11.3MB 的 notebook，均在 GitHub 100MB 上限内。

---

## 5. 环境与依赖

- conda 环境 `ttj`，Python **3.10.22**
- numpy 1.26.2 / pandas 2.1.3 / scipy 1.11.3 / matplotlib 3.8.1 / seaborn 0.13.0 / numba 0.58.1 / statsmodels 0.14.2
- BayesFlow 与 TensorFlow（版本见原仓库 `dependencies.txt`）
- Cython 噪声核需用 **MSVC x64** 编译：`python my_setup.py build_ext --inplace`，产物 `levy_noise.cp310-win_amd64.pyd`
- R（渲染 `ttj_analyses*.Rmd`，需 `rmarkdown`、`brms`/`BayesFactor` 等，见 Rmd 头部）

---

## 6. 运行顺序

**1_moni**
```
alpha_behavior.ipynb  →  density_sample_paths.ipynb
```

**2_Study1**（需先将作者 checkpoint 放入对应 `checkpoint_*/` 目录）
```
param_estim_no_deadline.ipynb   # 主分析参数估计 + deadline 上下文
param_estim_deadline.ipynb      # 额外分析参数估计
model_comp_deadline.ipynb       # 额外分析模型比较
model_comp_no_deadline.ipynb    # 主分析模型比较
ttj_analyses.Rmd                # 行为统计与 BF，渲染 html
```

**3_Study2**
```
param_estim_no_deadline_s2.ipynb
ttj_analyses_s2.Rmd
```

> 执行版（`*.executed.ipynb`）保留了本次真跑的完整输出与日志，可直接查阅，无需重跑。

---

## 7. 数据与权重获取

本仓库**不托管**原始数据与作者训练权重。复跑前请从原作者仓库
<https://github.com/jvliss/time_to_jump> 获取：
- `3_simulators/data/`（含 `individual_data/`、`individual_data_s2/`）
- `3_simulators/checkpoint_ttj_*/net{1,2}/`
- 参考结果 `estimates_*`（如需对照）

按原仓库目录结构放入对应位置即可；`3_simulators/data` 与 `estimates_param_estim` 需建 junction / 符号链接以适配 Rmd 的写死路径。

---

## 8. 引用

```bibtex
@article{liss2026timetojump,
  title   = {Time to jump: Exploring the distribution of noise in evidence accumulation as a function of time pressure},
  author  = {Liss, Julia V. and von Krause, Mischa and Elsem{\"u}ller, Lasse and Hunsmann, Eva Marie and Lerche, Veronika},
  journal = {Cognitive Psychology},
  volume  = {167},
  pages   = {101836},
  year    = {2026}
}
```

---

## 9. 许可与署名

- 作者**代码**：MIT License（见 `LICENSE`）
- 作者**数据、模型估计、训练权重、图**：CC BY 4.0（见 `LICENSE_DATA`）
- 本复现仓库为派生作品，保留上述许可并署名原作者，详见 `NOTICE`。

本仓库中标注为"复现结果"的文件（`*.executed.ipynb`、`estimates_*`、`simulates_*`、`figures/`、`*.html`、`*.log`）
由本次复现产生；标注为"源文件"的模型函数、噪声核与 Rmd 来自原作者（MIT）。
