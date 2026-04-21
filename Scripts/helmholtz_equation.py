"""The Helmholtz equation: eigenmodes, spectra, and Green's functions."""

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Circle
from scipy.special import jn_zeros, jv

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "Figures")
SAVE_DPI = 300

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update(
    {
        "mathtext.fontset": "cm",
        "font.family": "serif",
        "font.size": 12,
        "axes.prop_cycle": plt.cycler(color=sns.color_palette("deep")),
    }
)


def _save_fig(fig, save_as):
    """Save a figure to the Figures/ directory."""
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )


# --- Eigenfunctions and eigenvalues ---


def rect_mode(x, y, m, n, a=1.0, b=1.0):
    """Normalized Dirichlet eigenfunction of the rectangular cavity.

    <x,y|m,n> = (2/sqrt(ab)) sin(m pi x / a) sin(n pi y / b)
    """
    return (2 / np.sqrt(a * b)) * np.sin(m * np.pi * x / a) * np.sin(n * np.pi * y / b)


def rect_eigenvalue(m, n, a=1.0, b=1.0):
    """Eigenvalue k^2_{mn} for the rectangular cavity.

    k^2_{mn} = pi^2 (m^2/a^2 + n^2/b^2)
    """
    return np.pi**2 * (m**2 / a**2 + n**2 / b**2)


def circ_mode(r, theta, m, n, R=1.0):
    """Dirichlet eigenfunction of the circular drum (unnormalized).

    <r,theta|m,n> ~ J_m(j_{mn} r / R) cos(m theta)
    where j_{mn} is the nth zero of J_m.
    """
    j_mn = jn_zeros(m, n)[-1]
    return jv(m, j_mn * r / R) * np.cos(m * theta)


def circ_eigenvalue(m, n, R=1.0):
    """Eigenvalue k^2_{mn} for the circular drum.

    k^2_{mn} = (j_{mn} / R)^2
    """
    j_mn = jn_zeros(m, n)[-1]
    return (j_mn / R) ** 2


# --- 1. Rectangular cavity modes ---


def plot_rect_modes(save_as=None):
    """Six eigenmodes of the rectangular Dirichlet cavity."""
    a, b = 1.0, 1.0
    x = np.linspace(0, a, 300)
    y = np.linspace(0, b, 300)
    X, Y = np.meshgrid(x, y)

    modes = [(1, 1), (2, 1), (1, 2), (2, 2), (3, 1), (1, 3)]

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))

    for ax, (m, n) in zip(axes.flat, modes):
        psi = rect_mode(X, Y, m, n, a, b)
        k_sq_coeff = m**2 + n**2  # k^2 / pi^2

        vmax = np.abs(psi).max()
        ax.contourf(X, Y, psi, levels=50, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
        ax.contour(X, Y, psi, levels=[0], colors="k", linewidths=0.8, alpha=0.5)
        ax.set_aspect("equal")
        ax.set_title(rf"$|{m},{n}\rangle$,  $k^2 = {k_sq_coeff}\pi^2$", fontsize=13)
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")
        # Draw box boundary
        for spine in ax.spines.values():
            spine.set_edgecolor("k")
            spine.set_linewidth(1.5)

    fig.suptitle(
        r"Eigenmodes of the rectangular cavity: $\langle x,y|m,n\rangle$",
        fontsize=14,
        y=1.01,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- 2. Circular drum modes ---


def plot_circular_modes(save_as=None):
    """Six eigenmodes of the circular Dirichlet drum."""
    R = 1.0
    grid = np.linspace(-R * 1.05, R * 1.05, 400)
    X, Y = np.meshgrid(grid, grid)
    r = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)

    modes = [(0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (3, 1)]

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))

    for ax, (m, n) in zip(axes.flat, modes):
        psi = circ_mode(r, theta, m, n, R)
        psi[r > R] = np.nan  # mask exterior

        j_mn = jn_zeros(m, n)[-1]
        vmax = np.nanmax(np.abs(psi))
        ax.contourf(X, Y, psi, levels=50, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
        ax.contour(X, Y, psi, levels=[0], colors="k", linewidths=0.8, alpha=0.5)

        # Draw the circular boundary
        boundary = Circle((0, 0), R, fill=False, edgecolor="k", linewidth=2, zorder=5)
        ax.add_patch(boundary)
        ax.set_aspect("equal")
        ax.set_title(rf"$|{m},{n}\rangle$,  $j_{{{m},{n}}} = {j_mn:.3f}$", fontsize=13)
        ax.set_xlim(-1.08, 1.08)
        ax.set_ylim(-1.08, 1.08)
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")

    fig.suptitle(
        r"Eigenmodes of the circular drum: $\langle r,\theta|m,n\rangle"
        r" \propto J_m(j_{mn}\,r/R)\cos(m\theta)$",
        fontsize=14,
        y=1.01,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- 3. Eigenvalue spectrum ---


def plot_eigenvalue_spectrum(save_as=None):
    """Eigenvalue spectra of the rectangle and circle, showing how geometry
    determines the spectrum.
    """
    colors = sns.color_palette("deep")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

    # Rectangle eigenvalues (a = b = 1)
    rect_eigs = []
    for m in range(1, 6):
        for n in range(1, 6):
            k_sq = rect_eigenvalue(m, n)
            rect_eigs.append((k_sq, f"({m},{n})"))
    rect_eigs.sort(key=lambda x: x[0])

    vals_r = [e[0] for e in rect_eigs]
    labels_r = [e[1] for e in rect_eigs]
    markerline, stemlines, baseline = ax1.stem(
        vals_r, [1] * len(vals_r), linefmt="-", markerfmt="o", basefmt="k-"
    )
    plt.setp(stemlines, color=colors[0], linewidth=1.5)
    plt.setp(markerline, color=colors[0], markersize=5)
    for val, label in zip(vals_r[:12], labels_r[:12]):
        ax1.annotate(
            label,
            xy=(val, 1),
            xytext=(0, 8),
            textcoords="offset points",
            fontsize=8,
            ha="center",
            color=colors[0],
            rotation=45,
        )
    ax1.set_ylabel("Rectangle", fontsize=12)
    ax1.set_yticks([])
    ax1.set_title("Eigenvalue spectra: rectangle vs. circle", fontsize=14)

    # Circle eigenvalues (R = 1)
    circ_eigs = []
    for m in range(0, 5):
        for n in range(1, 5):
            k_sq = circ_eigenvalue(m, n)
            circ_eigs.append((k_sq, f"({m},{n})"))
    circ_eigs.sort(key=lambda x: x[0])

    vals_c = [e[0] for e in circ_eigs]
    labels_c = [e[1] for e in circ_eigs]
    markerline2, stemlines2, baseline2 = ax2.stem(
        vals_c, [1] * len(vals_c), linefmt="-", markerfmt="o", basefmt="k-"
    )
    plt.setp(stemlines2, color=colors[1], linewidth=1.5)
    plt.setp(markerline2, color=colors[1], markersize=5)
    for val, label in zip(vals_c[:12], labels_c[:12]):
        ax2.annotate(
            label,
            xy=(val, 1),
            xytext=(0, 8),
            textcoords="offset points",
            fontsize=8,
            ha="center",
            color=colors[1],
            rotation=45,
        )
    ax2.set_ylabel("Circle", fontsize=12)
    ax2.set_yticks([])
    ax2.set_xlabel(r"$k^2$", fontsize=13)

    for ax in (ax1, ax2):
        ax.set_xlim(0, 200)
        ax.set_ylim(0, 1.6)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- 4. Green's function mode expansion ---


def plot_greens_expansion(save_as=None):
    """Mode expansion of the Green's function in a rectangular cavity,
    showing convergence as more eigenmodes are included.
    """
    a, b = 1.0, 1.0
    x0, y0 = 0.35, 0.25  # source position
    k = 0.0  # static (Poisson) Green's function

    x = np.linspace(0, a, 200)
    y = np.linspace(0, b, 200)
    X, Y = np.meshgrid(x, y)

    n_max_values = [1, 3, 7, 15]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    for ax, n_max in zip(axes.flat, n_max_values):
        G = np.zeros_like(X)
        n_terms = 0
        for m in range(1, n_max + 1):
            for n in range(1, n_max + 1):
                psi_grid = rect_mode(X, Y, m, n, a, b)
                psi_source = rect_mode(x0, y0, m, n, a, b)
                k_sq = rect_eigenvalue(m, n, a, b)
                denom = k_sq - k**2
                G -= psi_grid * psi_source / denom
                n_terms += 1

        # -G is the positive response (peaks at source)
        response = -G
        vmax = np.percentile(response, 99)
        if vmax <= 0:
            vmax = 1.0
        ax.contourf(X, Y, response, levels=50, cmap="rocket", vmin=0, vmax=vmax)
        ax.plot(x0, y0, "w*", markersize=12, markeredgecolor="k", markeredgewidth=0.8)
        ax.set_aspect("equal")
        ax.set_title(
            rf"$N_{{\max}} = {n_max}$ ({n_terms} mode{'s' if n_terms > 1 else ''})",
            fontsize=13,
        )
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")

    fig.suptitle(
        r"Green's function $\langle \mathbf{r}|\hat{G}|\mathbf{r}'\rangle"
        r" = -\sum_{m,n}"
        r" \frac{\langle \mathbf{r}|m,n\rangle\langle m,n|\mathbf{r}'\rangle}"
        r"{k_{mn}^2 - k^2}$",
        fontsize=13,
        y=1.01,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- CLI ---


def main():
    import argparse

    figures = {
        "rect_modes": (
            "Rectangular cavity eigenmodes",
            lambda: plot_rect_modes(save_as="helmholtz_rect_modes.png"),
        ),
        "circular_modes": (
            "Circular drum eigenmodes",
            lambda: plot_circular_modes(save_as="helmholtz_circular_modes.png"),
        ),
        "spectrum": (
            "Eigenvalue spectrum comparison",
            lambda: plot_eigenvalue_spectrum(save_as="helmholtz_spectrum.png"),
        ),
        "greens": (
            "Green's function mode expansion",
            lambda: plot_greens_expansion(save_as="helmholtz_greens_expansion.png"),
        ),
    }

    parser = argparse.ArgumentParser(description="Helmholtz equation figures.")
    parser.add_argument("names", nargs="*", help="figures to generate (omit for all)")
    parser.add_argument(
        "--list", "-l", action="store_true", help="list available figures"
    )
    args = parser.parse_args()

    if args.list:
        for name, (desc, _) in figures.items():
            print(f"  {name:30s}  {desc}")
        return

    selected = args.names or list(figures.keys())
    for name in selected:
        if name not in figures:
            print(f"Unknown figure '{name}'. Use --list to see options.")
            return
        figures[name][1]()


if __name__ == "__main__":
    main()
