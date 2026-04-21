The [[Scalar and Vector Fields]] notebook introduced the gradient, divergence, and curl. The Laplacian combines the first two: it's the divergence of the gradient. Functions whose Laplacian is zero everywhere are called **harmonic**, and they turn out to be exactly the real and imaginary parts of the analytic functions from [[Complex Numbers]]. This is where the two threads converge.

## The Laplacian

Given a scalar field $f(x, y)$, the **Laplacian** is

$$\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}$$

It's a scalar — one number at each point — that measures how much $f$ at a point differs from the average of $f$ in a small neighborhood. If $\nabla^2 f > 0$, the point is a local valley (its value is below the local average); if $\nabla^2 f < 0$, it's a local peak; if $\nabla^2 f = 0$, the function value equals the local average in every direction.

Consider three scalar fields and their Laplacians:

- $f = x^2 + y^2$: $\quad \nabla^2 f = 2 + 2 = 4$ — constant and positive everywhere. The paraboloid is always curving upward.
- $f = x^2 - y^2$: $\quad \nabla^2 f = 2 + (-2) = 0$ — the upward curvature in $x$ exactly cancels the downward curvature in $y$.
- $f = e^{-(x^2 + y^2)}$: $\quad \nabla^2 f$ varies across the plane — positive far from the origin (the Gaussian is concave up), negative near the center (concave down).

![[Figures/laplacian_examples.png]]
*Figure 1: Three scalar fields ($x^2 + y^2$, $x^2 - y^2$, and the Gaussian) with their Laplacians, showing constant positive, identically zero, and spatially varying cases.*

The top row shows each field; the bottom row shows its Laplacian. The middle column — $x^2 - y^2$ — is special: its Laplacian is identically zero (uniform color). That makes it a **harmonic function**.

## Harmonic Functions

A function $f(x, y)$ is **harmonic** if

$$\nabla^2 f = 0$$

everywhere in its domain. Harmonic functions satisfy Laplace's equation, one of the most important PDEs in mathematics and physics. Some examples:

- $x^2 - y^2$ — the saddle surface
- $\ln r = \frac{1}{2}\ln(x^2 + y^2)$ — the logarithmic potential (harmonic away from the origin, where it has a singularity)
- $e^x \cos y$ — an exponentially weighted oscillation

![[Figures/harmonic_gallery.png]]
*Figure 2: Contour plots of three harmonic functions: the saddle $x^2 - y^2$, the logarithmic potential $\ln r$, and $e^x \cos y$.*

These functions look very different, but they share the same defining property: the curvature in $x$ and the curvature in $y$ always cancel. Every peak in one direction is balanced by a valley in the other. This is why harmonic functions have no local maxima or minima in the interior of their domain — a fact known as the **maximum principle**.

## The Connection to Complex Analysis

Here is the key insight: if $f(z)$ is an analytic complex function, then its real part $u = \mathrm{Re}(f)$ and imaginary part $v = \mathrm{Im}(f)$ are both harmonic.

Take $f(z) = z^2$. Writing $z = x + iy$:

$$z^2 = (x + iy)^2 = (x^2 - y^2) + i(2xy)$$

So $u(x, y) = x^2 - y^2$ and $v(x, y) = 2xy$. We already know $u$ is harmonic (its Laplacian is zero). And $v$:

$$\nabla^2 v = \frac{\partial^2 (2xy)}{\partial x^2} + \frac{\partial^2 (2xy)}{\partial y^2} = 0 + 0 = 0$$

Both are harmonic. This always works, for any analytic function.

![[Figures/complex_harmonic_panel.png]]
*Figure 3: The real part $x^2 - y^2$ and imaginary part $2xy$ of $z^2$, shown as contour-filled scalar fields.*

The two panels show $\mathrm{Re}(z^2)$ and $\mathrm{Im}(z^2)$ as scalar fields. Both are harmonic, but they are also related to each other in a precise way.

## Conjugate Harmonics and the Cauchy-Riemann Equations

The pair $(u, v)$ aren't just independently harmonic — they are **conjugate harmonics**, locked together by the **Cauchy-Riemann equations**:

$$\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}, \qquad \frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}$$

These equations say that the gradient of $u$ and the gradient of $v$ are perpendicular everywhere, and have equal magnitudes. Geometrically, the contour lines of $u$ and $v$ cross at right angles:

![[Figures/orthogonal_contours.png]]
*Figure 4: Overlaid contour lines of $\mathrm{Re}(z^2)$ and $\mathrm{Im}(z^2)$, crossing at right angles to form an orthogonal net.*

This orthogonality is not a coincidence — it's the defining geometric signature of an analytic function. The contour lines of $\mathrm{Re}(f)$ and $\mathrm{Im}(f)$ form an **orthogonal net** everywhere $f'(z) \neq 0$.

## A Second Example: $e^z$

The same structure appears in every analytic function. For $f(z) = e^z = e^{x+iy} = e^x(\cos y + i \sin y)$:

$$u = e^x \cos y, \qquad v = e^x \sin y$$

Both are harmonic. Their contours cross at right angles, just like $z^2$:

![[Figures/exp_harmonic_panel.png]]
*Figure 5: The real part $e^x \cos y$ of $e^z$ and the orthogonal contours of $\mathrm{Re}(e^z)$ and $\mathrm{Im}(e^z)$.*

The left panel shows $\mathrm{Re}(e^z)$ — the exponential growth in the $x$-direction modulated by $\cos y$. The right panel overlays the contours of both parts, confirming the orthogonal crossing.

## The Big Picture

The connection runs deep in both directions:

- **Complex $\to$ Real**: Every analytic function $f(z)$ produces a conjugate harmonic pair $(u, v)$ that solves Laplace's equation. Complex analysis is a factory for harmonic functions.
- **Real $\to$ Complex**: Given any harmonic function $u$, there exists (locally) a conjugate $v$ such that $f = u + iv$ is analytic. Harmonic functions come in pairs, and the pair always assembles into a complex analytic function.

This is why complex analysis is so powerful in physics. The real and imaginary parts of analytic functions automatically satisfy Laplace's equation, which governs electrostatics, steady-state heat flow, incompressible fluid flow, and gravitational potential. Solving a physics problem often reduces to finding the right analytic function.

## Where to Go Next

- **Conformal mappings** — analytic functions preserve angles (the orthogonal contours we saw). This makes them natural for transforming one geometry into another while preserving Laplace's equation.
- **Dirichlet problem** — finding a harmonic function with prescribed boundary values. The existence and uniqueness theorems are cornerstones of PDE theory.
- **Green's functions** — the logarithmic potential $\ln r$ is the fundamental solution to $\nabla^2 f = \delta$. Connects to the [[Scalar and Vector Fields]] discussion of gravitational potentials.
- **Harmonic conjugates in fluid dynamics** — $u$ is the velocity potential, $v$ is the stream function. The orthogonal contour lines are equipotentials and streamlines.
