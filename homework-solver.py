#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C4C 作业自动求解与排版 —— 求解器命令行入口 (homework-solver).

本文件是 C4C 挑战「作业自动求解与排版」的求解器交付物入口。
底层流水线实现位于 ``scripts/`` 目录：

    Input -> Ingest -> Parse + Classify -> Solve -> Render LaTeX -> Compile PDF

用法（与 scripts/pipeline.py 完全一致）::

    python homework-solver.py <输入文件> <输出目录> [--compile] [--course "Math 1A"] [--student "Name"]

示例::

    python homework-solver.py examples/limits.md out --compile --course "Math 1A" --student "SanQiuXi"

输出文件：``1_ingested.json`` / ``2_parsed.json`` / ``3_solutions.json`` / ``homework.tex`` / ``homework.pdf``。
"""
import os
import sys
import subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
_PIPELINE = os.path.join(_HERE, "scripts", "pipeline.py")


def main() -> int:
    if not os.path.exists(_PIPELINE):
        sys.stderr.write("未找到求解器流水线: %s\n" % _PIPELINE)
        return 2
    # 以子进程方式调用流水线，保证 scripts/ 内部的同目录导入正常工作。
    return subprocess.call([sys.executable, _PIPELINE] + sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
