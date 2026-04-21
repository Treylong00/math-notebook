"""Linear algebra in finite and infinite dimensions: inner products, orthogonality,
projections, and eigenvalues — bridging vectors and function spaces.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import FancyArrowPatch

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


# --- Helper functions ---


def _draw_vector(ax, origin, vec, color, label=None, lw=2):
    """Draw an arrow from origin to origin + vec on a 2D axes."""
    arrow = FancyArrowPatch(
        origin,
        (origin[0] + vec[0], origin[1] + vec[1]),
        arrowstyle="->,head_width=6,head_length=6",
        color=color,
        linewidth=lw,
        mutation_scale=1,
    )
    ax.add_patch(arrow)
    if label:
        mid = (origin[0] + vec[0], origin[1] + vec[1])
        ax.annotate(
            label,
            xy=mid,
            fontsize=14,
            color=color,
            ha="center",
            va="bottom",
        )


# --- Plot functions ---


def plot_inner_product_panel(save_as=None):
    """Two-panel figure: dot product as projection in R^2 (left),
    inner product of two functions visualized as area under f*g (right).
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    colors = sns.color_palette("deep")

    # --- Left panel: dot product / projection in R^2 ---
    a = np.array([3.0, 1.0])
    b = np.array([1.0, 2.5])

    # Projection of b onto a
    proj_scalar = np.dot(a, b) / np.dot(a, a)
    proj = proj_scalar * a

    _draw_vector(ax1, (0, 0), a, colors[0], label=r"$\mathbf{a}$")
    _draw_vector(ax1, (0, 0), b, colors[1], label=r"$\mathbf{b}$")
    _draw_vector(
        ax1, (0, 0), proj, colors[2], label=r"$\mathrm{proj}_\mathbf{a}\,\mathbf{b}$"
    )

    # Dashed line from b to proj
    ax1.plot(
        [b[0], proj[0]],
        [b[1], proj[1]],
        "--",
        color="gray",
        linewidth=1,
        alpha=0.7,
    )

    # Right angle marker
    perp_dir = b - proj
    perp_dir = perp_dir / np.linalg.norm(perp_dir)
    a_dir = a / np.linalg.norm(a)
    corner_size = 0.15
    corner = proj + corner_size * perp_dir
    corner2 = corner + corner_size * a_dir
    corner3 = proj + corner_size * a_dir
    ax1.plot(
        [corner[0], corner2[0], corner3[0]],
        [corner[1], corner2[1], corner3[1]],
        color="gray",
        linewidth=1,
    )

    ax1.set_xlim(-0.5, 4)
    ax1.set_ylim(-0.5, 3.5)
    ax1.set_aspect("equal")
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$y$")
    ax1.set_title(r"Dot product as projection in $\mathbb{R}^2$")
    ax1.grid(True, alpha=0.3)

    # --- Right panel: inner product of two functions ---
    x = np.linspace(0, 2 * np.pi, 500)

    def f(t):
        """First function: sin(t)."""
        return np.sin(t)

    def g(t):
        """Second function: sin(2t)."""
        return np.sin(2 * t)

    product = f(x) * g(x)

    ax2.plot(x, f(x), color=colors[0], linewidth=2, label=r"$f(x) = \sin x$")
    ax2.plot(x, g(x), color=colors[1], linewidth=2, label=r"$g(x) = \sin 2x$")
    ax2.fill_between(
        x,
        0,
        product,
        alpha=0.3,
        color=colors[2],
        label=r"$f(x)\,g(x)$",
    )
    ax2.axhline(0, color="k", linewidth=0.5)
    ax2.set_xlabel(r"$x$")
    ax2.set_title(r"$\langle f, g \rangle = \int_0^{2\pi} f(x)\,g(x)\,dx = 0$")
    ax2.legend(loc="upper right")
    ax2.set_xlim(0, 2 * np.pi)
    ax2.set_xticks([0, np.pi, 2 * np.pi])
    ax2.set_xticklabels([r"$0$", r"$\pi$", r"$2\pi$"])

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_orthogonal_functions(save_as=None):
    """Show sin(x), sin(2x), sin(3x) and their pairwise products
    integrating to zero, demonstrating orthogonality.
    """
    x = np.linspace(0, 2 * np.pi, 500)
    colors = sns.color_palette("deep")

    fig, axes = plt.subplots(2, 3, figsize=(16, 8))

    funcs = [
        (r"$\sin x$", np.sin(x)),
        (r"$\sin 2x$", np.sin(2 * x)),
        (r"$\sin 3x$", np.sin(3 * x)),
    ]

    # Top row: the three functions
    for col, (label, vals) in enumerate(funcs):
        ax = axes[0, col]
        ax.plot(x, vals, color=colors[col], linewidth=2)
        ax.axhline(0, color="k", linewidth=0.5)
        ax.set_title(label, fontsize=14)
        ax.set_xlim(0, 2 * np.pi)
        ax.set_ylim(-1.3, 1.3)
        ax.set_xticks([0, np.pi, 2 * np.pi])
        ax.set_xticklabels([r"$0$", r"$\pi$", r"$2\pi$"])
        if col == 0:
            ax.set_ylabel("Amplitude")

    # Bottom row: pairwise products
    pairs = [
        (0, 1, r"$\sin x \cdot \sin 2x$"),
        (0, 2, r"$\sin x \cdot \sin 3x$"),
        (1, 2, r"$\sin 2x \cdot \sin 3x$"),
    ]
    for col, (i, j, label) in enumerate(pairs):
        ax = axes[1, col]
        product = funcs[i][1] * funcs[j][1]
        ax.fill_between(x, 0, product, alpha=0.4, color=colors[3])
        ax.plot(x, product, color=colors[3], linewidth=1.5)
        ax.axhline(0, color="k", linewidth=0.5)
        integral_val = np.trapezoid(product, x)
        ax.set_title(f"{label}\n" + r"$\int = $" + f"{integral_val:.4f}", fontsize=12)
        ax.set_xlim(0, 2 * np.pi)
        ax.set_xticks([0, np.pi, 2 * np.pi])
        ax.set_xticklabels([r"$0$", r"$\pi$", r"$2\pi$"])
        if col == 0:
            ax.set_ylabel("Product")

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_fourier_projection(save_as=None):
    """Multi-panel: a function and its projection onto the first N
    Fourier basis functions (N = 1, 3, 5, 10).
    """
    x = np.linspace(0, 2 * np.pi, 1000)
    colors = sns.color_palette("deep")

    # Target function: sawtooth-like (x shifted to zero mean)
    def target(t):
        """Sawtooth wave centered at zero: f(x) = x - pi on [0, 2pi]."""
        return t - np.pi

    def fourier_partial_sum(t, n_terms):
        """Fourier sine series partial sum for f(x) = x - pi on [0, 2pi].

        The Fourier coefficients for f(x) = x - pi are b_n = -2/n,
        giving f(x) ~ sum_{n=1}^{N} (-2/n) sin(nx).
        """
        result = np.zeros_like(t)
        for n in range(1, n_terms + 1):
            b_n = -2.0 / n
            result += b_n * np.sin(n * t)
        return result

    ns = [1, 3, 5, 10]
    fig, axes = plt.subplots(1, 4, figsize=(18, 4))

    for idx, n in enumerate(ns):
        ax = axes[idx]
        ax.plot(x, target(x), color="gray", linewidth=2, alpha=0.5, label=r"$f(x)$")
        approx = fourier_partial_sum(x, n)
        ax.plot(
            x,
            approx,
            color=colors[0],
            linewidth=2,
            label=f"$N = {n}$",
        )
        ax.axhline(0, color="k", linewidth=0.5)
        ax.set_title(rf"$N = {n}$ term{'s' if n > 1 else ''}")
        ax.set_xlim(0, 2 * np.pi)
        ax.set_ylim(-4.5, 4.5)
        ax.set_xticks([0, np.pi, 2 * np.pi])
        ax.set_xticklabels([r"$0$", r"$\pi$", r"$2\pi$"])
        ax.legend(loc="upper left", fontsize=10)
        if idx == 0:
            ax.set_ylabel("Value")

    fig.suptitle(
        r"Projecting $f(x) = x - \pi$ onto Fourier basis functions",
        fontsize=14,
        y=1.02,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_eigen_panel(save_as=None):
    """Two-panel figure showing eigenvectors of a 2D linear transformation.
    Left: the original vectors (unit circle + eigenvectors).
    Right: after applying the matrix, eigenvectors only scale, others rotate.
    """
    colors = sns.color_palette("deep")

    # Matrix with real eigenvalues: A = [[2, 1], [1, 2]]
    # Eigenvalues: 3 and 1, eigenvectors: (1,1)/sqrt(2) and (1,-1)/sqrt(2)
    A = np.array([[2, 1], [1, 2]])
    eigenvalues, eigenvectors = np.linalg.eig(A)

    # Sort by eigenvalue magnitude (descending)
    order = np.argsort(-eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    # Unit circle
    theta = np.linspace(0, 2 * np.pi, 200)
    circle = np.array([np.cos(theta), np.sin(theta)])
    transformed = A @ circle

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # --- Left panel: before transformation ---
    ax1.plot(circle[0], circle[1], color="gray", linewidth=1.5, alpha=0.5)

    # Draw eigenvectors
    ev_colors = [colors[0], colors[1]]
    for i in range(2):
        ev = eigenvectors[:, i]
        _draw_vector(
            ax1,
            (0, 0),
            ev * 1.0,
            ev_colors[i],
            label=rf"$\mathbf{{v}}_{i + 1}$",
            lw=2.5,
        )
        _draw_vector(ax1, (0, 0), -ev * 1.0, ev_colors[i], lw=2.5)

    # Draw some other vectors
    other_angles = [np.pi / 6, np.pi / 3, 2 * np.pi / 3]
    for ang in other_angles:
        v = np.array([np.cos(ang), np.sin(ang)])
        _draw_vector(ax1, (0, 0), v, "gray", lw=1)

    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.set_aspect("equal")
    ax1.set_title("Before: unit circle + vectors")
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$y$")
    ax1.grid(True, alpha=0.3)

    # --- Right panel: after transformation ---
    ax2.plot(
        transformed[0],
        transformed[1],
        color="gray",
        linewidth=1.5,
        alpha=0.5,
        label="Transformed circle",
    )

    for i in range(2):
        ev = eigenvectors[:, i]
        t_ev = A @ ev
        lam = eigenvalues[i]
        _draw_vector(
            ax2,
            (0, 0),
            t_ev,
            ev_colors[i],
            label=rf"$A\mathbf{{v}}_{i + 1} = {lam:.0f}\,\mathbf{{v}}_{i + 1}$",
            lw=2.5,
        )
        _draw_vector(ax2, (0, 0), -t_ev, ev_colors[i], lw=2.5)

    # Transform the other vectors
    for ang in other_angles:
        v = np.array([np.cos(ang), np.sin(ang)])
        tv = A @ v
        _draw_vector(ax2, (0, 0), tv, "gray", lw=1)

    ax2.set_xlim(-4, 4)
    ax2.set_ylim(-4, 4)
    ax2.set_aspect("equal")
    ax2.set_title(r"After: $A$ stretches eigenvectors, rotates the rest")
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$y$")
    ax2.legend(loc="upper left", fontsize=11)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "inner_product": ("Inner product geometry", lambda: plot_inner_product_panel(save_as="linalg_inner_product.png")),
        "orthogonal": ("Orthogonal functions", lambda: plot_orthogonal_functions(save_as="linalg_orthogonal_functions.png")),
        "projection": ("Fourier projection", lambda: plot_fourier_projection(save_as="linalg_projection.png")),
        "eigen": ("Eigenvalues and eigenvectors", lambda: plot_eigen_panel(save_as="linalg_eigen.png")),
    }

    parser = argparse.ArgumentParser(description="Linear algebra figures.")
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
