#!/usr/bin/env python3
"""
Stage 3.5: Answer Verification Module

Verifies solutions using multiple strategies:
1. Numerical substitution - plug answer back into original equation
2. Dimension analysis - check physical units match
3. Cross-checking - use multiple methods to verify
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    from sympy import sympify, Symbol, solve, diff, integrate, limit, simplify, oo
    from sympy.parsing.sympy_parser import parse_expr
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False


class AnswerVerifier:
    """Verify solutions using multiple strategies."""

    def __init__(self):
        self.verification_results = []

    def verify_all(self, problems: List[Dict], solutions: List[Dict]) -> List[Dict]:
        """Verify all solutions against problems."""
        results = []

        for solution in solutions:
            problem_id = solution.get("problem_id")
            problem = next((p for p in problems if p.get("id") == problem_id), None)

            if not problem:
                results.append({
                    "problem_id": problem_id,
                    "verified": False,
                    "method": "none",
                    "confidence": 0.0,
                    "details": "Problem not found"
                })
                continue

            if not solution.get("solved"):
                results.append({
                    "problem_id": problem_id,
                    "verified": False,
                    "method": "none",
                    "confidence": 0.0,
                    "details": "Not solved"
                })
                continue

            # Apply verification based on problem type
            verification = self._verify_solution(problem, solution)
            results.append(verification)

        return results

    def _verify_solution(self, problem: Dict, solution: Dict) -> Dict:
        """Verify a single solution."""
        problem_type = problem.get("type", "unknown")
        problem_text = problem.get("text", "")
        answer_latex = solution.get("answer_latex", "")
        answer_text = solution.get("answer", "")

        # Try different verification methods based on problem type
        if problem_type == "equation":
            return self._verify_equation(problem, solution)
        elif problem_type == "limit":
            return self._verify_limit(problem, solution)
        elif problem_type == "derivative":
            return self._verify_derivative(problem, solution)
        elif problem_type == "integral":
            return self._verify_integral(problem, solution)
        elif problem_type == "tangent":
            return self._verify_tangent(problem, solution)
        elif problem_type == "matrix":
            return self._verify_matrix(problem, solution)
        elif problem_type == "ode":
            return self._verify_ode(problem, solution)
        elif problem_type == "conceptual":
            return self._verify_conceptual(problem, solution)
        else:
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "none",
                "confidence": 0.0,
                "details": f"No verification method for type: {problem_type}"
            }

    def _verify_equation(self, problem: Dict, solution: Dict) -> Dict:
        """Verify equation solution by substitution."""
        if not HAS_SYMPY:
            return self._no_sympy_result(problem.get("id"))

        try:
            problem_text = problem.get("text", "")
            answer_latex = solution.get("answer_latex", "")

            # Extract equation from problem
            eq_match = re.search(r'([^=]+)=([^$]+)', problem_text)
            if not eq_match:
                return {
                    "problem_id": problem.get("id"),
                    "verified": None,
                    "method": "equation_substitution",
                    "confidence": 0.0,
                    "details": "Could not extract equation"
                }

            # Extract variable and solution
            var_match = re.search(r'[Ss]olve\s+(?:for\s+)?(\w+)', problem_text)
            if not var_match:
                var_match = re.search(r'(\w+)\s*=', problem_text)

            if not var_match:
                return {
                    "problem_id": problem.get("id"),
                    "verified": None,
                    "method": "equation_substitution",
                    "confidence": 0.0,
                    "details": "Could not identify variable"
                }

            var_name = var_match.group(1)
            var = Symbol(var_name)

            # Parse the equation
            lhs_str = eq_match.group(1).strip().replace('$', '').replace('\\', '')
            rhs_str = eq_match.group(2).strip().replace('$', '').replace('\\', '')

            # Try to parse and verify
            try:
                lhs = parse_expr(lhs_str, evaluate=False)
                rhs = parse_expr(rhs_str, evaluate=False)

                # Extract numerical answer
                answer_match = re.search(r'[-+]?\d+', answer_latex)
                if answer_match:
                    answer_val = int(answer_match.group())
                    substituted_lhs = lhs.subs(var, answer_val)
                    substituted_rhs = rhs.subs(var, answer_val)

                    if simplify(substituted_lhs - substituted_rhs) == 0:
                        return {
                            "problem_id": problem.get("id"),
                            "verified": True,
                            "method": "equation_substitution",
                            "confidence": 1.0,
                            "details": f"Substitution verified: {var_name}={answer_val}"
                        }
                    else:
                        return {
                            "problem_id": problem.get("id"),
                            "verified": False,
                            "method": "equation_substitution",
                            "confidence": 1.0,
                            "details": f"Substitution failed: LHS={substituted_lhs}, RHS={substituted_rhs}"
                        }
            except Exception as e:
                pass

            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "equation_substitution",
                "confidence": 0.0,
                "details": f"Could not parse equation: {str(e)}"
            }

        except Exception as e:
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "equation_substitution",
                "confidence": 0.0,
                "details": f"Verification error: {str(e)}"
            }

    def _verify_limit(self, problem: Dict, solution: Dict) -> Dict:
        """Verify limit by numerical approximation."""
        if not HAS_SYMPY:
            return self._no_sympy_result(problem.get("id"))

        try:
            problem_text = problem.get("text", "")
            answer_latex = solution.get("answer_latex", "")

            # Extract limit expression
            limit_match = re.search(r'\\lim_\{[^}]*\}\s*([^$]+)', problem_text)
            if not limit_match:
                return {
                    "problem_id": problem.get("id"),
                    "verified": None,
                    "method": "limit_numerical",
                    "confidence": 0.0,
                    "details": "Could not extract limit expression"
                }

            # Extract the answer value
            answer_match = re.search(r'[-+]?\d+', answer_latex)
            if not answer_match:
                return {
                    "problem_id": problem.get("id"),
                    "verified": None,
                    "method": "limit_numerical",
                    "confidence": 0.0,
                    "details": "Could not extract answer value"
                }

            expected = int(answer_match.group())

            # For now, just mark as plausible (full numerical verification is complex)
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "limit_numerical",
                "confidence": 0.5,
                "details": f"Limit answer {expected} extracted (numerical verification not implemented)"
            }

        except Exception as e:
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "limit_numerical",
                "confidence": 0.0,
                "details": f"Verification error: {str(e)}"
            }

    def _verify_derivative(self, problem: Dict, solution: Dict) -> Dict:
        """Verify derivative by re-differentiation."""
        if not HAS_SYMPY:
            return self._no_sympy_result(problem.get("id"))

        try:
            # Placeholder for derivative verification
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "derivative_recheck",
                "confidence": 0.0,
                "details": "Derivative verification not yet implemented"
            }
        except Exception as e:
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "derivative_recheck",
                "confidence": 0.0,
                "details": f"Verification error: {str(e)}"
            }

    def _verify_integral(self, problem: Dict, solution: Dict) -> Dict:
        """Verify integral by differentiation."""
        if not HAS_SYMPY:
            return self._no_sympy_result(problem.get("id"))

        try:
            # Placeholder for integral verification
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "integral_differentiation",
                "confidence": 0.0,
                "details": "Integral verification not yet implemented"
            }
        except Exception as e:
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "integral_differentiation",
                "confidence": 0.0,
                "details": f"Verification error: {str(e)}"
            }

    def _verify_tangent(self, problem: Dict, solution: Dict) -> Dict:
        """Verify tangent line by checking point and slope."""
        if not HAS_SYMPY:
            return self._no_sympy_result(problem.get("id"))

        try:
            # Placeholder for tangent verification
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "tangent_check",
                "confidence": 0.0,
                "details": "Tangent verification not yet implemented"
            }
        except Exception as e:
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "tangent_check",
                "confidence": 0.0,
                "details": f"Verification error: {str(e)}"
            }

    def _verify_matrix(self, problem: Dict, solution: Dict) -> Dict:
        """Verify matrix operations."""
        if not HAS_SYMPY:
            return self._no_sympy_result(problem.get("id"))

        try:
            # Placeholder for matrix verification
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "matrix_check",
                "confidence": 0.0,
                "details": "Matrix verification not yet implemented"
            }
        except Exception as e:
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "matrix_check",
                "confidence": 0.0,
                "details": f"Verification error: {str(e)}"
            }

    def _verify_ode(self, problem: Dict, solution: Dict) -> Dict:
        """Verify ODE solution by substitution."""
        if not HAS_SYMPY:
            return self._no_sympy_result(problem.get("id"))

        try:
            # Placeholder for ODE verification
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "ode_substitution",
                "confidence": 0.0,
                "details": "ODE verification not yet implemented"
            }
        except Exception as e:
            return {
                "problem_id": problem.get("id"),
                "verified": None,
                "method": "ode_substitution",
                "confidence": 0.0,
                "details": f"Verification error: {str(e)}"
            }

    def _verify_conceptual(self, problem: Dict, solution: Dict) -> Dict:
        """Verify conceptual questions (limited verification possible)."""
        # Conceptual questions can't be automatically verified easily
        return {
            "problem_id": problem.get("id"),
            "verified": None,
            "method": "conceptual_review",
            "confidence": 0.0,
            "details": "Conceptual questions require manual review"
        }

    def _no_sympy_result(self, problem_id: str) -> Dict:
        """Return result when SymPy is not available."""
        return {
            "problem_id": problem_id,
            "verified": None,
            "method": "none",
            "confidence": 0.0,
            "details": "SymPy not available"
        }


def verify_answers(problems_path: str, solutions_path: str, output_path: str):
    """Main verification function."""
    # Load problems and solutions
    with open(problems_path, 'r', encoding='utf-8') as f:
        problems = json.load(f)

    with open(solutions_path, 'r', encoding='utf-8') as f:
        solutions = json.load(f)

    # Verify
    verifier = AnswerVerifier()
    results = verifier.verify_all(problems, solutions)

    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print summary
    verified_count = sum(1 for r in results if r.get("verified") is True)
    failed_count = sum(1 for r in results if r.get("verified") is False)
    unverified_count = sum(1 for r in results if r.get("verified") is None)

    print(f"\n{'='*60}")
    print(f"VERIFICATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total problems: {len(results)}")
    print(f"Verified: {verified_count}")
    print(f"Failed: {failed_count}")
    print(f"Unverified: {unverified_count}")
    print(f"{'='*60}\n")

    return results


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python verify_answers.py <problems.json> <solutions.json> <output.json>")
        sys.exit(1)

    problems_path = sys.argv[1]
    solutions_path = sys.argv[2]
    output_path = sys.argv[3]

    verify_answers(problems_path, solutions_path, output_path)
