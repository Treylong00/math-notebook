"""Operators and eigenvalue problems: from matrices to differential operators.

Visualizes eigenfunctions of the 1D Laplacian (-d²/dx²) under different
boundary conditions, the discrete spectrum, and eigenfunction expansions.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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


# --- Eigenfunctions ---


def dirichlet_eigenfunction(x, n):
    """n-th eigenfunction of -d²/dx² on [0, pi] with Dirichlet BCs.

    f_n(x) = sin(n*x), eigenvalue lambda_n = n^2.
    """
    return np.sin(n * x)


def periodic_eigenfunction_cos(x, n):
    """Cosine eigenfunction of -d²/dx² on [0, 2*pi] with periodic BCs.

    f_n(x) = cos(n*x), eigenvalue lambda_n = n^2.
    """
    return np.cos(n * x)


def periodic_eigenfunction_sin(x, n):
    """Sine eigenfunction of -d²/dx² on [0, 2*pi] with periodic BCs.

    f_n(x) = sin(n*x), eigenvalue lambda_n = n^2.
    """
    return np.sin(n * x)


def target_function(x):
    """A non-smooth function for eigenfunction expansion: sawtooth on [0, pi].

    f(x) = x*(pi - x), normalized for visual clarity.
    """
    return x * (np.pi - x)


def fourier_sine_coefficient(n):
    """Compute the n-th Fourier sine coefficient of x*(pi - x) on [0, pi].

    b_n = (2/pi) * integral_0^pi x*(pi-x)*sin(nx) dx
        = 4/(n^3 * pi) * (1 - (-1)^n)
    Only odd n contribute (b_n = 8/(n^3*pi) for odd n, 0 for even n).
    """
    if n % 2 == 0:
        return 0.0
    return 8.0 / (n**3 * np.pi)


def eigenfunction_partial_sum(x, n_terms):
    """Partial sum of eigenfunction expansion of x*(pi-x) on [0, pi].

    Uses the first n_terms nonzero Fourier sine coefficients.
    """
    result = np.zeros_like(x)
    for n in range(1, n_terms + 1):
        bn = fourier_sine_coefficient(n)
        result += bn * np.sin(n * x)
    return result


# --- Plot functions ---


def plot_eigenfunctions_panel(save_as=None):
    """Multi-panel: first 4 eigenfunctions of -d²/dx² on [0, pi], Dirichlet BCs."""
    x = np.linspace(0, np.pi, 500)
    colors = sns.color_palette("deep")

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.ravel()

    for i, n in enumerate([1, 2, 3, 4]):
        ax = axes[i]
        y = dirichlet_eigenfunction(x, n)
        ax.plot(x, y, color=colors[i], linewidth=2)
        ax.axhline(0, color="gray", linewidth=0.5, alpha=0.5)
        ax.fill_between(x, y, alpha=0.15, color=colors[i])
        ax.set_title(
            rf"$f_{n}(x) = \sin({n}x)$, $\quad\lambda_{n} = {n**2}$",
        )
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(rf"$f_{n}(x)$")
        ax.set_xlim(0, np.pi)
        ax.set_ylim(-1.3, 1.3)
        ax.set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])
        ax.set_xticklabels([r"$0$", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])

    fig.suptitle(
        r"Eigenfunctions of $-d^2/dx^2$ on $[0, \pi]$ with Dirichlet BCs",
        fontsize=14,
        y=1.02,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_boundary_conditions_panel(save_as=None):
    """Two-panel: Dirichlet BCs (left) vs periodic BCs (right)."""
    colors = sns.color_palette("deep")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Left: Dirichlet on [0, pi]
    x_dir = np.linspace(0, np.pi, 500)
    for n in range(1, 5):
        y = dirichlet_eigenfunction(x_dir, n)
        ax1.plot(x_dir, y, color=colors[n - 1], linewidth=1.8, label=rf"$\sin({n}x)$")

    ax1.axhline(0, color="gray", linewidth=0.5, alpha=0.5)
    ax1.set_title(r"Dirichlet: $f(0) = f(\pi) = 0$")
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$f(x)$")
    ax1.set_xlim(0, np.pi)
    ax1.set_xticks([0, np.pi / 2, np.pi])
    ax1.set_xticklabels([r"$0$", r"$\pi/2$", r"$\pi$"])
    ax1.legend(loc="upper right", fontsize=10)

    # Mark boundary conditions
    for xb in [0, np.pi]:
        ax1.plot(xb, 0, "ko", markersize=6, zorder=5)

    # Right: periodic on [0, 2*pi]
    x_per = np.linspace(0, 2 * np.pi, 500)
    ax2.plot(
        x_per,
        np.ones_like(x_per) * 0.5,
        color=colors[4],
        linewidth=1.8,
        linestyle="--",
        label=r"$\frac{1}{2}$ (const, $n=0$)",
    )
    for n in range(1, 4):
        yc = periodic_eigenfunction_cos(x_per, n)
        ys = periodic_eigenfunction_sin(x_per, n)
        ax2.plot(x_per, yc, color=colors[n - 1], linewidth=1.8, label=rf"$\cos({n}x)$")
        ax2.plot(
            x_per,
            ys,
            color=colors[n - 1],
            linewidth=1.8,
            linestyle="--",
            label=rf"$\sin({n}x)$",
        )

    ax2.axhline(0, color="gray", linewidth=0.5, alpha=0.5)
    ax2.set_title(r"Periodic: $f(0) = f(2\pi)$, $f'(0) = f'(2\pi)$")
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$f(x)$")
    ax2.set_xlim(0, 2 * np.pi)
    ax2.set_xticks([0, np.pi, 2 * np.pi])
    ax2.set_xticklabels([r"$0$", r"$\pi$", r"$2\pi$"])
    ax2.legend(loc="upper right", fontsize=9, ncol=2)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_spectrum(save_as=None):
    """Stem plot of eigenvalues lambda_n = n^2 for the Dirichlet Laplacian."""
    n_max = 10
    ns = np.arange(1, n_max + 1)
    eigenvalues = ns**2
    colors = sns.color_palette("deep")

    fig, ax = plt.subplots(figsize=(10, 5))
    markerline, stemlines, baseline = ax.stem(
        ns, eigenvalues, linefmt="-", markerfmt="o", basefmt="k-"
    )
    markerline.set_color(colors[0])
    markerline.set_markersize(8)
    stemlines.set_color(colors[0])
    stemlines.set_alpha(0.7)

    # Overlay the continuous curve n^2
    n_cont = np.linspace(0, n_max + 0.5, 200)
    ax.plot(
        n_cont,
        n_cont**2,
        color=colors[1],
        linewidth=1.5,
        alpha=0.4,
        linestyle="--",
        label=r"$y = n^2$",
    )

    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$\lambda_n = n^2$")
    ax.set_title(r"Discrete spectrum of $-d^2/dx^2$ on $[0, \pi]$")
    ax.set_xticks(ns)
    ax.legend(fontsize=11)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_eigenfunction_expansion(save_as=None):
    """A function expanded in eigenfunctions, showing partial sums converging."""
    x = np.linspace(0, np.pi, 500)
    f_exact = target_function(x)
    colors = sns.color_palette("deep")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, f_exact, "k-", linewidth=2.5, label=r"$f(x) = x(\pi - x)$", zorder=5)

    partial_sums = [1, 3, 5, 15]
    for i, n_terms in enumerate(partial_sums):
        y_approx = eigenfunction_partial_sum(x, n_terms)
        ax.plot(
            x,
            y_approx,
            color=colors[i],
            linewidth=1.5,
            alpha=0.8,
            label=rf"$N = {n_terms}$ terms",
        )

    ax.axhline(0, color="gray", linewidth=0.5, alpha=0.5)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$f(x)$")
    ax.set_title(r"Eigenfunction expansion: $f(x) = \sum b_n \sin(nx)$")
    ax.set_xlim(0, np.pi)
    ax.set_xticks([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi])
    ax.set_xticklabels([r"$0$", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])
    ax.legend(fontsize=11)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "eigenfunctions": ("Operator eigenfunctions", lambda: plot_eigenfunctions_panel(save_as="operators_eigenfunctions.png")),
        "boundary": ("Boundary conditions", lambda: plot_boundary_conditions_panel(save_as="operators_boundary_conditions.png")),
        "spectrum": ("Operator spectrum", lambda: plot_spectrum(save_as="operators_spectrum.png")),
        "expansion": ("Eigenfunction expansion", lambda: plot_eigenfunction_expansion(save_as="operators_expansion.png")),
    }

    parser = argparse.ArgumentParser(description="Operators and eigenvalues figures.")
    parser.add_argument("names", nargs="*", help="figures to generate (omit for all)")
    parser.add_argument("--list", "-l", action="store_true", help="list available figures")
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
