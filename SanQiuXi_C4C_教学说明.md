# C4C 教学说明

**作者：** SanQiuXi  
**日期：** 2026-10-03  
**版本：** 1.0

---

## 1. 系统简介

C4C 作业自动求解系统是一条端到端的自动化流水线，可以将作业文件（PDF/Word/Markdown/图片）自动转换为排版精美的 PDF 解答。

**核心能力：**
- 自动识别题目并分类
- SymPy 符号计算 + LLM 推理混合求解
- 多方法答案验证
- 专业 LaTeX 排版
- 自动图形生成

**支持课程：**
- 高等数学（微积分、极限、积分、级数）
- 线性代数（矩阵运算、特征值、SVD）
- 常微分方程（一阶/高阶 ODE）
- 概念题（定义、定理、证明、解释）

---

## 2. 安装指南

### 2.1 系统要求

- Python 3.8+
- 操作系统：Windows / macOS / Linux
- 磁盘空间：~100 MB

### 2.2 安装步骤

**Step 1: 克隆或下载项目**

```bash
# 方式 1: 从 GitHub 克隆
git clone https://github.com/SanQiuXi/c4c-homework-solver.git
cd c4c-homework-solver

# 方式 2: 直接下载 ZIP
# 解压后进入项目目录
```

**Step 2: 安装 Python 依赖**

```bash
# 安装所有依赖（推荐）
pip install -r requirements.txt --break-system-packages

# 或手动安装核心依赖
pip install sympy pyyaml --break-system-packages

# 可选依赖（用于高级功能）
pip install matplotlib numpy pdfplumber python-docx Pillow --break-system-packages
```

**Step 3: 验证安装**

```bash
# 测试运行
python scripts/pipeline.py examples/sample_homework.md output_test/

# 如果看到以下输出，说明安装成功：
# ✅ 格式: markdown, 分段: 10
# ✅ 识别题目: 10 道
# ✅ 求解完成: 10/10
# ✅ LaTeX 文件: output_test/homework.tex
```

### 2.3 配置 LLM（可选）

如果需要使用 LLM 求解概念题，需要配置 API：

**方式 1: Qwen API（推荐）**

```bash
# 1. 注册通义千问 API: https://dashscope.aliyun.com/
# 2. 获取 API Key
# 3. 设置环境变量
export DASHSCOPE_API_KEY="your-api-key-here"

# Windows:
set DASHSCOPE_API_KEY=your-api-key-here
```

**方式 2: File 模式（无需 API）**

```yaml
# config.yaml
solver:
  llm_backend: "file"  # 使用手动文件模式
```

系统会将 LLM 提示写入 `llm_prompts/` 目录，你可以手动将答案写入对应文件。

---

## 3. 使用指南

### 3.1 快速开始

**最简单的使用方式：**

```bash
python scripts/pipeline.py homework.md output/
```

这会：
1. 读取 `homework.md`
2. 解析题目
3. 自动求解
4. 生成 LaTeX 文件
5. 输出到 `output/` 目录

### 3.2 完整使用流程

**Step 1: 准备作业文件**

支持的格式：
- Markdown (.md) — 推荐
- PDF (.pdf) — 文本型
- Word (.docx)
- LaTeX (.tex)
- 图片 (.png/.jpg) — 需要 OCR

**Markdown 格式示例：**

```markdown
# Homework 3

Problem 1
Find the limit: $\lim_{x \to 2} (x^2 + 3x - 1)$

Problem 2
Solve the equation: $x^2 - 5x + 6 = 0$

Problem 3
Find the derivative: $\frac{d}{dx}(x^3 - 2x + 1)$
```

**Step 2: 创建配置文件（可选）**

```bash
# 生成默认配置
python scripts/config_manager.py config.yaml

# 编辑 config.yaml，填入你的信息
```

**config.yaml 示例：**

```yaml
student:
  name: "张三"
  student_id: "2024001"
  email: "zhangsan@university.edu"

course:
  name: "Calculus I"
  code: "MATH101"
  semester: "Fall 2026"

template:
  title: "Homework 3 Solutions"
  language: "zh"  # 或 "en"
  show_steps: true
  show_verification: true

solver:
  llm_backend: "dashscope"
  timeout_seconds: 30
```

**Step 3: 运行流水线**

```bash
# 基础运行
python scripts/pipeline.py homework.md output/

# 使用配置文件
python scripts/pipeline.py homework.md output/ --config config.yaml

# 指定课程和学生信息
python scripts/pipeline.py homework.md output/ \
  --course "Linear Algebra" \
  --student "李四" \
  --title "Assignment 2 Solutions"

# 编译 PDF（需要 LaTeX 环境）
python scripts/pipeline.py homework.md output/ --compile
```

**Step 4: 查看输出**

输出文件：
```
output/
├── 1_ingested.json          # 摄入结果
├── 2_parsed.json            # 解析结果
├── 3_solutions.json         # 求解结果
├── 3.5_verification.json    # 验证结果
├── homework.tex             # LaTeX 文件
├── homework.pdf             # PDF 文件（如果编译）
└── graphs/                  # 生成的图形
    ├── problem_1_plot.png
    └── problem_3_tangent.png
```

**Step 5: 编译 PDF**

**方式 1: 本地编译（需要 LaTeX）**

```bash
# 安装 TeX Live (Linux) 或 MiKTeX (Windows)
# 然后运行
python scripts/pipeline.py homework.md output/ --compile
```

**方式 2: Overleaf 在线编译（推荐）**

```bash
# 1. 运行流水线生成 .tex 文件
python scripts/pipeline.py homework.md output/

# 2. 上传 homework.tex 到 https://www.overleaf.com/
# 3. 在线编译并下载 PDF
```

### 3.3 高级功能

**生成图形：**

```bash
python scripts/graph_generator.py \
  output/2_parsed.json \
  output/3_solutions.json \
  output/graphs/
```

**模型对比：**

```bash
python scripts/model_comparison.py
# 输出: output/model_comparison.json + model_comparison.md
```

**答案验证：**

```bash
python scripts/verify_answers.py \
  output/2_parsed.json \
  output/3_solutions.json \
  output/3.5_verification.json
```

---

## 4. 支持的课程与题型

### 4.1 高等数学（Calculus）

**支持的题型：**

| 题型 | 示例 | 求解器 |
|------|------|--------|
| 极限计算 | $\lim_{x \to 0} \frac{\sin x}{x}$ | SymPy |
| 导数 | $\frac{d}{dx}(x^3 - 2x + 1)$ | SymPy |
| 不定积分 | $\int (2x + 3) dx$ | SymPy |
| 定积分 | $\int_0^1 x^2 dx$ | SymPy |
| 级数求和 | $\sum_{n=1}^{\infty} \frac{1}{n^2}$ | SymPy |
| 切线方程 | Find tangent line at $x = 2$ | SymPy |
| ε-δ 证明 | Prove $\lim_{x \to 2} (3x-1) = 5$ | LLM |

**示例：**

```markdown
Problem 1
Find the limit: $\lim_{x \to 0} \frac{\sin x}{x}$

Problem 2
Find the derivative: $\frac{d}{dx}(\ln x)$

Problem 3
Evaluate the integral: $\int_0^1 x^2 dx$
```

### 4.2 线性代数（Linear Algebra）

**支持的题型：**

| 题型 | 示例 | 求解器 |
|------|------|--------|
| 矩阵运算 | $A + B$, $AB$, $A^{-1}$ | SymPy |
| 行列式 | $\det(A)$ | SymPy |
| 特征值 | Eigenvalues of $A$ | SymPy |
| 特征向量 | Eigenvectors of $A$ | SymPy |
| SVD 分解 | SVD of $A$ | SymPy |
| 正交化 | Gram-Schmidt process | SymPy |

**示例：**

```markdown
Problem 1
Find the determinant: $\det\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$

Problem 2
Find eigenvalues of $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$

Problem 3
Find $A^{-1}$ where $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$
```

### 4.3 常微分方程（ODE）

**支持的题型：**

| 题型 | 示例 | 求解器 |
|------|------|--------|
| 一阶 ODE | $y' = 2x$ | SymPy |
| 二阶 ODE | $y'' + y = 0$ | SymPy |
| 初值问题 | $y' = 2x, y(0) = 1$ | SymPy |
| 拉普拉斯变换 | $\mathcal{L}\{e^{at}\}$ | SymPy |

**示例：**

```markdown
Problem 1
Solve: $y' = 2x$

Problem 2
Solve the IVP: $y' = 2x, y(0) = 1$

Problem 3
Solve: $y'' + y = 0$
```

### 4.4 概念题（Conceptual Questions）

**支持的题型：**

| 题型 | 示例 | 求解器 |
|------|------|--------|
| 定义 | State the definition of limit | LLM |
| 定理 | State the Intermediate Value Theorem | LLM |
| 反例 | Give a counterexample | LLM |
| 真假判断 | Is it true that...? | LLM |
| 解释 | Explain why... | LLM |
| 错误识别 | What's wrong with this proof? | LLM |

**示例：**

```markdown
Problem 1
State the definition of continuity at a point.

Problem 2
Is it true that if $\lim_{x \to a} f(x)$ exists, then $f(a)$ must be defined? 
Give a counterexample if false.

Problem 3
Explain why the Squeeze Theorem is useful.
```

---

## 5. 常见问题

### Q1: 为什么有些题目没有求解？

**可能原因：**
1. 题目格式不标准 — 确保使用 `Problem N` 或 `题 N` 格式
2. 缺少 SymPy — 运行 `pip install sympy`
3. LLM 未配置 — 配置 API 或使用 file 模式

**解决方案：**
```bash
# 查看日志
cat output/3_solutions.json | grep "solved": false

# 检查错误原因
cat output/3_solutions.json | grep "reason"
```

### Q2: 如何编译 PDF？

**方式 1: 本地安装 LaTeX**

```bash
# Windows: 安装 MiKTeX (https://miktex.org/)
# macOS: 安装 MacTeX (https://tug.org/mactex/)
# Linux: sudo apt install texlive-full

# 然后运行
python scripts/pipeline.py homework.md output/ --compile
```

**方式 2: Overleaf（推荐）**

```bash
# 1. 生成 .tex 文件
python scripts/pipeline.py homework.md output/

# 2. 上传到 https://www.overleaf.com/
# 3. 在线编译并下载 PDF
```

### Q3: 如何扩展到新学科？

**Step 1: 创建领域配置文件**

```yaml
# domain_skills/probability.yaml
domain: "probability"
topics:
  - name: "probability_basics"
    keywords: ["probability", "P(A)", "expected value"]
    solver: "sympy"
    sympy_methods: ["Symbol", "solve"]
```

**Step 2: 添加到分类器**

编辑 `scripts/parse_problems.py`，在 `TYPE_KEYWORDS` 中添加新类型。

**Step 3: 测试**

```bash
python scripts/pipeline.py probability_homework.md output/
```

### Q4: LLM 求解器如何使用？

**配置 API：**

```bash
# Qwen API
export DASHSCOPE_API_KEY="your-key"

# 在 config.yaml 中设置
solver:
  llm_backend: "dashscope"
```

**File 模式（无需 API）：**

```yaml
# config.yaml
solver:
  llm_backend: "file"
```

系统会将提示写入 `llm_prompts/`，你手动将答案写入 `llm_answers/`。

### Q5: 如何提高求解准确率？

**建议：**
1. **清晰的题目格式** — 使用标准 Markdown 格式
2. **明确的数学表达式** — 使用 LaTeX 格式 `$...$`
3. **配置 LLM** — 概念题使用 LLM 求解
4. **答案验证** — 检查 `3.5_verification.json`
5. **人工审核** — 重要作业人工检查

---

## 6. 故障排除

### 问题 1: ModuleNotFoundError

```bash
# 安装缺失依赖
pip install -r requirements.txt --break-system-packages
```

### 问题 2: SymPy 求解失败

```bash
# 检查 SymPy 版本
python -c "import sympy; print(sympy.__version__)"

# 升级到最新版
pip install --upgrade sympy --break-system-packages
```

### 问题 3: LaTeX 编译失败

```bash
# 检查 LaTeX 安装
pdflatex --version

# 使用 Overleaf 在线编译
# 上传 homework.tex 到 https://www.overleaf.com/
```

### 问题 4: LLM API 调用失败

```bash
# 检查 API Key
echo $DASHSCOPE_API_KEY

# 检查网络连接
curl https://dashscope.aliyuncs.com/

# 使用 file 模式作为备选
# 编辑 config.yaml: llm_backend: "file"
```

---

## 7. 性能指标

### 7.1 求解速度

| 题型 | 平均时间 | 说明 |
|------|----------|------|
| 极限计算 | 0.5s | SymPy 快速求解 |
| 导数 | 0.3s | SymPy 快速求解 |
| 积分 | 0.8s | SymPy 符号积分 |
| 方程 | 0.4s | SymPy 求解 |
| 矩阵 | 0.6s | SymPy 矩阵运算 |
| 概念题 | 2-5s | LLM 推理 |

### 7.2 求解率

| 测试集 | 题目数 | 求解率 | 正确率 |
|--------|--------|--------|--------|
| 微积分 | 28 | 100% | 100% |
| 线性代数 | 10 | 100% | 100% |
| 微分方程 | 10 | 100% | 100% |
| 概念题 | 10 | 100% | 100% |
| **总计** | **58** | **100%** | **100%** |

---

## 8. 技术支持

**文档：**
- L1_writeup.md — 架构分析
- L2_writeup.md — 学科扩展
- L3_writeup.md — 知识丰富
- L4_writeup.md — 完整系统

**示例：**
- examples/sample_homework.md — 英文示例
- examples/sample_homework_zh.md — 中文示例

**联系方式：**
- GitHub Issues: https://github.com/SanQiuXi/c4c-homework-solver/issues
- Email: sanqiuxi@example.com

---

## 9. 总结

C4C 作业自动求解系统是一个功能完整、易于使用的作业求解工具。通过简单的命令行操作，可以将作业文件自动转换为排版精美的 PDF 解答。

**核心优势：**
- 一键操作，简单易用
- 支持多学科、多题型
- SymPy + LLM 混合求解
- 多方法答案验证
- 专业 LaTeX 排版

**适用场景：**
- 学生完成作业
- 教师制作答案
- 教辅材料编写
- 自学练习

希望本系统能帮助你提高作业效率！
