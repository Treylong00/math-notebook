In [[Linear Algebra]], we saw that a matrix $A$ can have special vectors — eigenvectors — that it merely scales rather than rotates. In [[Hilbert Spaces]], we extended linear algebra to infinite-dimensional function spaces. Now we bring these ideas together: differential operators act on functions the same way matrices act on vectors, and they have their own eigenvectors — called **eigenfunctions**. The punchline is that the Fourier basis from [[Fourier Analysis]] is not an accident. Those sines and cosines are eigenfunctions of the Laplacian from [[Harmonic Functions]], and the entire Fourier theory is a special case of a much larger spectral theory.

## Differential Operators

A **linear operator** is a rule that takes a function and returns another function, respecting linearity. We already know one: the Laplacian $\nabla^2$ from [[Harmonic Functions]]. But let's start simpler.

The **derivative operator** $\hat{D}$ acts on a function $f$ by differentiating it:

$$\hat{D}f = \frac{df}{dx}$$

The **second derivative operator** $\hat{D}^2$ differentiates twice:

$$\hat{D}^2 f = \frac{d^2 f}{dx^2}$$

These are linear: $\hat{D}(af + bg) = a\hat{D}f + b\hat{D}g$, just like a matrix. The key difference is that the "vectors" are now functions, and the "matrix" is a differential operation.

The operator we will focus on is $-\hat{D}^2$, or equivalently $-\frac{d^2}{dx^2}$. The minus sign is a convention that makes all the eigenvalues positive, as we will see shortly. In higher dimensions, this becomes the negative Laplacian $-\nabla^2$, which governs vibrations, heat flow, and quantum mechanics.

## Eigenfunctions of $-d^2/dx^2$

An **eigenfunction** of an operator $\hat{A}$ is a nonzero function $f$ satisfying

$$\hat{A}f = \lambda f$$

for some scalar $\lambda$ called the **eigenvalue**. The operator merely scales the function — it does not change its shape.

For the operator $-\frac{d^2}{dx^2}$, we need to solve

$$-f''(x) = \lambda f(x)$$

This is a second-order ODE. If $\lambda > 0$, writing $\lambda = n^2$ for convenience, the general solution is

$$f(x) = A\cos(nx) + B\sin(nx)$$

which we can verify: $f''(x) = -n^2 f(x)$, so $-f'' = n^2 f = \lambda f$. The sines and cosines — the building blocks of Fourier analysis — are eigenfunctions of the negative second derivative, with eigenvalue $n^2$.

This is the deep reason Fourier analysis works. The complex exponentials $e^{inx}$ (equivalently, sines and cosines) are not arbitrary basis functions — they are the **eigenfunctions of the Laplacian**. Decomposing a function into Fourier modes is the same as expanding it in the eigenbasis of $-d^2/dx^2$.

## Boundary Conditions Shape the Spectrum

The equation $-f'' = \lambda f$ has solutions for any positive $\lambda$. But when we impose **boundary conditions** — constraints on $f$ at the edges of the domain — only certain eigenvalues survive. Different boundary conditions give different spectra.

### Dirichlet Boundary Conditions

On the interval $[0, \pi]$, require $f(0) = f(\pi) = 0$ (the function vanishes at both endpoints). The general solution $A\cos(nx) + B\sin(nx)$ must satisfy:
- $f(0) = A = 0$, so $A = 0$
- $f(\pi) = B\sin(n\pi) = 0$, so $n$ must be a positive integer

The eigenfunctions are $f_n(x) = \sin(nx)$ for $n = 1, 2, 3, \ldots$, with eigenvalues $\lambda_n = n^2$.

![[Figures/operators_eigenfunctions.png]]
*Figure 1: Dirichlet eigenfunctions $\sin(nx)$ on $[0, \pi]$ for $n = 1, 2, 3, 4$, with eigenvalues $\lambda_n = n^2$.*

Each successive eigenfunction oscillates faster (higher $n$) and has a larger eigenvalue ($n^2$). The eigenvalue measures the "curvature cost" of the function — more oscillations mean higher curvature, and the operator $-d^2/dx^2$ penalizes curvature.

### Periodic Boundary Conditions

On $[0, 2\pi]$, require $f(0) = f(2\pi)$ and $f'(0) = f'(2\pi)$ (the function and its derivative match at the endpoints). Now both $\cos(nx)$ and $\sin(nx)$ survive for each $n$, and the constant function ($n = 0$) is also an eigenfunction with eigenvalue $0$.

The eigenfunctions are $1, \cos(x), \sin(x), \cos(2x), \sin(2x), \ldots$ — exactly the Fourier basis on the circle.

![[Figures/operators_boundary_conditions.png]]
*Figure 2: Dirichlet eigenfunctions pinned to zero at the endpoints (left) versus periodic eigenfunctions matching at the boundaries (right).*

The left panel shows the Dirichlet eigenfunctions: sines only, pinned to zero at the endpoints. The right panel shows the periodic eigenfunctions: both sines and cosines, free to take any value as long as they match at the boundaries. Same operator, different boundary conditions, different eigenfunctions.

This is a physical distinction too. Dirichlet boundary conditions describe a vibrating string clamped at both ends — a guitar string. Periodic boundary conditions describe a vibrating loop — a ring or a drum head with circular symmetry.

## The Spectrum

The set of all eigenvalues of an operator is called its **spectrum**. For $-d^2/dx^2$ on $[0, \pi]$ with Dirichlet conditions, the spectrum is

$$\sigma = \{1, 4, 9, 16, 25, \ldots\} = \{n^2 : n \in \mathbb{N}\}$$

![[Figures/operators_spectrum.png]]
*Figure 3: The discrete spectrum $\lambda_n = n^2$ of $-d^2/dx^2$ with Dirichlet boundary conditions, showing the quadratic growth of eigenvalues.*

The eigenvalues grow quadratically — higher modes are increasingly "expensive." This is a **discrete spectrum**: the eigenvalues are isolated points with gaps between them.

Not all operators have discrete spectra. The same operator $-d^2/dx^2$ on the entire real line $\mathbb{R}$ (with no boundary conditions) has $e^{ikx}$ as an eigenfunction for every real $k$, with eigenvalue $k^2$. The spectrum is the entire half-line $[0, \infty)$ — a **continuous spectrum**.

The distinction matters in physics. A quantum particle confined to a box has discrete energy levels (bound states). A free particle has a continuous range of possible energies. The boundary conditions determine which case applies.

## Hermitian Operators

In [[Linear Algebra]], symmetric matrices $A = A^T$ have real eigenvalues and orthogonal eigenvectors. The infinite-dimensional analogue is a **Hermitian** (or **self-adjoint**) operator.

An operator $\hat{A}$ on a [[Hilbert Spaces|Hilbert space]] is Hermitian if

$$\langle \hat{A}f, g \rangle = \langle f, \hat{A}g \rangle$$

for all functions $f, g$ in the domain (with appropriate boundary conditions). The angle brackets denote the $L^2$ inner product from [[Hilbert Spaces]]:

$$\langle f, g \rangle = \int_a^b \overline{f(x)}\, g(x)\, dx$$

The operator $-d^2/dx^2$ is Hermitian with respect to Dirichlet boundary conditions. To see why, integrate by parts twice:

$$\langle -f'', g \rangle = \int_0^\pi (-f'')\, g\, dx = \int_0^\pi f'\, g'\, dx - [f'\, g]_0^\pi$$

The boundary term vanishes because $g(0) = g(\pi) = 0$. Integrating by parts again:

$$\int_0^\pi f'\, g'\, dx = -\int_0^\pi f\, g''\, dx + [f\, g']_0^\pi = \int_0^\pi f\, (-g'')\, dx = \langle f, -g'' \rangle$$

So $\langle -f'', g \rangle = \langle f, -g'' \rangle$, confirming the operator is Hermitian.

Hermitian operators have two crucial properties:

1. **Real eigenvalues.** If $\hat{A}f = \lambda f$, then $\lambda \in \mathbb{R}$. This is why $-d^2/dx^2$ has eigenvalues $n^2$ — real and positive.

2. **Orthogonal eigenfunctions.** If $\hat{A}f = \lambda f$ and $\hat{A}g = \mu g$ with $\lambda \neq \mu$, then $\langle f, g \rangle = 0$. The eigenfunctions for different eigenvalues are automatically orthogonal.

We already know this from [[Fourier Analysis]]: the functions $\sin(nx)$ are orthogonal on $[0, \pi]$:

$$\int_0^\pi \sin(nx)\sin(mx)\, dx = \begin{cases} \pi/2 & n = m \\ 0 & n \neq m \end{cases}$$

Now we see this orthogonality is not a lucky coincidence — it is guaranteed by the Hermitian property of the operator.

In quantum mechanics, observables (energy, momentum, position) must be represented by Hermitian operators. The requirement of real eigenvalues ensures that measurements yield real numbers. The orthogonality of eigenfunctions ensures that distinct measurement outcomes are distinguishable.

## The Spectral Theorem

The spectral theorem is the culmination of everything in this notebook. It says:

> The eigenfunctions of a Hermitian operator on a [[Hilbert Spaces|Hilbert space]] form a **complete orthonormal basis**.

"Complete" means every function in the space can be expanded as a (possibly infinite) sum of eigenfunctions. "Orthonormal" means the eigenfunctions are orthogonal and have unit norm.

For $-d^2/dx^2$ on $[0, \pi]$ with Dirichlet conditions, the spectral theorem says: the functions $\sqrt{2/\pi}\,\sin(nx)$ form a complete orthonormal basis for $L^2[0, \pi]$. Any square-integrable function $f$ can be written as

$$f(x) = \sum_{n=1}^{\infty} b_n \sin(nx), \qquad b_n = \frac{2}{\pi}\int_0^\pi f(x)\sin(nx)\, dx$$

This **is** the Fourier sine series — but now understood as an eigenfunction expansion of the Laplacian.

![[Figures/operators_expansion.png]]
*Figure 4: Eigenfunction expansion of $f(x) = x(\pi - x)$ in Dirichlet sine modes, with increasing numbers of terms.*

![[Figures/anim_eigenfunction_expansion.gif]]
*Animation 1: Eigenfunction partial sums converging to a triangle wave target function as terms are added.*

The figure shows $f(x) = x(\pi - x)$ expanded in eigenfunctions. With just a few terms, the partial sums capture the essential shape. As we add more eigenfunctions, the expansion converges to the exact function. This is the spectral theorem in action: any function can be built from eigenfunctions of the operator.

The power of this viewpoint is its generality. The Fourier basis is special to the Laplacian on an interval. But the spectral theorem applies to any Hermitian operator:

- **Legendre polynomials** are eigenfunctions of the angular part of the Laplacian in spherical coordinates
- **Hermite functions** are eigenfunctions of the quantum harmonic oscillator Hamiltonian $-d^2/dx^2 + x^2$
- **Spherical harmonics** are eigenfunctions of the Laplacian on the sphere $S^2$

Each operator generates its own "natural" basis, and the spectral theorem guarantees that basis is complete. Fourier analysis is the prototype, but the idea extends far beyond sines and cosines.

## Where to Go Next

The operator framework sets the stage for quantum mechanics, where everything is built from operators and their spectra:

- [[Probability and Complex Amplitudes]] — why quantum states are complex-valued, and what $|\psi|^2$ means
- [[The Schrodinger Equation]] — the eigenvalue equation $\hat{H}\psi = E\psi$ for the Hamiltonian operator, where eigenvalues are energy levels and eigenfunctions are stationary states


