# Log

Append-only chronological record of notebook activity. One entry per meaningful change: new notebook, new section, figure regen, refactor, lint pass. Entry prefix: `## [YYYY-MM-DD] <kind> | <title>` so the log stays greppable (`grep "^## \[" LOG.md | tail`).

Kinds: `ingest` (new material), `edit` (revision), `figure` (new/regenerated figure), `lint` (health check), `meta` (index/schema changes).

## [2026-04-20] ingest | New notebook: Greens Functions

Created [[Greens Functions]] covering three threads: the operator/resolvent unifying picture ($\hat G = -\hat L^{-1}$) in [[Dirac Notation]], the free-space Helmholtz Green's function in 1D/2D/3D with the $i\epsilon$ prescription, and three worked problems (Laplace/Coulomb convolution in 2D, driven cavity resonance pole, 1D delta-potential scattering via Lippmann-Schwinger). New script `Scripts/greens_functions.py` generates 4 figures: `greens_free_space_dims`, `greens_iepsilon`, `greens_coulomb_convolution`, `greens_delta_scattering`. Added entry to [[INDEX]], linked from [[Helmholtz Equation]] "Where to Go Next".

## [2026-04-20] edit | Helmholtz Equation — expanded ⟨r|k⟩ derivation

Resolved the third `<!-- Claude: ... -->` in [[Helmholtz Equation]] (Free-Space Eigenstates). The user's tentative expansion $\langle\mathbf{r}|\mathbf{k}\rangle = \int r(x)k(x)\,dx$ was incorrect — $|\mathbf{r}\rangle$ and $|\mathbf{k}\rangle$ are delta-normalized continuous basis kets, not $L^2$ functions. Replaced with a proper derivation: $\langle\mathbf{r}|\mathbf{k}\rangle$ is a single number (the plane-wave state evaluated at $\mathbf{r}$), derived from $\hat{\mathbf{P}}|\mathbf{k}\rangle = \mathbf{k}|\mathbf{k}\rangle$ in the position basis, with the $1/(2\pi)^{d/2}$ factor fixed by delta-normalization.

## [2026-04-20] edit | Helmholtz Equation — answered two inline questions

Resolved both `<!-- Claude: ... -->` comments in [[Helmholtz Equation]]. (1) Clarified that $k=0$ is the DC/static limit and harmonic functions are its spatial modes (connecting to electrostatics). (2) Clarified that harmonic functions are the zero-eigenvalue eigenstates of $\hat L$ by definition, with a note on when $\lambda=0$ is actually in the spectrum (Neumann yes, Dirichlet no). No figures changed.

## [2026-04-20] edit | Dirac Notation — reworked basis-decomposition figure

Resolved the open `<!-- Claude: ... -->` comment in [[Dirac Notation]]. Reworked `plot_basis_decomposition` in `Scripts/dirac_notation.py` into a 3-panel figure that makes the projection step explicit: $\psi(x)$ in the position basis, the weighted components $c_n\phi_n(x)$ stacked (bridging the two domains), and $|c_n|^2$ in the energy basis. Regenerated `Figures/dirac_basis_decomposition.png` and rewrote the caption and surrounding paragraph.

## [2026-04-20] meta | Initialize INDEX.md and LOG.md

Created [[INDEX]] as the cold-start entry point (reading order, dependency graph, per-notebook sections, figure inventory, script map) and this log. Added pointer from [[CLAUDE]]. No notebook content changed.
