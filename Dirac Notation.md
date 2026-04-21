The mathematics of quantum mechanics — [[Hilbert Spaces]], [[Operators and Eigenvalues]], [[Probability and Complex Amplitudes]] — involves a lot of integrals. Dirac notation is a compact language that replaces those integrals with an algebra of symbols, making the structure of quantum mechanics visible at a glance.

This isn't just shorthand. Dirac notation separates the abstract structure (vectors, operators, inner products) from any particular representation (position, momentum, energy), which is exactly the right way to think about quantum states.

## Kets and Bras

A quantum state is a vector in a [[Hilbert Spaces|Hilbert space]]. Dirac notation writes it as a **ket**:

$$|\psi\rangle$$

This is the abstract state — it doesn't commit to any basis or representation. It's the analog of a vector $\mathbf{v}$ in $\mathbb{R}^n$, except it lives in the infinite-dimensional space $L^2$.

Every ket has a corresponding **bra**:

$$\langle\psi|$$

The bra is the dual vector — the thing that, when combined with a ket, produces a number. If $|\psi\rangle$ is a column vector, $\langle\psi|$ is the conjugate-transpose row vector.

## Inner Products

The inner product of two states is a **bracket** — a bra meeting a ket:

$$\langle\phi|\psi\rangle = \int_{-\infty}^{\infty} \phi^*(x)\,\psi(x)\,dx$$

This single symbol $\langle\phi|\psi\rangle$ replaces the entire integral. The notation was designed so that "bra-ket" literally spells "bracket."

Key properties:
- **Normalization:** $\langle\psi|\psi\rangle = 1$ means $\int |\psi(x)|^2\,dx = 1$
- **Orthogonality:** $\langle\phi|\psi\rangle = 0$ means the states are perpendicular
- **Probability amplitude:** if $|n\rangle$ is an eigenstate, then $c_n = \langle n|\psi\rangle$ is the amplitude for measuring state $n$, and $|c_n|^2$ is the probability

## Basis Decomposition

Any state can be expanded in a complete orthonormal basis $\{|n\rangle\}$:

$$|\psi\rangle = \sum_n c_n\,|n\rangle, \qquad c_n = \langle n|\psi\rangle$$

The coefficients $c_n$ are inner products — projections of $|\psi\rangle$ onto each basis vector. The probability of measuring the system in state $|n\rangle$ is $P(n) = |c_n|^2 = |\langle n|\psi\rangle|^2$, which is the [[Probability and Complex Amplitudes|Born rule]] written in Dirac notation.

![[Figures/dirac_basis_decomposition.png]]
*Figure 1: A wavefunction $\psi(x)$ shown in the position basis (left) and its energy-basis decomposition $|\langle n|\psi\rangle|^2$ as a bar chart of measurement probabilities (right).*

The left panel shows the wavefunction $\psi(x) = \langle x|\psi\rangle$ — the state expressed in the position basis. The right panel shows the same state decomposed in the energy basis: each bar is $|\langle n|\psi\rangle|^2$, the probability of measuring energy $E_n$.

## Outer Products and Projectors

While $\langle\phi|\psi\rangle$ is a number (inner product), the **outer product** $|\phi\rangle\langle\psi|$ is an **operator** — it takes a state in and gives a state out:

$$(|\phi\rangle\langle\psi|)\,|\chi\rangle = |\phi\rangle\,\langle\psi|\chi\rangle$$

It projects $|\chi\rangle$ onto $|\psi\rangle$, then replaces the result with $|\phi\rangle$ scaled by the overlap.

When $|\phi\rangle = |\psi\rangle = |n\rangle$ (a normalized basis state), the outer product $|n\rangle\langle n|$ is a **projection operator** — it extracts the component of a state along $|n\rangle$:

$$\hat{P}_n\,|\psi\rangle = |n\rangle\langle n|\psi\rangle = c_n\,|n\rangle$$

![[Figures/dirac_projection.png]]
*Figure 2: Action of the projection operator $|2\rangle\langle 2|$ on a state $|\psi\rangle$: the original state (left), the projected component $c_2|2\rangle$ (middle), and the remainder after subtraction (right).*

The left panel shows $|\psi\rangle$, the middle shows the projected component $|2\rangle\langle 2|\psi\rangle = c_2|2\rangle$, and the right shows what remains after the projection is subtracted.

### Untangling the notation

A common source of confusion: if $f(x) = x^2$ and $f(2) = 4$, is that $|4\rangle\langle x|f\rangle$? No — and the confusion reveals something important about what the symbols mean.

The expression $\langle x | f \rangle = f(x)$ is not really an inner product in the usual sense. It's a notational device: $|x\rangle$ is a "position eigenstate" and $\langle x|f\rangle$ means "the value of $|f\rangle$ in the position representation at point $x$." The result $f(x)$ is a number — the value of the function at that point. There's no outer product involved in evaluating a function.

The outer product $|n\rangle\langle n|$ is an operator that acts on *states*, not on numbers. When we write $|n\rangle\langle n|\psi\rangle$, the bra $\langle n|$ computes the overlap $c_n = \langle n|\psi\rangle$ (a number), and then the ket $|n\rangle$ produces the state $c_n|n\rangle$. The input and output are both states — vectors in Hilbert space.

It's also worth noting that $f(x) = x^2$ is not in $L^2(\mathbb{R})$ — it's not square-integrable, so it doesn't represent a valid quantum state. Dirac notation is built for the Hilbert space setting, where states are normalizable. The function $\sin(nx)$ on an interval like $[0, \pi]$ *is* a valid state, and it's an eigenstate of $-d^2/dx^2$. But the expression $\sin(nx) = \langle x|n\rangle$ — it's the *position representation* of the energy eigenstate $|n\rangle$, not an outer product. Reading it aloud: "the value of the $n$-th eigenstate at position $x$."

To summarize the three key expressions and what each one *is*:

| Expression                                          | Type     | Meaning                                                  |
| --------------------------------------------------- | -------- | -------------------------------------------------------- |
| $\langle n \| \psi\rangle = c_n$                    | number   | overlap of $\|\psi\rangle$ with basis state $\|n\rangle$ |
| $\|n\rangle\langle n\| \psi\rangle = c_n\|n\rangle$ | state    | projection of $\|\psi\rangle$ onto $\|n\rangle$          |
| $\|n\rangle\langle n\|$                             | operator | the projector itself, waiting for a state to act on      |

## The Completeness Relation

If $\{|n\rangle\}$ is a complete orthonormal basis, then the sum of all projectors is the identity operator:

$$\sum_n |n\rangle\langle n| = \hat{I}$$

This is the **completeness relation** (or resolution of the identity). It says: if you project a state onto every basis vector and add the pieces back together, you recover the original state. It's the infinite-dimensional version of decomposing a vector into its components along each axis.

![[Figures/dirac_completeness.png]]
*Figure 3: Reconstruction of $|\psi\rangle$ from partial sums $\sum_{n=1}^{N}|n\rangle\langle n|\psi\rangle$ for increasing $N$, demonstrating convergence of the completeness relation to the identity.*

As $N$ increases, the partial sum $\sum_{n=1}^{N} |n\rangle\langle n|$ converges to the identity — the reconstruction approaches $|\psi\rangle$.

## Operators in Dirac Notation

An operator $\hat{A}$ acting on a state is written $\hat{A}|\psi\rangle$. The **matrix element** of $\hat{A}$ between two states is:

$$\langle m|\hat{A}|n\rangle = \int \phi_m^*(x)\,\hat{A}\,\phi_n(x)\,dx$$

This gives the $(m, n)$ entry of the operator's matrix in the $\{|n\rangle\}$ basis. The full operator can be reconstructed from its matrix elements using the completeness relation:

$$\hat{A} = \sum_{m,n} |m\rangle\langle m|\hat{A}|n\rangle\langle n|$$

The expectation value from [[Probability and Complex Amplitudes]] becomes:

$$\langle\hat{A}\rangle = \langle\psi|\hat{A}|\psi\rangle = \sum_{m,n} c_m^*\,\langle m|\hat{A}|n\rangle\,c_n$$

![[Figures/dirac_matrix_elements.png]]
*Figure 4: Matrix elements $\langle m|\hat{x}|n\rangle$ of the position operator in the particle-in-a-box energy eigenbasis, showing the selection-rule structure of allowed transitions.*

The matrix elements $\langle m|\hat{x}|n\rangle$ of the position operator in the particle-in-a-box basis. The structure of the matrix reveals selection rules: which transitions the operator connects.

## Position and Momentum Representations

The abstract ket $|\psi\rangle$ doesn't live in any particular basis. We choose a representation by inserting a completeness relation.

**Position representation:** using the continuous basis $\{|x\rangle\}$,

$$\psi(x) = \langle x|\psi\rangle$$

The familiar wavefunction $\psi(x)$ is just the inner product of the abstract state with a position eigenstate. The completeness relation is $\int |x\rangle\langle x|\,dx = \hat{I}$.

**Momentum representation:** using $\{|p\rangle\}$,

$$\tilde\psi(p) = \langle p|\psi\rangle$$

The momentum-space wavefunction is the state projected onto momentum eigenstates. The two representations are related by:

$$\langle x|p\rangle = \frac{1}{\sqrt{2\pi\hbar}}\,e^{ipx/\hbar}$$

This is the Fourier kernel from [[Fourier Analysis]] — changing from position to momentum representation is exactly a Fourier transform:

$$\tilde\psi(p) = \int \langle p|x\rangle\langle x|\psi\rangle\,dx = \frac{1}{\sqrt{2\pi\hbar}}\int e^{-ipx/\hbar}\,\psi(x)\,dx$$

![[Figures/dirac_position_momentum.png]]
*Figure 5: A Gaussian wavepacket with nonzero average momentum shown in the position representation $\psi(x)$ (left) and the momentum representation $\tilde\psi(p)$ (right).*

The same Gaussian wavepacket in both representations. The oscillations in $\psi(x)$ encode the average momentum; the localization in $\tilde\psi(p)$ reflects the narrow spread in momentum. The two are related by $\langle x|p\rangle = e^{ipx}/\sqrt{2\pi}$.

## Why Dirac Notation Matters

The power of Dirac notation is that it separates **what a state is** from **how you look at it**:

- $|\psi\rangle$ is the state itself — basis-independent
- $\langle x|\psi\rangle = \psi(x)$ is what you see in the position basis
- $\langle p|\psi\rangle = \tilde\psi(p)$ is what you see in the momentum basis
- $\langle n|\psi\rangle = c_n$ is what you see in the energy basis

The physics lives in $|\psi\rangle$. The representation is a choice. Dirac notation makes this distinction structural, not just philosophical — the completeness relation $\sum |n\rangle\langle n| = \hat{I}$ is the machinery for moving between representations, and the inner product $\langle\phi|\psi\rangle$ is invariant under the choice.

## Where to Go Next

- **[[The Schrodinger Equation]]** — Dirac notation makes the time-independent equation $\hat{H}|n\rangle = E_n|n\rangle$ and time evolution $|\psi(t)\rangle = e^{-i\hat{H}t/\hbar}|\psi(0)\rangle$ particularly clean
- **Tensor products** — multi-particle states live in $\mathcal{H}_1 \otimes \mathcal{H}_2$, written $|n\rangle \otimes |m\rangle = |n, m\rangle$. Entanglement is the statement that some states can't be factored.
- **Density matrices** — $\hat\rho = |\psi\rangle\langle\psi|$ for pure states, $\hat\rho = \sum_i p_i |\psi_i\rangle\langle\psi_i|$ for mixed states. The outer product becomes the fundamental object.
- **Symmetries and groups** — unitary operators $\hat{U}|\psi\rangle$ represent symmetry transformations. The representation theory of groups connects to the structure of quantum mechanics.
