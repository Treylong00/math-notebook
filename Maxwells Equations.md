Maxwell's equations and the Schrodinger equation look like completely different physics. One governs light, the other governs matter. But mathematically, they are the same kind of problem: an eigenvalue equation for a differential operator, with boundary conditions selecting which solutions are allowed. The same [[Linear Algebra]], [[Operators and Eigenvalues|operator theory]], and [[Dirac Notation]] that describe quantum states also describe electromagnetic modes.

This notebook makes that connection explicit, starting from the electromagnetic wave equation and building toward the shared mathematical structure.

## The Wave Equation as an Eigenvalue Problem

Maxwell's equations in a source-free, linear medium reduce to the vector wave equation. For a monochromatic field $\mathbf{E}(\mathbf{r}) e^{-i\omega t}$:

$$\nabla \times \nabla \times \mathbf{E} = \frac{\omega^2}{c^2} \varepsilon(\mathbf{r}) \, \mathbf{E}$$

This is an eigenvalue problem. The operator $\nabla \times \nabla \times$ acts on the field, and $\omega^2/c^2$ is the eigenvalue. In a uniform medium, plane waves $\mathbf{E} \propto e^{i\mathbf{k} \cdot \mathbf{r}}$ are the eigenfunctions — the same complex exponentials that appear as eigenfunctions of $-d^2/dx^2$ in [[Operators and Eigenvalues]].

For a 1D geometry (e.g., a slab waveguide or multilayer film), the equation simplifies to a scalar problem:

$$-\frac{d^2 E}{dx^2} + n^2(x) k_0^2 \, E = \beta^2 E$$

Compare this directly with the time-independent [[The Schrodinger Equation|Schrodinger equation]]:

$$-\frac{d^2 \psi}{dx^2} + V(x) \, \psi = E \, \psi$$

The refractive index profile $n^2(x)$ plays the role of the potential $V(x)$. The propagation constant $\beta^2$ plays the role of the energy $E$. The mathematics is identical.

## Dispersion Relations

A **dispersion relation** $\omega(k)$ describes how the frequency of a wave depends on its wavevector. It encodes the physics of the medium — how fast waves travel, whether there's a cutoff, whether different frequencies travel at different speeds.

In vacuum, $\omega = ck$ — all frequencies travel at the speed of light. In a dielectric with refractive index $n$, $\omega = ck/n$ — light slows down. In a plasma (or a metal below its plasma frequency), $\omega = \sqrt{\omega_p^2 + c^2 k^2}$ — there's a cutoff at $\omega_p$ below which waves can't propagate.

![[Figures/maxwell_dispersion.png]]
*Figure 1: Dispersion relations $\omega(k)$ for a dielectric (left), a plasma with cutoff at $\omega_p$ (middle), and a phonon-polariton system with a Reststrahlen gap between $\omega_{TO}$ and $\omega_{LO}$ (right).*

The left panel shows how a dielectric tilts the light line — higher index means a shallower slope (slower phase velocity). The middle panel shows plasma dispersion: below $\omega_p$, no propagating solutions exist — the wave is evanescent. The right panel shows **phonon-polariton** dispersion: when light couples to a lattice vibration, the dispersion splits into two branches with a gap (the Reststrahlen band) between $\omega_{TO}$ and $\omega_{LO}$ where no modes propagate.

These dispersion diagrams are the eigenvalue spectrum of Maxwell's curl operator in each medium — exactly analogous to the energy spectrum $E_n$ from [[Operators and Eigenvalues]].

## Interfaces and the Fresnel Equations

When light hits an interface between two media, it partially reflects and partially transmits. The **Fresnel equations** give the reflection and transmission coefficients as functions of the incidence angle and the refractive indices.

The reflection coefficient $r$ is complex — it has both a magnitude $|r|$ (how much reflects) and a phase $\arg(r)$ (the phase shift upon reflection). For p-polarized light (TM), there exists a **Brewster angle** $\theta_B = \arctan(n_2/n_1)$ where $|r_p|^2 = 0$ — no reflection at all.

![[Figures/maxwell_fresnel.png]]
*Figure 2: Fresnel reflectance $|r|^2$ for TE and TM polarizations versus incidence angle (left) and the corresponding reflection phase $\arg(r)$ showing the $\pi$ jump at Brewster's angle for TM (right).*

The left panel shows reflectance $|r|^2$ for both polarizations. TM light has a zero at Brewster's angle; TE light reflects more and more as $\theta \to 90°$. The right panel shows the phase — notice the $\pi$ phase jump in $r_p$ at Brewster's angle, where the sign of the reflection coefficient changes. This is a direct analog of the phase behavior in [[Complex Numbers]]: the reflection coefficient traces a path through the complex plane as the angle varies, and the Brewster angle is where it crosses the origin.

We can see the full picture by plotting $|r|$ and $\arg(r)$ over the entire $(\theta_i, n_2)$ parameter space:

![[Figures/maxwell_fresnel_contour.png]]
*Figure 3: Contour maps of Fresnel reflection magnitude $|r|$ and phase $\arg(r)$ over the $(\theta_i, n_2)$ parameter space for s-polarization (top row) and p-polarization (bottom row), with the Brewster angle traced as a dashed curve.*

The top row is s-polarization (TE), the bottom row is p-polarization (TM). The left column shows $|r|$ — how much reflects — and the right column shows $\arg(r)$ — the phase shift. The dashed white curve in the TM panels traces the Brewster angle $\theta_B = \arctan(n_2)$, where $|r_p| = 0$ and the phase jumps by $\pi$. Notice that s-polarization has no such zero — it reflects at every angle.

## Waveguide Modes as Eigenfunctions

A dielectric slab waveguide confines light by total internal reflection. The transverse field profile $E_y(x)$ satisfies the same eigenvalue equation as a quantum particle in a potential well:

$$-\frac{d^2 E_y}{dx^2} = (\beta^2 - n^2 k_0^2) E_y$$

Inside the slab ($|x| < d$), the field oscillates as $\cos(k_x x)$ or $\sin(k_x x)$. Outside, it decays exponentially — the evanescent tail. The discrete mode indices label the allowed solutions, just like quantum numbers.

![[Figures/maxwell_waveguide_modes.png]]
*Figure 4: Transverse electric field profiles $E_y(x)$ for the $\mathrm{TE}_0$, $\mathrm{TE}_1$, and $\mathrm{TE}_2$ modes of a dielectric slab waveguide, showing oscillatory cores and evanescent tails.*

The $\mathrm{TE}_0$ mode has no nodes, $\mathrm{TE}_1$ has one node, $\mathrm{TE}_2$ has two — exactly the pattern of the particle-in-a-box eigenfunctions $\sin(n\pi x/L)$ from [[The Schrodinger Equation]]. The evanescent tails are the optical analog of quantum tunneling: the field penetrates into the classically forbidden (lower-index) region.

## The Transfer Matrix

For multilayer systems, each interface and each propagation segment can be described by a $2 \times 2$ **transfer matrix** that connects the forward and backward field amplitudes:

$$\begin{pmatrix} E^+ \\ E^- \end{pmatrix}_{\text{out}} = M \begin{pmatrix} E^+ \\ E^- \end{pmatrix}_{\text{in}}$$

The total transfer matrix for a stack is the product $M = M_N \cdots M_2 \cdot M_1$. This is finite-dimensional [[Linear Algebra]] — the field amplitudes are a 2-component vector, and each layer is a linear operator acting on it.

![[Figures/maxwell_transfer_matrix.png]]
*Figure 5: Electric field amplitude through a multilayer dielectric stack, showing wavelength shortening in the higher-index layer and the forward/backward amplitudes connected by the transfer matrix.*

Inside the higher-index layer, the wavelength shortens (faster oscillation), just as a quantum particle's wavelength shortens in a region of lower potential. The transfer matrix $M$ encodes the Fresnel coefficients at each interface and the phase accumulated during propagation — it connects the amplitudes on one side to the amplitudes on the other.

This is directly analogous to quantum scattering: a particle hitting a potential barrier has transmission and reflection amplitudes given by the same $2 \times 2$ matrix structure.

## The Structural Analogy

The two eigenvalue problems side by side:

![[Figures/maxwell_schrodinger_analogy.png]]
*Figure 6: Side-by-side comparison of a quantum particle-in-a-box eigenfunction $\psi(x)$ with potential $V(x)$ and a dielectric waveguide mode $E_y(x)$ with refractive index profile $n(x)$.*

| | Quantum mechanics | Electromagnetics |
|---|---|---|
| Field | $\psi(x)$ | $E_y(x)$ |
| Operator | $-\frac{d^2}{dx^2} + V(x)$ | $-\frac{d^2}{dx^2} + n^2(x) k_0^2$ |
| Eigenvalue | Energy $E$ | $\beta^2$ (propagation constant) |
| Potential / profile | $V(x)$ | $n^2(x)$ |
| Bound states / guided modes | $E < V_{\infty}$ | $\beta > n_{\text{clad}} k_0$ |
| Tunneling / evanescent field | $\psi$ in classically forbidden region | $E_y$ in cladding |
| Discrete spectrum | Quantized $E_n$ | Discrete mode indices |

The physics is different — one is a probability amplitude, the other is an electric field. But the mathematics is identical: a second-order differential operator, boundary conditions selecting discrete eigenvalues, orthogonal eigenfunctions forming a complete basis.

This is why the tools of [[Hilbert Spaces]], [[Operators and Eigenvalues]], and [[Dirac Notation]] apply equally well to both. In photonics, you can expand an arbitrary field profile in guided modes:

$$E_y(x) = \sum_m a_m \, E_y^{(m)}(x) \quad \longleftrightarrow \quad |\psi\rangle = \sum_n c_n |n\rangle$$

The coefficients $a_m$ are found by projection (inner products), the modes are orthogonal, and completeness guarantees the expansion converges. The language is different, but the linear algebra is the same.

## Where to Go Next

- **Photonic crystals** — periodic $n(x)$ produces band structure, just as a periodic potential produces electronic bands. Bloch's theorem applies to both.
- **Coupled mode theory** — waveguide coupling described by $i\frac{d}{dz}|a\rangle = H|a\rangle$, formally identical to the Schrodinger equation with $z$ playing the role of time.
- **Quantum optics** — quantizing the EM field promotes each mode to a quantum harmonic oscillator. The mode expansion becomes $\hat{E} = \sum_k \hat{a}_k E_k(x) + \hat{a}_k^\dagger E_k^*(x)$, and [[Dirac Notation]] becomes essential.
- **Surface plasmon polaritons** — bound modes at metal-dielectric interfaces, with dispersion that crosses the light line.
- **Metamaterials and negative index** — engineered $\varepsilon(\omega)$ and $\mu(\omega)$ that produce exotic dispersion relations.
