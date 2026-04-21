# For Fun — Python-Powered Math Notebook

## Project Overview

An interactive mathematical notebook combining Python visualization scripts with an Obsidian vault. The goal is to explore and teach mathematical concepts — from complex analysis through quantum mechanics — through narrative writing paired with generated figures.

## Start Here (for AI agents)

On a cold start, read [`INDEX.md`](INDEX.md) first. It is the content catalog: reading order, dependency graph between notebooks, section outlines, and which figures belong to which page. Then check [`LOG.md`](LOG.md) for recent activity. The pattern is adapted from [`llm-wiki.md`](llm-wiki.md).

When you edit a notebook, add a figure, or change structure, append a one-line entry to `LOG.md` and update the relevant entry in `INDEX.md`. Treat those two files the way the llm-wiki pattern treats `index.md` / `log.md`: the LLM owns them.

## Architecture

```
.
├── Scripts/
│   ├── complex_numbers.py          # Complex analysis visualization
│   ├── scalar_vector_fields.py     # Scalar and vector field visualization
│   ├── harmonic_functions.py       # Laplacian, harmonic functions, complex connection
│   ├── fourier_analysis.py         # Fourier series, transforms, Parseval
│   ├── linear_algebra.py           # Inner products, orthogonality, eigenvalues
│   ├── hilbert_spaces.py           # L^2, completeness, normalization
│   ├── operators_eigenvalues.py    # Differential operators, spectral theory
│   ├── probability_amplitudes.py   # Born rule, interference, superposition
│   ├── schrodinger_equation.py     # Particle in a box, harmonic oscillator, time evolution
│   ├── dirac_notation.py           # Projections, basis decomposition, representations
│   ├── maxwells_equations.py       # Dispersion, Fresnel, waveguide modes, EM-QM analogy
│   ├── permittivity_mod_arg.py     # Complex permittivity: Drude, Lorentz, non-resonant
│   ├── anisotropic_media.py        # Anisotropic permittivity, isofrequency, hyperbolic modes
│   ├── conformal_mappings.py       # Conformal maps, Möbius, Joukowski, critical points
│   ├── helmholtz_equation.py       # Cavity modes, Bessel functions, Green's functions
│   └── animations.py               # GIF animations (manim)
├── Figures/                        # Generated PNGs and GIFs, referenced by Obsidian notes
├── Complex Numbers.md              # Complex analysis notebook
├── Scalar and Vector Fields.md     # Fields notebook
├── Harmonic Functions.md           # Laplacian and harmonics notebook
├── Fourier Analysis.md             # Fourier series and transforms notebook
├── Linear Algebra.md               # Function spaces notebook
├── Hilbert Spaces.md               # L^2 and completeness notebook
├── Operators and Eigenvalues.md    # Spectral theory notebook
├── Probability and Complex Amplitudes.md  # Quantum probability notebook
├── The Schrodinger Equation.md     # Quantum mechanics notebook
├── Dirac Notation.md               # Bra-ket notation, representations
├── Maxwells Equations.md           # EM modes, dispersion, QM-EM analogy
├── Complex Permittivity.md         # Drude, Lorentz, damping, complex plane trajectories
├── Anisotropic Media.md            # Permittivity tensors, hyperbolic dispersion, Dirac formalism
├── Conformal Mappings.md           # Angle preservation, Möbius, Joukowski airfoil
├── Helmholtz Equation.md           # Cavity modes, spectra, Green's functions, Dirac notation
├── .obsidian/                      # Obsidian vault config
└── pyproject.toml                  # uv-managed, Python 3.14+
```

## Workflow

1. **Define math** in the relevant `Scripts/*.py` script — complex functions are simple `f(z) -> w` callables, fields are callables on `(x, y)` grids
2. **Extract** with `complex_modulus`, `complex_real`, `complex_imag`, or `complex_phase`
3. **Plot** with `plot_curve`, `plot_surface`, `plot_phase`, or custom panel functions
4. **Save** figures to `Figures/` via `save_as="filename.png"` parameter
5. **Embed** in Obsidian notes with `![[Figures/filename.png]]`

### CLI usage

All scripts support selective figure generation:
```bash
uv run python Scripts/anisotropic_media.py              # generate all figures
uv run python Scripts/anisotropic_media.py --list        # list available figures
uv run python Scripts/anisotropic_media.py isofrequency  # generate one figure
```

Animations (`Scripts/animations.py`) use the same pattern and render GIFs to `Figures/`.

## Claude's Role

Claude acts as a **collaborator and tutor** on this project:

- **Notebook writing**: Draft and edit mathematical exposition in the Obsidian `.md` files. Follow the narrative flow — each concept should build on what came before. Use LaTeX (`$...$` and `$$...$$`) for all math notation.
- **Notebook comments**: The user leaves `<!-- Claude: ... -->` HTML comments in the notebook as instructions. Address the comment, replace it with the appropriate content, and remove the comment tag.
- **Visualization**: Write plotting functions in the relevant `.py` script and generate figures. Always include `save_as` when the figure is intended for the notebook.
- **Teaching**: Explain mathematical concepts when asked. Tailor explanations to build intuition before formalism. Use the existing visualizations as reference points.
- **Code quality**: Follow the established patterns. Lint with `ruff` before finishing.

## Code Conventions

- **Package manager**: uv (`uv run`, `uv add`)
- **Linter/formatter**: ruff (`uv run ruff check`, `uv run ruff format`)
- **Complex functions**: Define as `f(z) -> w` (one line of math, no masking). Masking and extraction happen in the extractor functions.
- **Plot style**: `seaborn-v0_8-whitegrid`, serif/Computer Modern fonts, `deep` color cycle, 300 DPI exports
- **Colormaps**: `rocket` for modulus contours, `twilight` for phase portraits, `viridis` for 3D surfaces
- **No lambdas assigned to variables** — use `def` (ruff E731)
- **Multi-panel figures**: Get their own `plot_*_panel` function

## Notebook Conventions

- **LaTeX**: Use `$\mathbb{R}$`, `$\mathbb{C}$`, `$\mathbb{R}[x]$` for standard sets. Use `\mathrm{}` for operator names (Re, Im, arg).
- **Figures**: Always placed in `Figures/`, embedded with `![[Figures/name.png]]`. Each figure gets an italic caption: `*Figure N: Description.*`
- **Animations**: GIF animations embedded with `![[Figures/anim_name.gif]]` and captioned as `*Animation N: Description.*`
- **Structure**: Each section should motivate → define → visualize. Don't introduce notation (like `arg`) before it has been defined.
- **Obsidian links**: Use `[[double brackets]]` for cross-references between notes
- **Comments for Claude**: `<!-- Claude: instruction -->` — address and remove
