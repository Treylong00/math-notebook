In [[Harmonic Functions]], we studied the Laplacian $\nabla^2$ and the functions that satisfy $\nabla^2 f = 0$. In [[Operators and Eigenvalues]], we saw that the equation $-f'' = \lambda f$ defines an eigenvalue problem whose solutions form a complete orthonormal basis. The **Helmholtz equation** is the point where these threads converge: it is the eigenvalue problem for the Laplacian operator in any number of dimensions, and its solutions are the building blocks of every wave phenomenon in physics.

## The Equation

Start with the wave equation for a scalar field $\Psi(\mathbf{r}, t)$:

$$\nabla^2 \Psi = \frac{1}{c^2} \frac{\partial^2 \Psi}{\partial t^2}$$

For a harmonic time dependence $\Psi(\mathbf{r}, t) = \psi(\mathbf{r}) e^{-i\omega t}$, the time derivatives give $-\omega^2/c^2$, and the spatial part satisfies

$$\nabla^2 \psi + k^2 \psi = 0, \qquad k = \frac{\omega}{c}$$

This is the **Helmholtz equation**. It asks: for a given frequency $\omega$, what spatial patterns $\psi(\mathbf{r})$ are consistent with wave propagation? When $k = 0$, it reduces to Laplace's equation $\nabla^2 \psi = 0$ — the harmonic functions from [[Harmonic Functions]] are the zero-frequency limit.

Yes — $k = 0$ corresponds to $\omega = 0$, which means no time dependence at all. The factor $e^{-i\omega t}$ becomes $1$, so $\Psi(\mathbf{r}, t) = \psi(\mathbf{r})$ is a field frozen in time: the static or "DC" limit. In electromagnetism that is exactly electrostatics and magnetostatics — and the electrostatic potential satisfying $\nabla^2 V = 0$ in source-free regions is literally a harmonic function. So [[Harmonic Functions|harmonic functions]] are the DC modes of the wave equation.


## The Helmholtz Operator

In the language of [[Dirac Notation]], the Helmholtz equation is an eigenvalue problem. Define the Laplacian as an operator $\hat{L} = \nabla^2$ acting on states $|\psi\rangle$ in a [[Hilbert Spaces|Hilbert space]]. Then

$$\hat{L}|\psi\rangle = -k^2|\psi\rangle$$

The eigenstates of $-\hat{L}$ are the spatial modes of the system, and the eigenvalues $k^2$ are related to the allowed frequencies by $\omega = ck$. This is the same structure as the time-independent Schrodinger equation from [[The Schrodinger Equation]], with $-\hat{L}$ playing the role of the Hamiltonian and $k^2$ playing the role of the energy.

Yes — by definition a harmonic function satisfies $\nabla^2 f = 0$, which is the eigenvalue equation $\hat{L}|f\rangle = 0\cdot|f\rangle$. So harmonic functions are exactly the zero-eigenvalue eigenstates of the Laplacian — the kernel of $\hat{L}$. Whether that eigenvalue actually appears in the spectrum of a given problem depends on the boundary conditions: on a bounded domain with Dirichlet boundaries ($\psi = 0$ on the walls), no nontrivial harmonic function vanishes on the boundary, so $\lambda = 0$ is excluded and the spectrum starts at a positive $k_1^2$. With Neumann boundaries ($\partial_n\psi = 0$), the constant function $\psi = \text{const}$ is harmonic *and* satisfies the boundary condition, so $\lambda = 0$ is the lowest eigenvalue.


## Free-Space Eigenstates

In unbounded space with no boundaries, the eigenstates of $\hat{L}$ are plane waves. In [[Dirac Notation]], they are the kets $|\mathbf{k}\rangle$ with position representation

$$\langle \mathbf{r} | \mathbf{k} \rangle = \frac{e^{i\mathbf{k}\cdot\mathbf{r}}}{(2\pi)^{d/2}}$$

where $d$ is the spatial dimension. It is worth being careful about what this bracket means. For two normalizable states $|\phi\rangle, |\psi\rangle \in L^2$, the inner product is the familiar integral $\langle\phi|\psi\rangle = \int \phi^*(\mathbf{r})\psi(\mathbf{r})\,d\mathbf{r}$. But $|\mathbf{r}\rangle$ and $|\mathbf{k}\rangle$ are *not* square-integrable functions — they are continuous basis kets, delta-normalized rather than unit-normalized. So $\langle \mathbf{r}|\mathbf{k}\rangle$ is not an integral of two functions. It is a single complex number: the value of the plane-wave state $|\mathbf{k}\rangle$ at position $\mathbf{r}$, exactly analogous to $\psi(\mathbf{r}) = \langle \mathbf{r}|\psi\rangle$ for an ordinary state.

The formula $e^{i\mathbf{k}\cdot\mathbf{r}}/(2\pi)^{d/2}$ is derived, not postulated. Define $|\mathbf{k}\rangle$ as the eigenstate of the momentum operator $\hat{\mathbf{P}}$, which in the position basis is $\hat{\mathbf{P}} = -i\nabla$. The eigenvalue equation $\hat{\mathbf{P}}|\mathbf{k}\rangle = \mathbf{k}|\mathbf{k}\rangle$, projected onto $\langle\mathbf{r}|$, becomes

$$-i\nabla \langle\mathbf{r}|\mathbf{k}\rangle = \mathbf{k}\,\langle\mathbf{r}|\mathbf{k}\rangle$$

whose solution is $\langle\mathbf{r}|\mathbf{k}\rangle = C\,e^{i\mathbf{k}\cdot\mathbf{r}}$. The constant $C = 1/(2\pi)^{d/2}$ is fixed by demanding the delta-normalization $\langle\mathbf{k}'|\mathbf{k}\rangle = \delta(\mathbf{k}' - \mathbf{k})$, since

$$\langle\mathbf{k}'|\mathbf{k}\rangle = \int \langle\mathbf{k}'|\mathbf{r}\rangle\langle\mathbf{r}|\mathbf{k}\rangle\,d\mathbf{r} = |C|^2 \int e^{-i(\mathbf{k}' - \mathbf{k})\cdot\mathbf{r}}\,d\mathbf{r} = (2\pi)^d |C|^2\,\delta(\mathbf{k}' - \mathbf{k})$$

using the Fourier representation of the delta function.

Applying the Laplacian to this plane wave is direct: $\nabla^2 e^{i\mathbf{k}\cdot\mathbf{r}} = -|\mathbf{k}|^2 e^{i\mathbf{k}\cdot\mathbf{r}}$, so

$$\hat{L}|\mathbf{k}\rangle = -|\mathbf{k}|^2 |\mathbf{k}\rangle$$

and the eigenvalue is $k^2 = |\mathbf{k}|^2$. In free space, $k^2$ can be any non-negative number — the spectrum is **continuous**. The plane waves form a complete orthonormal set:

$$\langle \mathbf{k}' | \mathbf{k} \rangle = \delta(\mathbf{k}' - \mathbf{k}), \qquad \int |\mathbf{k}\rangle\langle\mathbf{k}| \, d\mathbf{k} = \hat{I}$$

Any state can be expanded in the plane wave basis:

$$|\psi\rangle = \int \tilde{\psi}(\mathbf{k}) \, |\mathbf{k}\rangle \, d\mathbf{k}, \qquad \tilde{\psi}(\mathbf{k}) = \langle \mathbf{k} | \psi \rangle$$

This is precisely the [[Fourier Analysis|Fourier transform]] — the position and momentum representations from [[Dirac Notation]] reappear here as the two sides of the Fourier pair.

## Bounded Domains and Discrete Spectra

When the domain has boundaries, everything changes. Boundary conditions select a **discrete** subset of solutions from the continuous family, and the spectrum collapses from a continuum to a countable set of eigenvalues $\{k_{mn}^2\}$.

The most common boundary condition is **Dirichlet**: $\psi = 0$ on the boundary (the wave vanishes at the edges). This models a vibrating membrane clamped at its frame, an electromagnetic cavity with conducting walls, or a quantum particle confined to a box.

In the operator picture, imposing boundary conditions restricts the domain of $\hat{L}$ to a subspace of functions that vanish on the boundary. The restricted operator is Hermitian (by the argument in [[Operators and Eigenvalues]]), so we get all the guarantees: real eigenvalues, orthogonal eigenstates, and completeness.

The eigenstates $|m,n\rangle$ now satisfy

$$\hat{L}|m,n\rangle = -k_{mn}^2 |m,n\rangle, \qquad \langle m',n'|m,n\rangle = \delta_{mm'}\delta_{nn'}$$

$$\sum_{m,n} |m,n\rangle\langle m,n| = \hat{I}$$

The eigenvalues $k_{mn}^2$ depend on the shape and size of the domain — geometry determines the spectrum.

## The Rectangular Cavity

The simplest bounded domain is a rectangle $[0,a] \times [0,b]$ with Dirichlet boundary conditions. The Helmholtz equation separates into two independent 1D problems — one for each coordinate — and the eigenstates are tensor products:

$$|m,n\rangle = |m\rangle_x \otimes |n\rangle_y$$

In position representation:

$$\langle x,y|m,n\rangle = \frac{2}{\sqrt{ab}} \sin\!\left(\frac{m\pi x}{a}\right) \sin\!\left(\frac{n\pi y}{b}\right), \qquad m, n = 1, 2, 3, \ldots$$

with eigenvalues

$$k_{mn}^2 = \pi^2\!\left(\frac{m^2}{a^2} + \frac{n^2}{b^2}\right)$$

These are the 2D generalization of the particle-in-a-box eigenfunctions from [[The Schrodinger Equation]]. The quantum numbers $m$ and $n$ count the number of half-wavelengths in each direction, and the nodal lines (where $\psi = 0$) form a grid of horizontal and vertical lines.

![[Figures/helmholtz_rect_modes.png]]
*Figure 1: The first six eigenmodes of a square cavity with Dirichlet boundary conditions. Black lines mark the nodal lines ($\psi = 0$). The modes $|2,1\rangle$ and $|1,2\rangle$ share the same eigenvalue $k^2 = 5\pi^2$ — they are degenerate.*

The degeneracy between $|2,1\rangle$ and $|1,2\rangle$ (and between $|3,1\rangle$ and $|1,3\rangle$) is a consequence of the square symmetry: swapping $m$ and $n$ is the same as rotating the domain by $90°$. In a rectangle with $a \neq b$, this symmetry is broken and the degeneracies lift.

The tensor product structure $|m,n\rangle = |m\rangle_x \otimes |n\rangle_y$ means the 2D problem factorizes completely. This is special to separable geometries. For irregular domains, the eigenstates cannot be written as products, and numerical methods are needed.

## The Circular Drum

A circular domain of radius $R$ is another separable geometry, but the natural coordinates are polar $(r, \theta)$. Separation of variables gives

$$\psi(r,\theta) = R_{mn}(r) \, \Theta_m(\theta)$$

The angular part is $\Theta_m(\theta) = \cos(m\theta)$ (or $\sin(m\theta)$), which requires $m = 0, 1, 2, \ldots$ for single-valuedness. The radial part satisfies **Bessel's equation**, and the solutions that are regular at the origin are the Bessel functions $J_m$:

$$\langle r, \theta | m, n \rangle \propto J_m\!\left(\frac{j_{mn} \, r}{R}\right) \cos(m\theta)$$

where $j_{mn}$ is the $n$th zero of $J_m$ (so that $\psi = 0$ at $r = R$). The eigenvalues are

$$k_{mn}^2 = \left(\frac{j_{mn}}{R}\right)^2$$

![[Figures/helmholtz_circular_modes.png]]
*Figure 2: The first six eigenmodes of a circular drum with Dirichlet boundary conditions. The Bessel zero $j_{mn}$ that sets each eigenvalue is shown in the title. The $m = 0$ modes are radially symmetric; higher $m$ introduces angular nodal lines.*

The $|0,1\rangle$ mode is the fundamental — radially symmetric, no internal nodes. The $|1,1\rangle$ mode has a single nodal diameter splitting the drum into two halves vibrating in antiphase. The $|0,2\rangle$ mode has a nodal circle — a ring inside the drum where the displacement vanishes. These are the patterns Chladni observed by sprinkling sand on vibrating plates: the sand collects on the nodal lines.

For each $m > 0$, there is a degenerate partner with $\sin(m\theta)$ instead of $\cos(m\theta)$ — a rotation of the same pattern by $\pi/(2m)$. This degeneracy reflects the rotational symmetry of the circle, just as the $m \leftrightarrow n$ degeneracy in the square reflects its reflection symmetry.

## The Eigenvalue Spectrum

The set of all eigenvalues $\{k_{mn}^2\}$ is the **spectrum** of the domain. Two domains of the same area but different shapes have different spectra — the spacing, ordering, and degeneracy pattern of the eigenvalues encode the geometry.

![[Figures/helmholtz_spectrum.png]]
*Figure 3: Eigenvalue spectra of the unit square and the unit disk. The square has regular spacing with many degeneracies (from integer coincidences like $1^2 + 4^2 = 4^2 + 1^2$). The circle's spectrum is determined by the zeros of Bessel functions and has an irregular, non-repeating pattern.*

The square's spectrum has a rigid structure: the eigenvalues are $\pi^2(m^2 + n^2)$, and degeneracies occur whenever two pairs $(m,n)$ give the same sum of squares. The circle's spectrum depends on the zeros of Bessel functions — irrational numbers with no closed-form pattern. The spectra encode different geometries.

This leads to a famous question posed by Mark Kac in 1966: **"Can one hear the shape of a drum?"** If you know all the eigenvalues $\{k_{mn}^2\}$, can you reconstruct the shape of the domain? The answer, it turns out, is no — there exist pairs of non-congruent domains with identical spectra. But the question illustrates how tightly the spectrum and the geometry are coupled.

## The Green's Function

The eigenmodes do more than describe free vibrations — they let us solve the **driven** Helmholtz equation. A point source at $\mathbf{r}'$ produces a field satisfying

$$(\nabla^2 + k^2) G(\mathbf{r}, \mathbf{r}') = -\delta(\mathbf{r} - \mathbf{r}')$$

In operator form, this is $(\hat{L} + k^2)\hat{G} = -\hat{I}$, so

$$\hat{G} = -(\hat{L} + k^2)^{-1}$$

This is the **resolvent** of $\hat{L}$. Since we know the eigendecomposition of $\hat{L}$, we can invert it mode by mode. Inserting the completeness relation $\hat{I} = \sum_{m,n} |m,n\rangle\langle m,n|$:

$$\hat{G} = -\sum_{m,n} \frac{|m,n\rangle\langle m,n|}{k_{mn}^2 - k^2}$$

In position representation:

$$G(\mathbf{r}, \mathbf{r}') = \langle \mathbf{r}|\hat{G}|\mathbf{r}'\rangle = -\sum_{m,n} \frac{\langle \mathbf{r}|m,n\rangle\langle m,n|\mathbf{r}'\rangle}{k_{mn}^2 - k^2}$$

Each eigenmode contributes a term proportional to its value at the source ($\langle m,n|\mathbf{r}'\rangle$) times its spatial pattern ($\langle \mathbf{r}|m,n\rangle$), weighted by how close $k^2$ is to the eigenvalue $k_{mn}^2$.

![[Figures/helmholtz_greens_expansion.png]]
*Figure 4: The Green's function $-G(\mathbf{r}, \mathbf{r}')$ for a point source (star) in a rectangular cavity, built from an increasing number of eigenmodes. With one mode, the response is just the fundamental; with 225 modes, the response localizes sharply at the source.*

With a single mode, the Green's function looks like the fundamental eigenstate — it knows nothing about the source location beyond the overlap $\langle 1,1|\mathbf{r}'\rangle$. As more modes are added, the response sharpens and localizes at $\mathbf{r}'$. This is completeness at work: the delta function $\delta(\mathbf{r} - \mathbf{r}')$ is a sum of infinitely many eigenmodes, and truncating the sum gives a smoothed approximation.

When $k^2$ approaches an eigenvalue $k_{mn}^2$, the corresponding denominator $k_{mn}^2 - k^2$ approaches zero and that mode's contribution diverges. This is a **resonance**: the driving frequency matches a natural frequency of the cavity, and the response blows up. In a physical system with loss, the divergence is regularized — a small imaginary part in $k^2$ (as in the [[Complex Permittivity]] discussion) keeps the denominator finite and gives the resonance a finite width.

## Where to Go Next

- **[[Greens Functions]]** — the free-space Helmholtz Green's function in 1D/2D/3D, the $i\epsilon$ prescription that selects outgoing waves, and worked problems in electrostatics, driven cavities, and 1D scattering.
- **Scattering theory** — in unbounded domains, the Helmholtz equation describes waves scattered by obstacles. The Green's function gives the outgoing wave from each scattering event.
- **Waveguides and cavities** — the modes of [[Maxwells Equations|electromagnetic waveguides]] satisfy the Helmholtz equation in the transverse plane. The eigenvalues $k_{mn}^2$ determine the cutoff frequencies.
- **Spectral geometry** — the study of how eigenvalue spectra encode geometric information. Weyl's law gives the asymptotic density of eigenvalues in terms of the domain's area and perimeter.
- **Periodic potentials and Bloch's theorem** — when the domain has translational symmetry, the eigenstates acquire a phase factor across each period, leading to band structure.
