Complex numbers are cool and mysterious. First, you have to get comfortable with the real numbers, $\mathbb{R}$, and understand the elementary functions that map $\mathbb{R} \to \mathbb{R}$. The set of all such functions is denoted $\{f : \mathbb{R} \to \mathbb{R}\}$. There are some functions in $f$ that break down — they hit a wall where the real numbers aren't enough. These are the functions that lead us into $\mathbb{C}$.

## Polynomials

Consider the polynomial
$$f(x) = x^2 + 1$$

Every polynomial in $\mathbb{R}[x]$ maps $\mathbb{R} \to \mathbb{R}$, but some polynomials have no real *roots*, meaning there is no $x \in \mathbb{R}$ such that $f(x) = 0$. Compare $x^2 - 1$, which crosses zero at $x = \pm 1$, with $x^2 + 1$, which sits entirely above the x-axis:

![[Figures/polynomial_roots_panel.png]]
*Figure 1: Real plots of $x^2 - 1$ and $x^2 + 1$ alongside the modulus surface $|z^2 + 1|$ over the complex plane, showing roots at $z = \pm i$.*

The left panel shows the problem: $x^2 + 1$ never touches zero on the real line. Setting $f(x) = 0$ gives $x^2 = -1$, which requires the evaluation of $\sqrt{-1}$ and has no solution in $\mathbb{R}$. To make this solvable, we define $i = \sqrt{-1}$, allow it to be a new number, and suddenly $x = \pm i$ are roots.

The right panel shows where these roots live. Plotting $|z^2 + 1|$ over the complex plane, the surface dips down to zero at two points: $z = i$ and $z = -i$, located on the imaginary axis. The roots were always there — we just couldn't see them from the real line.

This isn't a trick. The **[[Fundamental Theorem of Algebra]]** guarantees that every polynomial of degree $n$ has exactly $n$ roots — but only if we work in $\mathbb{C}$. Polynomials are the original motivation for why complex numbers were invented.

## From $i$ to $a + bi$

So far, we've introduced $i = \sqrt{-1}$ to solve $x^2 + 1 = 0$. But why do we need more than just $i$? Consider a slightly different polynomial:

$$f(x) = x^2 - 2x + 5$$

Applying the quadratic formula:

$$x = \frac{2 \pm \sqrt{4 - 20}}{2} = \frac{2 \pm \sqrt{-16}}{2} = \frac{2 \pm 4i}{2} = 1 \pm 2i$$

The roots aren't purely real or purely imaginary — they have both a real part ($1$) and an imaginary part ($\pm 2$). The number $i$ alone isn't enough. The quadratic formula forces us to combine real and imaginary parts through addition, giving us numbers of the form $a + bi$. This isn't a choice we make — it's a consequence of the algebra.

![[Figures/quadratic_roots_panel.png]]
*Figure 2: Three-panel view of $f(z) = z^2 - 2z + 5$ showing slices along the real axis, the imaginary axis, and the full modulus surface with roots at $z = 1 \pm 2i$.*

The first panel shows $f(x) = x^2 - 2x + 5$ along the real axis — like $x^2 + 1$, it never touches zero. The second panel shows $|f(z)|$ along the imaginary axis — also no zeros there. The roots aren't on either axis. The third panel reveals where they are: at $z = 1 \pm 2i$, sitting off both axes in the complex plane. Finding these roots required the full form $a + bi$.

## What is a Complex Number?

Let's make this precise.

A **complex number** is a number of the form

$$z = a + bi$$

where $a, b \in \mathbb{R}$ and $i$ satisfies $i^2 = -1$. We call $a$ the **real part** and $b$ the **imaginary part**, written

$$\mathrm{Re}(z) = a, \quad \mathrm{Im}(z) = b$$

The set of all complex numbers is $\mathbb{C} = \{a + bi \mid a, b \in \mathbb{R}\}$. Every real number is a complex number with $b = 0$, so $\mathbb{R} \subset \mathbb{C}$.

### Arithmetic

Complex arithmetic follows from the rules of algebra plus the single identity $i^2 = -1$:

- **Addition:** $(a + bi) + (c + di) = (a + c) + (b + d)i$
- **Multiplication:** $(a + bi)(c + di) = (ac - bd) + (ad + bc)i$
- **Conjugate:** $\bar{z} = a - bi$ — reflect across the real axis
- **Division:** $\displaystyle\frac{z_1}{z_2} = \frac{z_1 \bar{z_2}}{z_2 \bar{z_2}} = \frac{z_1 \bar{z_2}}{|z_2|^2}$

### The Complex Plane

Since a complex number $z = a + bi$ is determined by two real numbers, we can plot it as a point $(a, b)$ in a plane — the real part on the horizontal axis, the imaginary part on the vertical axis. This is the **complex plane** (or Argand diagram), and it's exactly the grid we've been using in our plots: $x_1$ is $\mathrm{Re}(z)$ and $x_2$ is $\mathrm{Im}(z)$.

### Modulus and Argument

Every point in the complex plane also has polar coordinates $(r, \theta)$, just like any point in $\mathbb{R}^2$:

- **Modulus:** $|z| = \sqrt{a^2 + b^2}$ — the distance from the origin
- **Argument:** $\arg(z) = \theta = \arctan(b/a)$ — the angle from the positive real axis

These are related by the **polar form**:

$$z = |z| e^{i\theta}$$

This is Euler's formula at work: every complex number is a distance ($|z|$) times a rotation ($e^{i\theta}$). The Cartesian form $z = a + bi$ and the polar form $z = |z|e^{i\theta}$ are two ways of describing the same point.

Returning to our roots of $z^2 - 2z + 5$ at $z = 1 \pm 2i$:

![[Figures/euler_vectors.png]]
*Figure 3: Modulus and argument of $z^2 - 2z + 5$ over the complex plane, with vectors from the origin to the roots showing their polar representation.*

Each root can be expressed both ways. Take $z = 1 + 2i$: the modulus is $|z| = \sqrt{1^2 + 2^2} = \sqrt{5}$ and the argument is $\theta = \arctan(2/1) \approx 1.11$ radians. So $z = \sqrt{5} \, e^{i \cdot 1.11}$. The white arrows show these as vectors from the origin — their length is the modulus, their angle from the real axis is the argument.

This dual representation gives us two complementary ways to visualize complex functions, both visible in the figure above:
- **Left — Modulus** ($|f(z)|$): how far function values are from zero. Roots appear as dark regions where the surface dips to zero, poles as bright spikes.
- **Right — Argument** ($\arg(f(z))$): the angular component. Each color corresponds to an angle, and the full color wheel represents one rotation from $-\pi$ to $\pi$. At the roots, all colors converge to a single point.

## Square Root

The function $f(x) = \sqrt{x}$ is only defined for $x \geq 0$ in $\mathbb{R}$. The entire negative half of the real line is a gap in its domain. Extending to $\mathbb{C}$ fills this gap: $\sqrt{-4} = 2i$. But this extension comes with a subtlety — the complex square root is *multi-valued*. Every nonzero complex number has two square roots (e.g., $\sqrt{-1} = \pm i$), so we have to choose a *branch* to make it a proper function.

![[Figures/sqrt_real.png]]
*Figure 4: The real square root function $\sqrt{x}$, defined only for $x \geq 0$.*

On the reals, $\sqrt{x}$ is only defined for $x \geq 0$ — the entire negative half of the line is missing. Extending to $\mathbb{C}$ fills this gap, but introduces new structure:

![[Figures/sqrt_complex_panel.png]]
*Figure 5: Modulus and phase portrait of the complex square root, showing the smooth modulus surface and the branch cut along the negative real axis.*

The left panel shows $|\sqrt{z}|$ — the modulus is smooth everywhere, with no hint of a discontinuity. The right panel reveals what the modulus hides: the phase portrait of $\arg(\sqrt{z})$ has a sharp color discontinuity along the negative real axis. That discontinuity is the *branch cut* — the line where the two possible square roots swap. The branch cut is purely an artifact of the argument, invisible in the modulus. NumPy's `sqrt` picks the *principal branch*, which always returns a value with non-negative real part.

## Exponential and Trigonometry

In $\mathbb{R}$, the exponential $e^x$ and the trigonometric functions $\sin(x)$, $\cos(x)$ seem unrelated — one grows without bound, the others oscillate forever. In $\mathbb{C}$, Euler's formula reveals they are the same thing:

$$e^{ix} = \cos(x) + i\sin(x)$$

The exponential, when fed an imaginary input, *rotates* instead of growing. This is why the phase portraits we plot show circular color patterns — the argument of a complex number is the angle $\theta$ in $e^{i\theta}$, and the colors trace out rotations.

![[Figures/exp_panel.png]]
*Figure 6: Real exponential, sine, and cosine functions alongside the phase portrait of $e^z$ in the complex plane, showing horizontal phase bands.*

The left panel shows $e^x$, $\sin(x)$, and $\cos(x)$ as separate, seemingly unrelated real functions. The right panel shows $\arg(e^z)$ in the complex plane — the phase depends only on $\mathrm{Im}(z)$, producing horizontal bands. This makes sense: $e^{a + bi} = e^a \cdot e^{bi}$, and $e^a$ is real (it only scales), so the phase comes entirely from $e^{bi} = \cos(b) + i\sin(b)$. The trig functions aren't separate from the exponential — they *are* its imaginary behavior.
## Logarithm

The function $f(x) = \ln(x)$ is undefined for $x \leq 0$ in $\mathbb{R}$. In $\mathbb{C}$, we can take the logarithm of any nonzero complex number. For example:

$$\ln(-1) = i\pi$$

which follows directly from Euler's formula since $e^{i\pi} = -1$. Like the square root, the complex logarithm is multi-valued — $\ln(-1) = i\pi + 2\pi i k$ for any integer $k$. Each choice of $k$ is a different *branch*, and this branching structure is one of the richest features of complex analysis.

![[Figures/log_panel.png]]
*Figure 7: Modulus and phase portrait of the complex logarithm, showing the singularity at the origin and the branch cut along the negative real axis.*

The left panel shows $|\ln(z)|$ — the modulus grows as you move away from $z = 1$ (where $\ln(1) = 0$) and blows up at the origin (a logarithmic singularity, marked with a white dot). The right panel shows $\arg(\ln(z))$ — note the branch cut along the negative real axis, just like $\sqrt{z}$. This is the same branch cut, for the same reason: the argument jumps from $\pi$ to $-\pi$ as you cross the negative real axis, and $\ln(z) = \ln|z| + i\arg(z)$ inherits that discontinuity.

---

![[Figures/anim_conformal_mapping.gif]]
*Animation 1: A regular grid in the complex plane continuously deforming under the conformal map $z \to z^2$.*

## Where to Go Next

This notebook has covered the motivation, definition, and basic visualization of complex numbers. Here are natural directions to explore:

- **[[Conformal mappings]]** — complex functions that preserve angles. The Mobius transform $f(z) = (z+1)/(z-1)$ (already in `complex_numbers.py`) is a classic example. Visualize how it warps a grid of lines or circles.
- **Residue calculus** — computing real integrals by integrating in the complex plane. The poles we've been visualizing are exactly the points that contribute to these integrals.
- **Riemann surfaces** — instead of choosing a branch for $\sqrt{z}$ or $\ln(z)$, glue all branches together into a single surface. This eliminates branch cuts entirely.
- **Analytic continuation** — extending functions beyond their original domain. The $\zeta$ function, the $\Gamma$ function, and other special functions arise this way.
- **Julia and Mandelbrot sets** — iterating $z \mapsto z^2 + c$ and coloring by convergence. Connects complex dynamics to fractal geometry.
- **Complex integration and Cauchy's theorem** — why contour integrals around poles give $2\pi i$ times the residue, and why integrals around non-singular regions give zero.
- **Potential theory** — the real and imaginary parts of an analytic function are harmonic, connecting complex analysis to physics (electrostatics, fluid flow). The dipole and pole/antipole surfaces we plotted are already examples.
