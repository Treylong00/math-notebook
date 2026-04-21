"""Visualizing Green's functions: free-space dimensions, i-epsilon prescription,
Laplace/Coulomb response to a source, and 1D scattering from a delta potential."""

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.special import hankel1

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
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )


# --- Green's functions ---


def g_free_1d(x, k, eps=0.0):
    """Retarded 1D Helmholtz Green's function: G = i e^{i k |x|} / (2k)."""
    kk = k + 1j * eps
    return 1j * np.exp(1j * kk * np.abs(x)) / (2 * kk)


def g_free_2d(r, k, eps=1e-6):
    """2D free-space Helmholtz G = -(i/4) H_0^{(1)}(k r). Hankel blows up at r=0."""
    kk = k + 1j * eps
    r_safe = np.maximum(r, 1e-6)
    return -1j / 4.0 * hankel1(0, kk * r_safe)


def g_free_3d(r, k, eps=0.0):
    """3D free-space Helmholtz G = e^{i k r} / (4 pi r)."""
    kk = k + 1j * eps
    r_safe = np.maximum(r, 1e-6)
    return np.exp(1j * kk * r_safe) / (4 * np.pi * r_safe)


# --- Figure 1: free-space G in 1D / 2D / 3D ---


def plot_free_space_dimensions(save_as=None):
    """Show Re G, Im G for the free-space Helmholtz Green's function in 1D, 2D, 3D."""
    k = 2.0
    r = np.linspace(0.05, 6.0, 800)
    x = np.linspace(-6.0, 6.0, 800)

    g1 = g_free_1d(x, k)
    g2 = g_free_2d(r, k)
    g3 = g_free_3d(r, k)

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    colors = sns.color_palette("deep")

    axes[0].plot(x, g1.real, color=colors[0], linewidth=2, label=r"$\mathrm{Re}\,G$")
    axes[0].plot(
        x, g1.imag, color=colors[1], linewidth=2, linestyle="--", label=r"$\mathrm{Im}\,G$"
    )
    axes[0].plot(
        x, np.abs(g1), color="gray", linewidth=1, linestyle=":", label=r"$|G|$"
    )
    axes[0].set_title(r"1D: $G_0(x) = \dfrac{i\,e^{ik|x|}}{2k}$")
    axes[0].set_xlabel(r"$x$")
    axes[0].axhline(0, color="gray", linewidth=0.5, linestyle=":")
    axes[0].legend(loc="upper right", fontsize=10)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(r, g2.real, color=colors[0], linewidth=2, label=r"$\mathrm{Re}\,G$")
    axes[1].plot(
        r, g2.imag, color=colors[1], linewidth=2, linestyle="--", label=r"$\mathrm{Im}\,G$"
    )
    axes[1].plot(r, np.abs(g2), color="gray", linewidth=1, linestyle=":", label=r"$|G|$")
    axes[1].set_title(r"2D: $G_0(r) = -\dfrac{i}{4}H_0^{(1)}(kr)$")
    axes[1].set_xlabel(r"$r$")
    axes[1].axhline(0, color="gray", linewidth=0.5, linestyle=":")
    axes[1].set_ylim(-0.5, 0.5)
    axes[1].legend(loc="upper right", fontsize=10)
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(r, g3.real, color=colors[0], linewidth=2, label=r"$\mathrm{Re}\,G$")
    axes[2].plot(
        r, g3.imag, color=colors[1], linewidth=2, linestyle="--", label=r"$\mathrm{Im}\,G$"
    )
    axes[2].plot(r, np.abs(g3), color="gray", linewidth=1, linestyle=":", label=r"$|G|$")
    axes[2].set_title(r"3D: $G_0(r) = \dfrac{e^{ikr}}{4\pi r}$")
    axes[2].set_xlabel(r"$r$")
    axes[2].axhline(0, color="gray", linewidth=0.5, linestyle=":")
    axes[2].set_ylim(-0.2, 0.2)
    axes[2].legend(loc="upper right", fontsize=10)
    axes[2].grid(True, alpha=0.3)

    fig.suptitle(
        r"Free-space Helmholtz Green's functions (outgoing, $k=2$)", fontsize=13
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- Figure 2: i-epsilon prescription ---


def plot_iepsilon_prescription(save_as=None):
    """Compare retarded, advanced, and standing-wave Green's functions in 1D.

    Retarded  (k -> k + i eps)  -> outgoing waves,  G_R = i e^{ ikx} / 2k  for x>0
    Advanced  (k -> k - i eps)  -> incoming waves
    Standing wave (principal value) -> pure cos(k|x|)/(2k)
    """
    k = 2.0
    x = np.linspace(-6.0, 6.0, 1200)

    g_ret = 1j * np.exp(1j * k * np.abs(x)) / (2 * k)
    g_adv = -1j * np.exp(-1j * k * np.abs(x)) / (2 * k)
    g_std = np.cos(k * np.abs(x)) / (2 * k)  # = (G_R + G_A)/2

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    colors = sns.color_palette("deep")

    for ax, g, title, subtitle in zip(
        axes,
        (g_ret, g_adv, g_std),
        (
            r"Retarded: $k \to k + i\epsilon$",
            r"Advanced: $k \to k - i\epsilon$",
            r"Standing wave: principal value",
        ),
        (
            r"outgoing  $\sim e^{+ik|x|}$",
            r"incoming  $\sim e^{-ik|x|}$",
            r"$(G_R + G_A)/2$",
        ),
    ):
        ax.plot(x, g.real, color=colors[0], linewidth=2, label=r"$\mathrm{Re}\,G$")
        ax.plot(
            x, g.imag, color=colors[1], linewidth=2, linestyle="--", label=r"$\mathrm{Im}\,G$"
        )
        ax.set_title(title + "\n" + subtitle, fontsize=11)
        ax.set_xlabel(r"$x$")
        ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.axvline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.set_ylim(-0.35, 0.35)
        ax.legend(loc="upper right", fontsize=10)
        ax.grid(True, alpha=0.3)

    # Annotate direction arrows on retarded and advanced panels
    axes[0].annotate(
        "", xy=(4.5, 0.28), xytext=(3.0, 0.28),
        arrowprops=dict(arrowstyle="->", color=colors[2], lw=2),
    )
    axes[0].annotate(
        "", xy=(-4.5, 0.28), xytext=(-3.0, 0.28),
        arrowprops=dict(arrowstyle="->", color=colors[2], lw=2),
    )
    axes[1].annotate(
        "", xy=(3.0, 0.28), xytext=(4.5, 0.28),
        arrowprops=dict(arrowstyle="->", color=colors[2], lw=2),
    )
    axes[1].annotate(
        "", xy=(-3.0, 0.28), xytext=(-4.5, 0.28),
        arrowprops=dict(arrowstyle="->", color=colors[2], lw=2),
    )

    fig.suptitle(
        r"The $i\epsilon$ prescription selects the boundary condition at infinity ($k=2$)",
        fontsize=13,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- Figure 3: Laplace/Coulomb response to a Gaussian source (2D) ---


def plot_coulomb_convolution(save_as=None):
    """In 2D, the Laplace Green's function is G(r) = -ln(r) / (2 pi).

    Solve  -nabla^2 V = rho  via  V = G * rho  for a Gaussian charge density,
    and show rho(x,y), G(x,y) (centered), V(x,y) side by side.
    """
    N = 401
    L = 6.0
    x = np.linspace(-L, L, N)
    y = np.linspace(-L, L, N)
    X, Y = np.meshgrid(x, y)

    # Gaussian charge density
    sigma = 0.6
    rho = np.exp(-(X**2 + Y**2) / (2 * sigma**2)) / (2 * np.pi * sigma**2)

    # Green's function centered at origin (for display only)
    R = np.sqrt(X**2 + Y**2)
    R_safe = np.maximum(R, 1e-3)
    G_display = -np.log(R_safe) / (2 * np.pi)

    # Analytic potential for a Gaussian charge: V(r) = -(1/4pi) [ Ei(-r^2/(2 sigma^2)) ] ...
    # Compute via FFT-based convolution for generality.
    dx = x[1] - x[0]
    # Use the centered log kernel; clip at a small radius
    V = np.zeros_like(rho)
    # Vectorized convolution via FFT
    kernel = G_display
    # Normalize via FFT convolution and recenter
    kernel_shifted = np.fft.ifftshift(kernel)
    rho_ft = np.fft.fft2(rho)
    ker_ft = np.fft.fft2(kernel_shifted)
    V = np.real(np.fft.ifft2(rho_ft * ker_ft)) * dx * dx

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    im0 = axes[0].imshow(
        rho, extent=(-L, L, -L, L), origin="lower", cmap="rocket", aspect="equal"
    )
    axes[0].set_title(r"Source  $\rho(\mathbf{r})$: Gaussian charge")
    axes[0].set_xlabel(r"$x$")
    axes[0].set_ylabel(r"$y$")
    fig.colorbar(im0, ax=axes[0], fraction=0.046)

    vmax = np.nanmax(G_display[R > 0.2])
    vmin = np.nanmin(G_display[R > 0.2])
    im1 = axes[1].imshow(
        np.clip(G_display, vmin, vmax),
        extent=(-L, L, -L, L),
        origin="lower",
        cmap="viridis",
        aspect="equal",
    )
    axes[1].set_title(r"Green's function  $G(\mathbf{r}) = -\dfrac{\ln r}{2\pi}$")
    axes[1].set_xlabel(r"$x$")
    fig.colorbar(im1, ax=axes[1], fraction=0.046)

    im2 = axes[2].imshow(
        V, extent=(-L, L, -L, L), origin="lower", cmap="mako", aspect="equal"
    )
    axes[2].set_title(r"Potential  $V = G * \rho$")
    axes[2].set_xlabel(r"$x$")
    fig.colorbar(im2, ax=axes[2], fraction=0.046)

    fig.suptitle(
        r"Laplace Green's function: convolution builds $V$ from $\rho$  ($-\nabla^2 V = \rho$)",
        fontsize=13,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- Figure 4: 1D scattering from a delta potential ---


def plot_delta_scattering(save_as=None):
    """1D scattering psi'' + k^2 psi = 2 m alpha delta(x) psi  (units hbar=1, m=1/2 -> k^2 = E).

    Exact solution for incident wave e^{ikx}:
        psi(x) = e^{ikx} + r e^{-ikx}    for x < 0
        psi(x) = t e^{ikx}                for x > 0
    with  r = -i alpha/(k + i alpha),  t = k/(k + i alpha).
    Plot Re psi, |psi|^2 for a few alpha values.
    """
    k = 3.0
    x = np.linspace(-6.0, 6.0, 1600)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    colors = sns.color_palette("deep")

    alphas = [0.0, 1.5, 5.0]
    labels = [r"$\alpha=0$ (no barrier)", r"$\alpha=1.5$", r"$\alpha=5$"]

    for idx, alpha in enumerate(alphas):
        r = -1j * alpha / (k + 1j * alpha)
        t = k / (k + 1j * alpha)
        psi = np.where(
            x < 0,
            np.exp(1j * k * x) + r * np.exp(-1j * k * x),
            t * np.exp(1j * k * x),
        )
        color = colors[idx]
        ax1.plot(x, psi.real, color=color, linewidth=1.8, label=labels[idx])
        ax2.plot(x, np.abs(psi) ** 2, color=color, linewidth=1.8, label=labels[idx])

    for ax in (ax1, ax2):
        ax.axvline(0, color="crimson", linewidth=1.2, linestyle="--", alpha=0.7)
        ax.text(0.1, ax.get_ylim()[1] * 0.9 if ax is ax2 else 1.4, r"$V(x)=\alpha\delta(x)$",
                color="crimson", fontsize=10)
        ax.set_xlabel(r"$x$")
        ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.legend(loc="lower left", fontsize=10)
        ax.grid(True, alpha=0.3)

    ax1.set_ylabel(r"$\mathrm{Re}\,\psi(x)$")
    ax1.set_title(r"Wavefunction (real part) — interference on the left")
    ax1.set_ylim(-2.5, 2.5)

    ax2.set_ylabel(r"$|\psi(x)|^2$")
    ax2.set_title(r"Probability density — standing wave left, travelling right")
    ax2.set_ylim(0, 4.2)

    fig.suptitle(
        r"1D scattering from $V(x) = \alpha\delta(x)$ via the Lippmann-Schwinger equation"
        r"  ($k=3$)",
        fontsize=13,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "dimensions": (
            "Free-space G in 1D / 2D / 3D",
            lambda: plot_free_space_dimensions(save_as="greens_free_space_dims.png"),
        ),
        "iepsilon": (
            "i-epsilon prescription (retarded / advanced / standing)",
            lambda: plot_iepsilon_prescription(save_as="greens_iepsilon.png"),
        ),
        "coulomb": (
            "Laplace/Coulomb: V = G * rho for Gaussian source",
            lambda: plot_coulomb_convolution(save_as="greens_coulomb_convolution.png"),
        ),
        "scattering": (
            "1D scattering from a delta potential",
            lambda: plot_delta_scattering(save_as="greens_delta_scattering.png"),
        ),
    }

    parser = argparse.ArgumentParser(description="Green's function figures.")
    parser.add_argument("names", nargs="*", help="figures to generate (omit for all)")
    parser.add_argument("--list", "-l", action="store_true", help="list available figures")
    args = parser.parse_args()

    if args.list:
        for name, (desc, _) in figures.items():
            print(f"  {name:20s}  {desc}")
        return

    selected = args.names or list(figures.keys())
    for name in selected:
        if name not in figures:
            print(f"Unknown figure '{name}'. Use --list to see options.")
            return
        figures[name][1]()


if __name__ == "__main__":
    main()
