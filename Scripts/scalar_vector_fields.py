"""Visualizing scalar and vector fields in R^2."""

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


# --- Scalar fields f: R^2 -> R ---


def scalar_paraboloid(x, y):
    """f(x, y) = x^2 + y^2"""
    return x**2 + y**2


def scalar_saddle(x, y):
    """f(x, y) = x^2 - y^2"""
    return x**2 - y**2


def scalar_gaussian(x, y):
    """f(x, y) = e^{-(x^2 + y^2)}"""
    return np.exp(-(x**2 + y**2))


def scalar_gravitational(x, y, eps=0.1):
    """f(x, y) = -1 / sqrt(x^2 + y^2) — gravitational potential, softened."""
    return -1 / np.sqrt(x**2 + y**2 + eps**2)


# --- Vector fields F: R^2 -> R^2 ---


def field_gradient(scalar_f, x, y, dx=1e-6):
    """Compute the gradient of a scalar field numerically."""
    df_dx = (scalar_f(x + dx, y) - scalar_f(x - dx, y)) / (2 * dx)
    df_dy = (scalar_f(x, y + dx) - scalar_f(x, y - dx)) / (2 * dx)
    return df_dx, df_dy


def field_rotation(x, y):
    """F(x, y) = (-y, x) — counterclockwise rotation."""
    return -y, x


def field_source(x, y, eps=0.1):
    """F(x, y) = (x, y) / r — radial outward, unit magnitude."""
    r = np.sqrt(x**2 + y**2 + eps**2)
    return x / r, y / r


def field_sink(x, y, eps=0.1):
    """F(x, y) = -(x, y) / r — radial inward."""
    u, v = field_source(x, y, eps)
    return -u, -v


def field_vortex(x, y, eps=0.1):
    """F(x, y) = (-y, x) / r — rotation with 1/r magnitude."""
    r = np.sqrt(x**2 + y**2 + eps**2)
    return -y / r, x / r


# --- Differential operators ---


def divergence(field_f, x, y, dx=1e-6):
    """Compute divergence of a vector field numerically: du/dx + dv/dy."""
    u_plus, _ = field_f(x + dx, y)
    u_minus, _ = field_f(x - dx, y)
    _, v_plus = field_f(x, y + dx)
    _, v_minus = field_f(x, y - dx)
    return (u_plus - u_minus) / (2 * dx) + (v_plus - v_minus) / (2 * dx)


def curl_2d(field_f, x, y, dx=1e-6):
    """Compute 2D curl of a vector field numerically: dv/dx - du/dy."""
    _, v_plus = field_f(x + dx, y)
    _, v_minus = field_f(x - dx, y)
    u_plus, _ = field_f(x, y + dx)
    u_minus, _ = field_f(x, y - dx)
    return (v_plus - v_minus) / (2 * dx) - (u_plus - u_minus) / (2 * dx)


# --- Panel plot functions ---


def plot_scalar_fields_panel(save_as=None):
    """Three-panel contour plots: paraboloid, saddle, gaussian."""
    X, Y = make_grid(-3, 3, 500)
    fields = [
        (scalar_paraboloid, r"$f(x,y) = x^2 + y^2$"),
        (scalar_saddle, r"$f(x,y) = x^2 - y^2$"),
        (scalar_gaussian, r"$f(x,y) = e^{-(x^2+y^2)}$"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for ax, (f, title) in zip(axes, fields):
        Z = f(X, Y)
        contour = ax.contourf(X, Y, Z, levels=100, cmap="rocket")
        ax.contour(X, Y, Z, levels=10, colors="k", linewidths=0.3, alpha=0.3)
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")
        ax.set_title(title)
        ax.set_aspect("equal")
        fig.colorbar(contour, ax=ax)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_gradient_panel(save_as=None):
    """Three-panel: each scalar field with gradient vectors overlaid on contours."""
    X, Y = make_grid(-3, 3, 500)
    fields = [
        (scalar_paraboloid, r"$\nabla(x^2 + y^2)$"),
        (scalar_saddle, r"$\nabla(x^2 - y^2)$"),
        (scalar_gaussian, r"$\nabla e^{-(x^2+y^2)}$"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    stride = 25
    for ax, (f, title) in zip(axes, fields):
        Z = f(X, Y)
        ax.contourf(X, Y, Z, levels=100, cmap="rocket")
        ax.contour(X, Y, Z, levels=10, colors="k", linewidths=0.3, alpha=0.3)

        u, v = field_gradient(f, X, Y)
        ax.quiver(
            X[::stride, ::stride],
            Y[::stride, ::stride],
            u[::stride, ::stride],
            v[::stride, ::stride],
            color="white",
            alpha=0.8,
            scale=60,
            width=0.004,
        )
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")
        ax.set_title(title)
        ax.set_aspect("equal")

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_vector_fields_panel(save_as=None):
    """Three-panel streamlines: rotation, source, vortex."""
    X, Y = make_grid(-3, 3, 500)
    fields = [
        (field_rotation, r"Rotation: $(-y, x)$"),
        (field_source, r"Source: $(x, y)/r$"),
        (field_vortex, r"Vortex: $(-y, x)/r$"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for ax, (f, title) in zip(axes, fields):
        u, v = f(X, Y)
        magnitude = np.sqrt(u**2 + v**2)
        strm = ax.streamplot(
            X[0, :],
            Y[:, 0],
            u,
            v,
            color=magnitude,
            cmap="rocket",
            density=1.5,
            linewidth=1,
            arrowsize=1.2,
        )
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")
        ax.set_title(title)
        ax.set_aspect("equal")
        fig.colorbar(strm.lines, ax=ax, label=r"$\|\mathbf{F}\|$")

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_divergence_panel(save_as=None):
    """Two-panel: source and rotation fields with divergence contour underlay."""
    X, Y = make_grid(-3, 3, 500)
    fields = [
        (field_source, r"Source — $\nabla \cdot \mathbf{F} > 0$"),
        (field_rotation, r"Rotation — $\nabla \cdot \mathbf{F} = 0$"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, (f, title) in zip(axes, fields):
        div = divergence(f, X, Y)
        contour = ax.contourf(X, Y, div, levels=100, cmap="rocket")
        fig.colorbar(contour, ax=ax, label=r"$\nabla \cdot \mathbf{F}$")

        u, v = f(X, Y)
        ax.streamplot(
            X[0, :],
            Y[:, 0],
            u,
            v,
            color="white",
            density=1.2,
            linewidth=0.7,
            arrowsize=1,
        )
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")
        ax.set_title(title)
        ax.set_aspect("equal")

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_curl_panel(save_as=None):
    """Two-panel: rotation and source fields with curl contour underlay."""
    X, Y = make_grid(-3, 3, 500)
    fields = [
        (field_rotation, r"Rotation — $\nabla \times \mathbf{F} = 2$"),
        (field_source, r"Source — $\nabla \times \mathbf{F} = 0$"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, (f, title) in zip(axes, fields):
        c = curl_2d(f, X, Y)
        contour = ax.contourf(X, Y, c, levels=100, cmap="rocket")
        fig.colorbar(contour, ax=ax, label=r"$\nabla \times \mathbf{F}$")

        u, v = f(X, Y)
        ax.streamplot(
            X[0, :],
            Y[:, 0],
            u,
            v,
            color="white",
            density=1.2,
            linewidth=0.7,
            arrowsize=1,
        )
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")
        ax.set_title(title)
        ax.set_aspect("equal")

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_gravitational_panel(save_as=None):
    """Two-panel: gravitational potential contours + gravitational field streamlines."""
    X, Y = make_grid(-3, 3, 500)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: scalar potential
    phi = scalar_gravitational(X, Y)
    contour = ax1.contourf(X, Y, phi, levels=100, cmap="rocket")
    ax1.contour(X, Y, phi, levels=15, colors="k", linewidths=0.3, alpha=0.3)
    ax1.plot(0, 0, "wo", markersize=6, markeredgecolor="k")
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$y$")
    ax1.set_title(r"Potential $\phi = -1/r$")
    ax1.set_aspect("equal")
    fig.colorbar(contour, ax=ax1, label=r"$\phi$")

    # Right: gravitational field g = -grad(phi)
    ax2.contourf(X, Y, phi, levels=100, cmap="rocket")
    gx, gy = field_gradient(scalar_gravitational, X, Y)
    gx, gy = -gx, -gy  # g = -grad(phi)
    ax2.streamplot(
        X[0, :],
        Y[:, 0],
        gx,
        gy,
        color="white",
        density=1.5,
        linewidth=0.8,
        arrowsize=1.2,
    )
    ax2.plot(0, 0, "wo", markersize=6, markeredgecolor="k")
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$y$")
    ax2.set_title(r"Field $\mathbf{g} = -\nabla\phi$")
    ax2.set_aspect("equal")

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "scalar_fields": ("Scalar field examples", lambda: plot_scalar_fields_panel(save_as="scalar_fields_panel.png")),
        "gradient": ("Gradient overlay panel", lambda: plot_gradient_panel(save_as="gradient_panel.png")),
        "vector_fields": ("Vector field examples", lambda: plot_vector_fields_panel(save_as="vector_fields_panel.png")),
        "divergence": ("Divergence panel", lambda: plot_divergence_panel(save_as="divergence_panel.png")),
        "curl": ("Curl panel", lambda: plot_curl_panel(save_as="curl_panel.png")),
        "gravitational": ("Gravitational field panel", lambda: plot_gravitational_panel(save_as="gravitational_panel.png")),
    }

    parser = argparse.ArgumentParser(description="Scalar and vector field visualizations.")
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
