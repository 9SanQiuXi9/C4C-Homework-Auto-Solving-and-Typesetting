#!/usr/bin/env python3
"""
LLM Solver — 当 SymPy 符号计算无法处理时，调用大语言模型求解。

支持的后端:
  1. dashscope  — 阿里云通义千问 (Qwen)，通过 DashScope API
  2. openai     — 任何 OpenAI 兼容 API（大多数国产模型都支持）
  3. file       — 将 prompt 写入文件，等待人工/外部填入解答（无需 API）

环境变量:
  LLM_BACKEND       — dashscope | openai | file（默认 file）
  DASHSCOPE_API_KEY — DashScope API 密钥
  OPENAI_API_KEY    — OpenAI 兼容 API 密钥
  OPENAI_BASE_URL   — API 端点（默认 https://dashscope.aliyuncs.com/compatible-mode/v1）
  LLM_MODEL         — 模型名（默认 qwen-max）
  LLM_TIMEOUT       — 超时秒数（默认 60）

用法:
    from llm_solver import llm_solve
    result = llm_solve(problem_dict)
"""

import json
import os
import re
import sys
import time
from pathlib import Path

# ═══════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════

LLM_BACKEND = os.environ.get("LLM_BACKEND", "file")
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get(
    "OPENAI_BASE_URL",
    "https://dashscope.aliyuncs.com/compatible-mode/v1",
)
LLM_MODEL = os.environ.get("LLM_MODEL", "qwen-max")
LLM_TIMEOUT = int(os.environ.get("LLM_TIMEOUT", "60"))

PROMPT_DIR = Path(__file__).resolve().parent.parent / "llm_prompts"


# ═══════════════════════════════════════════════
# Prompt 构造
# ═══════════════════════════════════════════════

SYSTEM_PROMPT = """\
You are a math expert solving university-level homework. Return your answer in LaTeX.

Rules:
1. Show step-by-step working.
2. Wrap the final answer in \\boxed{...}.
3. Use $...$ for inline math, $$...$$ for display math.
4. For conceptual/proof questions, write a clear mathematical explanation.
5. For graph/draw questions, describe the key features of the graph precisely.
6. If the problem has sub-parts (a), (b), (c), label each part clearly.
7. Keep answers concise but complete.
"""


def _build_prompt(problem: dict) -> str:
    """把 problem dict 转为给 LLM 的文本 prompt。"""
    parts = []
    parts.append(f"Problem ID: {problem['id']}")
    parts.append(f"Type: {problem.get('type', 'unknown')}")
    parts.append(f"\nProblem text:\n{problem['text']}")

    subs = problem.get("sub_problems", [])
    if subs:
        parts.append("\nSub-problems:")
        for sub in subs:
            sid = sub.get("id", "?")
            parts.append(f"  ({sid}) {sub['text']}")

    return "\n".join(parts)


# ═══════════════════════════════════════════════
# Response 解析
# ═══════════════════════════════════════════════

def _parse_llm_response(response: str, problem: dict) -> dict:
    """从 LLM 的文本回复中提取结构化解答。"""
    response = response.strip()
    if not response:
        return _llm_unsolved(problem, "LLM 返回空回复")

    response = _clean_markdown(response)

    boxed = _extract_boxed(response)

    steps = _split_steps(response)

    sub_solutions = _parse_sub_solutions(response, problem)

    return {
        "problem_id": problem["id"],
        "problem_text": problem["text"],
        "solved": True,
        "steps": steps,
        "answer": boxed or response[:200],
        "answer_latex": boxed or _extract_final_answer(response),
        "solver": "llm",
        "sub_solutions": sub_solutions,
    }


def _clean_markdown(text: str) -> str:
    """去除常见 markdown 格式标记，保留纯 LaTeX。"""
    text = text.replace("**", "")
    text = re.sub(r"(?<!\$)\*(?!\*)(.+?)(?<!\$)\*(?!\*)", r"\\emph{\1}", text)
    return text


def _extract_boxed(text: str) -> str:
    """提取最后一个 \\boxed{...} 的内容。"""
    matches = list(re.finditer(r"\\boxed\{", text))
    if not matches:
        return ""
    last = matches[-1]
    start = last.end()
    depth = 1
    i = start
    while i < len(text) and depth > 0:
        if text[i] == "{" :
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    if depth == 0:
        return text[start:i - 1]
    return ""


def _extract_final_answer(text: str) -> str:
    """如果没有 \\boxed，尝试提取最后一段有意义的数学内容。"""
    lines = text.strip().split("\n")
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        math_matches = re.findall(r"\$\$(.+?)\$\$", line, re.DOTALL)
        if math_matches:
            return math_matches[-1]
        math_matches = re.findall(r"\$(.+?)\$", line, re.DOTALL)
        if math_matches:
            return math_matches[-1]
        if len(line) < 300:
            return line
    return text[:200]


def _split_steps(text: str) -> list:
    """把 LLM 回复拆成步骤列表。"""
    paragraphs = re.split(r"\n\s*\n", text.strip())
    steps = []
    for p in paragraphs:
        p = p.strip()
        if p:
            steps.append(p)
    if not steps:
        steps = [text[:500]]
    return steps


def _parse_sub_solutions(response: str, problem: dict) -> list:
    """尝试从 LLM 回复中拆分出子题解答。"""
    subs = problem.get("sub_problems", [])
    if not subs:
        return []

    cleaned = response.replace("**", "")

    sub_ids = [str(sub.get("id", "")) for sub in subs]
    header_pattern = r"(?:^|\n)\s*\((" + "|".join(re.escape(s) for s in sub_ids) + r")\)\s*"
    parts = re.split(header_pattern, cleaned, flags=re.IGNORECASE)

    sub_solutions = []
    for sub in subs:
        sid = str(sub.get("id", ""))
        idx = None
        for i, p in enumerate(parts):
            if p.lower() == sid.lower():
                idx = i
                break

        if idx is not None and idx + 1 < len(parts):
            sub_text = parts[idx + 1].strip()
            boxed = _extract_boxed(sub_text)
            steps = _split_steps(sub_text)
            sub_solutions.append({
                "problem_id": f"{problem['id']}.{sid}",
                "problem_text": sub["text"],
                "solved": True,
                "steps": steps,
                "answer": boxed or sub_text[:200],
                "answer_latex": boxed or _extract_final_answer(sub_text),
                "solver": "llm",
                "sub_solutions": [],
            })
        else:
            sub_solutions.append({
                "problem_id": f"{problem['id']}.{sid}",
                "problem_text": sub["text"],
                "solved": False,
                "steps": [],
                "answer": None,
                "answer_latex": "",
                "reason": "LLM 未返回此子题的解答",
                "solver": "llm",
                "sub_solutions": [],
            })

    solved_count = sum(1 for s in sub_solutions if s["solved"])
    if solved_count == 0 and subs:
        return []
    return sub_solutions


# ═══════════════════════════════════════════════
# 后端: DashScope / OpenAI 兼容 API
# ═══════════════════════════════════════════════

def _call_openai_compatible(prompt: str) -> str:
    """通过 OpenAI 兼容 API 调用 LLM。"""
    try:
        import urllib.request
        import urllib.error
    except ImportError:
        return ""

    api_key = OPENAI_API_KEY or DASHSCOPE_API_KEY
    if not api_key:
        return ""

    url = f"{OPENAI_BASE_URL}/chat/completions"
    payload = json.dumps({
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 4096,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=LLM_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  [LLM] API 调用失败: {e}")
        return ""


# ═══════════════════════════════════════════════
# 后端: 文件模式（无 API 时的 fallback）
# ═══════════════════════════════════════════════

def _call_file(prompt: str, problem: dict) -> str:
    """将 prompt 写入文件，检查是否有预填的解答文件。"""
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    pid = problem["id"]
    prompt_path = PROMPT_DIR / f"{pid}_prompt.txt"
    answer_path = PROMPT_DIR / f"{pid}_answer.txt"

    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(f"{SYSTEM_PROMPT}\n\n---\n\n{prompt}\n")

    if answer_path.exists():
        with open(answer_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    return ""


# ═══════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════

def _llm_unsolved(problem: dict, reason: str) -> dict:
    return {
        "problem_id": problem["id"],
        "problem_text": problem["text"],
        "solved": False,
        "steps": [],
        "answer": None,
        "answer_latex": "",
        "reason": reason,
        "solver": "llm",
        "sub_solutions": [],
    }


def llm_solve(problem: dict) -> dict:
    """
    用 LLM 求解一道题。

    按 LLM_BACKEND 选择后端:
      - "dashscope" / "openai" → 调用 API
      - "file" → 文件模式

    返回与 solve.py 兼容的 solution dict。
    """
    prompt = _build_prompt(problem)
    backend = LLM_BACKEND.lower()

    response = ""

    if backend in ("dashscope", "openai"):
        response = _call_openai_compatible(prompt)

    if backend == "file" or not response:
        response = _call_file(prompt, problem)

    if not response:
        if backend in ("dashscope", "openai"):
            return _llm_unsolved(
                problem,
                f"LLM API 未配置或调用失败。设置 {LLM_BACKEND.upper()}_API_KEY 环境变量，"
                f"或使用 LLM_BACKEND=file 并将解答写入 llm_prompts/{problem['id']}_answer.txt",
            )
        pid = problem["id"]
        answer_file = PROMPT_DIR / f"{pid}_answer.txt"
        return _llm_unsolved(
            problem,
            f"文件模式: 请将解答写入 {answer_file}",
        )

    return _parse_llm_response(response, problem)


def llm_solve_batch(problems: list) -> list:
    """批量 LLM 求解。"""
    results = []
    for p in problems:
        result = llm_solve(p)
        status = "✅" if result["solved"] else "❌"
        print(f"    {status} [LLM] {p['id']}")
        results.append(result)
    return results
