The permittivity $\varepsilon$ describes how a material responds to an electric field. In general it is a complex, frequency-dependent quantity:

$$\tilde{\varepsilon}(\omega) = \varepsilon'(\omega) + i\varepsilon''(\omega)$$

The real part $\varepsilon'$ governs how much the field is stored (polarization), while the imaginary part $\varepsilon''$ governs how much is absorbed (loss). Since $\tilde{\varepsilon}$ is a [[Complex Numbers|complex number]], we can also express it in polar form — $|\tilde{\varepsilon}|$ and $\arg(\tilde{\varepsilon})$ — which often reveals structure that the Cartesian decomposition hides.

## Three Models of Permittivity

We examine three canonical models, each capturing a different physical regime:

**Non-resonant dielectric** — a material far from any resonance (e.g., glass in the visible):

$$\tilde{\varepsilon}(\omega) = \varepsilon_\infty$$

Constant and purely real. No dispersion, no absorption. This is the idealization underlying Snell's law and simple optics.

**Drude model** — free-electron response (metals, doped semiconductors):

$$\tilde{\varepsilon}(\omega) = \varepsilon_\infty - \frac{\omega_p^2}{\omega^2 + i\gamma\omega}$$

The plasma frequency $\omega_p$ sets the scale. Below $\omega_p$, $\varepsilon' < 0$ — the material is metallic and reflects. Above $\omega_p$, $\varepsilon' > 0$ — it becomes transparent. The damping $\gamma$ controls how lossy the metal is.

**Lorentz oscillator** — bound-charge resonance (phonons, excitons):

$$\tilde{\varepsilon}(\omega) = \varepsilon_\infty + \frac{\omega_p^2}{\omega_0^2 - \omega^2 - i\gamma\omega}$$

A resonance at $\omega_0$. Near resonance, $\varepsilon'$ swings through zero (anomalous dispersion) and $\varepsilon''$ peaks (maximum absorption). This is the classical model for any bound oscillator.

## Real and Imaginary Parts

The most direct view: $\varepsilon'$ and $\varepsilon''$ plotted against frequency.

![[Figures/permittivity_components.png]]
*Figure 1: Real and imaginary parts of the permittivity versus frequency for the non-resonant, Drude, and Lorentz models.*

The non-resonant dielectric is a flat line — no frequency dependence at all. The Drude model shows $\varepsilon'$ crossing zero at the plasma frequency, transitioning from metallic ($\varepsilon' < 0$) to dielectric ($\varepsilon' > 0$), with $\varepsilon''$ peaking at low frequencies where free-electron damping is strongest. The Lorentz oscillator shows the classic resonance shape: $\varepsilon'$ has an S-shaped curve through the resonance (anomalous dispersion), and $\varepsilon''$ has a sharp absorption peak centered at $\omega_0$.

## Modulus and Argument

The same information expressed in polar form: $|\tilde{\varepsilon}|$ tells you the overall strength of the response, and $\arg(\tilde{\varepsilon})$ tells you the phase lag between the polarization and the applied field.

![[Figures/permittivity_mod_arg.png]]
*Figure 2: Modulus and argument of the complex permittivity versus frequency for the non-resonant, Drude, and Lorentz models.*

The modulus view makes the resonance structure clear. For the Drude model, $|\tilde{\varepsilon}|$ diverges at low frequency — the metal response becomes arbitrarily strong as $\omega \to 0$. For the Lorentz model, $|\tilde{\varepsilon}|$ peaks at the resonance.

The argument is perhaps more revealing. A purely real, positive $\varepsilon$ has $\arg = 0$ — no phase lag. A purely real, negative $\varepsilon$ has $\arg = \pm\pi$ — the polarization is exactly out of phase with the field. A lossy material falls somewhere in between. The Drude model shows a smooth transition from $\arg \approx -\pi$ (metallic, low $\omega$) toward $0$ (transparent, high $\omega$). The Lorentz model sweeps through a rapid phase change at resonance.

## Trajectories in the Complex Plane

Instead of plotting $\varepsilon'$ and $\varepsilon''$ separately against frequency, we can trace the path of $\tilde{\varepsilon}(\omega)$ as a point moving through the complex $(\varepsilon', \varepsilon'')$ plane as $\omega$ increases. The color encodes frequency.

![[Figures/permittivity_complex_plane.png]]
*Figure 3: Frequency-parameterized trajectories of the complex permittivity in the $(\varepsilon', \varepsilon'')$ plane for the non-resonant, Drude, and Lorentz models.*

![[Figures/anim_permittivity_trajectory.gif]]
*Animation 1: The Lorentz permittivity $\tilde{\varepsilon}(\omega)$ tracing its trajectory through the complex plane as frequency increases.*

The non-resonant model is trivially a single point on the real axis. The Drude model sweeps in from large negative $\varepsilon'$ (metallic, low $\omega$) through the lower half-plane, curving back toward $\varepsilon_\infty$ on the real axis at high frequency. The Lorentz model traces a loop: starting at $\varepsilon_\infty + \omega_p^2/\omega_0^2$ on the real axis (low $\omega$), swinging down into the lower half-plane at resonance (absorption), and returning to $\varepsilon_\infty$ at high frequency.

<!-- This is a pretty shitty way to visualize the complex permittivity on the complex plane. Although, it is interesting that the Lorentzian form of the permittivity traces out a circle. Would be nice if the first and second plots wouldn't collapse due to the data set. -->

These trajectories connect directly to the complex analysis from [[Complex Numbers]]: the modulus $|\tilde{\varepsilon}|$ is the distance from the origin, the argument $\arg(\tilde{\varepsilon})$ is the angle, and the resonance corresponds to the trajectory sweeping closest to (or through) the origin.

## The Effect of Damping

The damping parameter $\gamma$ controls the width of resonance features. The contour plots below show $|\tilde{\varepsilon}|$ and $\arg(\tilde{\varepsilon})$ over the full $(\omega, \gamma)$ parameter space.

![[Figures/permittivity_contour.png]]
*Figure 4: Contour maps of $|\tilde{\varepsilon}|$ and $\arg(\tilde{\varepsilon})$ over the $(\omega, \gamma)$ parameter space for each permittivity model.*

The non-resonant model is completely flat — no dependence on $\gamma$, confirming it has no dissipative mechanism. The Drude and Lorentz models show how increasing $\gamma$ broadens and smears the resonance features. In the modulus plots, the sharp peaks (Drude at low $\omega$, Lorentz near $\omega_0$) spread and flatten with increasing damping. In the argument plots, the sharp phase transitions soften — a lossier material has a more gradual transition between dielectric and metallic behavior.

This is directly analogous to how the branch cuts and pole structures in [[Complex Numbers]] behave: a pole on the real axis produces a sharp feature, and moving the pole off the real axis (adding an imaginary part to the frequency — which is what damping does) smooths the singularity into a broad resonance.

## Where to Go Next

- **Kramers-Kronig relations** — $\varepsilon'$ and $\varepsilon''$ are not independent. Causality constrains them: knowing one over all frequencies determines the other. This is a consequence of analyticity in the upper half of the complex frequency plane.
- **Drude-Lorentz combinations** — real materials have multiple resonances. The total permittivity is a sum of Lorentz oscillators plus a Drude term: $\tilde{\varepsilon} = \varepsilon_\infty - \omega_p^2/(\omega^2 + i\gamma\omega) + \sum_j S_j/(\omega_j^2 - \omega^2 - i\gamma_j\omega)$.
- **Surface polaritons** — at interfaces where $\varepsilon' < 0$ on one side and $\varepsilon' > 0$ on the other, bound surface waves can propagate. The Drude model's negative $\varepsilon'$ region is exactly where surface plasmon polaritons live. See [[Maxwells Equations]].
- **Anisotropic permittivity** — in crystals, $\varepsilon$ becomes a tensor. Different crystal axes can have different resonance frequencies, leading to birefringence and optical activity.
