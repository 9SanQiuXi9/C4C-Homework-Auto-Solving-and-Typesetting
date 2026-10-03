# Oracle: Integration and Series — Core Knowledge Summary

> Distilled from Stewart's Calculus Ch. 5-7 and SymPy computational patterns.

## 1. Definite Integration

### Fundamental Theorem of Calculus
If $F'(x) = f(x)$, then $\int_a^b f(x)\,dx = F(b) - F(a)$.

### Key Integration Rules
- **Power rule**: $\int x^n\,dx = \frac{x^{n+1}}{n+1} + C$ for $n \neq -1$
- **Trig**: $\int \sin x\,dx = -\cos x + C$, $\int \cos x\,dx = \sin x + C$
- **Exponential**: $\int e^x\,dx = e^x + C$, $\int \frac{1}{x}\,dx = \ln|x| + C$

### SymPy Usage
```python
from sympy import integrate, Symbol
x = Symbol('x')
integrate(x**2, x)             # indefinite: x**3/3
integrate(x**2, (x, 0, 1))    # definite: 1/3
```

## 2. Volume by Disk Method

Rotating $y = f(x)$ around the $x$-axis from $a$ to $b$:
$$V = \pi \int_a^b [f(x)]^2\,dx$$

### Example: Wine Barrel
Rotate $y = R - cx^2$ around $x$-axis for $x \in [-h/2, h/2]$:
$$V = \pi \int_{-h/2}^{h/2} (R - cx^2)^2\,dx$$

Expand and integrate term by term. Use symmetry for even functions.

## 3. Optimization via Differentiation

To find extrema of $g(T)$:
1. Compute $g'(T)$
2. Solve $g'(T) = 0$
3. Verify minimum via $g''(T) > 0$

### EPQ Formula
Minimizing $\bar{Z} = \frac{S}{DT} + C + \frac{HT}{2}(1 - D/P)$ gives:
$$T^* = \sqrt{\frac{2S}{HD(1 - D/P)}}$$

## 4. Series and Telescoping Sums

### Product-to-Sum Identity
$$2\sin\left(\frac{x}{2}\right)\cos(ix) = \sin\left(i + \tfrac{1}{2}\right)x - \sin\left(i - \tfrac{1}{2}\right)x$$

Summing from $i = 1$ to $n$ telescopes to:
$$\sum_{i=1}^n \cos(ix) = \frac{\sin\left(n + \frac{1}{2}\right)x - \sin\left(\frac{x}{2}\right)}{2\sin\left(\frac{x}{2}\right)}$$

## 5. Limit of Polygon Areas

A regular $n$-gon inscribed in a unit circle has area:
$$A_n = \frac{n}{2}\sin\left(\frac{2\pi}{n}\right)$$

As $n \to \infty$:
$$\lim_{n\to\infty} A_n = \pi$$

This is the area of the unit circle, confirming the geometric intuition.

## 6. Binomial Theorem via Differentiation

$f(x) = (1+x)^n = \sum_{k=0}^n a_k x^k$

The $k$-th derivative at $x = 0$:
$$f^{(k)}(0) = n(n-1)\cdots(n-k+1) = k!\,a_k$$

Therefore $a_k = \binom{n}{k} = \frac{n!}{k!(n-k)!}$.
