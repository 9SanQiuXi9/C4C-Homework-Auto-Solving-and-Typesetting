# Worked Examples: Calculus I — Limits & Derivatives

> Distilled from Berkeley Math 1A office hours, TA sessions, and exam review worksheets.
> Authority: secondary (worked examples from instructional staff)

---

## Category 1: Epsilon-Delta Proofs

### Example 1: Linear Function (Easy)

**Problem:** Prove that $\lim_{x \to 3} (2x + 1) = 7$ using the ε-δ definition.

**Solution (Four Keywords Method):**

**Given:** Let $\varepsilon > 0$ be arbitrary.

**Choose:** We need $|2x + 1 - 7| < \varepsilon$ whenever $0 < |x - 3| < \delta$.

Simplify: $|2x - 6| = 2|x - 3| < \varepsilon$

So we need $|x - 3| < \varepsilon / 2$.

**Choose** $\delta = \varepsilon / 2$.

**Suppose:** $0 < |x - 3| < \delta$.

**Check:** $|2x + 1 - 7| = |2x - 6| = 2|x - 3| < 2\delta = 2(\varepsilon/2) = \varepsilon$. $\square$

**Key Insight:** For linear functions, δ is a simple multiple of ε. No bounding needed.

---

### Example 2: Quadratic Function (Medium)

**Problem:** Prove that $\lim_{x \to 2} x^2 = 4$ using the ε-δ definition.

**Solution:**

**Given:** Let $\varepsilon > 0$ be arbitrary.

**Choose:** We need $|x^2 - 4| < \varepsilon$ whenever $0 < |x - 2| < \delta$.

Factor: $|x^2 - 4| = |x - 2||x + 2|$.

**Problem:** The factor $|x + 2|$ depends on $x$, so we can't directly solve for δ.

**Strategy:** Bound $|x + 2|$ by restricting δ.

**Suppose** $\delta \leq 1$. Then $|x - 2| < 1$, so $-1 < x - 2 < 1$, so $1 < x < 3$, so $3 < x + 2 < 5$.

Thus $|x + 2| < 5$.

Now we need $|x - 2| \cdot 5 < \varepsilon$, so $|x - 2| < \varepsilon / 5$.

**Choose** $\delta = \min(1, \varepsilon / 5)$.

**Suppose:** $0 < |x - 2| < \delta$.

**Check:** Since $\delta \leq 1$, we have $|x + 2| < 5$.

$|x^2 - 4| = |x - 2||x + 2| < |x - 2| \cdot 5 < \delta \cdot 5 \leq (\varepsilon/5) \cdot 5 = \varepsilon$. $\square$

**Key Insight:** For nonlinear functions, use $\delta = \min(1, \varepsilon/C)$ where $C$ bounds the variable factor.

---

### Example 3: Reciprocal Function (Hard)

**Problem:** Prove that $\lim_{x \to 1} \frac{1}{x} = 1$ using the ε-δ definition.

**Solution:**

**Given:** Let $\varepsilon > 0$ be arbitrary.

**Choose:** We need $\left|\frac{1}{x} - 1\right| < \varepsilon$ whenever $0 < |x - 1| < \delta$.

Simplify: $\left|\frac{1 - x}{x}\right| = \frac{|x - 1|}{|x|}$.

**Problem:** We need to bound $1/|x|$, which requires $x$ to be bounded away from 0.

**Strategy:** Restrict δ so that $x$ stays away from 0.

**Suppose** $\delta \leq 1/2$. Then $|x - 1| < 1/2$, so $1/2 < x < 3/2$, so $|x| > 1/2$, so $1/|x| < 2$.

Now we need $\frac{|x - 1|}{|x|} < 2|x - 1| < \varepsilon$, so $|x - 1| < \varepsilon / 2$.

**Choose** $\delta = \min(1/2, \varepsilon / 2)$.

**Suppose:** $0 < |x - 1| < \delta$.

**Check:** Since $\delta \leq 1/2$, we have $|x| > 1/2$, so $1/|x| < 2$.

$\left|\frac{1}{x} - 1\right| = \frac{|x - 1|}{|x|} < 2|x - 1| < 2\delta \leq 2(\varepsilon/2) = \varepsilon$. $\square$

**Key Insight:** For rational functions, bound the denominator away from 0 first.

---

## Category 2: Limit Evaluation Techniques

### Example 4: Factoring (0/0 form)

**Problem:** Evaluate $\lim_{x \to 2} \frac{x^2 - 4}{x - 2}$.

**Solution:**

Direct substitution gives $\frac{0}{0}$ (indeterminate).

Factor numerator: $x^2 - 4 = (x - 2)(x + 2)$.

$\lim_{x \to 2} \frac{(x - 2)(x + 2)}{x - 2} = \lim_{x \to 2} (x + 2) = 4$.

**Key Insight:** When you get 0/0, factor and cancel common terms.

---

### Example 5: Rationalization (0/0 with square roots)

**Problem:** Evaluate $\lim_{x \to 0} \frac{\sqrt{x + 4} - 2}{x}$.

**Solution:**

Direct substitution gives $\frac{0}{0}$.

**Strategy:** Multiply by conjugate.

$\frac{\sqrt{x + 4} - 2}{x} \cdot \frac{\sqrt{x + 4} + 2}{\sqrt{x + 4} + 2} = \frac{(x + 4) - 4}{x(\sqrt{x + 4} + 2)} = \frac{x}{x(\sqrt{x + 4} + 2)} = \frac{1}{\sqrt{x + 4} + 2}$.

$\lim_{x \to 0} \frac{1}{\sqrt{x + 4} + 2} = \frac{1}{4}$.

**Key Insight:** For 0/0 with square roots, multiply by conjugate to rationalize.

---

### Example 6: Squeeze Theorem

**Problem:** Evaluate $\lim_{x \to 0} x^2 \sin\left(\frac{1}{x}\right)$.

**Solution:**

Direct substitution gives $0 \cdot \text{undefined}$ (oscillatory).

**Strategy:** Bound the oscillatory part.

We know $-1 \leq \sin\left(\frac{1}{x}\right) \leq 1$ for all $x \neq 0$.

Multiply by $x^2 \geq 0$: $-x^2 \leq x^2 \sin\left(\frac{1}{x}\right) \leq x^2$.

Since $\lim_{x \to 0} (-x^2) = 0$ and $\lim_{x \to 0} x^2 = 0$, by the Squeeze Theorem:

$\lim_{x \to 0} x^2 \sin\left(\frac{1}{x}\right) = 0$.

**Key Insight:** When one factor is bounded and the other goes to 0, use Squeeze Theorem.

---

## Category 3: Tangent Line Problems

### Example 7: Horizontal Tangent

**Problem:** Find the points on $y = x^3 - 3x$ where the tangent line is horizontal.

**Solution:**

Horizontal tangent means $y' = 0$.

$y' = 3x^2 - 3 = 3(x^2 - 1) = 3(x - 1)(x + 1)$.

Set $y' = 0$: $x = 1$ or $x = -1$.

At $x = 1$: $y = 1 - 3 = -2$. Point: $(1, -2)$.

At $x = -1$: $y = -1 + 3 = 2$. Point: $(-1, 2)$.

**Answer:** The tangent line is horizontal at $(1, -2)$ and $(-1, 2)$.

---

### Example 8: Tangent Line at a Point

**Problem:** Find the equation of the tangent line to $y = \sqrt{x}$ at $x = 4$.

**Solution:**

At $x = 4$: $y = \sqrt{4} = 2$. Point: $(4, 2)$.

$y' = \frac{1}{2\sqrt{x}}$.

At $x = 4$: $y'(4) = \frac{1}{2\sqrt{4}} = \frac{1}{4}$.

Slope: $m = 1/4$.

Tangent line: $y - 2 = \frac{1}{4}(x - 4)$, so $y = \frac{1}{4}x + 1$.

**Answer:** $y = \frac{1}{4}x + 1$.

---

## Category 4: L'Hôpital's Rule

### Example 9: 0/0 Form

**Problem:** Evaluate $\lim_{x \to 0} \frac{e^x - 1}{x}$.

**Solution:**

Direct substitution: $\frac{e^0 - 1}{0} = \frac{0}{0}$ (indeterminate).

**Check L'Hôpital prerequisites:** ✓ 0/0 form, ✓ both numerator and denominator are differentiable.

Apply L'Hôpital's Rule:

$\lim_{x \to 0} \frac{e^x - 1}{x} = \lim_{x \to 0} \frac{\frac{d}{dx}(e^x - 1)}{\frac{d}{dx}(x)} = \lim_{x \to 0} \frac{e^x}{1} = e^0 = 1$.

**Answer:** 1.

---

### Example 10: ∞/∞ Form

**Problem:** Evaluate $\lim_{x \to \infty} \frac{\ln(x)}{x}$.

**Solution:**

Direct substitution: $\frac{\infty}{\infty}$ (indeterminate).

**Check L'Hôpital prerequisites:** ✓ ∞/∞ form, ✓ both differentiable.

Apply L'Hôpital's Rule:

$\lim_{x \to \infty} \frac{\ln(x)}{x} = \lim_{x \to \infty} \frac{1/x}{1} = \lim_{x \to \infty} \frac{1}{x} = 0$.

**Answer:** 0.

**Key Insight:** L'Hôpital shows that $\ln(x)$ grows much slower than $x$.

---

## Summary of Techniques

| Problem Type | Technique | Key Step |
|---|---|---|
| ε-δ (linear) | Direct | $\delta = \varepsilon / C$ |
| ε-δ (nonlinear) | Bound + min | $\delta = \min(1, \varepsilon/C)$ |
| 0/0 (polynomial) | Factor | Cancel common terms |
| 0/0 (square root) | Rationalize | Multiply by conjugate |
| 0 · bounded | Squeeze | Bound oscillatory part |
| 0/0 or ∞/∞ | L'Hôpital | Differentiate top and bottom |
| Tangent (horizontal) | Set y' = 0 | Solve for x |
| Tangent (at point) | Point-slope | $y - y_0 = m(x - x_0)$ |
