"""Visualizing the Laplacian, harmonic functions, and their connection to complex analysis."""

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


def make_grid(a, b, n):
    """Create a 2D meshgrid over [a, b] x [a, b] with n points per axis."""
    x = np.linspace(a, b, n)
    y = np.linspace(a, b, n)
    return np.meshgrid(x, y)


def _save_fig(fig, save_as):
    """Save a figure to the Figures/ directory."""
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )


# --- Scalar fields ---


def scalar_paraboloid(x, y):
    """f(x, y) = x^2 + y^2 — Laplacian is 4 (not harmonic)."""
    return x**2 + y**2


def scalar_saddle(x, y):
    """f(x, y) = x^2 - y^2 — Laplacian is 0 (harmonic). Also Re(z^2)."""
    return x**2 - y**2


def scalar_xy(x, y):
    """f(x, y) = 2xy — Laplacian is 0 (harmonic). Also Im(z^2)."""
    return 2 * x * y


def scalar_gaussian(x, y):
    """f(x, y) = e^{-(x^2 + y^2)} — Laplacian is nonzero (not harmonic)."""
    return np.exp(-(x**2 + y**2))


def scalar_log_r(x, y, eps=0.05):
    """f(x, y) = ln(r) = (1/2) ln(x^2 + y^2) — harmonic away from origin."""
    return 0.5 * np.log(x**2 + y**2 + eps**2)


def scalar_ex_cosy(x, y):
    """f(x, y) = e^x cos(y) — Re(e^z), harmonic."""
    return np.exp(x) * np.cos(y)


def scalar_ex_siny(x, y):
    """f(x, y) = e^x sin(y) — Im(e^z), harmonic."""
    return np.exp(x) * np.sin(y)


# --- Numerical differential operators ---


def laplacian(f, x, y, dx=1e-4):
    """Compute the Laplacian numerically: d^2f/dx^2 + d^2f/dy^2."""
    d2f_dx2 = (f(x + dx, y) - 2 * f(x, y) + f(x - dx, y)) / dx**2
    d2f_dy2 = (f(x, y + dx) - 2 * f(x, y) + f(x, y - dx)) / dx**2
    return d2f_dx2 + d2f_dy2


def gradient(f, x, y, dx=1e-6):
    """Compute the gradient of a scalar field numerically."""
    df_dx = (f(x + dx, y) - f(x - dx, y)) / (2 * dx)
    df_dy = (f(x, y + dx) - f(x, y - dx)) / (2 * dx)
    return df_dx, df_dy


# --- Plot functions ---


def plot_laplacian_examples(save_as=None):
    """Two rows of three panels: f on top, Laplacian(f) on bottom.
    Paraboloid and Gaussian have nonzero Laplacian; saddle is harmonic.
    """
    X, Y = make_grid(-2.5, 2.5, 500)
    fields = [
        (scalar_paraboloid, r"$x^2 + y^2$"),
        (scalar_saddle, r"$x^2 - y^2$"),
        (scalar_gaussian, r"$e^{-(x^2+y^2)}$"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    for col, (f, label) in enumerate(fields):
        Z = f(X, Y)
        lap = laplacian(f, X, Y)

        # Top row: the function
        ax_top = axes[0, col]
        c1 = ax_top.contourf(X, Y, Z, levels=100, cmap="rocket")
        ax_top.contour(X, Y, Z, levels=10, colors="k", linewidths=0.3, alpha=0.3)
        ax_top.set_title(rf"$f = {label[1:-1]}$")
        ax_top.set_xlabel(r"$x$")
        ax_top.set_ylabel(r"$y$")
        ax_top.set_aspect("equal")
        fig.colorbar(c1, ax=ax_top)

        # Bottom row: the Laplacian
        ax_bot = axes[1, col]
        vmax = max(abs(np.nanmin(lap)), abs(np.nanmax(lap)))
        if vmax < 1e-6:
            vmax = 1
        c2 = ax_bot.contourf(
            X, Y, lap, levels=100, cmap="twilight", vmin=-vmax, vmax=vmax
        )
        ax_bot.set_title(r"$\nabla^2 f$")
        ax_bot.set_xlabel(r"$x$")
        ax_bot.set_ylabel(r"$y$")
        ax_bot.set_aspect("equal")
        fig.colorbar(c2, ax=ax_bot)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_harmonic_gallery(save_as=None):
    """Three-panel: three harmonic functions with contours."""
    X, Y = make_grid(-2.5, 2.5, 500)
    fields = [
        (scalar_saddle, r"$x^2 - y^2$"),
        (scalar_log_r, r"$\ln r$"),
        (scalar_ex_cosy, r"$e^x \cos y$"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for ax, (f, title) in zip(axes, fields):
        Z = f(X, Y)
        contour = ax.contourf(X, Y, Z, levels=100, cmap="rocket")
        ax.contour(X, Y, Z, levels=15, colors="k", linewidths=0.3, alpha=0.3)
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")
        ax.set_title(title)
        ax.set_aspect("equal")
        fig.colorbar(contour, ax=ax)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_complex_harmonic_panel(save_as=None):
    """Two-panel: Re(z^2) and Im(z^2) as scalar fields, showing they are
    conjugate harmonics. Contours of one are level curves perpendicular
    to the contours of the other.
    """
    X, Y = make_grid(-2.5, 2.5, 500)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Re(z^2) = x^2 - y^2
    u = scalar_saddle(X, Y)
    ax1.contourf(X, Y, u, levels=100, cmap="rocket")
    ax1.contour(X, Y, u, levels=15, colors="k", linewidths=0.5, alpha=0.5)
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$y$")
    ax1.set_title(r"$u = \mathrm{Re}(z^2) = x^2 - y^2$")
    ax1.set_aspect("equal")

    # Im(z^2) = 2xy
    v = scalar_xy(X, Y)
    ax2.contourf(X, Y, v, levels=100, cmap="rocket")
    ax2.contour(X, Y, v, levels=15, colors="k", linewidths=0.5, alpha=0.5)
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$y$")
    ax2.set_title(r"$v = \mathrm{Im}(z^2) = 2xy$")
    ax2.set_aspect("equal")

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_orthogonal_contours(save_as=None):
    """Single figure: contour lines of Re(z^2) and Im(z^2) overlaid,
    showing they cross at right angles everywhere.
    """
    X, Y = make_grid(-2.5, 2.5, 500)
    u = scalar_saddle(X, Y)
    v = scalar_xy(X, Y)

    fig, ax = plt.subplots(figsize=(7, 7))
    colors = sns.color_palette("deep")
    ax.contour(X, Y, u, levels=15, colors=[colors[0]], linewidths=1, alpha=0.8)
    ax.contour(X, Y, v, levels=15, colors=[colors[1]], linewidths=1, alpha=0.8)

    # Legend proxy
    ax.plot([], [], color=colors[0], label=r"$u = x^2 - y^2$ (const)")
    ax.plot([], [], color=colors[1], label=r"$v = 2xy$ (const)")
    ax.legend(loc="upper left")

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_title(
        r"Contours of $\mathrm{Re}(z^2)$ and $\mathrm{Im}(z^2)$ cross at right angles"
    )
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_exp_harmonic_panel(save_as=None):
    """Two-panel: Re(e^z) and Im(e^z) as conjugate harmonics,
    with orthogonal contour overlay.
    """
    X, Y = make_grid(-2, 2, 500)
    u = scalar_ex_cosy(X, Y)
    v = scalar_ex_siny(X, Y)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Left: both as contour fills side by side
    ax1.contourf(X, Y, u, levels=100, cmap="rocket")
    ax1.contour(X, Y, u, levels=15, colors="k", linewidths=0.3, alpha=0.3)
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$y$")
    ax1.set_title(r"$u = e^x \cos y = \mathrm{Re}(e^z)$")
    ax1.set_aspect("equal")

    # Right: orthogonal contours
    colors = sns.color_palette("deep")
    ax2.contour(X, Y, u, levels=15, colors=[colors[0]], linewidths=1, alpha=0.8)
    ax2.contour(X, Y, v, levels=15, colors=[colors[1]], linewidths=1, alpha=0.8)
    ax2.plot([], [], color=colors[0], label=r"$\mathrm{Re}(e^z)$ (const)")
    ax2.plot([], [], color=colors[1], label=r"$\mathrm{Im}(e^z)$ (const)")
    ax2.legend(loc="upper left")
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$y$")
    ax2.set_title(r"Orthogonal contours of $\mathrm{Re}(e^z)$ and $\mathrm{Im}(e^z)$")
    ax2.set_aspect("equal")
    ax2.grid(True, alpha=0.2)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "laplacian": ("Laplacian examples", lambda: plot_laplacian_examples(save_as="laplacian_examples.png")),
        "gallery": ("Harmonic function gallery", lambda: plot_harmonic_gallery(save_as="harmonic_gallery.png")),
        "complex_harmonic": ("Complex-harmonic connection", lambda: plot_complex_harmonic_panel(save_as="complex_harmonic_panel.png")),
        "orthogonal": ("Orthogonal contour families", lambda: plot_orthogonal_contours(save_as="orthogonal_contours.png")),
        "exp_harmonic": ("Exponential harmonic panel", lambda: plot_exp_harmonic_panel(save_as="exp_harmonic_panel.png")),
    }

    parser = argparse.ArgumentParser(description="Harmonic function visualizations.")
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
