"""Visualizing anisotropic permittivity, isofrequency surfaces, and hyperbolic dispersion."""

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


# --- Isofrequency contour computation ---


def isofrequency_contour(kx, kz, eps_perp, eps_z):
    """Compute the isofrequency surface value for a uniaxial medium.

    The dispersion relation is kx^2/eps_z + kz^2/eps_perp = omega^2/c^2.
    We set omega/c = 1, so the zero contour of
    F = kx^2/eps_z + kz^2/eps_perp - 1 gives the isofrequency surface.
    """
    return kx**2 / eps_z + kz**2 / eps_perp - 1


def mode_index_surface(theta, eps_perp, eps_z):
    """Compute the extraordinary mode index n(theta) for a uniaxial medium.

    1/n^2(theta) = cos^2(theta)/eps_perp + sin^2(theta)/eps_z

    Returns n(theta) where theta is the angle from the optic axis.
    For hyperbolic media, n^2 can go negative — return NaN there.
    """
    inv_n2 = np.cos(theta) ** 2 / eps_perp + np.sin(theta) ** 2 / eps_z
    n2 = np.where(inv_n2 > 0, 1.0 / inv_n2, np.nan)
    return np.sqrt(n2)


# --- Phonon polariton permittivity models ---


def eps_lorentz_phonon(omega, eps_inf, omega_to, omega_lo, gamma):
    """Lorentz permittivity for a single phonon resonance.

    eps(omega) = eps_inf * (omega_lo^2 - omega^2 - i*gamma*omega)
                         / (omega_to^2 - omega^2 - i*gamma*omega)

    The Reststrahlen band (eps < 0) lies between omega_to and omega_lo.
    """
    return (
        eps_inf
        * (omega_lo**2 - omega**2 - 1j * gamma * omega)
        / (omega_to**2 - omega**2 - 1j * gamma * omega)
    )


def moo3_permittivity(omega):
    """Approximate permittivity tensor components for MoO3.

    Three principal axes with distinct phonon resonances (in cm^-1 units):
      x ([100]): omega_TO ~ 820,  omega_LO ~ 972
      y ([010]): omega_TO ~ 545,  omega_LO ~ 851
      z ([001]): omega_TO ~ 958,  omega_LO ~ 1004

    Returns (eps_x, eps_y, eps_z) as complex arrays.
    """
    gamma = 4.0  # damping (cm^-1)
    eps_x = eps_lorentz_phonon(
        omega, eps_inf=4.0, omega_to=820, omega_lo=972, gamma=gamma
    )
    eps_y = eps_lorentz_phonon(
        omega, eps_inf=5.2, omega_to=545, omega_lo=851, gamma=gamma
    )
    eps_z = eps_lorentz_phonon(
        omega, eps_inf=2.4, omega_to=958, omega_lo=1004, gamma=gamma
    )
    return eps_x, eps_y, eps_z


# --- Biaxial isofrequency ---


def isofrequency_biaxial(kx, ky, eps_x, eps_y, omega_over_c=1.0):
    """Isofrequency contour for in-plane propagation in a biaxial medium.

    For a wave propagating in the xy-plane (kz=0) with z-polarized E-field,
    the dispersion relation is:
        kx^2/eps_y + ky^2/eps_x = omega^2/c^2

    Returns F such that the zero contour F=0 is the isofrequency surface.
    """
    return kx**2 / eps_y + ky**2 / eps_x - omega_over_c**2


# --- Fresnel equation / eigenpolarization ---


def fresnel_eigenvalues(khat, eps_x, eps_y, eps_z):
    """Solve the Fresnel equation for the two mode indices n_o, n_e.

    Given propagation direction khat = (sin(theta), 0, cos(theta)) in the xz-plane,
    returns the two solutions n^2 from the Fresnel equation.
    """
    sx, sz = khat[0], khat[2]
    # Fresnel equation for biaxial reduces to quadratic in n^2
    # For uniaxial (eps_x = eps_y = eps_perp):
    # ordinary: n_o^2 = eps_perp
    # extraordinary: 1/n_e^2 = sx^2/eps_z + sz^2/eps_perp
    n_o_sq = eps_x
    inv_ne_sq = sx**2 / eps_z + sz**2 / eps_x
    n_e_sq = np.where(np.abs(inv_ne_sq) > 1e-12, 1.0 / inv_ne_sq, np.nan)
    return n_o_sq, n_e_sq


# --- Plot functions ---


def plot_isofrequency_panel(save_as=None):
    """Three-panel: isofrequency contours for isotropic, elliptic, and hyperbolic media.

    Shows the transition from circular to elliptic to hyperbolic as the
    permittivity tensor changes sign structure.
    """
    kx = np.linspace(-3, 3, 500)
    kz = np.linspace(-3, 3, 500)
    KX, KZ = np.meshgrid(kx, kz)
    colors = sns.color_palette("deep")

    cases = [
        (2.25, 2.25, r"Isotropic: $\varepsilon_\perp = \varepsilon_z = 2.25$"),
        (2.25, 5.0, r"Elliptic: $\varepsilon_\perp = 2.25,\ \varepsilon_z = 5$"),
        (
            2.25,
            -2.0,
            r"Hyperbolic (Type I): $\varepsilon_\perp = 2.25,\ \varepsilon_z = -2$",
        ),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for ax, (eps_perp, eps_z, title) in zip(axes, cases):
        F = isofrequency_contour(KX, KZ, eps_perp, eps_z)

        # Background: modulus of F for context
        ax.contourf(KX, KZ, np.abs(F), levels=100, cmap="rocket", alpha=0.3)

        # The isofrequency contour itself (F = 0)
        ax.contour(KX, KZ, F, levels=[0], colors=[colors[0]], linewidths=2.5)

        # Light line (vacuum circle) for reference
        theta_circ = np.linspace(0, 2 * np.pi, 200)
        ax.plot(
            np.cos(theta_circ),
            np.sin(theta_circ),
            color="gray",
            linewidth=1,
            linestyle="--",
            alpha=0.6,
            label="Vacuum",
        )

        ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.axvline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.set_xlabel(r"$k_x / (\omega/c)$")
        ax.set_ylabel(r"$k_z / (\omega/c)$")
        ax.set_title(title, fontsize=10)
        ax.set_aspect("equal")
        ax.legend(fontsize=8, loc="upper right")
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_hyperbolic_types(save_as=None):
    """Two-panel: Type I vs Type II hyperbolic media."""
    kx = np.linspace(-4, 4, 500)
    kz = np.linspace(-4, 4, 500)
    KX, KZ = np.meshgrid(kx, kz)
    colors = sns.color_palette("deep")

    cases = [
        (2.25, -2.0, r"Type I: $\varepsilon_\perp > 0,\ \varepsilon_z < 0$"),
        (-2.0, 2.25, r"Type II: $\varepsilon_\perp < 0,\ \varepsilon_z > 0$"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, (eps_perp, eps_z, title) in zip(axes, cases):
        F = isofrequency_contour(KX, KZ, eps_perp, eps_z)
        ax.contourf(KX, KZ, np.abs(F), levels=100, cmap="rocket", alpha=0.3)
        ax.contour(KX, KZ, F, levels=[0], colors=[colors[0]], linewidths=2.5)

        # Asymptotes: kx^2/eps_z + kz^2/eps_perp = 0 => kz/kx = +-sqrt(-eps_perp/eps_z)
        if eps_perp * eps_z < 0:
            slope = np.sqrt(abs(eps_perp / eps_z))
            k_line = np.linspace(-4, 4, 200)
            ax.plot(
                k_line,
                slope * k_line,
                color="white",
                linewidth=1,
                linestyle=":",
                alpha=0.7,
            )
            ax.plot(
                k_line,
                -slope * k_line,
                color="white",
                linewidth=1,
                linestyle=":",
                alpha=0.7,
            )

        # Vacuum circle
        theta_circ = np.linspace(0, 2 * np.pi, 200)
        ax.plot(
            np.cos(theta_circ),
            np.sin(theta_circ),
            color="gray",
            linewidth=1,
            linestyle="--",
            alpha=0.6,
        )

        ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.axvline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.set_xlabel(r"$k_x / (\omega/c)$")
        ax.set_ylabel(r"$k_z / (\omega/c)$")
        ax.set_title(title)
        ax.set_aspect("equal")
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_mode_index_surface(save_as=None):
    """Three-panel polar plot: n(theta) for isotropic, elliptic, and hyperbolic media."""
    theta = np.linspace(0, 2 * np.pi, 1000)
    colors = sns.color_palette("deep")

    cases = [
        (2.25, 2.25, "Isotropic"),
        (2.25, 5.0, "Elliptic"),
        (2.25, -2.0, "Hyperbolic (Type I)"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5), subplot_kw={"projection": "polar"})

    for ax, (eps_perp, eps_z, title) in zip(axes, cases):
        # Ordinary ray: n_o = sqrt(eps_perp), isotropic
        n_o = np.sqrt(max(eps_perp, 0)) * np.ones_like(theta)
        ax.plot(theta, n_o, color=colors[0], linewidth=2, label="Ordinary")

        # Extraordinary ray
        n_e = mode_index_surface(theta, eps_perp, eps_z)
        valid = np.isfinite(n_e)
        # Plot only valid portions
        if np.any(valid):
            # Break into contiguous segments to avoid connecting across gaps
            segments = np.split(np.arange(len(theta)), np.where(~valid)[0])
            for seg in segments:
                seg = seg[seg < len(theta)]
                if len(seg) > 1:
                    ax.plot(
                        theta[seg],
                        n_e[seg],
                        color=colors[1],
                        linewidth=2,
                        label="Extraordinary" if seg[0] == segments[0][0] else None,
                    )

        ax.set_title(title, pad=15)
        ax.legend(fontsize=8, loc="lower right")

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_permittivity_tensor_operator(save_as=None):
    """Visualize the permittivity tensor as a Dirac operator acting on polarization.

    Three panels: input polarization vector, tensor action, output vector.
    Shows how eps stretches/flips different polarization components.
    """
    colors = sns.color_palette("deep")

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    cases = [
        ([1, 1], 2.25, 2.25, "Isotropic", r"$\varepsilon_x = \varepsilon_z = 2.25$"),
        ([1, 1], 2.25, 5.0, "Elliptic", r"$\varepsilon_x = 2.25,\ \varepsilon_z = 5$"),
        (
            [1, 1],
            2.25,
            -2.0,
            "Hyperbolic",
            r"$\varepsilon_x = 2.25,\ \varepsilon_z = -2$",
        ),
    ]

    for ax, (e_in, eps_x, eps_z, title, label) in zip(axes, cases):
        e_in = np.array(e_in, dtype=float)
        e_in = e_in / np.linalg.norm(e_in)

        # Apply tensor
        e_out = np.array([eps_x * e_in[0], eps_z * e_in[1]])

        # Plot
        ax.arrow(
            0,
            0,
            e_in[0] * 0.9,
            e_in[1] * 0.9,
            head_width=0.08,
            head_length=0.05,
            fc=colors[0],
            ec=colors[0],
            linewidth=2,
            label=r"$|\mathbf{E}\rangle$",
        )
        scale = max(abs(e_out[0]), abs(e_out[1]))
        e_out_norm = e_out / scale * 1.8  # scale for visibility
        ax.arrow(
            0,
            0,
            e_out_norm[0] * 0.9,
            e_out_norm[1] * 0.9,
            head_width=0.08,
            head_length=0.05,
            fc=colors[1],
            ec=colors[1],
            linewidth=2,
            label=r"$\hat{\varepsilon}|\mathbf{E}\rangle$",
        )

        # Axes
        ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.axvline(0, color="gray", linewidth=0.5, linestyle=":")

        # Draw eigenvector directions
        ax.plot(
            [0, 2.2], [0, 0], color="gray", linewidth=0.8, linestyle="--", alpha=0.5
        )
        ax.plot(
            [0, 0], [0, 2.2], color="gray", linewidth=0.8, linestyle="--", alpha=0.5
        )
        ax.text(2.0, -0.2, r"$|x\rangle$", fontsize=11, color="gray")
        ax.text(-0.35, 2.0, r"$|z\rangle$", fontsize=11, color="gray")

        ax.set_xlabel(r"$E_x$")
        ax.set_ylabel(r"$E_z$")
        ax.set_title(f"{title}\n{label}", fontsize=10)
        ax.set_aspect("equal")
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.5, 2.5)
        ax.legend(fontsize=9, loc="upper left")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_isofrequency_transition(save_as=None):
    """Show how the isofrequency contour evolves as eps_z sweeps from
    positive (elliptic) through zero to negative (hyperbolic).
    """
    kx = np.linspace(-4, 4, 500)
    kz = np.linspace(-4, 4, 500)
    KX, KZ = np.meshgrid(kx, kz)

    eps_perp = 2.25
    eps_z_vals = [4.0, 2.25, 0.5, -0.5, -2.0, -4.0]

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    colors = sns.color_palette("deep")

    for ax, eps_z in zip(axes.flat, eps_z_vals):
        F = isofrequency_contour(KX, KZ, eps_perp, eps_z)
        ax.contourf(KX, KZ, np.log1p(np.abs(F)), levels=100, cmap="rocket", alpha=0.3)
        ax.contour(KX, KZ, F, levels=[0], colors=[colors[0]], linewidths=2.5)

        # Vacuum circle
        theta_circ = np.linspace(0, 2 * np.pi, 200)
        ax.plot(
            np.cos(theta_circ),
            np.sin(theta_circ),
            color="gray",
            linewidth=1,
            linestyle="--",
            alpha=0.6,
        )

        ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.axvline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.set_xlabel(r"$k_x$")
        ax.set_ylabel(r"$k_z$")

        regime = "elliptic" if eps_z > 0 else "hyperbolic"
        ax.set_title(rf"$\varepsilon_z = {eps_z}$ ({regime})", fontsize=10)
        ax.set_aspect("equal")
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)

    plt.suptitle(
        rf"$\varepsilon_\perp = {eps_perp}$ fixed, sweeping $\varepsilon_z$: "
        r"elliptic $\to$ hyperbolic transition",
        fontsize=13,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_phonon_polariton_dispersion(save_as=None):
    """Dispersion diagram for a uniaxial polar crystal with a Reststrahlen band.

    Left: eps(omega) showing the Reststrahlen band where eps < 0.
    Right: omega vs kx dispersion, showing how hyperbolic branches emerge
    inside the Reststrahlen band. Horizontal dashed lines mark omega_TO and
    omega_LO. A vertical slice at fixed omega gives an isofrequency contour.
    """
    colors = sns.color_palette("deep")

    # Phonon parameters (arbitrary units, normalized so omega_TO = 1)
    omega_to = 1.0
    omega_lo = 1.4
    eps_inf = 2.0
    gamma = 0.02

    omega = np.linspace(0.01, 2.5, 1000)

    # Permittivity along the optic axis
    eps_z = eps_lorentz_phonon(omega, eps_inf, omega_to, omega_lo, gamma)
    eps_perp_val = 5.0  # transverse permittivity (constant for simplicity)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # --- Left panel: eps_z(omega) ---
    ax = axes[0]
    ax.plot(
        omega, np.real(eps_z), color=colors[0], linewidth=2, label=r"$\varepsilon'_z$"
    )
    ax.plot(
        omega,
        np.imag(eps_z),
        color=colors[1],
        linewidth=1.5,
        linestyle="--",
        label=r"$\varepsilon''_z$",
    )
    ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")

    # Shade the Reststrahlen band
    ax.axvspan(
        omega_to, omega_lo, alpha=0.15, color=colors[3], label="Reststrahlen band"
    )
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.set_xlabel(r"$\omega / \omega_{TO}$")
    ax.set_ylabel(r"$\varepsilon_z(\omega)$")
    ax.set_title(r"Permittivity along optic axis")
    ax.set_ylim(-15, 15)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # --- Right panel: omega vs kx dispersion ---
    ax = axes[1]

    # For each omega, solve for kx from:
    #   kx^2/eps_z(omega) + kz^2/eps_perp = omega^2/c^2
    # At kz=0: kx^2 = eps_z(omega) * omega^2/c^2
    # So we plot omega vs kx by computing kx(omega) = omega * sqrt(eps_z(omega))
    # for the extraordinary wave at kz=0

    eps_z_fine = eps_lorentz_phonon(omega, eps_inf, omega_to, omega_lo, gamma)
    kx_of_omega = omega * np.sqrt(np.real(eps_z_fine).clip(min=0))

    # Upper branch (above omega_LO)
    mask_upper = omega > omega_lo
    ax.plot(
        kx_of_omega[mask_upper],
        omega[mask_upper],
        color=colors[0],
        linewidth=2.5,
    )

    # Lower branch (below omega_TO)
    mask_lower = omega < omega_to
    ax.plot(
        kx_of_omega[mask_lower],
        omega[mask_lower],
        color=colors[0],
        linewidth=2.5,
    )

    # Inside Reststrahlen: extraordinary wave at kz != 0
    # kx^2/eps_z + kz^2/eps_perp = omega^2/c^2
    # With eps_z < 0 and eps_perp > 0: hyperbolic dispersion
    # For fixed kz, solve: kx^2 = eps_z(omega) * (omega^2 - kz^2/eps_perp)
    for kz_val in [1.0, 2.0, 3.0]:
        mask_rest = (omega > omega_to) & (omega < omega_lo)
        omega_rest = omega[mask_rest]
        eps_z_rest = np.real(
            eps_lorentz_phonon(omega_rest, eps_inf, omega_to, omega_lo, gamma)
        )
        kx_sq = eps_z_rest * (omega_rest**2 - kz_val**2 / eps_perp_val)
        valid = kx_sq > 0
        if np.any(valid):
            ax.plot(
                np.sqrt(kx_sq[valid]),
                omega_rest[valid],
                color=colors[1],
                linewidth=1.5,
                alpha=0.6,
                label=rf"$k_z = {kz_val}$" if kz_val == 1.0 else None,
            )

    # Light line
    ax.plot(
        omega * np.sqrt(eps_perp_val),
        omega,
        color="gray",
        linewidth=1,
        linestyle="--",
        alpha=0.5,
        label="Light line",
    )

    # Reststrahlen band shading
    ax.axhspan(omega_to, omega_lo, alpha=0.15, color=colors[3])
    ax.axhline(omega_to, color="gray", linewidth=0.5, linestyle=":")
    ax.axhline(omega_lo, color="gray", linewidth=0.5, linestyle=":")
    ax.text(7.5, omega_to - 0.05, r"$\omega_{TO}$", fontsize=10, ha="right", va="top")
    ax.text(
        7.5, omega_lo + 0.03, r"$\omega_{LO}$", fontsize=10, ha="right", va="bottom"
    )

    ax.set_xlabel(r"$k_x c / \omega_{TO}$")
    ax.set_ylabel(r"$\omega / \omega_{TO}$")
    ax.set_title("Phonon polariton dispersion")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 2.0)
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_moo3_permittivity(save_as=None):
    """Three-axis permittivity of MoO3 showing distinct Reststrahlen bands.

    Plots Re(eps) for all three crystal axes vs frequency, with shaded
    Reststrahlen bands highlighting the spectral windows where each
    component goes negative.
    """
    colors = sns.color_palette("deep")
    omega = np.linspace(400, 1100, 2000)
    eps_x, eps_y, eps_z = moo3_permittivity(omega)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        omega,
        np.real(eps_x),
        color=colors[0],
        linewidth=2,
        label=r"$\varepsilon_x$ ([100])",
    )
    ax.plot(
        omega,
        np.real(eps_y),
        color=colors[1],
        linewidth=2,
        label=r"$\varepsilon_y$ ([010])",
    )
    ax.plot(
        omega,
        np.real(eps_z),
        color=colors[2],
        linewidth=2,
        label=r"$\varepsilon_z$ ([001])",
    )

    # Shade Reststrahlen bands
    bands = [
        (545, 851, colors[1], r"RB$_y$"),
        (820, 972, colors[0], r"RB$_x$"),
        (958, 1004, colors[2], r"RB$_z$"),
    ]
    for omega_to, omega_lo, color, label in bands:
        ax.axvspan(omega_to, omega_lo, alpha=0.1, color=color)
        ax.text(
            (omega_to + omega_lo) / 2,
            12,
            label,
            ha="center",
            fontsize=9,
            color=color,
        )

    ax.axhline(0, color="gray", linewidth=1, linestyle=":")
    ax.set_xlabel(r"Frequency (cm$^{-1}$)")
    ax.set_ylabel(r"Re$(\varepsilon)$")
    ax.set_title(r"MoO$_3$ principal permittivities")
    ax.set_ylim(-15, 15)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_moo3_isofrequency(save_as=None):
    """In-plane isofrequency contours for MoO3 at selected frequencies.

    Shows how the contour topology changes across the Reststrahlen bands:
    elliptic when both in-plane components are positive, hyperbolic when
    one goes negative, and no propagation when both are negative.
    """
    colors = sns.color_palette("deep")

    # Frequencies sampling different regimes (cm^-1)
    freqs = [500, 700, 860, 930, 970, 990]

    k_range = np.linspace(-5, 5, 600)
    KX, KY = np.meshgrid(k_range, k_range)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    for ax, freq in zip(axes.flat, freqs):
        omega = np.array([freq])
        eps_x, eps_y, eps_z = moo3_permittivity(omega)
        ex = np.real(eps_x[0])
        ey = np.real(eps_y[0])

        # Classify the regime
        if ex > 0 and ey > 0:
            regime = "elliptic"
        elif ex < 0 and ey < 0:
            regime = "no propagation"
        elif ex * ey < 0:
            regime = "hyperbolic"
        else:
            regime = "degenerate"

        # In-plane dispersion: kx^2/eps_y + ky^2/eps_x = (omega/c)^2
        # Normalize k by omega/c = 1
        F = isofrequency_biaxial(KX, KY, ex, ey)

        ax.contourf(KX, KY, np.log1p(np.abs(F)), levels=100, cmap="rocket", alpha=0.3)

        try:
            ax.contour(KX, KY, F, levels=[0], colors=[colors[0]], linewidths=2.5)
        except ValueError:
            pass  # no contour if no zero crossing

        # Vacuum circle
        theta_circ = np.linspace(0, 2 * np.pi, 200)
        ax.plot(
            np.cos(theta_circ),
            np.sin(theta_circ),
            color="gray",
            linewidth=1,
            linestyle="--",
            alpha=0.6,
        )

        ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.axvline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.set_xlabel(r"$k_x / (\omega/c)$")
        ax.set_ylabel(r"$k_y / (\omega/c)$")
        ax.set_title(
            rf"$\omega = {freq}$ cm$^{{-1}}$ ({regime})"
            + "\n"
            + rf"$\varepsilon_x = {ex:.1f},\ \varepsilon_y = {ey:.1f}$",
            fontsize=9,
        )
        ax.set_aspect("equal")
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)

    plt.suptitle(
        r"MoO$_3$ in-plane isofrequency contours at different frequencies",
        fontsize=13,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "isofrequency": ("Isofrequency contour panel", lambda: plot_isofrequency_panel(save_as="aniso_isofrequency.png")),
        "hyperbolic_types": ("Type I vs Type II hyperbolic", lambda: plot_hyperbolic_types(save_as="aniso_hyperbolic_types.png")),
        "mode_index": ("Extraordinary mode index surface", lambda: plot_mode_index_surface(save_as="aniso_mode_index.png")),
        "tensor_operator": ("Permittivity tensor as operator", lambda: plot_permittivity_tensor_operator(save_as="aniso_tensor_operator.png")),
        "transition": ("Elliptic-to-hyperbolic transition", lambda: plot_isofrequency_transition(save_as="aniso_isofrequency_transition.png")),
        "phonon_polariton": ("Phonon polariton dispersion", lambda: plot_phonon_polariton_dispersion(save_as="aniso_phonon_polariton.png")),
        "moo3_permittivity": ("MoO3 permittivity components", lambda: plot_moo3_permittivity(save_as="aniso_moo3_permittivity.png")),
        "moo3_isofrequency": ("MoO3 isofrequency contours", lambda: plot_moo3_isofrequency(save_as="aniso_moo3_isofrequency.png")),
    }

    parser = argparse.ArgumentParser(description="Anisotropic media visualizations.")
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
