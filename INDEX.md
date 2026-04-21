# Index

Entry point for an AI (or human) intaking the state of this notebook. Lists every `.md` page, its role, its dependencies, its sections, and the figures it embeds. Updated on every notebook edit or figure regen — see [[LOG]] for the chronological record.

Project schema and conventions live in [[CLAUDE]]. The pattern this index follows is sketched in [[llm-wiki]].

## Reading Order

The notebooks form a directed graph — each one builds on earlier threads. The canonical "main line" from complex numbers to the Schrödinger equation:

1. [[Complex Numbers]]
2. [[Scalar and Vector Fields]]
3. [[Harmonic Functions]]
4. [[Fourier Analysis]]
5. [[Linear Algebra]]
6. [[Hilbert Spaces]]
7. [[Operators and Eigenvalues]]
8. [[Probability and Complex Amplitudes]]
9. [[Dirac Notation]]
10. [[The Schrodinger Equation]]

Branches off the main line:

- [[Conformal Mappings]] — after Complex Numbers + Harmonic Functions
- [[Helmholtz Equation]] — after Harmonic Functions + Operators and Eigenvalues
- [[Greens Functions]] — after Helmholtz Equation + Dirac Notation
- [[Maxwells Equations]] — after Linear Algebra + Operators + Dirac Notation
- [[Complex Permittivity]] — after Complex Numbers
- [[Anisotropic Media]] — after Dirac Notation + Maxwells + Complex Permittivity

Standalone / reference:

- [[Fundamental Theorem of Algebra]] — short theorem page with proof sketches

## Dependency Graph

```
Complex Numbers ─┬─> Harmonic Functions ─┬─> Conformal Mappings
                 │                       │
                 │                       └─> Fourier Analysis ─> Linear Algebra ─┐
                 │                                                                │
Scalar/Vector ───┘                                              Hilbert Spaces <──┤
Fields                                                              │             │
                                                                    v             │
                                            Operators and Eigenvalues <───────────┘
                                                    │  │  │
                                          ┌─────────┘  │  └──────────┐
                                          v            v             v
                              Helmholtz Equation   Probability   Maxwells Equations
                                                       │              │
                                                       v              │
                                                 Dirac Notation <─────┤
                                                       │              │
                                                       v              v
                                               Schrodinger Eq.   Complex Permittivity
                                                                      │
                                                                      v
                                                              Anisotropic Media
```

## Notebook Catalog

Each entry: one-line topic, sections, linked figures (filename stem only). Figures live in `Figures/`; scripts that generate them live in `Scripts/` per [[CLAUDE]].

### [[Complex Numbers]]
Introduces $\mathbb{C}$ via polynomial roots; builds $z = a+bi$, polar form, square root, exp/trig, logarithm.
Sections: Polynomials · From $i$ to $a+bi$ · What is a Complex Number? · Square Root · Exponential and Trigonometry · Logarithm · Where to Go Next.
Figures: `euler_vectors`, `complex_sqrt_panel`, `complex_sqrt_phase`, `exp_panel`, etc. (script: `complex_numbers.py`).

### [[Fundamental Theorem of Algebra]]
Statement and proof sketches. Short reference page, no figures.

### [[Scalar and Vector Fields]]
Gradient, divergence, curl as visual/geometric operators.
Sections: Scalar Fields · The Gradient · Vector Fields · Divergence · Curl · Gravitational Field · Where to Go Next.
Figures: `gradient_panel`, `divergence_panel`, `curl_panel`, `gravitational_panel` (script: `scalar_vector_fields.py`).

### [[Harmonic Functions]]
Laplacian, harmonic functions, connection to analytic functions via Cauchy-Riemann.
Sections: The Laplacian · Harmonic Functions · Connection to Complex Analysis · Conjugate Harmonics and Cauchy-Riemann · A Second Example: $e^z$ · The Big Picture · Where to Go Next.
Figures: `laplacian_examples`, `harmonic_gallery`, `complex_harmonic_panel`, `exp_harmonic_panel` (script: `harmonic_functions.py`).

### [[Conformal Mappings]]
Angle-preserving maps, Jacobian as scaled rotation, Möbius, Joukowski airfoil.
Sections: Grid Deformations · Angle Preservation · Jacobian as a Scaled Rotation · Critical Points · Möbius Transforms · Joukowski Airfoil · Where to Go Next.
Figures: `conformal_grid_gallery`, `conformal_angle_preservation`, `conformal_jacobian_element`, `conformal_critical_points`, `conformal_mobius_circles`, `conformal_joukowski`; animation `anim_conformal_mapping` (script: `conformal_mappings.py`).

### [[Fourier Analysis]]
Fourier series, square-wave construction, Fourier transform, Gaussian transform, Parseval.
Sections: Why Decompose into Frequencies? · Fourier Series · Building a Square Wave · The Fourier Transform · Transform of a Gaussian · Parseval's Theorem · Where to Go Next.
Figures: Fourier-series / transform figures; animation `anim_fourier_convergence` (script: `fourier_analysis.py`).

### [[Linear Algebra]]
Inner products, orthogonality, projection, eigenvalues — lifting from $\mathbb{R}^n$ to function spaces.
Sections: Vectors and Functions · Inner Products · Orthogonality · Bases and Projections · Eigenvalues and Eigenvectors · From Matrices to Operators · Where to Go Next.
Figures: `linalg_inner_product`, `linalg_orthogonal_functions`, `linalg_projection`, `linalg_eigen` (script: `linear_algebra.py`).

### [[Hilbert Spaces]]
$L^2$, completeness, orthonormal bases, the geometry of function spaces; setup for QM.
Sections: $L^2$: Square-Integrable Functions · Completeness · Orthonormal Bases · The Geometry of $L^2$ · From $L^2$ to Quantum Mechanics · Where to Go Next.
Figures: `hilbert_l2_membership`, `hilbert_completeness`, `hilbert_distance`, `hilbert_normalization` (script: `hilbert_spaces.py`).

### [[Operators and Eigenvalues]]
Differential operators, eigenfunctions of $-d^2/dx^2$, boundary conditions, Hermitian operators, spectral theorem.
Sections: Differential Operators · Eigenfunctions of $-d^2/dx^2$ · Boundary Conditions Shape the Spectrum · The Spectrum · Hermitian Operators · The Spectral Theorem · Where to Go Next.
Figures / animation: `anim_eigenfunction_expansion` (script: `operators_eigenvalues.py`).

### [[Probability and Complex Amplitudes]]
Complex amplitudes, Born rule, interference, phase, superposition, expectation values.
Sections: Complex Amplitudes · The Born Rule · Interference · Phase Matters · Superposition · Expectation Values · Looking Forward.
Figures: see `probability_amplitudes.py`.

### [[Dirac Notation]]
Kets, bras, projectors, completeness, operators, position/momentum representations.
Sections: Kets and Bras · Inner Products · Basis Decomposition · Outer Products and Projectors · The Completeness Relation · Operators in Dirac Notation · Position and Momentum Representations · Why Dirac Notation Matters · Where to Go Next.
Figures: `dirac_projection`, `dirac_basis_decomposition`, `dirac_completeness`, `dirac_matrix_elements`, `dirac_position_momentum` (script: `dirac_notation.py`).

### [[The Schrodinger Equation]]
Time-dependent and time-independent equations, particle in a box, harmonic oscillator, time evolution, uncertainty.
Sections: The Schrodinger Equation · Time-Independent Schrodinger Equation · Particle in a Box · Quantum Harmonic Oscillator · Time Evolution · The Uncertainty Principle · Where to Go Next.
Animations: `anim_wavefunction_evolution` (script: `schrodinger_equation.py`).

### [[Greens Functions]]
Green's functions as inverse operators; free-space Helmholtz G in 1D/2D/3D; $i\epsilon$ prescription; worked problems in electrostatics, driven cavities, and 1D scattering.
Sections: The Operator Picture · Free-Space Helmholtz Green's Function · Worked Problem 1: Laplace, Coulomb, Static Limit · Worked Problem 2: Driven Cavity and the Resolvent Pole · Worked Problem 3: 1D Scattering from a Delta Potential · Where to Go Next.
Figures: `greens_free_space_dims`, `greens_iepsilon`, `greens_coulomb_convolution`, `greens_delta_scattering` (script: `greens_functions.py`).

### [[Maxwells Equations]]
EM wave equation as eigenvalue problem, dispersion, Fresnel, waveguide modes, transfer matrix, QM analogy.
Sections: Wave Equation as Eigenvalue Problem · Dispersion Relations · Interfaces and Fresnel · Waveguide Modes as Eigenfunctions · The Transfer Matrix · The Structural Analogy · Where to Go Next.
Figures: see `maxwells_equations.py`.

### [[Complex Permittivity]]
Drude, Lorentz, non-resonant models; real/imag parts, modulus/argument, complex-plane trajectories, damping.
Sections: Three Models of Permittivity · Real and Imaginary Parts · Modulus and Argument · Trajectories in the Complex Plane · The Effect of Damping · Where to Go Next.
Figures / animation: `anim_permittivity_trajectory` (script: `permittivity_mod_arg.py`).

### [[Anisotropic Media]]
Permittivity tensor as operator, isofrequency contours, Type I vs II, hyperbolic modes, phonon polaritons, biaxial MoO$_3$.
Sections: Permittivity Tensor as Operator · The Dispersion Relation · Isofrequency Contours · Type I vs Type II · Mode Index Surface · Elliptic-to-Hyperbolic Transition · The Operator Perspective · Phonon Polariton Dispersion · Biaxial MoO$_3$ · Biaxial Isofrequency Contours · Where to Go Next.
Figures: `aniso_tensor_operator`, `aniso_isofrequency`, `aniso_hyperbolic_types`, `aniso_mode_index`, `aniso_isofrequency_transition`, `aniso_phonon_polariton`, `aniso_moo3_permittivity`, `aniso_moo3_isofrequency`; animations `anim_isofrequency_transition`, `anim_moo3_isofrequency` (script: `anisotropic_media.py`).

## Script ↔ Notebook Map

| Script | Primary Notebook |
| --- | --- |
| `complex_numbers.py` | Complex Numbers |
| `scalar_vector_fields.py` | Scalar and Vector Fields |
| `harmonic_functions.py` | Harmonic Functions |
| `conformal_mappings.py` | Conformal Mappings |
| `fourier_analysis.py` | Fourier Analysis |
| `linear_algebra.py` | Linear Algebra |
| `hilbert_spaces.py` | Hilbert Spaces |
| `operators_eigenvalues.py` | Operators and Eigenvalues |
| `probability_amplitudes.py` | Probability and Complex Amplitudes |
| `dirac_notation.py` | Dirac Notation |
| `schrodinger_equation.py` | The Schrodinger Equation |
| `maxwells_equations.py` | Maxwells Equations |
| `permittivity_mod_arg.py` | Complex Permittivity |
| `anisotropic_media.py` | Anisotropic Media |
| `helmholtz_equation.py` | Helmholtz Equation |
| `greens_functions.py` | Greens Functions |
| `animations.py` | Shared (all GIFs) |

Each script supports `uv run python Scripts/<name>.py [--list | <figure-name>]`. See [[CLAUDE]].

## State

- 16 notebooks + 1 reference page. No open `<!-- Claude: ... -->` TODO comments at last index update.
- 86 files in `Figures/` (≈78 PNG + 7 GIF animations).
- Figures are regenerated on demand from scripts — never hand-edited.

## Maintenance

When a notebook is added, removed, renamed, or gets a new section or figure, update this index. When in doubt, regenerate the Notebook Catalog section from `^## ` headings and `![[Figures/...]]` embeds. Append a one-line entry to [[LOG]] each time.
