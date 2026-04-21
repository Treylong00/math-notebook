In [[Helmholtz Equation]] we introduced a Green's function as the response of a bounded cavity to a point source, and wrote it as a sum over eigenmodes. That is one slice of a much bigger story: a Green's function is the **inverse of a linear operator**, and essentially every driven linear PDE in physics — Laplace, Helmholtz, the heat equation, the Schrödinger equation — is solved by convolving the source with the appropriate Green's function. This notebook develops that unifying picture, then derives the free-space Helmholtz Green's function in 1D, 2D, and 3D (with the $i\epsilon$ prescription that selects outgoing waves), and finally walks through three worked problems.

## The Operator Picture

The driven version of a linear PDE is a statement about an operator $\hat{L}$ and a source $|f\rangle$:

$$\hat{L}\,|\psi\rangle = -|f\rangle$$

If $\hat{L}$ is invertible, the solution is $|\psi\rangle = -\hat{L}^{-1}|f\rangle$. The **Green's function** is that inverse:

$$\hat{G} = -\hat{L}^{-1}, \qquad \hat{L}\hat{G} = -\hat{I}$$

In [[Dirac Notation]], the matrix element in the position basis is the familiar $G(\mathbf{r}, \mathbf{r}') = \langle \mathbf{r}|\hat{G}|\mathbf{r}'\rangle$. Sandwiching $\hat{L}\hat{G} = -\hat{I}$ between $\langle\mathbf{r}|$ and $|\mathbf{r}'\rangle$ recovers the defining equation

$$\hat{L}_\mathbf{r}\,G(\mathbf{r}, \mathbf{r}') = -\delta(\mathbf{r} - \mathbf{r}')$$

because $\langle \mathbf{r}|\hat{I}|\mathbf{r}'\rangle = \delta(\mathbf{r}-\mathbf{r}')$ is the completeness relation for the position basis from [[Dirac Notation]].

Once we know $\hat{G}$, the solution to any driven problem follows by inserting a completeness relation:

$$\psi(\mathbf{r}) = -\langle\mathbf{r}|\hat{L}^{-1}|f\rangle = \langle\mathbf{r}|\hat{G}|f\rangle = \int \langle\mathbf{r}|\hat{G}|\mathbf{r}'\rangle\langle\mathbf{r}'|f\rangle\,d\mathbf{r}' = \int G(\mathbf{r},\mathbf{r}')\,f(\mathbf{r}')\,d\mathbf{r}'$$

This is why Green's functions are so powerful: **superposition** turns the response to a point source into the response to anything. A complicated source is a sum of point sources, and linearity says the response is the sum of point responses.

### Spectral form: the resolvent

From [[Operators and Eigenvalues]], if $\hat{L}$ has an orthonormal eigenbasis $\{|n\rangle\}$ with eigenvalues $\lambda_n$, then $\hat{L} = \sum_n \lambda_n |n\rangle\langle n|$. Inverting mode by mode:

$$\hat{G} = -\hat{L}^{-1} = -\sum_n \frac{|n\rangle\langle n|}{\lambda_n}$$

This is called the **resolvent** of $\hat{L}$. It makes the pole structure obvious: wherever an eigenvalue passes through zero, the Green's function blows up. Physically, that is **resonance** — the driving term lines up with a free mode and the response diverges.

In the position representation,

$$G(\mathbf{r}, \mathbf{r}') = -\sum_n \frac{\langle\mathbf{r}|n\rangle\langle n|\mathbf{r}'\rangle}{\lambda_n} = -\sum_n \frac{\phi_n(\mathbf{r})\,\phi_n^*(\mathbf{r}')}{\lambda_n}$$

which is exactly the bounded-cavity formula from [[Helmholtz Equation]], with $\lambda_n = k_{mn}^2 - k^2$.

### The same pattern across the notebook

The $\hat{G} = -\hat{L}^{-1}$ pattern is the glue connecting problems that look very different:

| Equation | Operator $\hat{L}$ | Green's function problem |
| --- | --- | --- |
| Laplace (electrostatics) | $\nabla^2$ | $\nabla^2 G = -\delta(\mathbf{r}-\mathbf{r}')$ |
| Helmholtz (waves) | $\nabla^2 + k^2$ | $(\nabla^2 + k^2) G = -\delta(\mathbf{r}-\mathbf{r}')$ |
| Heat equation | $\partial_t - D\nabla^2$ | $(\partial_t - D\nabla^2) G = \delta(t)\delta(\mathbf{r})$ |
| Schrödinger (propagator) | $i\hbar\partial_t - \hat{H}$ | $(i\hbar\partial_t - \hat{H}) G = i\hbar\,\delta(t)\delta(\mathbf{r}-\mathbf{r}')$ |

The operators differ, but the logic — invert the operator, insert a completeness relation, convolve with the source — is identical. For the Schrödinger case, $\hat{G}$ is the [[The Schrodinger Equation|quantum propagator]] $\hat{U}(t) = e^{-i\hat{H}t/\hbar}$ for $t > 0$, and the [[Dirac Notation]] statement $|\psi(t)\rangle = \hat{U}(t)|\psi(0)\rangle$ is a Green's-function convolution in disguise.

## Free-Space Helmholtz Green's Function

On an unbounded domain the spectrum of $\hat{L} = \nabla^2$ is continuous, and the eigenbasis is the plane waves $|\mathbf{k}\rangle$ from [[Helmholtz Equation#Free-Space Eigenstates|Free-Space Eigenstates]]. The eigenvalue of $\hat{L}$ on $|\mathbf{k}\rangle$ is $-|\mathbf{k}|^2$, so $(\hat{L} + k^2)$ has eigenvalue $k^2 - |\mathbf{k}|^2$. The resolvent in the position basis is then

$$G(\mathbf{r}, \mathbf{r}') = \int \frac{\langle\mathbf{r}|\mathbf{k}'\rangle\langle\mathbf{k}'|\mathbf{r}'\rangle}{k^2 - |\mathbf{k}'|^2}\,d^d k' = \int \frac{d^d k'}{(2\pi)^d}\,\frac{e^{i\mathbf{k}'\cdot(\mathbf{r}-\mathbf{r}')}}{k^2 - |\mathbf{k}'|^2}$$

which is just the Fourier transform of $1/(k^2 - |\mathbf{k}'|^2)$ — except that the denominator vanishes on the sphere $|\mathbf{k}'| = k$. The integral is ill-defined until we say how to go around those poles.

### The $i\epsilon$ prescription

Replace $k$ with $k + i\epsilon$ for infinitesimal $\epsilon > 0$. This pushes the poles slightly off the real $|\mathbf{k}'|$-axis, the integral becomes well-defined, and at the end we take $\epsilon \to 0^+$. The choice of sign selects the boundary condition at infinity.

In 1D the integral reduces to a contour integral closable in the upper or lower half-plane. With $k \to k + i\epsilon$, the pole at $+(k+i\epsilon)$ lies in the upper half-plane and the one at $-(k+i\epsilon)$ in the lower. Closing in the direction dictated by the sign of $x - x'$ gives

$$G_R(x, x') = \frac{i}{2k}\,e^{ik|x - x'|}$$

This is the **retarded** (outgoing) Green's function: it radiates away from the source. Swapping $\epsilon \to -\epsilon$ gives the **advanced** (incoming) Green's function $G_A = G_R^*$, which corresponds to waves converging on the source — mathematically valid, physically unusual. Their half-sum is the **principal-value** solution, which is a pure standing wave.

![[Figures/greens_iepsilon.png]]
*Figure 1: The three choices of $i\epsilon$ prescription in 1D. Retarded ($k \to k+i\epsilon$) gives outgoing waves on both sides of the source. Advanced ($k \to k-i\epsilon$) gives incoming waves. The principal value gives a standing wave with no net energy flow — $\mathrm{Im}\,G = 0$. Arrows indicate the direction of phase propagation.*

Physically the retarded choice is the one you almost always want: a point source turned on at $\mathbf{r}'$ radiates outward, not inward. The $i\epsilon$ sits in the same family of regularizations as the small imaginary part added to $k^2$ in a [[Complex Permittivity|lossy medium]] — a little bit of damping, deformed to a limit, that picks out causality.

### Dimensional dependence

Performing the angular integrals explicitly gives closed forms that depend sharply on dimension:

$$G_0^{(1)}(x, x') = \frac{i\,e^{ik|x-x'|}}{2k}, \qquad G_0^{(2)}(\mathbf{r}, \mathbf{r}') = -\frac{i}{4}\,H_0^{(1)}(k|\mathbf{r}-\mathbf{r}'|), \qquad G_0^{(3)}(\mathbf{r}, \mathbf{r}') = \frac{e^{ik|\mathbf{r}-\mathbf{r}'|}}{4\pi|\mathbf{r}-\mathbf{r}'|}$$

where $H_0^{(1)}$ is the Hankel function of the first kind — the 2D analog of an outgoing spherical wave. The three fall off very differently at large $r$:

- **1D:** $|G| = 1/(2k)$, constant — a plane wave never weakens
- **2D:** $|G| \sim 1/\sqrt{kr}$ — cylindrical waves spread in a line
- **3D:** $|G| \sim 1/(4\pi r)$ — spherical waves spread over a growing sphere

![[Figures/greens_free_space_dims.png]]
*Figure 2: Free-space Helmholtz Green's functions for $k=2$. In 1D the amplitude is constant (waves never thin out); in 2D the Hankel function diverges logarithmically at the origin and decays as $1/\sqrt{r}$ (note the slow modulation of the envelope); in 3D the familiar $1/r$ spherical wave is the standard textbook form. In every case $\mathrm{Re}\,G$ and $\mathrm{Im}\,G$ are $\pi/2$ out of phase — the signature of an outgoing travelling wave.*

The $1/r$ in 3D is the spherical Coulomb-like fall-off, but modulated by a wave phase $e^{ikr}$. Setting $k=0$ collapses the phase to $1$ and leaves just $1/(4\pi r)$ — the electrostatic Coulomb potential. That is the next worked problem.

## Worked Problem 1: Laplace, Coulomb, and the Static Limit

The Laplace Green's function is the $k \to 0$ limit of the Helmholtz one. In 3D,

$$G_L^{(3)}(\mathbf{r}, \mathbf{r}') = \frac{1}{4\pi\,|\mathbf{r}-\mathbf{r}'|}$$

which is the Coulomb potential of a unit point charge (in Gaussian-style units where $-\nabla^2 V = \rho$). In 2D the $k\to 0$ limit is singular and the right Green's function is logarithmic:

$$G_L^{(2)}(\mathbf{r}, \mathbf{r}') = -\frac{1}{2\pi}\ln|\mathbf{r}-\mathbf{r}'|$$

In [[Dirac Notation]] these are matrix elements of $\hat{G}_L = -(\nabla^2)^{-1}$. The potential of any charge distribution is then the convolution

$$V(\mathbf{r}) = \langle\mathbf{r}|\hat{G}_L|\rho\rangle = \int G_L(\mathbf{r},\mathbf{r}')\,\rho(\mathbf{r}')\,d\mathbf{r}'$$

![[Figures/greens_coulomb_convolution.png]]
*Figure 3: Solving $-\nabla^2 V = \rho$ in 2D by convolution with the Laplace Green's function. Left: a Gaussian charge distribution. Middle: the logarithmic Green's function centered on the origin. Right: the resulting potential $V = G_L * \rho$ — a smoothed well whose shape far from the source approaches the pure $-\ln r /(2\pi)$ behavior of a point charge.*

Two things to notice. First, the potential is far smoother than the source — convolution with $-\ln r$ smears sharp features. Second, outside the charge distribution the potential agrees with the point-charge potential; this is a visual version of the shell theorem / Gauss's law. The machinery is the same in 3D with $-\ln r /(2\pi)$ replaced by $1/(4\pi r)$.

## Worked Problem 2: Driven Cavity and the Resolvent Pole

Return to the bounded cavity from [[Helmholtz Equation]]. The resolvent form

$$G(\mathbf{r},\mathbf{r}') = -\sum_{m,n}\frac{\phi_{mn}(\mathbf{r})\,\phi_{mn}^*(\mathbf{r}')}{k_{mn}^2 - k^2}$$

tells us immediately what happens when we drive the cavity at a frequency $\omega = ck$: each mode's contribution is inversely proportional to the detuning $k_{mn}^2 - k^2$. Tune $k$ near an eigenvalue $k_{mn}$ and that mode dominates — its weight diverges like $1/(k_{mn}^2 - k^2)$. This is resonance, and the spectral form of the Green's function makes it transparent: resonances are poles of the resolvent.

In a real physical system loss regularizes the pole. Replacing $k^2 \to k^2 + i\gamma$ (with $\gamma > 0$) shifts each denominator to $k_{mn}^2 - k^2 - i\gamma$. The magnitude on resonance is now $1/\gamma$ rather than $\infty$, and the width of the peak in $k$ is $\sim \gamma / (2k_{mn})$. This is the same kind of regularization as the $i\epsilon$ in free space, and it is where the imaginary parts of [[Complex Permittivity|complex permittivity]] do their work: damping converts a diverging cavity response into a Lorentzian line.

Figure 4 of [[Helmholtz Equation]] already visualizes the mode-by-mode reconstruction of the Green's function in a rectangular cavity — that image is precisely the convergence of the truncated resolvent sum to the delta function.

## Worked Problem 3: 1D Scattering from a Delta Potential

Scattering is the cleanest illustration of why Green's functions matter. Consider the 1D Schrödinger-like equation with $\hbar = 2m = 1$:

$$(\partial_x^2 + k^2)\,\psi(x) = 2\alpha\,\delta(x)\,\psi(x)$$

with an incoming plane wave $\psi_{\text{in}}(x) = e^{ikx}$ coming from the left. The full state is the incident wave plus the response to the "source" $2\alpha\delta(x)\psi$:

$$\psi(x) = \psi_{\text{in}}(x) - \int G_0^{(1)}(x, x')\,2\alpha\,\delta(x')\,\psi(x')\,dx' = \psi_{\text{in}}(x) - 2\alpha\,G_0^{(1)}(x, 0)\,\psi(0)$$

This is the **Lippmann-Schwinger equation** — the self-consistent statement that the scattered field is generated by the potential acting on the total field. In [[Dirac Notation]] it reads $|\psi\rangle = |\psi_{\text{in}}\rangle - \hat{G}_0\,\hat{V}\,|\psi\rangle$, where $\hat{V}$ is the (operator form of the) potential and $\hat{G}_0$ is the free-space resolvent.

For a delta potential the equation collapses to a single algebraic condition at $x=0$. Using $G_0^{(1)}(0,0) = i/(2k)$,

$$\psi(0) = 1 - 2\alpha\,\frac{i}{2k}\,\psi(0) \quad\Rightarrow\quad \psi(0) = \frac{k}{k + i\alpha}$$

Substituting back gives the full wavefunction, which splits naturally into incident + reflected on the left and transmitted on the right:

$$\psi(x) = \begin{cases} e^{ikx} + r\,e^{-ikx}, & x < 0 \\ t\,e^{ikx}, & x > 0 \end{cases}, \qquad r = -\frac{i\alpha}{k + i\alpha},\quad t = \frac{k}{k + i\alpha}$$

with $|r|^2 + |t|^2 = 1$ (probability conservation — a direct consequence of the unitarity of the underlying Hamiltonian from [[Operators and Eigenvalues]]).

![[Figures/greens_delta_scattering.png]]
*Figure 4: Scattering off $V(x) = \alpha\delta(x)$ for three barrier strengths. Left: the real part of $\psi(x)$ — on the right, a pure travelling wave $t\,e^{ikx}$; on the left, the interference of incident and reflected waves produces a partial standing pattern. Right: the probability density $|\psi|^2$ — flat and equal to 1 for $\alpha=0$ (nothing to reflect), oscillating between $(1-|r|)^2$ and $(1+|r|)^2$ on the left for $\alpha>0$, and the constant $|t|^2 < 1$ on the right. As $\alpha$ grows, reflection wins and transmission falls.*

Nothing about this derivation depended on the potential being a delta — that was just what made the integral trivial. For a general potential $V(x)$ the Lippmann-Schwinger equation $|\psi\rangle = |\psi_{\text{in}}\rangle - \hat{G}_0 \hat{V}|\psi\rangle$ is still exact; solving it iteratively gives the Born series

$$|\psi\rangle = |\psi_{\text{in}}\rangle - \hat{G}_0\hat{V}|\psi_{\text{in}}\rangle + \hat{G}_0\hat{V}\hat{G}_0\hat{V}|\psi_{\text{in}}\rangle - \cdots$$

each term being one more scattering event. The first-order truncation — the **Born approximation** — is the workhorse of scattering theory, from neutron diffraction to optical imaging to particle physics.

## Where to Go Next

- **Scattering theory** — cross sections, partial waves, and the optical theorem are all statements about matrix elements of $\hat{G}_0$ and $\hat{V}$.
- **Retarded Green's functions in time** — the time-domain version $G(\mathbf{r}, t; \mathbf{r}', t')$ encodes causality through $\theta(t-t')$, and its Fourier transform in $t$ returns the frequency-domain Green's functions of this page.
- **Quantum field theory** — propagators are Green's functions of operator-valued fields; Feynman diagrams are graphical rules for the Born series.
- **[[The Schrodinger Equation|Quantum propagator]]** — the evolution operator $\hat{U}(t) = e^{-i\hat{H}t/\hbar}$ is the Green's function of the time-dependent Schrödinger equation; its matrix element $\langle x|\hat{U}(t)|x'\rangle$ is the path integral kernel.
- **Boundary-value problems** — with Dirichlet or Neumann data on a surface, the Green's function picks up image charges and the method of images becomes a systematic technique.
