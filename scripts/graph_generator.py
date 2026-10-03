#!/usr/bin/env python3
"""
Automatic Graph Generation Module

Generates visualizations for mathematical functions, vector fields,
and other mathematical objects using matplotlib.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys

# Try to import matplotlib, but don't fail if not available
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib import rcParams
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# Try to import numpy for numerical computations
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class GraphGenerator:
    """Generate graphs for mathematical problems."""

    def __init__(self, output_dir: str = "output/graphs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if HAS_MATPLOTLIB:
            # Configure matplotlib for better quality
            rcParams['figure.dpi'] = 150
            rcParams['font.size'] = 10
            rcParams['axes.grid'] = True
            rcParams['grid.alpha'] = 0.3

    def generate_for_problem(self, problem: Dict, solution: Dict) -> Optional[str]:
        """Generate appropriate graph for a problem."""
        if not HAS_MATPLOTLIB or not HAS_NUMPY:
            return None

        problem_type = problem.get("type", "")
        problem_text = problem.get("text", "")

        # Determine what type of graph to generate
        if problem_type == "tangent":
            return self._generate_tangent_graph(problem, solution)
        elif problem_type == "limit":
            return self._generate_limit_graph(problem, solution)
        elif problem_type == "derivative":
            return self._generate_derivative_graph(problem, solution)
        elif problem_type == "integral":
            return self._generate_integral_graph(problem, solution)
        elif "vector field" in problem_text.lower():
            return self._generate_vector_field(problem, solution)
        elif "plot" in problem_text.lower() or "graph" in problem_text.lower():
            return self._generate_function_plot(problem, solution)

        return None

    def _generate_tangent_graph(self, problem: Dict, solution: Dict) -> str:
        """Generate graph showing function and tangent line."""
        problem_text = problem.get("text", "")

        # Extract function and point (simplified parsing)
        # In practice, this would need more robust parsing
        x_val = 1.0  # Default
        func = lambda x: x**2  # Default function

        # Try to extract from problem text
        x_match = re.search(r'at\s+x\s*=\s*(\d+)', problem_text)
        if x_match:
            x_val = float(x_match.group(1))

        # Generate x values
        x = np.linspace(x_val - 2, x_val + 2, 100)
        y = func(x)

        # Calculate tangent line
        y_val = func(x_val)
        slope = 2 * x_val  # Derivative of x^2
        tangent_y = slope * (x - x_val) + y_val

        # Plot
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y, 'b-', linewidth=2, label='f(x) = x²')
        ax.plot(x, tangent_y, 'r--', linewidth=2, label=f'Tangent at x={x_val}')
        ax.plot(x_val, y_val, 'ko', markersize=8)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Function and Tangent Line')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Save
        output_path = self.output_dir / f"problem_{problem.get('id')}_tangent.png"
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        plt.close()

        return str(output_path)

    def _generate_limit_graph(self, problem: Dict, solution: Dict) -> str:
        """Generate graph showing limit behavior."""
        problem_text = problem.get("text", "")

        # Default: show a function with a limit
        x = np.linspace(-2, 2, 200)

        # Example: sin(x)/x
        with np.errstate(divide='ignore', invalid='ignore'):
            y = np.sin(x) / x
        y[np.abs(x) < 0.01] = 1.0  # Handle the limit at x=0

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y, 'b-', linewidth=2, label='f(x) = sin(x)/x')
        ax.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='Limit = 1')
        ax.plot(0, 1, 'ro', markersize=8)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Limit Visualization')
        ax.legend()
        ax.set_ylim(-0.5, 1.5)
        ax.grid(True, alpha=0.3)

        output_path = self.output_dir / f"problem_{problem.get('id')}_limit.png"
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        plt.close()

        return str(output_path)

    def _generate_derivative_graph(self, problem: Dict, solution: Dict) -> str:
        """Generate graph showing function and its derivative."""
        x = np.linspace(-3, 3, 200)
        y = x**3 - 3*x  # Example function
        dy = 3*x**2 - 3  # Derivative

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y, 'b-', linewidth=2, label='f(x)')
        ax.plot(x, dy, 'r-', linewidth=2, label="f'(x)")
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Function and Derivative')
        ax.legend()
        ax.grid(True, alpha=0.3)

        output_path = self.output_dir / f"problem_{problem.get('id')}_derivative.png"
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        plt.close()

        return str(output_path)

    def _generate_integral_graph(self, problem: Dict, solution: Dict) -> str:
        """Generate graph showing area under curve."""
        x = np.linspace(0, 3, 200)
        y = x**2

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y, 'b-', linewidth=2, label='f(x) = x²')
        ax.fill_between(x[(x >= 1) & (x <= 2)], y[(x >= 1) & (x <= 2)],
                        alpha=0.3, color='blue', label='Area = ∫[1,2] x² dx')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Definite Integral')
        ax.legend()
        ax.grid(True, alpha=0.3)

        output_path = self.output_dir / f"problem_{problem.get('id')}_integral.png"
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        plt.close()

        return str(output_path)

    def _generate_vector_field(self, problem: Dict, solution: Dict) -> str:
        """Generate vector field plot."""
        x = np.linspace(-2, 2, 15)
        y = np.linspace(-2, 2, 15)
        X, Y = np.meshgrid(x, y)

        # Example vector field: F(x,y) = (y, -x)
        U = Y
        V = -X

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.quiver(X, Y, U, V, color='blue', alpha=0.7)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Vector Field F(x,y) = (y, -x)')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

        output_path = self.output_dir / f"problem_{problem.get('id')}_vector_field.png"
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        plt.close()

        return str(output_path)

    def _generate_function_plot(self, problem: Dict, solution: Dict) -> str:
        """Generate generic function plot."""
        x = np.linspace(-5, 5, 300)
        y = np.sin(x) * np.exp(-0.1 * x**2)  # Example: damped sine wave

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y, 'b-', linewidth=2)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Function Plot')
        ax.grid(True, alpha=0.3)

        output_path = self.output_dir / f"problem_{problem.get('id')}_plot.png"
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        plt.close()

        return str(output_path)


def generate_graphs_for_solutions(problems_path: str, solutions_path: str,
                                   output_dir: str = "output/graphs") -> List[str]:
    """Generate graphs for all solutions."""
    if not HAS_MATPLOTLIB or not HAS_NUMPY:
        print("Warning: matplotlib or numpy not available, skipping graph generation")
        return []

    with open(problems_path, 'r', encoding='utf-8') as f:
        problems = json.load(f)

    with open(solutions_path, 'r', encoding='utf-8') as f:
        solutions = json.load(f)

    generator = GraphGenerator(output_dir)
    generated = []

    for solution in solutions:
        if not solution.get("solved"):
            continue

        problem_id = solution.get("problem_id")
        problem = next((p for p in problems if p.get("id") == problem_id), None)

        if problem:
            graph_path = generator.generate_for_problem(problem, solution)
            if graph_path:
                generated.append(graph_path)
                print(f"Generated graph: {graph_path}")

    return generated


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3:
        problems_path = sys.argv[1]
        solutions_path = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "output/graphs"

        generated = generate_graphs_for_solutions(problems_path, solutions_path, output_dir)
        print(f"\nGenerated {len(generated)} graphs")
    else:
        print("Usage: python graph_generator.py <problems.json> <solutions.json> [output_dir]")
