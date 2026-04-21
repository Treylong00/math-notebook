"""Visualizing Hilbert spaces, L^2 membership, completeness, and quantum mechanics."""

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


# --- Functions for L^2 membership demonstration ---


def gaussian(x):
    """f(x) = exp(-x^2) -- in L^2."""
    return np.exp(-(x**2))


def inv_x(x):
    """f(x) = 1/|x| -- not in L^2 (diverges at origin and decays too slowly)."""
    return np.where(np.abs(x) > 0.05, 1.0 / np.abs(x), np.nan)


def sinc(x):
    """f(x) = sin(x)/x -- in L^2."""
    return np.sinc(x / np.pi)  # np.sinc(t) = sin(pi*t)/(pi*t), so sinc(x/pi)=sin(x)/x


def inv_sqrt_abs(x):
    """f(x) = 1/sqrt(|x|) -- not in L^2 near the origin."""
    return np.where(np.abs(x) > 0.01, 1.0 / np.sqrt(np.abs(x)), np.nan)


# --- Plot functions ---


def plot_l2_membership_panel(save_as=None):
    """Four-panel figure showing functions in and not in L^2.

    Top row: f(x). Bottom row: |f(x)|^2 with shaded area representing the integral.
    Green panels are in L^2 (finite integral), red panels are not.
    """
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))

    x_wide = np.linspace(-6, 6, 1000)
    x_narrow = np.linspace(-4, 4, 1000)

    functions = [
        (gaussian, x_wide, r"$e^{-x^2}$", True, r"\sqrt{\pi/2}"),
        (sinc, x_wide, r"$\frac{\sin x}{x}$", True, r"\pi"),
        (inv_x, x_narrow, r"$\frac{1}{|x|}$", False, r"\infty"),
        (inv_sqrt_abs, x_narrow, r"$\frac{1}{\sqrt{|x|}}$", False, r"\infty"),
    ]

    for col, (func, x, label, in_l2, integral_val) in enumerate(functions):
        y = func(x)
        y_sq = y**2
        color = sns.color_palette("deep")[2] if in_l2 else sns.color_palette("deep")[3]
        status = r"\in L^2" if in_l2 else r"\notin L^2"

        # Top row: f(x)
        ax_top = axes[0, col]
        ax_top.plot(x, y, color=color, linewidth=1.5)
        ax_top.set_title(f"{label}", fontsize=14)
        ax_top.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax_top.axvline(0, color="gray", linewidth=0.5, linestyle=":")
        ax_top.set_xlabel(r"$x$")
        if col == 0:
            ax_top.set_ylabel(r"$f(x)$")
        ax_top.grid(True, alpha=0.3)

        # Bottom row: |f(x)|^2 with shading
        ax_bot = axes[1, col]
        ax_bot.plot(x, y_sq, color=color, linewidth=1.5)
        ax_bot.fill_between(x, 0, y_sq, alpha=0.3, color=color)
        ax_bot.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax_bot.axvline(0, color="gray", linewidth=0.5, linestyle=":")
        ax_bot.set_xlabel(r"$x$")
        if col == 0:
            ax_bot.set_ylabel(r"$|f(x)|^2$")
        ax_bot.set_title(
            rf"$\int |f|^2 \, dx = {integral_val}$ — ${status}$", fontsize=11
        )
        ax_bot.grid(True, alpha=0.3)

        # Cap y-axis for divergent functions
        if not in_l2:
            ax_top.set_ylim(-0.5, 8)
            ax_bot.set_ylim(-0.5, 15)

    fig.suptitle(
        r"$L^2$ Membership: Which functions have finite $\int |f(x)|^2 \, dx$?",
        fontsize=15,
        y=1.02,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_completeness_panel(save_as=None):
    """Two-panel figure: Fourier partial sums converging to a square wave,
    and the L^2 norm of the error decreasing to zero.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    x = np.linspace(-np.pi, np.pi, 1000)

    # Target: square wave
    def square_wave(t):
        """Square wave on [-pi, pi]: +1 on (0, pi), -1 on (-pi, 0)."""
        return np.sign(t)

    target = square_wave(x)

    # Fourier partial sums of the square wave: sum_{k=0}^{N} (4/pi) * sin((2k+1)x)/(2k+1)
    ns = [1, 3, 5, 10, 25, 50]
    colors = sns.color_palette("deep", len(ns))
    norms = []
    n_range = np.arange(1, 61)

    # Left panel: partial sums
    ax1.plot(x, target, "k--", linewidth=2, label="Target", alpha=0.5)
    for idx, n in enumerate(ns):
        partial = np.zeros_like(x)
        for k in range(n):
            partial += (4 / np.pi) * np.sin((2 * k + 1) * x) / (2 * k + 1)
        ax1.plot(x, partial, color=colors[idx], linewidth=1, label=rf"$S_{{{n}}}$")

    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$f(x)$")
    ax1.set_title("Fourier partial sums converging to a square wave")
    ax1.legend(fontsize=9, ncol=2)
    ax1.grid(True, alpha=0.3)

    # Right panel: L^2 norm of error
    for n in n_range:
        partial = np.zeros_like(x)
        for k in range(n):
            partial += (4 / np.pi) * np.sin((2 * k + 1) * x) / (2 * k + 1)
        error = target - partial
        l2_norm = np.sqrt(np.trapezoid(error**2, x))
        norms.append(l2_norm)

    ax2.plot(n_range, norms, "o-", markersize=3, color=sns.color_palette("deep")[0])
    ax2.set_xlabel(r"Number of terms $N$")
    ax2.set_ylabel(r"$\|f - S_N\|_{L^2}$")
    ax2.set_title(r"$L^2$ error $\to 0$: completeness in action")
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(bottom=0)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_distance_panel(save_as=None):
    """Two-panel figure: distance between functions as shaded |f-g|^2,
    and a conceptual function-space diagram.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Left panel: distance as shaded area
    x = np.linspace(-np.pi, np.pi, 500)

    def f_func(t):
        """f(x) = cos(x)."""
        return np.cos(t)

    def g_func(t):
        """g(x) = 0.5 * cos(x) + 0.3 * sin(2x)."""
        return 0.5 * np.cos(t) + 0.3 * np.sin(2 * t)

    f_vals = f_func(x)
    g_vals = g_func(x)
    diff_sq = (f_vals - g_vals) ** 2

    ax1.plot(x, f_vals, linewidth=2, label=r"$f(x) = \cos x$")
    ax1.plot(
        x,
        g_vals,
        linewidth=2,
        label=r"$g(x) = \frac{1}{2}\cos x + \frac{3}{10}\sin 2x$",
    )
    ax1.fill_between(
        x,
        f_vals,
        g_vals,
        alpha=0.3,
        color=sns.color_palette("deep")[3],
        label=r"$|f - g|$",
    )
    ax1.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$f(x)$")
    dist_val = np.sqrt(np.trapezoid(diff_sq, x))
    ax1.set_title(rf"$\|f - g\|_{{L^2}} = {dist_val:.3f}$")
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Right panel: conceptual function space diagram
    ax2.set_xlim(-0.5, 4)
    ax2.set_ylim(-0.5, 3.5)
    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_title("Functions as points in a space", fontsize=13)

    # Draw an ellipse to represent the space
    theta = np.linspace(0, 2 * np.pi, 200)
    ellipse_x = 2.0 + 1.8 * np.cos(theta)
    ellipse_y = 1.5 + 1.3 * np.sin(theta)
    ax2.plot(ellipse_x, ellipse_y, "k-", linewidth=1.5, alpha=0.4)
    ax2.text(3.5, 2.7, r"$L^2$", fontsize=16, fontstyle="italic", alpha=0.6)

    # Points for f, g, and their projection
    f_pt = (1.2, 2.2)
    g_pt = (2.8, 1.0)
    origin = (0.5, 0.5)

    ax2.plot(*f_pt, "o", color=sns.color_palette("deep")[0], markersize=10, zorder=5)
    ax2.text(
        f_pt[0] - 0.15,
        f_pt[1] + 0.2,
        r"$f$",
        fontsize=14,
        color=sns.color_palette("deep")[0],
        fontweight="bold",
    )

    ax2.plot(*g_pt, "o", color=sns.color_palette("deep")[1], markersize=10, zorder=5)
    ax2.text(
        g_pt[0] + 0.15,
        g_pt[1] + 0.2,
        r"$g$",
        fontsize=14,
        color=sns.color_palette("deep")[1],
        fontweight="bold",
    )

    # Distance line between f and g
    ax2.plot(
        [f_pt[0], g_pt[0]],
        [f_pt[1], g_pt[1]],
        "--",
        color=sns.color_palette("deep")[3],
        linewidth=2,
    )
    mid = ((f_pt[0] + g_pt[0]) / 2, (f_pt[1] + g_pt[1]) / 2)
    ax2.text(
        mid[0] + 0.1,
        mid[1] + 0.2,
        r"$\|f - g\|$",
        fontsize=12,
        color=sns.color_palette("deep")[3],
        fontweight="bold",
    )

    # Origin / zero function
    ax2.plot(*origin, "o", color="gray", markersize=8, zorder=5)
    ax2.text(origin[0] - 0.1, origin[1] - 0.25, r"$0$", fontsize=13, color="gray")

    # Vectors from origin
    for pt, col in [
        (f_pt, sns.color_palette("deep")[0]),
        (g_pt, sns.color_palette("deep")[1]),
    ]:
        arrow = FancyArrowPatch(
            origin,
            pt,
            arrowstyle="->,head_width=6,head_length=6",
            color=col,
            linewidth=1.5,
            alpha=0.5,
        )
        ax2.add_patch(arrow)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_normalization_panel(save_as=None):
    """Two-panel figure: a wavefunction before and after normalization,
    with shaded integral showing |psi|^2 = 1.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    x = np.linspace(-5, 5, 1000)

    # Unnormalized wavefunction: a Gaussian-ish bump
    def psi_unnorm(t):
        """Unnormalized wavefunction: 2 * exp(-t^2 / 2)."""
        return 2.0 * np.exp(-(t**2) / 2)

    psi_raw = psi_unnorm(x)
    psi_sq_raw = psi_raw**2
    raw_integral = np.trapezoid(psi_sq_raw, x)

    # Left panel: unnormalized
    ax1.plot(
        x, psi_raw, linewidth=2, color=sns.color_palette("deep")[0], label=r"$\psi(x)$"
    )
    ax1.fill_between(x, 0, psi_sq_raw, alpha=0.3, color=sns.color_palette("deep")[3])
    ax1.plot(
        x,
        psi_sq_raw,
        linewidth=1.5,
        color=sns.color_palette("deep")[3],
        linestyle="--",
        label=r"$|\psi(x)|^2$",
    )
    ax1.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.set_xlabel(r"$x$")
    ax1.set_title(rf"Before: $\int |\psi|^2 \, dx = {raw_integral:.2f}$", fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-0.5, 4.5)

    # Right panel: normalized
    norm_const = np.sqrt(raw_integral)
    psi_normed = psi_raw / norm_const
    psi_sq_normed = psi_normed**2
    normed_integral = np.trapezoid(psi_sq_normed, x)

    ax2.plot(
        x,
        psi_normed,
        linewidth=2,
        color=sns.color_palette("deep")[0],
        label=r"$\hat{\psi}(x) = \psi / \|\psi\|$",
    )
    ax2.fill_between(x, 0, psi_sq_normed, alpha=0.3, color=sns.color_palette("deep")[2])
    ax2.plot(
        x,
        psi_sq_normed,
        linewidth=1.5,
        color=sns.color_palette("deep")[2],
        linestyle="--",
        label=r"$|\hat{\psi}(x)|^2$",
    )
    ax2.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.set_xlabel(r"$x$")
    ax2.set_title(
        rf"After: $\int |\hat{{\psi}}|^2 \, dx = {normed_integral:.2f}$",
        fontsize=13,
    )
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.5, 4.5)

    fig.suptitle(r"Normalization: rescaling so $\|\psi\| = 1$", fontsize=15, y=1.02)
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "l2_membership": ("L2 membership criteria", lambda: plot_l2_membership_panel(save_as="hilbert_l2_membership.png")),
        "completeness": ("Completeness and convergence", lambda: plot_completeness_panel(save_as="hilbert_completeness.png")),
        "distance": ("L2 distance metric", lambda: plot_distance_panel(save_as="hilbert_distance.png")),
        "normalization": ("Normalization of states", lambda: plot_normalization_panel(save_as="hilbert_normalization.png")),
    }

    parser = argparse.ArgumentParser(description="Hilbert space figures.")
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
