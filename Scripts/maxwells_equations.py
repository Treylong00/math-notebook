"""Visualizing Maxwell's equations as an eigenvalue problem and the connection
between electromagnetic modes, dispersion, and quantum formalism."""

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


# --- Dispersion relations ---


def dispersion_vacuum(k):
    """omega = c * k (vacuum light line, c = 1)."""
    return np.abs(k)


def dispersion_dielectric(k, n_r=1.5):
    """omega = c * k / n (dielectric, phase velocity = c/n)."""
    return np.abs(k) / n_r


def dispersion_plasma(k, omega_p=1.0):
    """omega = sqrt(omega_p^2 + c^2 k^2) — plasma/Drude dispersion."""
    return np.sqrt(omega_p**2 + k**2)


def dispersion_phonon_polariton(k, omega_to=1.0, omega_lo=1.5, eps_inf=1.0):
    """Phonon-polariton dispersion: two branches from coupling of light with
    a transverse optical phonon. Solves eps(omega) * omega^2 = c^2 k^2 where
    eps(omega) = eps_inf * (omega_lo^2 - omega^2) / (omega_to^2 - omega^2).
    """
    # Solve the quartic: eps_inf*(omega_lo^2 - w^2)/(omega_to^2 - w^2) * w^2 = k^2
    # Rearrange to: eps_inf*(omega_lo^2 - w^2)*w^2 = k^2*(omega_to^2 - w^2)
    # eps_inf*omega_lo^2*w^2 - eps_inf*w^4 = k^2*omega_to^2 - k^2*w^2
    # eps_inf*w^4 - (eps_inf*omega_lo^2 + k^2)*w^2 + k^2*omega_to^2 = 0
    a = eps_inf
    b = -(eps_inf * omega_lo**2 + k**2)
    c = k**2 * omega_to**2
    disc = b**2 - 4 * a * c
    disc = np.maximum(disc, 0)
    w2_upper = (-b + np.sqrt(disc)) / (2 * a)
    w2_lower = (-b - np.sqrt(disc)) / (2 * a)
    return np.sqrt(np.maximum(w2_lower, 0)), np.sqrt(np.maximum(w2_upper, 0))


# --- Fresnel coefficients ---


def fresnel_rs(theta_i, n1, n2):
    """Fresnel reflection coefficient for s-polarization (TE)."""
    cos_i = np.cos(theta_i)
    sin_t2 = (n1 / n2 * np.sin(theta_i)) ** 2
    cos_t = np.sqrt(np.maximum(1 - sin_t2, 0).astype(complex))
    return (n1 * cos_i - n2 * cos_t) / (n1 * cos_i + n2 * cos_t)


def fresnel_rp(theta_i, n1, n2):
    """Fresnel reflection coefficient for p-polarization (TM)."""
    cos_i = np.cos(theta_i)
    sin_t2 = (n1 / n2 * np.sin(theta_i)) ** 2
    cos_t = np.sqrt(np.maximum(1 - sin_t2, 0).astype(complex))
    return (n2 * cos_i - n1 * cos_t) / (n2 * cos_i + n1 * cos_t)


# --- Waveguide modes ---


def slab_te_mode(x, d, n_mode):
    """TE mode profile of a symmetric dielectric slab waveguide.

    x: transverse coordinate
    d: half-width of slab
    n_mode: mode index (0, 1, 2, ...)
    """
    kx = (n_mode + 1) * np.pi / (2 * d)
    profile = np.where(
        np.abs(x) <= d,
        np.cos(kx * x) if n_mode % 2 == 0 else np.sin(kx * x),
        0.0,
    )
    # Evanescent tails
    gamma = kx * 0.5  # simplified decay constant
    profile = np.where(
        x > d,
        (np.cos(kx * d) if n_mode % 2 == 0 else np.sin(kx * d))
        * np.exp(-gamma * (x - d)),
        profile,
    )
    profile = np.where(
        x < -d,
        (np.cos(kx * d) if n_mode % 2 == 0 else -np.sin(kx * d))
        * np.exp(-gamma * (-x - d)),
        profile,
    )
    return profile


# --- Plot functions ---


def plot_dispersion_panel(save_as=None):
    """Three-panel: vacuum vs dielectric dispersion, plasma dispersion,
    phonon-polariton anti-crossing.
    """
    k = np.linspace(0, 4, 500)
    colors = sns.color_palette("deep")

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

    # Panel 1: vacuum vs dielectric
    ax1.plot(k, dispersion_vacuum(k), color=colors[0], linewidth=2, label="Vacuum")
    ax1.plot(
        k,
        dispersion_dielectric(k, n_r=1.5),
        color=colors[1],
        linewidth=2,
        linestyle="--",
        label=r"Dielectric ($n = 1.5$)",
    )
    ax1.plot(
        k,
        dispersion_dielectric(k, n_r=2.5),
        color=colors[2],
        linewidth=2,
        linestyle=":",
        label=r"Dielectric ($n = 2.5$)",
    )
    ax1.set_xlabel(r"$k$")
    ax1.set_ylabel(r"$\omega$")
    ax1.set_title(r"$\omega = ck/n$ — light slows in matter")
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Panel 2: plasma dispersion
    omega_p = 1.0
    ax2.plot(
        k, dispersion_plasma(k, omega_p), color=colors[3], linewidth=2, label="Plasma"
    )
    ax2.plot(
        k,
        dispersion_vacuum(k),
        color=colors[0],
        linewidth=1,
        linestyle="--",
        alpha=0.5,
        label="Light line",
    )
    ax2.axhline(omega_p, color="gray", linewidth=0.8, linestyle=":", alpha=0.7)
    ax2.text(0.1, omega_p + 0.08, r"$\omega_p$", fontsize=11, color="gray")
    ax2.set_xlabel(r"$k$")
    ax2.set_ylabel(r"$\omega$")
    ax2.set_title(r"$\omega^2 = \omega_p^2 + c^2 k^2$ — plasma")
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    # Panel 3: phonon-polariton
    omega_to, omega_lo = 1.0, 1.5
    lower, upper = dispersion_phonon_polariton(k, omega_to, omega_lo)
    ax3.plot(k, lower, color=colors[0], linewidth=2, label="Lower polariton")
    ax3.plot(k, upper, color=colors[1], linewidth=2, label="Upper polariton")
    ax3.plot(
        k, dispersion_vacuum(k), color="gray", linewidth=0.8, linestyle="--", alpha=0.5
    )
    ax3.axhline(omega_to, color="gray", linewidth=0.8, linestyle=":")
    ax3.axhline(omega_lo, color="gray", linewidth=0.8, linestyle=":")
    ax3.text(
        3.5, omega_to - 0.1, r"$\omega_{TO}$", fontsize=10, color="gray", ha="center"
    )
    ax3.text(
        3.5, omega_lo + 0.06, r"$\omega_{LO}$", fontsize=10, color="gray", ha="center"
    )
    # Shade the Reststrahlen band
    ax3.axhspan(omega_to, omega_lo, alpha=0.08, color="red")
    ax3.set_xlabel(r"$k$")
    ax3.set_ylabel(r"$\omega$")
    ax3.set_title("Phonon-polariton anti-crossing")
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 3)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_fresnel_panel(save_as=None):
    """Two-panel: Fresnel reflection coefficients |r|^2 and phase for
    s- and p-polarization at an air-glass interface.
    """
    theta = np.linspace(0, np.pi / 2 - 0.01, 500)
    n1, n2 = 1.0, 1.5
    theta_B = np.arctan(n2 / n1)  # Brewster's angle

    rs = fresnel_rs(theta, n1, n2)
    rp = fresnel_rp(theta, n1, n2)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    colors = sns.color_palette("deep")

    # Left: reflectance
    ax1.plot(
        np.degrees(theta), np.abs(rs) ** 2, color=colors[0], linewidth=2, label="TE (s)"
    )
    ax1.plot(
        np.degrees(theta), np.abs(rp) ** 2, color=colors[1], linewidth=2, label="TM (p)"
    )
    ax1.axvline(
        np.degrees(theta_B), color="gray", linewidth=0.8, linestyle=":", alpha=0.7
    )
    ax1.text(np.degrees(theta_B) + 1, 0.5, r"$\theta_B$", fontsize=11, color="gray")
    ax1.set_xlabel(r"$\theta_i$ (degrees)")
    ax1.set_ylabel(r"$|r|^2$")
    ax1.set_title(r"Reflectance — air ($n=1$) to glass ($n=1.5$)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 90)
    ax1.set_ylim(0, 1.05)

    # Right: phase of reflection coefficient
    ax2.plot(
        np.degrees(theta),
        np.angle(rs),
        color=colors[0],
        linewidth=2,
        label="TE (s)",
    )
    ax2.plot(
        np.degrees(theta),
        np.angle(rp),
        color=colors[1],
        linewidth=2,
        label="TM (p)",
    )
    ax2.axvline(
        np.degrees(theta_B), color="gray", linewidth=0.8, linestyle=":", alpha=0.7
    )
    ax2.set_xlabel(r"$\theta_i$ (degrees)")
    ax2.set_ylabel(r"$\arg(r)$")
    ax2.set_title("Reflection phase")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 90)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_waveguide_modes(save_as=None):
    """Three-panel: first three TE modes of a slab waveguide,
    analogous to eigenfunctions of the Schrodinger equation.
    """
    x = np.linspace(-3, 3, 1000)
    d = 1.0  # half-width
    colors = sns.color_palette("deep")

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for idx, ax in enumerate(axes):
        profile = slab_te_mode(x, d, idx)
        # Normalize for display
        profile = profile / np.max(np.abs(profile))

        ax.fill_between(x, profile, alpha=0.2, color=colors[idx])
        ax.plot(x, profile, color=colors[idx], linewidth=2)

        # Draw the slab boundaries
        ax.axvline(-d, color="gray", linewidth=1.5, linestyle="-", alpha=0.5)
        ax.axvline(d, color="gray", linewidth=1.5, linestyle="-", alpha=0.5)
        ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")

        # Shade slab region
        ax.axvspan(-d, d, alpha=0.05, color="gray")

        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$E_y(x)$")
        ax.set_title(rf"$\mathrm{{TE}}_{idx}$ mode")
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-1.3, 1.3)

    plt.suptitle(
        r"Waveguide modes $\longleftrightarrow$ eigenfunctions of $-d^2/dx^2 + V(x)$",
        fontsize=13,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_transfer_matrix(save_as=None):
    """Visualize the transfer matrix approach: field amplitudes propagating
    through a multilayer stack, analogous to quantum tunneling.
    """
    colors = sns.color_palette("deep")

    # Three-layer system: air | glass | air
    n_layers = [1.0, 2.5, 1.0]
    d_layers = [2.0, 1.5, 2.0]
    k0 = 6.0  # free-space wavenumber

    fig, ax = plt.subplots(figsize=(10, 5))

    x_start = 0.0
    boundaries = [x_start]
    for d in d_layers:
        x_start += d
        boundaries.append(x_start)

    # Plot field in each layer
    for i, (n, d) in enumerate(zip(n_layers, d_layers)):
        x = np.linspace(boundaries[i], boundaries[i + 1], 300)
        k = n * k0

        if i == 0:
            # Incident + reflected
            field = np.cos(k * x) + 0.3 * np.cos(k * x + 1.2)
        elif i == 1:
            # Shorter wavelength inside
            amplitude = 0.8
            field = amplitude * np.cos(k * (x - boundaries[i]))
        else:
            # Transmitted
            field = 0.65 * np.cos(k * (x - boundaries[i]) - 0.5)

        ax.plot(x, field, color=colors[i], linewidth=2)
        ax.fill_between(x, field, alpha=0.1, color=colors[i])

    # Draw boundaries and label regions
    for b in boundaries[1:-1]:
        ax.axvline(b, color="black", linewidth=1.5, linestyle="-", alpha=0.6)

    mid = [(boundaries[i] + boundaries[i + 1]) / 2 for i in range(len(d_layers))]
    labels = [r"$n_1 = 1.0$", r"$n_2 = 2.5$", r"$n_3 = 1.0$"]
    for m, label in zip(mid, labels):
        ax.text(m, 1.2, label, ha="center", fontsize=11)

    # Transfer matrix annotation
    ax.annotate(
        "",
        xy=(boundaries[2], -0.9),
        xytext=(boundaries[1], -0.9),
        arrowprops=dict(arrowstyle="<->", color="gray", lw=1.5),
    )
    ax.text(
        (boundaries[1] + boundaries[2]) / 2,
        -1.1,
        r"$M = P \cdot D \cdot P^{-1}$",
        ha="center",
        fontsize=11,
        color="gray",
    )

    ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax.set_xlabel(r"$z$")
    ax.set_ylabel(r"$E(z)$")
    ax.set_title(
        "Field through a multilayer: transfer matrix connects amplitudes at each interface"
    )
    ax.set_ylim(-1.4, 1.5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_schrodinger_maxwell_analogy(save_as=None):
    """Side-by-side: particle in a potential well vs EM mode in a waveguide.
    Shows the structural identity of the two eigenvalue problems.
    """
    x = np.linspace(-3, 3, 1000)
    colors = sns.color_palette("deep")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Left: quantum particle in a box
    d = 1.0
    v_qm = np.where(np.abs(x) <= d, 0, 3)
    ax1.fill_between(x, v_qm, alpha=0.1, color="gray")
    ax1.plot(x, v_qm, color="gray", linewidth=1.5, label=r"$V(x)$")

    # First two eigenstates offset by energy
    for n, e_offset in [(0, 0.5), (1, 1.5)]:
        kx = (n + 1) * np.pi / (2 * d)
        psi = np.where(
            np.abs(x) <= d, np.cos(kx * x) if n % 2 == 0 else np.sin(kx * x), 0
        )
        gamma = kx * 0.4
        psi = np.where(
            x > d,
            (np.cos(kx * d) if n % 2 == 0 else np.sin(kx * d))
            * np.exp(-gamma * (x - d)),
            psi,
        )
        psi = np.where(
            x < -d,
            (np.cos(kx * d) if n % 2 == 0 else -np.sin(kx * d))
            * np.exp(-gamma * (-x - d)),
            psi,
        )
        psi = psi / np.max(np.abs(psi)) * 0.4
        ax1.plot(x, psi + e_offset, color=colors[n], linewidth=2)
        ax1.fill_between(x, psi + e_offset, e_offset, alpha=0.15, color=colors[n])
        ax1.axhline(e_offset, color=colors[n], linewidth=0.5, linestyle="--", alpha=0.5)
        ax1.text(2.2, e_offset, rf"$E_{n}$", fontsize=11, color=colors[n])

    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$\psi_n(x)$, offset by $E_n$")
    ax1.set_title(r"QM: $-\psi'' + V\psi = E\psi$")
    ax1.set_ylim(-0.5, 3.5)
    ax1.grid(True, alpha=0.3)

    # Right: EM mode in a waveguide (refractive index profile)
    n_core, n_clad = 2.0, 1.0
    n_profile = np.where(np.abs(x) <= d, n_core**2, n_clad**2)
    ax2.fill_between(x, n_profile, alpha=0.1, color="gray")
    ax2.plot(x, n_profile, color="gray", linewidth=1.5, label=r"$n^2(x)$")

    for m, beta_offset in [(0, 1.5), (1, 2.8)]:
        profile = slab_te_mode(x, d, m)
        profile = profile / np.max(np.abs(profile)) * 0.4
        ax2.plot(x, profile + beta_offset, color=colors[m], linewidth=2)
        ax2.fill_between(
            x, profile + beta_offset, beta_offset, alpha=0.15, color=colors[m]
        )
        ax2.axhline(
            beta_offset, color=colors[m], linewidth=0.5, linestyle="--", alpha=0.5
        )
        ax2.text(2.2, beta_offset, rf"$\beta_{m}^2$", fontsize=11, color=colors[m])

    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$E_y^{(m)}(x)$, offset by $\beta_m^2$")
    ax2.set_title(r"EM: $-E'' + n^2(x) k_0^2 E = \beta^2 E$")
    ax2.set_ylim(-0.5, 4.5)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_fresnel_contour_panel(save_as=None):
    """2x2 panel: |r| and arg(r) as contour plots over (theta_i, n2).

    Top row: s-polarization (TE).
    Bottom row: p-polarization (TM).
    """
    theta = np.linspace(0, np.pi / 2 - 0.01, 500)
    n2_vals = np.linspace(0.2, 3.0, 500)
    THETA, N2 = np.meshgrid(theta, n2_vals)
    n1 = 1.0

    rs = fresnel_rs(THETA, n1, N2)
    rp = fresnel_rp(THETA, n1, N2)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Top-left: |r_s|
    c00 = axes[0, 0].contourf(
        np.degrees(THETA), N2, np.abs(rs), levels=100, cmap="rocket"
    )
    axes[0, 0].contour(
        np.degrees(THETA),
        N2,
        np.abs(rs),
        levels=10,
        colors="k",
        linewidths=0.3,
        alpha=0.3,
    )
    axes[0, 0].set_title(r"$|r_s|$ (TE)")
    axes[0, 0].set_ylabel(r"$n_2$")
    fig.colorbar(c00, ax=axes[0, 0])

    # Top-right: arg(r_s)
    c01 = axes[0, 1].contourf(
        np.degrees(THETA),
        N2,
        np.angle(rs),
        levels=100,
        cmap="twilight",
        vmin=-np.pi,
        vmax=np.pi,
    )
    axes[0, 1].set_title(r"$\arg(r_s)$ (TE)")
    axes[0, 1].set_ylabel(r"$n_2$")
    fig.colorbar(c01, ax=axes[0, 1])

    # Bottom-left: |r_p|
    c10 = axes[1, 0].contourf(
        np.degrees(THETA), N2, np.abs(rp).astype(float), levels=100, cmap="rocket"
    )
    axes[1, 0].contour(
        np.degrees(THETA),
        N2,
        np.abs(rp).astype(float),
        levels=10,
        colors="k",
        linewidths=0.3,
        alpha=0.3,
    )
    # Brewster angle curve: theta_B = arctan(n2/n1)
    theta_b_curve = np.degrees(np.arctan(n2_vals / n1))
    axes[1, 0].plot(
        theta_b_curve,
        n2_vals,
        color="white",
        linewidth=1.5,
        linestyle="--",
        label=r"$\theta_B$",
    )
    axes[1, 0].legend(fontsize=9, loc="upper left")
    axes[1, 0].set_title(r"$|r_p|$ (TM)")
    axes[1, 0].set_xlabel(r"$\theta_i$ (degrees)")
    axes[1, 0].set_ylabel(r"$n_2$")
    fig.colorbar(c10, ax=axes[1, 0])

    # Bottom-right: arg(r_p)
    c11 = axes[1, 1].contourf(
        np.degrees(THETA),
        N2,
        np.angle(rp).astype(float),
        levels=100,
        cmap="twilight",
        vmin=-np.pi,
        vmax=np.pi,
    )
    axes[1, 1].plot(
        theta_b_curve,
        n2_vals,
        color="white",
        linewidth=1.5,
        linestyle="--",
        label=r"$\theta_B$",
    )
    axes[1, 1].legend(fontsize=9, loc="upper left")
    axes[1, 1].set_title(r"$\arg(r_p)$ (TM)")
    axes[1, 1].set_xlabel(r"$\theta_i$ (degrees)")
    axes[1, 1].set_ylabel(r"$n_2$")
    fig.colorbar(c11, ax=axes[1, 1])

    # Shared formatting
    for ax in axes.flat:
        ax.set_xlim(0, 90)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "dispersion": ("Dispersion relations", lambda: plot_dispersion_panel(save_as="maxwell_dispersion.png")),
        "fresnel": ("Fresnel coefficients", lambda: plot_fresnel_panel(save_as="maxwell_fresnel.png")),
        "fresnel_contour": ("Fresnel contour plot", lambda: plot_fresnel_contour_panel(save_as="maxwell_fresnel_contour.png")),
        "waveguide": ("Waveguide modes", lambda: plot_waveguide_modes(save_as="maxwell_waveguide_modes.png")),
        "transfer_matrix": ("Transfer matrix method", lambda: plot_transfer_matrix(save_as="maxwell_transfer_matrix.png")),
        "analogy": ("Schrodinger-Maxwell analogy", lambda: plot_schrodinger_maxwell_analogy(save_as="maxwell_schrodinger_analogy.png")),
    }

    parser = argparse.ArgumentParser(description="Maxwell's equations figures.")
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
