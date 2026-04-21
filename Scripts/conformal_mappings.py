"""Conformal mappings: grid deformations, angle preservation, critical points,
Möbius transforms, and the Joukowski airfoil.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Arc, Wedge

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


def _draw_mapped_grid(ax, f, x_range, y_range, nx=11, ny=11):
    """Draw horizontal and vertical grid lines mapped through a complex function f."""
    colors = sns.color_palette("deep")

    for lines, n_lines, color, fixed_is_y in [
        ("horiz", ny, colors[0], True),
        ("vert", nx, colors[1], False),
    ]:
        rng_fixed = y_range if fixed_is_y else x_range
        rng_param = x_range if fixed_is_y else y_range

        for val in np.linspace(rng_fixed[0], rng_fixed[1], n_lines):
            t = np.linspace(rng_param[0], rng_param[1], 500)
            z = (t + 1j * val) if fixed_is_y else (val + 1j * t)

            with np.errstate(divide="ignore", invalid="ignore"):
                w = f(z)

            w_re = np.real(w).copy()
            w_im = np.imag(w).copy()

            bad = ~np.isfinite(w_re) | ~np.isfinite(w_im)
            w_re[bad] = np.nan
            w_im[bad] = np.nan

            # Break line at large jumps (near poles / branch cuts)
            dw = np.sqrt(np.diff(w_re) ** 2 + np.diff(w_im) ** 2)
            jumps = np.concatenate([[False], dw > 8])
            w_re[jumps] = np.nan
            w_im[jumps] = np.nan

            ax.plot(w_re, w_im, color=color, linewidth=0.8, alpha=0.7)


# --- 1. Grid deformation gallery ---


def plot_grid_gallery(save_as=None):
    """Four-panel grid deformations under z^2, e^z, 1/z, and a Möbius transform."""
    maps = [
        (r"$f(z) = z^2$", lambda z: z**2, (-1.5, 1.5), (-1.5, 1.5), (-4, 4), (-4, 4)),
        (
            r"$f(z) = e^z$",
            np.exp,
            (-2, 2),
            (-np.pi, np.pi),
            (-8, 8),
            (-8, 8),
        ),
        (
            r"$f(z) = 1/z$",
            lambda z: 1 / z,
            (0.3, 2.5),
            (-1.5, 1.5),
            (-3.5, 3.5),
            (-3.5, 3.5),
        ),
        (
            r"$f(z) = \frac{z-1}{z+1}$",
            lambda z: (z - 1) / (z + 1),
            (0.1, 5),
            (-3, 3),
            (-1.8, 1.8),
            (-1.8, 1.8),
        ),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(12, 12))

    for ax, (title, f, xr, yr, wxr, wyr) in zip(axes.flat, maps):
        _draw_mapped_grid(ax, f, xr, yr)
        ax.set_title(title, fontsize=14)
        ax.set_xlim(*wxr)
        ax.set_ylim(*wyr)
        ax.set_aspect("equal")
        ax.set_xlabel(r"$\mathrm{Re}(w)$")
        ax.set_ylabel(r"$\mathrm{Im}(w)$")

    fig.suptitle(
        "Conformal maps deform grids but preserve the angle at every crossing",
        fontsize=13,
        y=1.01,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- 2. Angle preservation ---


def plot_angle_preservation(save_as=None):
    """Two curves crossing at 60° in the z-plane and their images under z^2,
    showing that the angle between them is preserved.
    """
    colors = sns.color_palette("deep")

    z0 = 1.0 + 0.5j
    w0 = z0**2

    alpha1 = 0.0  # first curve direction
    alpha2 = np.pi / 3  # second curve direction (60°)

    fp = 2 * z0  # f'(z0)
    rotation = np.angle(fp)

    mapped_alpha1 = alpha1 + rotation
    mapped_alpha2 = alpha2 + rotation

    t = np.linspace(-0.8, 0.8, 500)
    curve1_z = z0 + t * np.exp(1j * alpha1)
    curve2_z = z0 + t * np.exp(1j * alpha2)
    curve1_w = curve1_z**2
    curve2_w = curve2_z**2

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # z-plane
    ax1.plot(
        curve1_z.real, curve1_z.imag, color=colors[0], linewidth=2.5, label="Curve 1"
    )
    ax1.plot(
        curve2_z.real, curve2_z.imag, color=colors[1], linewidth=2.5, label="Curve 2"
    )
    ax1.plot(z0.real, z0.imag, "ko", markersize=6, zorder=5)

    arc_r = 0.25
    arc1 = Arc(
        (z0.real, z0.imag),
        2 * arc_r,
        2 * arc_r,
        angle=0,
        theta1=np.degrees(alpha1),
        theta2=np.degrees(alpha2),
        color=colors[3],
        linewidth=2.5,
    )
    ax1.add_patch(arc1)
    mid = (alpha1 + alpha2) / 2
    ax1.annotate(
        r"$60°$",
        xy=(
            z0.real + (arc_r + 0.12) * np.cos(mid),
            z0.imag + (arc_r + 0.12) * np.sin(mid),
        ),
        fontsize=14,
        color=colors[3],
        fontweight="bold",
        ha="center",
    )

    ax1.set_title(r"$z$-plane", fontsize=14)
    ax1.set_xlabel(r"$\mathrm{Re}(z)$")
    ax1.set_ylabel(r"$\mathrm{Im}(z)$")
    ax1.set_aspect("equal")
    ax1.legend(fontsize=10)

    # w-plane
    ax2.plot(
        curve1_w.real,
        curve1_w.imag,
        color=colors[0],
        linewidth=2.5,
        label="Image of curve 1",
    )
    ax2.plot(
        curve2_w.real,
        curve2_w.imag,
        color=colors[1],
        linewidth=2.5,
        label="Image of curve 2",
    )
    ax2.plot(w0.real, w0.imag, "ko", markersize=6, zorder=5)

    arc2 = Arc(
        (w0.real, w0.imag),
        2 * arc_r,
        2 * arc_r,
        angle=0,
        theta1=np.degrees(mapped_alpha1),
        theta2=np.degrees(mapped_alpha2),
        color=colors[3],
        linewidth=2.5,
    )
    ax2.add_patch(arc2)
    mid_w = (mapped_alpha1 + mapped_alpha2) / 2
    ax2.annotate(
        r"$60°$",
        xy=(
            w0.real + (arc_r + 0.12) * np.cos(mid_w),
            w0.imag + (arc_r + 0.12) * np.sin(mid_w),
        ),
        fontsize=14,
        color=colors[3],
        fontweight="bold",
        ha="center",
    )

    ax2.set_title(r"$w = z^2$", fontsize=14)
    ax2.set_xlabel(r"$\mathrm{Re}(w)$")
    ax2.set_ylabel(r"$\mathrm{Im}(w)$")
    ax2.set_aspect("equal")
    ax2.legend(fontsize=10)

    fig.suptitle(
        r"Angle preservation: the $60°$ crossing is mapped to a $60°$ crossing",
        fontsize=13,
        y=1.01,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- 2b. Jacobian element ---


def plot_jacobian_element(save_as=None):
    """Differential area element at z₀ = 1+0.5i mapped through z², showing
    the Cauchy-Riemann equations and the Jacobian as a scaled rotation.
    """
    colors = sns.color_palette("deep")

    z0 = 1.0 + 0.5j
    w0 = z0**2  # 0.75 + 1.0j
    h = 0.2

    # f(z) = z²: u = x² - y², v = 2xy
    # At (x, y) = (1, 0.5): u_x = 2, u_y = -1, v_x = 1, v_y = 2
    u_x, u_y = 2.0, -1.0
    v_x, v_y = 1.0, 2.0

    # Dense boundary of the square for smooth mapped curve
    t = np.linspace(0, 1, 200)
    edges_z = np.concatenate(
        [
            z0 + h * t,
            z0 + h + 1j * h * t,
            z0 + h * (1 - t) + 1j * h,
            z0 + 1j * h * (1 - t),
        ]
    )
    edges_w = edges_z**2

    # Jacobian image vectors (scaled by h)
    dx_img = np.array([u_x * h, v_x * h])  # (0.4, 0.2)
    dy_img = np.array([u_y * h, v_y * h])  # (-0.2, 0.4)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))

    # ===== z-plane =====
    ax1.fill(edges_z.real, edges_z.imag, color=colors[0], alpha=0.12)
    ax1.plot(edges_z.real, edges_z.imag, color="k", linewidth=1.2)

    arr_z = dict(
        width=0.007,
        head_width=0.025,
        head_length=0.018,
        length_includes_head=True,
        zorder=5,
    )
    ax1.arrow(z0.real, z0.imag, h, 0, color=colors[0], **arr_z)
    ax1.arrow(z0.real, z0.imag, 0, h, color=colors[1], **arr_z)

    # Right angle marker
    m = 0.028
    ax1.plot(
        [z0.real + m, z0.real + m, z0.real],
        [z0.imag, z0.imag + m, z0.imag + m],
        "k-",
        linewidth=1,
    )

    ax1.text(
        z0.real + h / 2,
        z0.imag - 0.03,
        r"$\mathrm{d}x$",
        fontsize=13,
        color=colors[0],
        ha="center",
        fontweight="bold",
    )
    ax1.text(
        z0.real - 0.03,
        z0.imag + h / 2,
        r"$\mathrm{d}y$",
        fontsize=13,
        color=colors[1],
        ha="right",
        va="center",
        fontweight="bold",
    )

    ax1.plot(z0.real, z0.imag, "ko", markersize=5, zorder=6)
    ax1.text(z0.real + 0.02, z0.imag - 0.035, r"$z_0$", fontsize=12, va="top")

    ax1.set_title(r"$z$-plane", fontsize=14)
    ax1.set_xlabel(r"$\mathrm{Re}(z)$")
    ax1.set_ylabel(r"$\mathrm{Im}(z)$")
    ax1.set_aspect("equal")
    ax1.set_xlim(0.82, 1.38)
    ax1.set_ylim(0.32, 0.88)

    # ===== w-plane =====
    ax2.fill(edges_w.real, edges_w.imag, color=colors[0], alpha=0.12)
    ax2.plot(edges_w.real, edges_w.imag, color="k", linewidth=1.2)

    arr_w = dict(
        width=0.01,
        head_width=0.035,
        head_length=0.025,
        length_includes_head=True,
        zorder=5,
    )
    ax2.arrow(w0.real, w0.imag, dx_img[0], dx_img[1], color=colors[0], **arr_w)
    ax2.arrow(w0.real, w0.imag, dy_img[0], dy_img[1], color=colors[1], **arr_w)

    # Component dashed lines — blue arrow (image of dx)
    tip_b = (w0.real + dx_img[0], w0.imag + dx_img[1])
    ax2.plot(
        [w0.real, tip_b[0]],
        [w0.imag, w0.imag],
        color=colors[0],
        linewidth=1,
        linestyle=":",
        alpha=0.5,
    )
    ax2.plot(
        [tip_b[0], tip_b[0]],
        [w0.imag, tip_b[1]],
        color=colors[0],
        linewidth=1,
        linestyle=":",
        alpha=0.5,
    )

    # Component dashed lines — orange arrow (image of dy)
    tip_o = (w0.real + dy_img[0], w0.imag + dy_img[1])
    ax2.plot(
        [w0.real, w0.real],
        [w0.imag, tip_o[1]],
        color=colors[1],
        linewidth=1,
        linestyle=":",
        alpha=0.5,
    )
    ax2.plot(
        [w0.real, tip_o[0]],
        [tip_o[1], tip_o[1]],
        color=colors[1],
        linewidth=1,
        linestyle=":",
        alpha=0.5,
    )

    # Component labels
    ax2.text(
        w0.real + dx_img[0] / 2,
        w0.imag - 0.04,
        r"$u_x$",
        fontsize=12,
        color=colors[0],
        ha="center",
    )
    ax2.text(
        tip_b[0] + 0.03,
        w0.imag + dx_img[1] / 2,
        r"$v_x$",
        fontsize=12,
        color=colors[0],
        ha="left",
        va="center",
    )
    ax2.text(
        w0.real - 0.03,
        w0.imag + dy_img[1] / 2,
        r"$v_y$",
        fontsize=12,
        color=colors[1],
        ha="right",
        va="center",
    )
    ax2.text(
        w0.real + dy_img[0] / 2,
        tip_o[1] + 0.03,
        r"$u_y$",
        fontsize=12,
        color=colors[1],
        ha="center",
    )

    # Rotated right angle marker
    rot = np.arctan2(dx_img[1], dx_img[0])
    c_r, s_r = np.cos(rot), np.sin(rot)
    m_w = 0.04
    p1 = (w0.real + m_w * c_r, w0.imag + m_w * s_r)
    p2 = (p1[0] - m_w * s_r, p1[1] + m_w * c_r)
    p3 = (w0.real - m_w * s_r, w0.imag + m_w * c_r)
    ax2.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], "k-", linewidth=1)

    ax2.plot(w0.real, w0.imag, "ko", markersize=5, zorder=6)
    ax2.text(
        w0.real - 0.1,
        w0.imag - 0.05,
        r"$w_0 = z_0^2$",
        fontsize=11,
        va="top",
        ha="right",
    )

    # Cauchy-Riemann annotation box
    cr_text = "\n".join(
        [
            r"$u_x = v_y = 2$",
            r"$u_y = -v_x = -1$",
            "",
            r"$|f'(z_0)| = \sqrt{5}$",
            r"$\arg f'(z_0) \approx 26.6°$",
        ]
    )
    ax2.text(
        0.03,
        0.03,
        cr_text,
        transform=ax2.transAxes,
        fontsize=11,
        va="bottom",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="wheat", alpha=0.85),
    )

    ax2.set_title(r"$w = z^2$", fontsize=14)
    ax2.set_xlabel(r"$\mathrm{Re}(w)$")
    ax2.set_ylabel(r"$\mathrm{Im}(w)$")
    ax2.set_aspect("equal")
    ax2.set_xlim(0.15, 1.5)
    ax2.set_ylim(0.55, 1.85)

    fig.suptitle(
        "Cauchy-Riemann equations: the Jacobian is a scaled rotation",
        fontsize=13,
        y=1.01,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- 3. Critical points ---


def plot_critical_points(save_as=None):
    """Polar grid in the first quadrant mapped through z, z^2, z^3,
    showing how angles at the origin are multiplied by the order.
    """
    colors = sns.color_palette("deep")

    r_values = np.linspace(0.2, 1.4, 7)
    theta_values = np.linspace(0, np.pi / 2, 7)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    panels = [
        (axes[0], 1, r"$w = z$ (identity)"),
        (axes[1], 2, r"$w = z^2$ (angles $\times\, 2$)"),
        (axes[2], 3, r"$w = z^3$ (angles $\times\, 3$)"),
    ]

    for ax, n, title in panels:
        # Image of circular arcs
        for r0 in r_values:
            theta = np.linspace(0, np.pi / 2, 300)
            z = r0 * np.exp(1j * theta)
            w = z**n
            ax.plot(w.real, w.imag, color=colors[0], linewidth=0.9, alpha=0.7)

        # Image of radial lines
        for th0 in theta_values:
            r = np.linspace(0, 1.4, 200)
            z = r * np.exp(1j * th0)
            w = z**n
            ax.plot(w.real, w.imag, color=colors[1], linewidth=0.9, alpha=0.7)

        # Highlight the sector boundary
        mapped_angle = n * np.pi / 2
        wedge = Wedge(
            (0, 0), 1.4**n, 0, np.degrees(mapped_angle), color=colors[0], alpha=0.06
        )
        ax.add_patch(wedge)

        # Angle arc
        arc_r = 0.35 * (1.4 ** (n - 1))
        arc = Arc(
            (0, 0),
            2 * arc_r,
            2 * arc_r,
            angle=0,
            theta1=0,
            theta2=np.degrees(mapped_angle),
            color=colors[3],
            linewidth=2.5,
        )
        ax.add_patch(arc)
        mid = mapped_angle / 2
        label_r = arc_r + 0.15 * (1.4 ** (n - 1))
        ax.annotate(
            rf"${int(np.degrees(mapped_angle))}°$",
            xy=(label_r * np.cos(mid), label_r * np.sin(mid)),
            fontsize=13,
            color=colors[3],
            fontweight="bold",
            ha="center",
            va="center",
        )

        ax.set_title(title, fontsize=13)
        ax.plot(0, 0, "ko", markersize=5, zorder=5)
        ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.axvline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.set_aspect("equal")
        lim = 1.4**n * 1.15
        ax.set_xlim(-lim * 0.3, lim)
        ax.set_ylim(-lim * 0.3, lim)

    fig.suptitle(
        r"At a critical point ($f'(0)=0$), angles are multiplied by the order of the zero",
        fontsize=13,
        y=1.02,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- 4. Möbius transforms: circles to circles ---


def plot_mobius_circles(save_as=None):
    """Circles in the z-plane and their circular images under a Möbius transform."""
    colors = sns.color_palette("deep")

    def mobius(z):
        return (z - 1) / (z + 1)

    theta = np.linspace(0, 2 * np.pi, 800)

    # Circles in the z-plane (all in the right half-plane, away from pole at -1)
    circles = [
        ("Unit circle", 0 + 0j, 1.0),
        (None, 1.5 + 0j, 0.8),
        (None, 0.5 + 1j, 0.6),
        (None, 2.0 + 0j, 1.5),
        (None, 0 + 2j, 0.7),
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    for i, (label, center, radius) in enumerate(circles):
        z = center + radius * np.exp(1j * theta)
        w = mobius(z)

        # Filter out points near the pole
        w_re = np.real(w).copy()
        w_im = np.imag(w).copy()
        bad = ~np.isfinite(w_re) | ~np.isfinite(w_im) | (np.abs(w) > 15)
        w_re[bad] = np.nan
        w_im[bad] = np.nan
        dw = np.sqrt(np.diff(w_re) ** 2 + np.diff(w_im) ** 2)
        jumps = np.concatenate([[False], dw > 5])
        w_re[jumps] = np.nan
        w_im[jumps] = np.nan

        c = colors[i % len(colors)]
        ax1.plot(z.real, z.imag, color=c, linewidth=2, label=label)
        ax2.plot(w_re, w_im, color=c, linewidth=2)

    # The imaginary axis (a line) — maps to the unit circle
    t = np.linspace(-4, 4, 500)
    z_line = 1j * t
    w_line = mobius(z_line)
    ax1.plot(
        z_line.real,
        z_line.imag,
        color="gray",
        linewidth=2,
        linestyle="--",
        label="Imaginary axis",
    )
    ax2.plot(
        w_line.real,
        w_line.imag,
        color="gray",
        linewidth=2,
        linestyle="--",
        label="Image (unit circle)",
    )

    # Mark the pole
    ax1.plot(-1, 0, "kx", markersize=10, markeredgewidth=2, zorder=5)
    ax1.annotate(
        "pole",
        xy=(-1, 0),
        xytext=(-1.4, -0.6),
        fontsize=10,
        color="k",
        arrowprops=dict(arrowstyle="->", color="k", lw=1),
    )

    for ax in (ax1, ax2):
        ax.set_aspect("equal")
        ax.axhline(0, color="gray", linewidth=0.4, linestyle=":")
        ax.axvline(0, color="gray", linewidth=0.4, linestyle=":")

    ax1.set_title(r"$z$-plane", fontsize=14)
    ax1.set_xlabel(r"$\mathrm{Re}(z)$")
    ax1.set_ylabel(r"$\mathrm{Im}(z)$")
    ax1.set_xlim(-3, 4)
    ax1.set_ylim(-3.5, 3.5)
    ax1.legend(fontsize=9, loc="upper right")

    ax2.set_title(r"$w = (z-1)/(z+1)$", fontsize=14)
    ax2.set_xlabel(r"$\mathrm{Re}(w)$")
    ax2.set_ylabel(r"$\mathrm{Im}(w)$")
    ax2.set_xlim(-3, 3)
    ax2.set_ylim(-3, 3)
    ax2.legend(fontsize=9, loc="upper right")

    fig.suptitle(
        r"Möbius transforms map every circle or line to a circle or line",
        fontsize=13,
        y=1.01,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- 5. Joukowski airfoil ---


def plot_joukowski(save_as=None):
    """Joukowski transform z + 1/z mapping a circle to an airfoil shape."""
    colors = sns.color_palette("deep")

    # Circle passing through z = 1, slightly offset for thickness and camber
    c = 0.10  # real offset → thickness
    d = 0.08  # imaginary offset → camber
    center = complex(-c, d)
    R = abs(1.0 - center)

    theta = np.linspace(0, 2 * np.pi, 2000)
    z_circle = center + R * np.exp(1j * theta)
    w_airfoil = z_circle + 1 / z_circle

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # z-plane: circle + unit circle for reference
    unit = np.exp(1j * theta)
    ax1.plot(unit.real, unit.imag, color="gray", linewidth=1, linestyle="--", alpha=0.5)
    ax1.plot(z_circle.real, z_circle.imag, color=colors[0], linewidth=2.5)
    ax1.plot(center.real, center.imag, "o", color=colors[0], markersize=5)

    # Mark critical points z = ±1
    ax1.plot(1, 0, "ko", markersize=7, zorder=5)
    ax1.plot(-1, 0, "ko", markersize=7, zorder=5)
    ax1.annotate(r"$z = 1$", xy=(1, 0), xytext=(1.2, -0.35), fontsize=11)
    ax1.annotate(r"$z = -1$", xy=(-1, 0), xytext=(-1.6, -0.35), fontsize=11)

    ax1.set_title(r"$z$-plane", fontsize=14)
    ax1.set_xlabel(r"$\mathrm{Re}(z)$")
    ax1.set_ylabel(r"$\mathrm{Im}(z)$")
    ax1.set_aspect("equal")
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-1.5, 1.5)

    # w-plane: airfoil
    ax2.plot(w_airfoil.real, w_airfoil.imag, color=colors[0], linewidth=2.5)
    ax2.fill(w_airfoil.real, w_airfoil.imag, color=colors[0], alpha=0.08)

    # Mark trailing edge
    w_te = 1.0 + 1.0  # image of z = 1: 1 + 1/1 = 2
    ax2.plot(w_te, 0, "ko", markersize=5, zorder=5)
    ax2.annotate(
        "trailing edge\n(cusp at critical point)",
        xy=(w_te, 0),
        xytext=(1.0, -0.45),
        fontsize=10,
        arrowprops=dict(arrowstyle="->", color="k", lw=1),
    )

    ax2.set_title(r"$w = z + 1/z$", fontsize=14)
    ax2.set_xlabel(r"$\mathrm{Re}(w)$")
    ax2.set_ylabel(r"$\mathrm{Im}(w)$")
    ax2.set_aspect("equal")
    ax2.set_xlim(-3, 3)
    ax2.set_ylim(-1.2, 1.2)

    fig.suptitle("Joukowski transform: circle to airfoil", fontsize=14, y=1.01)
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- CLI ---


def main():
    import argparse

    figures = {
        "grid_gallery": (
            "Grid deformations under four maps",
            lambda: plot_grid_gallery(save_as="conformal_grid_gallery.png"),
        ),
        "angle_preservation": (
            "Angle preservation under z^2",
            lambda: plot_angle_preservation(save_as="conformal_angle_preservation.png"),
        ),
        "jacobian": (
            "Jacobian as scaled rotation (CR equations)",
            lambda: plot_jacobian_element(save_as="conformal_jacobian_element.png"),
        ),
        "critical_points": (
            "Angle multiplication at critical points",
            lambda: plot_critical_points(save_as="conformal_critical_points.png"),
        ),
        "mobius": (
            "Möbius circles-to-circles",
            lambda: plot_mobius_circles(save_as="conformal_mobius_circles.png"),
        ),
        "joukowski": (
            "Joukowski airfoil",
            lambda: plot_joukowski(save_as="conformal_joukowski.png"),
        ),
    }

    parser = argparse.ArgumentParser(description="Conformal mapping figures.")
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
