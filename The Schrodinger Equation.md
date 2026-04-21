Every thread we've followed — [[Complex Numbers]], [[Harmonic Functions]], [[Fourier Analysis]], [[Linear Algebra]], [[Hilbert Spaces]], [[Operators and Eigenvalues]], [[Probability and Complex Amplitudes]] — converges here. The Schrodinger equation is the equation of motion for quantum mechanics. It says how a wavefunction evolves in time, and its structure is built from every concept we've developed: differential operators, eigenvalue problems, complex exponentials, Fourier transforms, inner products, and the Born rule.

## The Schrodinger Equation

The **time-dependent Schrodinger equation** is

$$i\hbar \frac{\partial \psi}{\partial t} = \hat{H}\psi$$

where $\hat{H}$ is the **Hamiltonian operator** — the operator that represents total energy. For a single particle in one dimension with potential $V(x)$:

$$\hat{H} = -\frac{\hbar^2}{2m}\frac{d^2}{dx^2} + V(x)$$

The first term is kinetic energy — a second derivative, just like the Laplacian from [[Harmonic Functions]], scaled by $-\hbar^2/2m$. The second term is potential energy. Together, $\hat{H}$ is the operator from [[Operators and Eigenvalues]], and the Schrodinger equation says that $\hat{H}$ generates time evolution through the complex exponential machinery of [[Complex Numbers]].

We will use **natural units** $\hbar = 1$, $m = 1/2$ where convenient. In these units, the kinetic energy operator simplifies to $-d^2/dx^2$ and the equations become cleaner without losing any physics.

## The Time-Independent Schrodinger Equation

If we look for solutions of definite energy — states where the energy is sharp, not a superposition — we separate variables. Write $\psi(x, t) = \psi(x)\,e^{-iEt/\hbar}$ and substitute into the time-dependent equation. The time part cancels, leaving

$$\hat{H}\psi = E\psi$$

This is an **eigenvalue equation**. The wavefunction $\psi(x)$ is an eigenfunction of the Hamiltonian, and the energy $E$ is the corresponding eigenvalue. This is exactly the structure from [[Operators and Eigenvalues]]: a differential operator acting on a function, producing a scalar multiple of that function.

Not every $E$ works. The boundary conditions and the potential $V(x)$ select a discrete set of allowed energies $E_1, E_2, E_3, \ldots$ with corresponding eigenfunctions $\psi_1, \psi_2, \psi_3, \ldots$ The spectrum of the Hamiltonian gives the allowed energy levels of the quantum system.

## Particle in a Box

The simplest quantum system: a particle confined to an interval $[0, L]$ with impenetrable walls. The potential is

$$V(x) = \begin{cases} 0 & 0 < x < L \\ \infty & \text{otherwise} \end{cases}$$

Inside the box, the time-independent Schrodinger equation (in natural units) becomes

$$-\frac{d^2\psi}{dx^2} = E\psi$$

This is the same equation we solved in [[Operators and Eigenvalues]]: the eigenfunctions of $-d^2/dx^2$ with boundary conditions $\psi(0) = \psi(L) = 0$ are

$$\psi_n(x) = \sqrt{\frac{2}{L}}\sin\!\left(\frac{n\pi x}{L}\right), \qquad n = 1, 2, 3, \ldots$$

with energies

$$E_n = \frac{n^2 \pi^2}{L^2}$$

The energy grows as $n^2$. The ground state ($n = 1$) has one half-arch; the $n$-th state has $n$ half-arches. These are the same sine functions that formed our [[Fourier Analysis]] basis — the eigenfunctions of the Laplacian on an interval are the Fourier basis.

![[Figures/schrodinger_particle_box.png]]
*Figure 1: Particle-in-a-box wavefunctions $\psi_n(x)$ offset by energy level (left) and their probability densities $|\psi_n|^2$ (right) for the first several modes.*

The left panel shows the wavefunctions $\psi_n(x)$, offset by their energy level. The right panel shows the probability densities $|\psi_n|^2$. Notice that higher energy states have more nodes (zero crossings), and the probability density distributes more evenly across the box as $n$ increases.

## Quantum Harmonic Oscillator

Now replace the infinite walls with a parabolic potential:

$$V(x) = \frac{1}{2}m\omega^2 x^2$$

This is the quantum version of a mass on a spring. The time-independent Schrodinger equation becomes

$$-\frac{\hbar^2}{2m}\frac{d^2\psi}{dx^2} + \frac{1}{2}m\omega^2 x^2 \psi = E\psi$$

The solutions are **Hermite functions** — Hermite polynomials multiplied by a Gaussian envelope:

$$\psi_n(x) \propto H_n(\alpha x)\,e^{-\alpha x^2/2}$$

where $\alpha = \sqrt{m\omega/\hbar}$ and $H_n$ is the $n$-th Hermite polynomial ($H_0 = 1$, $H_1 = 2x$, $H_2 = 4x^2 - 2$, and so on). The Gaussian ensures the wavefunction decays at infinity — the particle is bound. The Hermite polynomial creates the oscillatory structure inside the well.

The energy levels are beautifully simple:

$$E_n = \hbar\omega\!\left(n + \frac{1}{2}\right), \qquad n = 0, 1, 2, \ldots$$

They are **evenly spaced**, separated by $\hbar\omega$. And there is a **zero-point energy** $E_0 = \hbar\omega/2$ — even in the ground state, the particle cannot sit still. This is a direct consequence of the uncertainty principle, which we will see shortly.

![[Figures/schrodinger_harmonic_oscillator.png]]
*Figure 2: Harmonic oscillator eigenfunctions $\psi_n(x)$ superimposed on the parabolic potential $V(x) = \frac{1}{2}m\omega^2 x^2$, each offset by its energy level $E_n$.*

Each eigenfunction is drawn offset by its energy level, superimposed on the parabolic potential. The ground state ($n = 0$) is a Gaussian — the minimum-uncertainty state. Each successive level adds one node. The wavefunctions extend slightly beyond the classical turning points (where $E_n = V(x)$), a purely quantum phenomenon called **tunneling**.

## Time Evolution

We have found the stationary states — eigenfunctions of $\hat{H}$ that solve the time-independent equation. But the full time-dependent equation allows **superpositions**. The general solution is

$$\psi(x, t) = \sum_n c_n\,\psi_n(x)\,e^{-iE_n t/\hbar}$$

Each eigenstate $\psi_n$ acquires a time-dependent phase factor $e^{-iE_n t/\hbar}$ — a complex exponential rotating in the complex plane at frequency $E_n/\hbar$. This is [[Complex Numbers]] in action: each energy eigenstate spins at its own rate.

A single eigenstate has $|\psi_n(x, t)|^2 = |\psi_n(x)|^2$ — the probability density doesn't change with time. That's why they are called **stationary states**. But a superposition of two or more eigenstates with different energies creates **interference** between the rotating phases, and the probability density oscillates.

Take the particle in a box with $\psi(x, 0) = \frac{1}{\sqrt{2}}(\psi_1(x) + \psi_2(x))$. The two components rotate at different rates, so

$$|\psi(x, t)|^2 = \frac{1}{2}\!\left[|\psi_1|^2 + |\psi_2|^2 + 2\,\psi_1\psi_2\cos\!\left((E_2 - E_1)\frac{t}{\hbar}\right)\right]$$

The cross-term oscillates with period $T = 2\pi\hbar/(E_2 - E_1)$. The probability sloshes back and forth inside the box:

![[Figures/schrodinger_time_evolution.png]]
*Figure 3: Time evolution of the probability density $|\psi(x,t)|^2$ for a superposition of the first two particle-in-a-box eigenstates at four equally spaced times within one oscillation period.*

![[Figures/anim_wavefunction_evolution.gif]]
*Animation 1: A Gaussian wavepacket bouncing inside a particle-in-a-box potential, showing probability density $|\psi(x,t)|^2$ and the real part of the wavefunction.*

At $t = 0$, the probability is concentrated on the left side of the box. By $t = T/4$, it has spread to the center. At $t = T/2$, it has shifted to the right. At $t = 3T/4$, it swings back through center. This is the quantum analog of a classical particle bouncing between the walls — except the motion is smooth, wave-like, and governed by complex phase evolution.

The coefficients $c_n$ are determined by the initial condition through the inner product from [[Hilbert Spaces]]:

$$c_n = \langle \psi_n, \psi(\cdot, 0) \rangle = \int \psi_n(x)^*\,\psi(x, 0)\,dx$$

This is Fourier analysis: decompose the initial wavefunction into the energy eigenbasis, then evolve each component independently.

## The Uncertainty Principle

The Heisenberg uncertainty principle states

$$\Delta x \cdot \Delta p \geq \frac{\hbar}{2}$$

where $\Delta x$ and $\Delta p$ are the standard deviations of position and momentum in the state $\psi$. You cannot simultaneously know both to arbitrary precision. This is not a statement about measurement disturbance — it is a fundamental property of waves.

The connection to [[Fourier Analysis]] makes this inevitable. Momentum eigenstates are complex exponentials $e^{ikx}$, so the momentum-space wavefunction $\tilde{\psi}(k)$ is the Fourier transform of $\psi(x)$. The uncertainty principle is the Fourier uncertainty relation in disguise:

- A wavefunction **localized in position** (narrow in $x$) must be a superposition of many momentum components (wide in $k$).
- A wavefunction **localized in momentum** (narrow in $k$) must be spread out over many positions (wide in $x$).

The **Gaussian wavepacket** is the state that saturates the bound — it achieves $\Delta x \cdot \Delta p = \hbar/2$ exactly. This is why the harmonic oscillator ground state (a Gaussian) is special: it is the minimum-uncertainty state, the closest a quantum particle can come to having a definite position and momentum simultaneously.

![[Figures/schrodinger_uncertainty.png]]
*Figure 4: Narrow and broad Gaussian wavepackets in position space (left) and their Fourier transforms in momentum space (right), illustrating the uncertainty tradeoff $\Delta x \cdot \Delta p \geq \hbar/2$.*

The left panel shows position-space probability densities: the narrow Gaussian is well-localized in $x$ but, as the right panel reveals, its momentum-space representation is wide. The broad Gaussian is spread in $x$ but sharply peaked in $k$. You can squeeze one, but the other always spreads.

This also explains the zero-point energy of the harmonic oscillator. If the particle sat at the bottom of the well with zero momentum, we would have $\Delta x = 0$ and $\Delta p = 0$, violating the uncertainty principle. The ground state energy $E_0 = \hbar\omega/2$ is the cost of confinement — the minimum energy compatible with the uncertainty bound.

## Where to Go Next

The Schrodinger equation in one dimension has shown us the essential quantum mechanics: eigenvalue problems determine allowed energies, complex phase drives time evolution, and the Fourier relationship between position and momentum enforces uncertainty. From here, the theory extends in several directions:

- **Higher dimensions**: The Laplacian $\nabla^2$ replaces $d^2/dx^2$, and separation of variables in different coordinate systems (Cartesian, spherical, cylindrical) leads to different families of eigenfunctions.
- **The hydrogen atom**: Spherical symmetry and the Coulomb potential $V(r) = -e^2/r$ give the energy levels $E_n = -13.6/n^2$ eV and the atomic orbitals — spherical harmonics times radial functions. <!-- definitely want to review this. then go into phonons and lattices -->
- **Angular momentum and spin**: Orbital angular momentum is quantized ($l = 0, 1, 2, \ldots$), and particles carry an intrinsic spin angular momentum with no classical analog.
- **Multi-particle systems**: Tensor products of Hilbert spaces, entanglement, and the Pauli exclusion principle for fermions.
- <!-- Would like a page on the Helmholtz equation. -->

Each of these builds on the same foundation: operators, eigenvalues, Hilbert spaces, and the Schrodinger equation.
