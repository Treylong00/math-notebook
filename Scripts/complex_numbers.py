"""Visualizing surfaces with poles and complex functions."""

import os
import numpy as np
import matplotlib.pyplot as plt
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
    x1 = np.linspace(a, b, n)
    x2 = np.linspace(a, b, n)
    return np.meshgrid(x1, x2)


# --- Real-valued surfaces with poles ---


def single_pole(x1, x2, radius_lowerbound=0.05):
    """1 / (x1^2 + x2^2) — single pole at the origin, masked by input radius."""
    title = r"$f(x_1, x_2) = \frac{1}{x_1^2 + x_2^2}$"
    r2 = x1**2 + x2**2
    surface = np.where(r2 > radius_lowerbound, 1 / r2, np.nan)
    return surface, title


def dipole(x1, x2, radius_lowerbound=0.1):
    """Sum of two poles at (-1, 0) and (1, 0)."""
    title = (
        r"$f(x_1, x_2) = \frac{1}{(x_1 - 1)^2 + x_2^2}"
        r" + \frac{1}{(x_1 + 1)^2 + x_2^2}$"
    )
    r2_right = (x1 - 1) ** 2 + x2**2
    r2_left = (x1 + 1) ** 2 + x2**2
    guard = (r2_right > radius_lowerbound) & (r2_left > radius_lowerbound)
    surface = np.where(guard, 1 / r2_right + 1 / r2_left, np.nan)
    return surface, title


def pole_antipole(x1, x2, radius_lowerbound=0.1):
    """Pole at (1, 0) minus pole at (-1, 0) — opposite signs create a saddle."""
    title = (
        r"$f(x_1, x_2) = \frac{1}{(x_1 - 1)^2 + x_2^2}"
        r" - \frac{1}{(x_1 + 1)^2 + x_2^2}$"
    )
    r2_right = (x1 - 1) ** 2 + x2**2
    r2_left = (x1 + 1) ** 2 + x2**2
    guard = (r2_right > radius_lowerbound) & (r2_left > radius_lowerbound)
    surface = np.where(guard, 1 / r2_right - 1 / r2_left, np.nan)
    return surface, title


# --- Complex functions (z -> w) ---


def complex_inverse(z):
    """f(z) = 1/z — single pole at origin."""
    return 1 / z


def complex_dipole(z):
    """f(z) = 1/(z^2 - 1) — poles at z = +-1."""
    return 1 / (z**2 - 1)


def complex_sinc(z):
    """f(z) = sin(z) / z."""
    return np.sin(z) / z


def complex_sqrt(z):
    """f(z) = sqrt(z) — branch cut along the negative real axis."""
    return np.sqrt(z)


def complex_exp(z):
    """f(z) = e^z."""
    return np.exp(z)


def complex_log(z):
    """f(z) = ln(z) — principal branch, branch cut along negative real axis."""
    return np.log(z)


def mobius_transform(z):
    """f(z) = (z + 1) / (z - 1)."""
    return (z + 1) / (z - 1)


# --- Extract surfaces from any complex function ---


def complex_modulus(x1, x2, f, height_upperbound=5):
    """Plot |f(z)| as a 3D surface."""
    z = x1 + 1j * x2
    w = f(z)
    surface = np.abs(w)
    surface = np.where(surface < height_upperbound, surface, np.nan)
    return surface


def complex_real(x1, x2, f, height_upperbound=5):
    """Plot Re(f(z)) as a 3D surface."""
    z = x1 + 1j * x2
    w = f(z)
    surface = np.real(w)
    surface = np.where(np.abs(w) < height_upperbound, surface, np.nan)
    return surface


def complex_imag(x1, x2, f, height_upperbound=5):
    """Plot Im(f(z)) as a 3D surface."""
    z = x1 + 1j * x2
    w = f(z)
    surface = np.imag(w)
    surface = np.where(np.abs(w) < height_upperbound, surface, np.nan)
    return surface


def complex_phase(x1, x2, f):
    """Compute arg(f(z)) for a phase portrait."""
    z = x1 + 1j * x2
    w = f(z)
    return np.angle(w)


# --- 2D curve plotting ---


def plot_curve(x, y, title, xlabel=r"$x$", ylabel=r"$f(x)$", save_as=None):
    """Plot a 2D curve. Optionally save to Figures/."""
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax.axvline(0, color="gray", linewidth=0.5, linestyle=":")
    ax.grid(True, alpha=0.3)
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )
    plt.show()


# --- 3D surface plotting ---


def plot_surface(x1, x2, surface, title, suptitle=None, save_as=None):
    """Render a 3D surface plot. Optionally save to Figures/."""
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(x1, x2, surface, cmap="viridis", edgecolor="none")
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_zlabel(r"$z$")
    ax.set_title(title)
    fig.suptitle(suptitle)
    ax.set_aspect("equal")
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )
    plt.show()


def plot_phase(x1, x2, phase, title, suptitle=None, save_as=None):
    """Render a 2D phase portrait colored by argument. Optionally save to Figures/."""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pcolormesh(
        x1, x2, phase, cmap="twilight", shading="auto", vmin=-np.pi, vmax=np.pi
    )
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title(title)
    ax.set_aspect("equal")
    if suptitle:
        fig.suptitle(suptitle)
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )
    plt.show()


def plot_polynomial_roots_panel(save_as=None):
    """Two-panel figure: real curve and contour plot with roots marked."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left panel: real curve, no x-intercepts
    x = np.linspace(-3, 3, 200)
    ax1.plot(x, x**2 + 1, label=r"$x^2 + 1$")
    ax1.plot(x, x**2 - 1, label=r"$x^2 - 1$", linestyle="--")
    ax1.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$f(x)$")
    ax1.set_title(r"$x^2-1$ has real roots, $x^2+1$ does not")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Right panel: contour plot of |z^2 + 1| with roots marked
    X1, X2 = make_grid(-2, 2, 500)
    Z = X1 + 1j * X2
    modulus = np.abs(Z**2 + 1)
    contour = ax2.contourf(X1, X2, modulus, levels=100, cmap="rocket")
    ax2.contour(X1, X2, modulus, levels=10, colors="k", linewidths=0.3, alpha=0.3)
    ax2.plot([0, 0], [1, -1], "ro", markersize=8, label=r"Roots: $z = \pm i$")
    ax2.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.axvline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.set_xlabel(r"$\mathrm{Re}(z)$")
    ax2.set_ylabel(r"$\mathrm{Im}(z)$")
    ax2.set_title(r"$|z^2 + 1|$ in the complex plane")
    ax2.legend()
    ax2.set_aspect("equal")
    fig.colorbar(contour, ax=ax2, label=r"$|z^2 + 1|$")

    plt.tight_layout()
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )
    plt.show()


def plot_sqrt_real(save_as=None):
    """Real sqrt(x) line plot."""
    x = np.linspace(-1, 4, 200)
    y = np.sqrt(np.where(x >= 0, x, np.nan))
    plot_curve(x, y, title=r"$f(x) = \sqrt{x}$, $x \in \mathbb{R}$", save_as=save_as)


def plot_sqrt_complex_panel(save_as=None):
    """Two-panel: |sqrt(z)| modulus contour and arg(sqrt(z)) phase portrait."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    X1, X2 = make_grid(-3, 3, 500)
    Z = X1 + 1j * X2
    W = np.sqrt(Z)

    # Left panel: modulus |sqrt(z)|
    modulus = np.abs(W)
    contour = ax1.contourf(X1, X2, modulus, levels=100, cmap="rocket")
    ax1.contour(X1, X2, modulus, levels=10, colors="k", linewidths=0.3, alpha=0.3)
    ax1.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.axvline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.set_xlabel(r"$\mathrm{Re}(z)$")
    ax1.set_ylabel(r"$\mathrm{Im}(z)$")
    ax1.set_title(r"$|\sqrt{z}|$")
    ax1.set_aspect("equal")
    fig.colorbar(contour, ax=ax1)

    # Right panel: arg(sqrt(z)) phase portrait
    phase = np.angle(W)
    ax2.pcolormesh(
        X1, X2, phase, cmap="twilight", shading="auto", vmin=-np.pi, vmax=np.pi
    )
    ax2.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.axvline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.set_xlabel(r"$\mathrm{Re}(z)$")
    ax2.set_ylabel(r"$\mathrm{Im}(z)$")
    ax2.set_title(r"$\arg(\sqrt{z})$")
    ax2.set_aspect("equal")

    plt.tight_layout()
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )
    plt.show()


def plot_exp_panel(save_as=None):
    """Two-panel: real e^x and sin(x)/cos(x) curves, then |e^z| and arg(e^z)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left panel: real exp and trig
    x = np.linspace(-2, 2, 200)
    ax1.plot(x, np.exp(x), label=r"$e^x$")
    ax1.plot(x, np.sin(x), label=r"$\sin(x)$", linestyle="--")
    ax1.plot(x, np.cos(x), label=r"$\cos(x)$", linestyle=":")
    ax1.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.axvline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$f(x)$")
    ax1.set_title(r"In $\mathbb{R}$: unrelated functions")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Right panel: arg(e^z) phase portrait — shows rotation
    X1, X2 = make_grid(-3, 3, 500)
    phase = complex_phase(X1, X2, complex_exp)
    ax2.pcolormesh(
        X1, X2, phase, cmap="twilight", shading="auto", vmin=-np.pi, vmax=np.pi
    )
    ax2.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.axvline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.set_xlabel(r"$\mathrm{Re}(z)$")
    ax2.set_ylabel(r"$\mathrm{Im}(z)$")
    ax2.set_title(r"$\arg(e^z)$ — phase is $\mathrm{Im}(z)$")
    ax2.set_aspect("equal")

    plt.tight_layout()
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )
    plt.show()


def plot_log_panel(save_as=None):
    """Two-panel: |ln(z)| modulus and arg(ln(z)) phase portrait."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    X1, X2 = make_grid(-3, 3, 500)
    Z = X1 + 1j * X2
    W = np.log(Z)

    # Left panel: modulus |ln(z)|
    modulus = np.abs(W)
    contour = ax1.contourf(X1, X2, modulus, levels=100, cmap="rocket")
    ax1.contour(X1, X2, modulus, levels=10, colors="k", linewidths=0.3, alpha=0.3)
    ax1.plot(0, 0, "wo", markersize=6, markeredgecolor="k")
    ax1.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.axvline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.set_xlabel(r"$\mathrm{Re}(z)$")
    ax1.set_ylabel(r"$\mathrm{Im}(z)$")
    ax1.set_title(r"$|\ln(z)|$")
    ax1.set_aspect("equal")
    fig.colorbar(contour, ax=ax1)

    # Right panel: arg(ln(z)) phase portrait — branch cut visible
    phase = np.angle(W)
    ax2.pcolormesh(
        X1, X2, phase, cmap="twilight", shading="auto", vmin=-np.pi, vmax=np.pi
    )
    ax2.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.axvline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.set_xlabel(r"$\mathrm{Re}(z)$")
    ax2.set_ylabel(r"$\mathrm{Im}(z)$")
    ax2.set_title(r"$\arg(\ln(z))$")
    ax2.set_aspect("equal")

    plt.tight_layout()
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )
    plt.show()


def _quadratic(z):
    return z**2 - 2 * z + 5


def plot_quadratic_roots_panel(save_as=None):
    """Three-panel figure for x^2 - 2x + 5: real slice, imaginary slice, contour."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

    # Panel 1: f(x) along real axis (z = x + 0i)
    x = np.linspace(-3, 5, 200)
    y = _quadratic(x)
    ax1.plot(x, y)
    ax1.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$f(x)$")
    ax1.set_title(r"Along the real axis: $z = x$")
    ax1.grid(True, alpha=0.3)

    # Panel 2: |f(z)| along imaginary axis (z = 0 + yi)
    y_vals = np.linspace(-4, 4, 200)
    z_imag = 1j * y_vals
    ax2.plot(y_vals, np.abs(_quadratic(z_imag)))
    ax2.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.set_xlabel(r"$y$")
    ax2.set_ylabel(r"$|f(iy)|$")
    ax2.set_title(r"Along the imaginary axis: $z = iy$")
    ax2.grid(True, alpha=0.3)

    # Panel 3: contour plot of |f(z)| with roots marked
    X1, X2 = make_grid(-3, 5, 500)
    Z = X1 + 1j * X2
    modulus = np.abs(_quadratic(Z))
    contour = ax3.contourf(X1, X2, modulus, levels=100, cmap="rocket")
    ax3.contour(X1, X2, modulus, levels=10, colors="k", linewidths=0.3, alpha=0.3)
    # Roots at 1 + 2i and 1 - 2i
    ax3.plot([1, 1], [2, -2], "ro", markersize=8, label=r"Roots: $1 \pm 2i$")
    ax3.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax3.axvline(0, color="gray", linewidth=0.5, linestyle=":")
    ax3.set_xlabel(r"$\mathrm{Re}(z)$")
    ax3.set_ylabel(r"$\mathrm{Im}(z)$")
    ax3.set_title(r"$|z^2 - 2z + 5|$ in the complex plane")
    ax3.legend()
    ax3.set_aspect("equal")
    fig.colorbar(contour, ax=ax3, label=r"$|z^2 - 2z + 5|$")

    plt.tight_layout()
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )
    plt.show()


def plot_euler_vectors(save_as=None):
    """Two-panel: polar form with vectors on contour, and phase portrait."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

    X1, X2 = make_grid(-3, 4, 500)
    Z = X1 + 1j * X2

    # Left panel: contour with Euler vectors
    modulus = np.abs(_quadratic(Z))
    ax1.contourf(X1, X2, modulus, levels=100, cmap="rocket")
    ax1.contour(X1, X2, modulus, levels=10, colors="k", linewidths=0.3, alpha=0.3)

    roots = [1 + 2j, 1 - 2j]
    for z in roots:
        a, b = z.real, z.imag
        r = abs(z)
        theta = np.angle(z)

        ax1.annotate(
            "",
            xy=(a, b),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="white", lw=2),
        )
        ax1.plot(a, b, "ro", markersize=8)

        sign = "+" if b >= 0 else "-"
        cartesian = rf"$z = {int(a)} {sign} {int(abs(b))}i$"
        polar = rf"$z = \sqrt{{{int(r**2)}}} \, e^{{i \cdot {theta:.2f}}}$"

        offset_y = 0.35 if b >= 0 else -0.35
        va = "bottom" if b >= 0 else "top"
        ax1.text(
            a + 0.15,
            b + offset_y,
            cartesian + "\n" + polar,
            fontsize=10,
            color="white",
            va=va,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="black", alpha=0.7),
        )

        arc_r = 0.6
        arc_angles = np.linspace(0, theta, 50)
        ax1.plot(
            arc_r * np.cos(arc_angles),
            arc_r * np.sin(arc_angles),
            color="white",
            lw=1.5,
            linestyle="--",
        )
        mid = theta / 2
        ax1.text(
            arc_r * 1.3 * np.cos(mid),
            arc_r * 1.3 * np.sin(mid),
            r"$\theta$",
            fontsize=11,
            color="white",
            ha="center",
            va="center",
        )

    ax1.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.axvline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.set_xlabel(r"$\mathrm{Re}(z)$")
    ax1.set_ylabel(r"$\mathrm{Im}(z)$")
    ax1.set_title(r"$|z^2 - 2z + 5|$ — polar form")
    ax1.set_aspect("equal")

    # Right panel: phase portrait
    phase = np.angle(_quadratic(Z))
    ax2.pcolormesh(
        X1, X2, phase, cmap="twilight", shading="auto", vmin=-np.pi, vmax=np.pi
    )
    ax2.plot([1, 1], [2, -2], "ro", markersize=8)
    ax2.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.axvline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.set_xlabel(r"$\mathrm{Re}(z)$")
    ax2.set_ylabel(r"$\mathrm{Im}(z)$")
    ax2.set_title(r"$\arg(z^2 - 2z + 5)$")
    ax2.set_aspect("equal")

    plt.tight_layout()
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )
    plt.show()


def main():
    import argparse

    figures = {
        "polynomial_roots": ("Polynomial root comparison", lambda: plot_polynomial_roots_panel(save_as="polynomial_roots_panel.png")),
        "quadratic_roots": ("Quadratic roots in complex plane", lambda: plot_quadratic_roots_panel(save_as="quadratic_roots_panel.png")),
        "euler": ("Euler vectors on contour", lambda: plot_euler_vectors(save_as="euler_vectors.png")),
        "sqrt_real": ("Square root on real line", lambda: plot_sqrt_real(save_as="sqrt_real.png")),
        "sqrt_complex": ("Complex square root panel", lambda: plot_sqrt_complex_panel(save_as="sqrt_complex_panel.png")),
        "exp": ("Complex exponential panel", lambda: plot_exp_panel(save_as="exp_panel.png")),
        "log": ("Complex logarithm panel", lambda: plot_log_panel(save_as="log_panel.png")),
    }

    parser = argparse.ArgumentParser(description="Complex-number visualizations.")
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
