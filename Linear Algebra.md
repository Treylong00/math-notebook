The [[Fourier Analysis]] notebook showed that periodic functions can be decomposed into sums of sines, cosines, and complex exponentials. But *why* does this work? Why are sines and cosines the "right" building blocks? The answer comes from linear algebra — not the finite-dimensional kind you learn first, but its extension to spaces of functions. The same ideas that let you decompose a vector into components along coordinate axes let you decompose a function into Fourier modes.

This notebook develops the key ideas of linear algebra — inner products, orthogonality, projection, eigenvalues — first in $\mathbb{R}^n$ where the geometry is visible, then in function spaces where the same logic applies but the dimensions are infinite.

## Vectors and Functions

A vector in $\mathbb{R}^n$ is a list of $n$ numbers:

$$\mathbf{v} = \begin{pmatrix} v_1 \\ v_2 \\ \vdots \\ v_n \end{pmatrix}$$

A function $f: [a, b] \to \mathbb{R}$ assigns a number to every point in an interval. You can think of it as an "infinitely long list" of values — one for each point $x$ in $[a, b]$. In this sense, a function is an infinite-dimensional vector. The value $f(x)$ plays the role of the component $v_i$, but instead of a discrete index $i$ you have a continuous variable $x$.

This analogy is the starting point. If functions are vectors, then the operations we perform on vectors — measuring length, computing angles, projecting, decomposing — should have function-space analogues. They do, and they are the foundation of Fourier analysis and much of modern mathematics.

## Inner Products

### In $\mathbb{R}^n$

The **dot product** (or inner product) of two vectors $\mathbf{a}, \mathbf{b} \in \mathbb{R}^n$ is

$$\mathbf{a} \cdot \mathbf{b} = \sum_{i=1}^n a_i b_i$$

It measures how much two vectors "agree" — how much they point in the same direction. The dot product gives us:

- **Length**: $\|\mathbf{a}\| = \sqrt{\mathbf{a} \cdot \mathbf{a}}$
- **Angle**: $\cos\theta = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\|\,\|\mathbf{b}\|}$
- **Projection**: the component of $\mathbf{b}$ along $\mathbf{a}$ is $\frac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{a} \cdot \mathbf{a}}\,\mathbf{a}$

### For Functions

The inner product for functions on an interval $[a, b]$ replaces the sum with an integral:

$$\langle f, g \rangle = \int_a^b f(x)\,g(x)\,dx$$

(For complex-valued functions, we conjugate the first factor: $\langle f, g \rangle = \int_a^b f^*(x)\,g(x)\,dx$.)

This is the direct analogue of the dot product. Instead of multiplying corresponding components $a_i b_i$ and summing, we multiply the function values $f(x) g(x)$ and integrate. The integral plays the role of the sum; the continuous variable $x$ plays the role of the index $i$.

Just like the dot product, this inner product gives us:

- **Norm**: $\|f\| = \sqrt{\langle f, f \rangle} = \sqrt{\int_a^b |f(x)|^2\,dx}$
- **Orthogonality**: $f$ and $g$ are orthogonal if $\langle f, g \rangle = 0$
- **Projection**: the component of $g$ along $f$ is $\frac{\langle f, g \rangle}{\langle f, f \rangle}\,f$

![[Figures/linalg_inner_product.png]]
*Figure 1: Vector projection in $\mathbb{R}^2$ (left) and the signed-area visualization of the function inner product $\langle f, g \rangle$ (right).*

The left panel shows projection in $\mathbb{R}^2$: the vector $\mathrm{proj}_\mathbf{a}\,\mathbf{b}$ is the shadow of $\mathbf{b}$ onto $\mathbf{a}$, computed using the dot product. The right panel shows the function-space analogue: the inner product $\langle f, g \rangle$ is the integral of $f(x)\,g(x)$, visualized as signed area. When the positive and negative regions cancel perfectly, the integral is zero — the functions are orthogonal.

## Orthogonality

### Orthogonal Vectors

Two vectors are **orthogonal** if their inner product is zero: $\mathbf{a} \cdot \mathbf{b} = 0$. In $\mathbb{R}^2$ and $\mathbb{R}^3$, this means they are perpendicular. The standard basis vectors $\mathbf{e}_1, \mathbf{e}_2, \ldots, \mathbf{e}_n$ are mutually orthogonal — every pair has dot product zero.

### Orthogonal Functions

The same definition applies to functions: $f$ and $g$ are orthogonal on $[a, b]$ if

$$\langle f, g \rangle = \int_a^b f(x)\,g(x)\,dx = 0$$

The sines $\sin(nx)$ are mutually orthogonal on $[0, 2\pi]$:

$$\int_0^{2\pi} \sin(mx)\,\sin(nx)\,dx = \begin{cases} 0 & m \neq n \\ \pi & m = n \end{cases}$$

This is not a coincidence or an accident of trigonometry — it is the reason Fourier analysis works. The sine functions form an orthogonal set, just like the coordinate axes in $\mathbb{R}^n$. Different Fourier modes are "perpendicular" in function space.

![[Figures/linalg_orthogonal_functions.png]]
*Figure 2: The first three sine functions $\sin(nx)$ (top) and their pairwise products (bottom), showing that each product integrates to zero.*

The top row shows $\sin x$, $\sin 2x$, and $\sin 3x$. The bottom row shows their pairwise products. In every case, the positive and negative lobes cancel perfectly, making the integral zero. This is orthogonality in action.

## Bases and Projections

### In $\mathbb{R}^n$

Any vector can be written as a sum of components along orthogonal basis vectors:

$$\mathbf{v} = \sum_{i=1}^n c_i\,\mathbf{e}_i, \qquad c_i = \frac{\mathbf{e}_i \cdot \mathbf{v}}{\mathbf{e}_i \cdot \mathbf{e}_i}$$

Each coefficient $c_i$ is a projection — the component of $\mathbf{v}$ in the $\mathbf{e}_i$ direction.

### In Function Space

A function can be expanded in an orthogonal basis the same way. Using the complex exponentials $e_n(x) = e^{inx}$ as basis functions on $[0, 2\pi]$:

$$f(x) = \sum_{n=-\infty}^{\infty} c_n\,e^{inx}, \qquad c_n = \frac{\langle e_n, f \rangle}{\langle e_n, e_n \rangle} = \frac{1}{2\pi}\int_0^{2\pi} e^{-inx}\,f(x)\,dx$$

This is the Fourier series. Each Fourier coefficient $c_n$ is a projection — the component of $f$ in the $e^{inx}$ direction. The formula is identical in structure to the finite-dimensional case. The only difference is that the sum is infinite and the inner product is an integral.

![[Figures/linalg_projection.png|697]]
*Figure 3: Fourier partial sums of the sawtooth function $f(x) = x - \pi$ for $N = 1, 3, 5,$ and $10$ terms.*

This figure shows a sawtooth function $f(x) = x - \pi$ and its approximation by $N$ Fourier terms. With $N = 1$, we capture only the fundamental frequency. As $N$ increases, the projection onto a larger subspace of basis functions captures more of the function's shape. By $N = 10$, the approximation is close everywhere except near the jump discontinuity.

## Eigenvalues and Eigenvectors

### The Geometric Idea

A matrix $A$ acts on vectors by stretching, rotating, and reflecting them. Most vectors change direction when $A$ acts on them. But some special vectors only get scaled:

$$A\mathbf{v} = \lambda\,\mathbf{v}$$

These are the **eigenvectors** of $A$, and the scaling factors $\lambda$ are the **eigenvalues**. An eigenvector points in a direction that $A$ preserves — the matrix can stretch or flip it, but cannot rotate it away from its original line.

![[Figures/linalg_eigen.png]]
*Figure 4: Unit-circle vectors before (left) and after (right) applying the matrix $A = \bigl(\begin{smallmatrix}2 & 1\\1 & 2\end{smallmatrix}\bigr)$, with eigenvectors highlighted along $(1,1)$ and $(1,-1)$.*

The left panel shows several vectors on the unit circle. The right panel shows the result of applying the matrix $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$. The gray vectors all change direction — they rotate. But the two colored eigenvectors stay on their original lines: $\mathbf{v}_1$ along $(1,1)$ is scaled by $\lambda_1 = 3$, and $\mathbf{v}_2$ along $(1,-1)$ is scaled by $\lambda_2 = 1$. The unit circle is deformed into an ellipse whose axes align with the eigenvectors.

### Why Eigenvalues Matter

Eigenvalues reveal the essential behavior of a linear transformation:

- If all eigenvalues are positive, $A$ stretches space without flipping.
- If an eigenvalue is negative, $A$ reflects along that eigenvector's direction.
- If an eigenvalue is zero, $A$ collapses that direction entirely.
- The determinant of $A$ is the product of its eigenvalues; the trace is their sum.

Eigenvectors also give you the best coordinates for understanding $A$. In the eigenvector basis, $A$ becomes diagonal — it just scales each axis independently. A complicated transformation decomposes into simple, independent scalings.

## From Matrices to Operators

In finite dimensions, a matrix maps vectors to vectors. In function space, the analogous objects are **operators** — rules that take a function and produce a new function. The most important example is the derivative:

$$D[f] = \frac{df}{dx}$$

This is a linear operator: $D[f + g] = D[f] + D[g]$ and $D[\alpha f] = \alpha\,D[f]$. Just like a matrix, we can ask for its eigenvectors (here called **eigenfunctions**) — functions that the operator only scales:

$$D[f] = \lambda\,f \quad \Longleftrightarrow \quad \frac{df}{dx} = \lambda\,f$$

The solutions are $f(x) = e^{\lambda x}$. The exponentials are eigenfunctions of the derivative operator. Every eigenvalue $\lambda$ is allowed, and the corresponding eigenfunction is $e^{\lambda x}$.

A more physically important example is the negative second derivative $L = -\frac{d^2}{dx^2}$. Its eigenvalue equation is

$$-\frac{d^2 f}{dx^2} = \lambda\,f$$

With periodic boundary conditions on $[0, 2\pi]$, the eigenfunctions are exactly the Fourier modes $e^{inx}$, with eigenvalues $\lambda = n^2$. The Fourier basis is not arbitrary — it is the eigenbasis of this operator. Decomposing a function into Fourier modes is like diagonalizing a matrix: it turns a complicated operator into simple multiplication by eigenvalues.

This is the deep reason Fourier analysis works: sines and cosines are not just convenient — they are the eigenfunctions of the Laplacian. Every time you decompose a function into Fourier modes, you are doing exactly what diagonalization does for matrices.

## Where to Go Next

The ideas in this notebook — inner products, orthogonality, projection, eigenvalues — are the vocabulary of linear algebra. But function spaces require more care than $\mathbb{R}^n$: infinite sums may not converge, not every operator has eigenvalues, and the geometry of infinite dimensions has surprises. Making these ideas rigorous leads to:

- [[Hilbert Spaces]] — the precise setting for infinite-dimensional inner product spaces, where completeness and convergence are handled carefully
- [[Operators and Eigenvalues]] — bounded and unbounded operators on Hilbert spaces, spectral theory, and the rigorous treatment of differential operators as infinite-dimensional analogues of matrices
