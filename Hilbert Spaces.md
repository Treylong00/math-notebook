In [[Linear Algebra]], we built the machinery of inner products, orthogonality, and bases in finite-dimensional spaces. We even started applying these ideas to *functions* -- treating $\sin(nx)$ and $\cos(nx)$ as basis vectors and Fourier coefficients as coordinates. But we were hand-waving. We never asked: *what space do these functions actually live in?*

Not every function qualifies. Some blow up, some oscillate too wildly, some aren't integrable. To do analysis -- to talk about convergence, approximation, and completeness -- we need to be precise about which functions we're allowed to work with. That precision leads us to Hilbert spaces.

## $L^2$: Square-Integrable Functions

Recall the inner product on functions from [[Linear Algebra]]:

$$\langle f, g \rangle = \int_a^b f(x) \, \overline{g(x)} \, dx$$

For this to make sense, the integral needs to converge. In particular, taking $g = f$, we need

$$\langle f, f \rangle = \int_a^b |f(x)|^2 \, dx < \infty$$

This is our membership criterion. A function $f$ belongs to $L^2(a, b)$ -- the space of **square-integrable functions** on $(a, b)$ -- if and only if the integral of $|f|^2$ is finite. On all of $\mathbb{R}$, the condition is

$$f \in L^2(\mathbb{R}) \iff \int_{-\infty}^{\infty} |f(x)|^2 \, dx < \infty$$

The inner product gives us a **norm**:

$$\|f\| = \sqrt{\langle f, f \rangle} = \sqrt{\int |f(x)|^2 \, dx}$$

This is the function-space analog of the Euclidean length $\|\mathbf{v}\| = \sqrt{v_1^2 + \cdots + v_n^2}$. It measures the "size" of a function -- not its maximum value, but its total energy.

### Who's In, Who's Out

![[Figures/hilbert_l2_membership.png]]
*Figure 1: Four test functions and their squared moduli, showing which belong to $L^2$: the Gaussian and sinc pass, while $1/|x|$ and $1/\sqrt{|x|}$ fail.*

The Gaussian $e^{-x^2}$ decays so fast that $\int |f|^2 \, dx$ converges easily. The sinc function $\sin(x)/x$ decays slowly, but fast enough -- its square is integrable. On the other hand, $1/|x|$ blows up at the origin *and* decays too slowly at infinity: $\int |1/x|^2 \, dx$ diverges on both counts. The function $1/\sqrt{|x|}$ is subtler -- it decays fast enough at infinity, but its square $1/|x|$ diverges at the origin. Close, but not in $L^2$.

The bottom row makes the test visual: $f \in L^2$ precisely when the shaded area under $|f(x)|^2$ is finite.

## Completeness

Having an inner product and a norm is necessary, but not sufficient. The crucial property that makes $L^2$ a **Hilbert space** is **completeness**: every Cauchy sequence of functions converges to something that is itself in $L^2$.

### The Analogy

Think about rational numbers versus real numbers. The sequence

$$1, \; 1.4, \; 1.41, \; 1.414, \; 1.4142, \; \ldots$$

is a Cauchy sequence of rationals -- the terms get arbitrarily close to each other. But the limit is $\sqrt{2}$, which is *not* rational. So $\mathbb{Q}$ is incomplete: Cauchy sequences can "escape" the space. Completing $\mathbb{Q}$ -- filling in the gaps -- gives us $\mathbb{R}$.

The same phenomenon happens with functions. You can build Cauchy sequences of continuous functions whose limit is discontinuous (like a square wave). The space of continuous functions is *not* complete under the $L^2$ norm. But $L^2$ itself is -- it already contains all the limits. This is what makes it the right setting for analysis.

### Completeness in Action

The Fourier series of a square wave is a sequence of smooth functions converging to a discontinuous limit. Each partial sum $S_N$ is a finite combination of sines, hence smooth. The square wave is not smooth, but it *is* in $L^2$, and the partial sums converge to it in the $L^2$ norm:

![[Figures/hilbert_completeness.png]]
*Figure 2: Fourier partial sums converging to a square wave (left) and the $L^2$ approximation error $\|f - S_N\|$ decreasing with $N$ (right).*

The left panel shows the partial sums approaching the square wave. The right panel shows the $L^2$ error $\|f - S_N\|$ decreasing toward zero. The convergence isn't pointwise at the discontinuities (that's the Gibbs phenomenon visible in the left panel), but in the $L^2$ sense -- the total "energy" of the error vanishes. Completeness guarantees that this limit exists *within* $L^2$.

## Orthonormal Bases

In $\mathbb{R}^n$, the standard basis $\{\mathbf{e}_1, \ldots, \mathbf{e}_n\}$ lets us write any vector as $\mathbf{v} = \sum_{k=1}^n c_k \, \mathbf{e}_k$ with $c_k = \langle \mathbf{v}, \mathbf{e}_k \rangle$. Can we do the same in $L^2$?

Yes -- but the basis is **countably infinite**. On the interval $[-\pi, \pi]$, the functions

$$e_n(x) = \frac{e^{inx}}{\sqrt{2\pi}}, \quad n \in \mathbb{Z}$$

form an orthonormal basis for $L^2[-\pi, \pi]$. They satisfy

$$\langle e_m, e_n \rangle = \frac{1}{2\pi} \int_{-\pi}^{\pi} e^{i(n-m)x} \, dx = \delta_{mn}$$

where $\delta_{mn}$ is the Kronecker delta: $1$ if $m = n$, $0$ otherwise. This is exactly the orthonormality condition from [[Linear Algebra]], just with infinitely many vectors.

Any $f \in L^2[-\pi, \pi]$ can be expanded as

$$f(x) = \sum_{n=-\infty}^{\infty} c_n \, e_n(x), \quad c_n = \langle f, e_n \rangle = \frac{1}{\sqrt{2\pi}} \int_{-\pi}^{\pi} f(x) \, e^{-inx} \, dx$$

This is the **generalized Fourier series**. The coefficients $c_n$ are the coordinates of $f$ in the Fourier basis -- exactly like the Fourier coefficients from [[Fourier Analysis]], repackaged in the language of Hilbert spaces. The convergence is in the $L^2$ norm: $\|f - S_N\| \to 0$, which is precisely what the completeness figure above demonstrates.

**Parseval's theorem** (which we saw in [[Fourier Analysis]]) now has a geometric interpretation: it says

$$\|f\|^2 = \sum_{n=-\infty}^{\infty} |c_n|^2$$

This is the infinite-dimensional Pythagorean theorem -- the squared length of a vector equals the sum of the squares of its components.

## The Geometry of $L^2$

The inner product on $L^2$ gives us all the geometric tools we had in $\mathbb{R}^n$, now applied to functions.

### Distance

The **distance** between two functions is the norm of their difference:

$$d(f, g) = \|f - g\| = \sqrt{\int |f(x) - g(x)|^2 \, dx}$$

This measures how much total energy separates two functions. Two functions can differ wildly at a single point but still be "close" in $L^2$ -- what matters is the *aggregate* discrepancy, not pointwise differences.

### Angle

The **angle** between two functions is defined through the inner product, just as in $\mathbb{R}^n$:

$$\cos \theta = \frac{\langle f, g \rangle}{\|f\| \, \|g\|}$$

When $\langle f, g \rangle = 0$, the functions are orthogonal -- perpendicular in the geometry of $L^2$. The Fourier basis functions are all mutually orthogonal, just like the coordinate axes in $\mathbb{R}^n$.

### Projections

Given a subspace $V \subset L^2$ (say, the span of the first $N$ Fourier basis functions), the **nearest point** in $V$ to a function $f$ is its orthogonal projection:

$$\mathrm{proj}_V(f) = \sum_{n} \langle f, e_n \rangle \, e_n$$

This is the best approximation to $f$ using only the basis functions in $V$. The error $f - \mathrm{proj}_V(f)$ is orthogonal to every function in $V$ -- exactly the geometric picture from [[Linear Algebra]], extended to infinite dimensions.

![[Figures/hilbert_distance.png]]
*Figure 3: $L^2$ distance between two functions shown as the gap between their graphs (left) and as a metric in an abstract function space (right).*

The left panel shows the distance between two functions visualized as the gap between their graphs -- the $L^2$ distance is the square root of the area under $|f - g|^2$. The right panel shows the abstract picture: functions are points in a space, and the distance between them is a genuine metric.

## From $L^2$ to Quantum Mechanics

Everything we've built -- inner products, norms, completeness, orthonormal bases -- is exactly the mathematical framework of quantum mechanics.

In quantum mechanics, the state of a particle is described by a **wavefunction** $\psi(x) \in L^2(\mathbb{R})$. The requirement that $\psi$ be in $L^2$ is not a mathematical convenience -- it encodes the physical requirement that the particle must be *somewhere*:

$$\int_{-\infty}^{\infty} |\psi(x)|^2 \, dx = 1$$

The quantity $|\psi(x)|^2$ is the **probability density** -- the chance of finding the particle near position $x$. The normalization condition $\|\psi\| = 1$ says that the total probability is $1$: the particle exists.

![[Figures/hilbert_normalization.png]]
*Figure 4: An unnormalized wavefunction $\psi$ (left) and the normalized $\hat{\psi} = \psi/\|\psi\|$ with unit-area $|\hat{\psi}|^2$ (right).*

A physical wavefunction must satisfy $\|\psi\| = 1$. If we start with an unnormalized $\psi$ (left panel), we divide by its norm to get $\hat{\psi} = \psi / \|\psi\|$ (right panel). After normalization, the shaded area under $|\hat{\psi}|^2$ equals exactly $1$.

### The Inner Product as Physics

The inner product $\langle \phi, \psi \rangle$ between two wavefunctions is the **probability amplitude** -- its squared modulus $|\langle \phi, \psi \rangle|^2$ gives the probability of measuring a system in state $\psi$ and finding it in state $\phi$. When two states are orthogonal, $\langle \phi, \psi \rangle = 0$, they are completely distinguishable -- there is zero probability of confusing one for the other.

Expanding a wavefunction in an orthonormal basis $\{e_n\}$ gives

$$\psi = \sum_n c_n \, e_n, \quad c_n = \langle e_n, \psi \rangle$$

The coefficients $c_n$ are probability amplitudes, and $|c_n|^2$ is the probability of measuring the system in state $e_n$. Parseval's theorem becomes the statement that probabilities sum to $1$:

$$\sum_n |c_n|^2 = \|\psi\|^2 = 1$$

Every formal property of Hilbert spaces -- completeness, orthogonality, projections, Parseval's theorem -- has a direct physical meaning. The mathematics isn't just convenient notation; it *is* the physics.

## Where to Go Next

Hilbert spaces give us the stage. The next step is to study the **actors**: linear operators on $L^2$. In [[Linear Algebra]], operators were matrices; in $L^2$, they are things like differentiation ($d/dx$), multiplication by $x$, and integral transforms. The eigenvalue equation

$$\hat{A} \psi = \lambda \psi$$

becomes the central object -- in quantum mechanics, $\hat{A}$ is an observable (position, momentum, energy), $\lambda$ is a measurement outcome, and $\psi$ is the state that gives that outcome with certainty.

This leads to:

- **[[Operators and Eigenvalues]]** -- self-adjoint operators, spectral theory, the connection between eigenvalues and measurement
- **[[Dirac notation]]** -- the physicist's shorthand $|\psi\rangle$, $\langle \phi | \psi \rangle$, which makes the Hilbert space structure even more transparent
- **Spectral theorem** -- the infinite-dimensional analog of diagonalization, which guarantees that self-adjoint operators have a complete set of eigenfunctions
