#!/usr/bin/env python3
"""
Model Comparison Report Generator

Compares performance of different LLM backends (Qwen, Kimi, Claude)
on various problem types and generates a detailed report.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class ModelResult:
    """Result from a single model on a single problem."""
    problem_id: str
    problem_type: str
    model_name: str
    solved: bool
    correct: bool
    time_seconds: float
    steps_count: int
    confidence: float
    error_message: str = ""


@dataclass
class ModelStats:
    """Statistics for a model across all problems."""
    model_name: str
    total_problems: int
    solved_count: int
    correct_count: int
    avg_time: float
    solve_rate: float
    accuracy: float
    by_type: Dict[str, Dict[str, float]]


class ModelComparator:
    """Compare multiple models on the same problem set."""

    def __init__(self):
        self.results: List[ModelResult] = []
        self.models_tested: List[str] = []

    def add_result(self, result: ModelResult):
        """Add a result from a model run."""
        self.results.append(result)
        if result.model_name not in self.models_tested:
            self.models_tested.append(result.model_name)

    def calculate_stats(self, model_name: str) -> ModelStats:
        """Calculate statistics for a specific model."""
        model_results = [r for r in self.results if r.model_name == model_name]

        if not model_results:
            return ModelStats(
                model_name=model_name,
                total_problems=0,
                solved_count=0,
                correct_count=0,
                avg_time=0.0,
                solve_rate=0.0,
                accuracy=0.0,
                by_type={},
            )

        total = len(model_results)
        solved = sum(1 for r in model_results if r.solved)
        correct = sum(1 for r in model_results if r.correct)
        avg_time = sum(r.time_seconds for r in model_results) / total if total > 0 else 0.0

        # Calculate by problem type
        by_type = {}
        types = set(r.problem_type for r in model_results)
        for ptype in types:
            type_results = [r for r in model_results if r.problem_type == ptype]
            type_total = len(type_results)
            type_solved = sum(1 for r in type_results if r.solved)
            type_correct = sum(1 for r in type_results if r.correct)

            by_type[ptype] = {
                "total": type_total,
                "solved": type_solved,
                "correct": type_correct,
                "solve_rate": type_solved / type_total if type_total > 0 else 0.0,
                "accuracy": type_correct / type_total if type_total > 0 else 0.0,
            }

        return ModelStats(
            model_name=model_name,
            total_problems=total,
            solved_count=solved,
            correct_count=correct,
            avg_time=avg_time,
            solve_rate=solved / total if total > 0 else 0.0,
            accuracy=correct / total if total > 0 else 0.0,
            by_type=by_type,
        )

    def generate_report(self, output_path: str) -> Dict[str, Any]:
        """Generate a comprehensive comparison report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "models_tested": self.models_tested,
            "total_problems": len(set(r.problem_id for r in self.results)),
            "model_stats": {},
            "comparison": {},
            "recommendations": [],
        }

        # Calculate stats for each model
        for model_name in self.models_tested:
            stats = self.calculate_stats(model_name)
            report["model_stats"][model_name] = asdict(stats)

        # Generate comparison insights
        if len(self.models_tested) >= 2:
            stats_list = [self.calculate_stats(m) for m in self.models_tested]

            # Find best model by solve rate
            best_solve = max(stats_list, key=lambda s: s.solve_rate)
            report["comparison"]["best_solve_rate"] = {
                "model": best_solve.model_name,
                "rate": f"{best_solve.solve_rate:.1%}",
            }

            # Find best model by accuracy
            best_accuracy = max(stats_list, key=lambda s: s.accuracy)
            report["comparison"]["best_accuracy"] = {
                "model": best_accuracy.model_name,
                "accuracy": f"{best_accuracy.accuracy:.1%}",
            }

            # Find fastest model
            fastest = min(stats_list, key=lambda s: s.avg_time)
            report["comparison"]["fastest"] = {
                "model": fastest.model_name,
                "avg_time": f"{fastest.avg_time:.2f}s",
            }

            # Generate recommendations
            for stats in stats_list:
                if stats.solve_rate >= 0.9:
                    report["recommendations"].append(
                        f"{stats.model_name}: Excellent solve rate ({stats.solve_rate:.1%}), recommended for production use."
                    )
                elif stats.solve_rate >= 0.7:
                    report["recommendations"].append(
                        f"{stats.model_name}: Good solve rate ({stats.solve_rate:.1%}), suitable for most tasks."
                    )
                else:
                    report["recommendations"].append(
                        f"{stats.model_name}: Low solve rate ({stats.solve_rate:.1%}), consider using for specific problem types only."
                    )

        # Save report
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return report


def generate_markdown_report(report: Dict[str, Any], output_path: str):
    """Generate a human-readable Markdown report."""
    lines = [
        "# Model Comparison Report",
        "",
        f"**Generated:** {report['timestamp']}",
        f"**Models Tested:** {', '.join(report['models_tested'])}",
        f"**Total Problems:** {report['total_problems']}",
        "",
        "## Summary",
        "",
    ]

    # Overall statistics table
    lines.append("### Overall Performance")
    lines.append("")
    lines.append("| Model | Solve Rate | Accuracy | Avg Time |")
    lines.append("|-------|------------|----------|----------|")

    for model_name, stats in report['model_stats'].items():
        lines.append(
            f"| {model_name} | {stats['solve_rate']:.1%} | "
            f"{stats['accuracy']:.1%} | {stats['avg_time']:.2f}s |"
        )

    lines.append("")

    # Performance by problem type
    lines.append("### Performance by Problem Type")
    lines.append("")

    for model_name, stats in report['model_stats'].items():
        lines.append(f"#### {model_name}")
        lines.append("")
        lines.append("| Type | Solve Rate | Accuracy |")
        lines.append("|------|------------|----------|")

        for ptype, type_stats in stats['by_type'].items():
            lines.append(
                f"| {ptype} | {type_stats['solve_rate']:.1%} | "
                f"{type_stats['accuracy']:.1%} |"
            )
        lines.append("")

    # Comparison insights
    if report.get('comparison'):
        lines.append("## Key Insights")
        lines.append("")

        if 'best_solve_rate' in report['comparison']:
            best = report['comparison']['best_solve_rate']
            lines.append(f"- **Best Solve Rate:** {best['model']} ({best['rate']})")

        if 'best_accuracy' in report['comparison']:
            best = report['comparison']['best_accuracy']
            lines.append(f"- **Best Accuracy:** {best['model']} ({best['accuracy']})")

        if 'fastest' in report['comparison']:
            fastest = report['comparison']['fastest']
            lines.append(f"- **Fastest:** {fastest['model']} ({fastest['avg_time']} avg)")

        lines.append("")

    # Recommendations
    if report.get('recommendations'):
        lines.append("## Recommendations")
        lines.append("")
        for rec in report['recommendations']:
            lines.append(f"- {rec}")
        lines.append("")

    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


if __name__ == "__main__":
    # Example usage: create a sample comparison
    comparator = ModelComparator()

    # Simulate results for demonstration
    sample_problems = [
        ("1", "limit"),
        ("2", "equation"),
        ("3", "derivative"),
        ("4", "conceptual"),
    ]

    models = ["Qwen", "Kimi", "Claude"]

    for model in models:
        for prob_id, prob_type in sample_problems:
            # Simulate different performance per model
            if model == "Claude":
                solved = True
                correct = True
                time_sec = 2.5
            elif model == "Qwen":
                solved = prob_type != "conceptual"
                correct = solved
                time_sec = 3.0
            else:  # Kimi
                solved = True
                correct = prob_type != "derivative"
                time_sec = 2.8

            comparator.add_result(ModelResult(
                problem_id=prob_id,
                problem_type=prob_type,
                model_name=model,
                solved=solved,
                correct=correct,
                time_seconds=time_sec,
                steps_count=3,
                confidence=0.9,
            ))

    # Generate reports
    report = comparator.generate_report("output/model_comparison.json")
    generate_markdown_report(report, "output/model_comparison.md")

    print("Model comparison report generated:")
    print("  - output/model_comparison.json")
    print("  - output/model_comparison.md")
