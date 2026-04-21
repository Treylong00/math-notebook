In an isotropic material, the permittivity is a single number — light behaves the same in every direction. In an anisotropic material, the permittivity depends on the polarization direction, and we need a tensor. When that tensor has eigenvalues of opposite sign, the isofrequency surface opens from a closed ellipse into an open hyperbola, and the material supports **hyperbolic modes** with fundamentally different physics.

This notebook develops that story using the operator language from [[Dirac Notation]] and connects to the dispersion and mode concepts from [[Maxwells Equations]] and [[Complex Permittivity]].

## The Permittivity Tensor as an Operator

In an anisotropic medium, the constitutive relation is $\mathbf{D} = \varepsilon_0 \hat{\varepsilon} \mathbf{E}$, where $\hat{\varepsilon}$ is a tensor. In the principal axis frame, it is diagonal:

$$\hat{\varepsilon} = \begin{pmatrix} \varepsilon_x & 0 & 0 \\ 0 & \varepsilon_y & 0 \\ 0 & 0 & \varepsilon_z \end{pmatrix}$$

In [[Dirac Notation]], this is a sum of projectors weighted by the principal permittivities:

$$\hat{\varepsilon} = \varepsilon_x |x\rangle\langle x| + \varepsilon_y |y\rangle\langle y| + \varepsilon_z |z\rangle\langle z|$$

The crystal axes $|x\rangle, |y\rangle, |z\rangle$ are the eigenstates, and the permittivity values are the eigenvalues. The operator $\hat{\varepsilon}$ acts on a polarization state $|\mathbf{E}\rangle$ by scaling each component independently.

![[Figures/aniso_tensor_operator.png]]
*Figure 1: Action of the permittivity tensor on an input polarization vector for the isotropic, elliptic, and hyperbolic cases.*

In the isotropic case, the tensor scales all polarizations equally — the output vector is parallel to the input. In the elliptic case, different components are scaled by different amounts — the output rotates relative to the input. In the hyperbolic case, one eigenvalue is negative: the $z$-component of $\mathbf{D}$ points **opposite** to $\mathbf{E}$. This sign flip is what produces hyperbolic dispersion.

## The Dispersion Relation

For a plane wave $\mathbf{E} \propto e^{i\mathbf{k}\cdot\mathbf{r}}$ in a uniaxial medium ($\varepsilon_x = \varepsilon_y = \varepsilon_\perp$, optic axis along $z$), the wave equation from [[Maxwells Equations]] gives the extraordinary-wave dispersion relation:

$$\frac{k_x^2 + k_y^2}{\varepsilon_z} + \frac{k_z^2}{\varepsilon_\perp} = \frac{\omega^2}{c^2}$$

At a fixed frequency, this defines the **isofrequency surface** — the set of all allowed wavevectors $\mathbf{k}$. The shape depends entirely on the signs of $\varepsilon_\perp$ and $\varepsilon_z$.

## Isofrequency Contours

![[Figures/aniso_isofrequency.png]]
*Figure 2: Isofrequency contours in the $(k_x, k_z)$ plane for the isotropic, elliptic, and hyperbolic cases.*

When both permittivities are positive and equal, the isofrequency contour is a circle — all propagation directions see the same refractive index. When they differ but remain positive, the circle stretches into an ellipse — light propagates faster along some directions than others. This is ordinary birefringence.

When one permittivity goes negative, the contour opens into a **hyperbola**. The isofrequency surface is no longer bounded — wavevectors of arbitrarily large magnitude are allowed. This is fundamentally different from any isotropic material, where the maximum $|\mathbf{k}|$ is fixed by the refractive index.

## Type I vs Type II

There are two ways to get a hyperbolic medium, depending on which component is negative:

$$\text{Type I:} \quad \varepsilon_\perp > 0, \quad \varepsilon_z < 0$$
$$\text{Type II:} \quad \varepsilon_\perp < 0, \quad \varepsilon_z > 0$$

![[Figures/aniso_hyperbolic_types.png]]
*Figure 3: Isofrequency contours for Type I ($\varepsilon_\perp > 0$, $\varepsilon_z < 0$) and Type II ($\varepsilon_\perp < 0$, $\varepsilon_z > 0$) hyperbolic media with asymptotes.*

The two types produce hyperbolae that open in perpendicular directions. Type I opens along $k_x$ — large transverse wavevectors are allowed. Type II opens along $k_z$ — large longitudinal wavevectors are allowed. The white dotted lines are the asymptotes, set by the ratio $\sqrt{|\varepsilon_\perp / \varepsilon_z|}$.

In the Dirac picture, the difference is which eigenvalue of $\hat{\varepsilon}$ is negative — which component of the polarization has its displacement reversed relative to the field.

## Mode Index Surface

The refractive index that a wave experiences depends on its propagation direction. For a uniaxial medium, the extraordinary index is:

$$\frac{1}{n_e^2(\theta)} = \frac{\cos^2\theta}{\varepsilon_\perp} + \frac{\sin^2\theta}{\varepsilon_z}$$

where $\theta$ is the angle from the optic axis. In polar coordinates, $n(\theta)$ traces out the **index surface**.

![[Figures/aniso_mode_index.png]]
*Figure 4: Polar plots of the ordinary and extraordinary refractive index surfaces for the isotropic, elliptic, and hyperbolic cases.*

For the isotropic case, the ordinary and extraordinary surfaces coincide — a circle. For the elliptic case, the extraordinary surface is an ellipse inside or outside the ordinary circle. For the hyperbolic case, the extraordinary surface diverges at certain angles — those are the directions where $n_e^2 \to \infty$, corresponding to waves that propagate with vanishing phase velocity. At other angles, $n_e^2$ goes negative and no extraordinary mode exists (the gaps in the plot).

## The Elliptic-to-Hyperbolic Transition

As $\varepsilon_z$ sweeps from positive to negative, the isofrequency contour continuously deforms from a closed ellipse to an open hyperbola:

![[Figures/aniso_isofrequency_transition.png]]
*Figure 5: Isofrequency contours as $\varepsilon_z$ sweeps from positive through zero to negative, showing the elliptic-to-hyperbolic topological transition.*

![[Figures/anim_isofrequency_transition.gif]]
*Animation 1: The isofrequency contour continuously deforming from a closed ellipse to an open hyperbola as $\varepsilon_z$ sweeps from positive to negative.*

The transition happens at $\varepsilon_z = 0$, where the contour degenerates — the ellipse opens up and the two branches of the hyperbola emerge. This is an **topological** transition: a closed surface becomes an open one. In the operator picture, this is where one eigenvalue of $\hat{\varepsilon}$ crosses zero, and the operator changes from positive definite (all eigenvalues positive) to indefinite (mixed signs).

## The Operator Perspective

The full wave equation in an anisotropic medium is an eigenvalue problem:

$$\hat{\Theta} |\mathbf{H}\rangle = \frac{\omega^2}{c^2} |\mathbf{H}\rangle, \qquad \hat{\Theta} = \nabla \times \left(\hat{\varepsilon}^{-1} \nabla \times \right)$$

The operator $\hat{\Theta}$ is Hermitian for lossless media, so all the machinery of [[Operators and Eigenvalues]] applies: real eigenvalues, orthogonal eigenmodes, completeness. The modes of the hyperbolic medium are eigenstates of $\hat{\Theta}$, and an arbitrary field can be expanded in these modes:
<!--We haven't covered what Hermitian means. How does the machinery change for lossy media?-->

$$|\mathbf{E}\rangle = \sum_\sigma \int c_\sigma(\mathbf{k}) \, |\mathbf{k}, \sigma\rangle \, d\mathbf{k}$$

where $\sigma = o, e$ labels the two eigenpolarizations (ordinary and extraordinary). The inner product $c_\sigma(\mathbf{k}) = \langle \mathbf{k}, \sigma | \mathbf{E} \rangle$ gives the amplitude of each mode — exactly the same structure as the quantum expansion $|\psi\rangle = \sum_n c_n |n\rangle$ from [[Hilbert Spaces]].

What makes hyperbolic media special is not that the formalism breaks down — it doesn't — but that the indefiniteness of $\hat{\varepsilon}$ changes the character of the solutions. The unbounded isofrequency surface means an infinite density of electromagnetic states, sub-wavelength imaging becomes possible, and the Purcell factor (spontaneous emission rate) diverges. The linear algebra is the same; the physics is exotic.

## Phonon Polariton Dispersion

So far we have treated $\varepsilon$ as a fixed number. But in a real polar crystal, $\varepsilon(\omega)$ is frequency-dependent — it follows the [[Complex Permittivity|Lorentz oscillator]] model for phonon resonances:

$$\varepsilon_z(\omega) = \varepsilon_\infty \frac{\omega_{LO}^2 - \omega^2 - i\gamma\omega}{\omega_{TO}^2 - \omega^2 - i\gamma\omega}$$

Between the transverse optical ($\omega_{TO}$) and longitudinal optical ($\omega_{LO}$) phonon frequencies lies the **Reststrahlen band**, where $\varepsilon_z < 0$. If the transverse permittivity $\varepsilon_\perp$ remains positive in this range, the medium is hyperbolic — but only within a specific frequency window.

![[Figures/aniso_phonon_polariton.png]]
*Figure 6: Phonon-polariton permittivity $\varepsilon_z(\omega)$ with the Reststrahlen band and the corresponding extraordinary-wave dispersion relation $\omega(\mathbf{k})$ showing hyperbolic branches.*

The left panel shows $\varepsilon_z(\omega)$: positive outside the Reststrahlen band, negative inside it. The right panel shows the dispersion $\omega(\mathbf{k})$. Outside the Reststrahlen band, the extraordinary wave follows a light-line-like dispersion — an ordinary polariton. Inside the band, $\varepsilon_z < 0$ opens hyperbolic branches: for each fixed $k_z$, the dispersion curve allows arbitrarily large $k_x$. These are **hyperbolic phonon polaritons**.

The connection to isofrequency contours is direct. A horizontal slice through the dispersion diagram at a fixed $\omega$ inside the Reststrahlen band recovers the hyperbolic isofrequency contour at that frequency. A slice outside the band gives an elliptic contour. The dispersion diagram and the isofrequency contour are two cuts through the same three-dimensional surface in $(\mathbf{k}, \omega)$ space.

## Biaxial Materials: MoO$_3$

Everything above assumed uniaxial symmetry: $\varepsilon_x = \varepsilon_y \neq \varepsilon_z$. But nature provides **biaxial** crystals where all three principal permittivities are different. The permittivity tensor is:

$$\hat{\varepsilon}(\omega) = \varepsilon_x(\omega)\, |x\rangle\langle x| + \varepsilon_y(\omega)\, |y\rangle\langle y| + \varepsilon_z(\omega)\, |z\rangle\langle z|$$

If each axis has its own phonon resonance at a different frequency, each $\varepsilon_i(\omega)$ has its own Reststrahlen band. The sign pattern of the tensor — which eigenvalues are positive and which are negative — changes as $\omega$ sweeps through these bands.

Molybdenum trioxide (MoO$_3$) is a van der Waals crystal with three distinct phonon resonances along its three crystal axes:

![[Figures/aniso_moo3_permittivity.png]]
*Figure 7: Frequency-dependent permittivity components $\varepsilon_x$, $\varepsilon_y$, and $\varepsilon_z$ of MoO$_3$ showing three distinct Reststrahlen bands along each crystal axis.*

The three Reststrahlen bands overlap in a complicated pattern. At any given frequency, zero, one, two, or all three components can be negative. This creates multiple spectral windows with different dispersion topologies — and crucially, the **in-plane** permittivities $\varepsilon_x$ and $\varepsilon_y$ are themselves different, so the isofrequency contours break rotational symmetry even within the crystal surface.

## Biaxial Isofrequency Contours

For in-plane propagation ($k_z = 0$) in a biaxial medium, the dispersion relation becomes:

$$\frac{k_x^2}{\varepsilon_y(\omega)} + \frac{k_y^2}{\varepsilon_x(\omega)} = \frac{\omega^2}{c^2}$$

The shape of the isofrequency contour now depends on the signs of both $\varepsilon_x$ and $\varepsilon_y$ at the chosen frequency:

![[Figures/aniso_moo3_isofrequency.png]]
*Figure 8: In-plane isofrequency contours of MoO$_3$ at selected frequencies showing elliptic, hyperbolic, and forbidden regimes set by the signs of $\varepsilon_x$ and $\varepsilon_y$.*

![[Figures/anim_moo3_isofrequency.gif]]
*Animation 2: MoO$_3$ in-plane isofrequency contour sweeping through frequency, showing topology changes across Reststrahlen bands.*

Below the first Reststrahlen band, both in-plane permittivities are positive and the contour is an ellipse. As $\omega$ enters a band where one component goes negative, the contour opens into a **hyperbola** — but now with a preferred in-plane direction, not the rotationally symmetric hyperbola of the uniaxial case. At frequencies where both are negative, no in-plane propagation is allowed. At other frequencies, the roles swap and the hyperbola opens along the perpendicular direction.

This is the key feature of biaxial hyperbolic materials: the hyperbolic dispersion is **directional within the surface plane**. In MoO$_3$, phonon polaritons launched along the $[100]$ direction can behave completely differently from those along $[010]$ — not just in magnitude (birefringence), but in their fundamental topology (elliptic vs. hyperbolic). This in-plane anisotropy has no analogue in uniaxial systems.

## Where to Go Next

- **Hyperbolic metamaterials** — metal-dielectric multilayers and nanowire arrays that engineer the effective $\hat{\varepsilon}$ to be hyperbolic at desired frequencies.
- **Sub-wavelength imaging** — the hyperbolic dispersion allows propagation of evanescent waves that would decay in ordinary media, enabling super-resolution.
- **Photonic density of states** — the open isofrequency surface means a divergent (in the ideal case) local density of states, with consequences for spontaneous emission and thermal radiation. <!--Definitely want a page on this -->
- **Topological photonics** — the elliptic-to-hyperbolic transition is a topological phase transition in $\mathbf{k}$-space, with analogies to electronic topological transitions. <!-- This seems cool. Would like a page and maybe a reference to some interesting articles on this or keywords to search for. -->
- **Canalization and directional propagation** — in biaxial hyperbolic media like MoO$_3$, the flat portions of the isofrequency contour concentrate energy into narrow angular channels, enabling ray-like propagation of polaritons at specific angles set by the crystal structure.
