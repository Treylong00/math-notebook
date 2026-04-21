"""Visualizing Dirac notation concepts: projections, basis decomposition, representations."""

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


# --- Wavefunctions and basis functions ---


def gaussian_wavepacket(x, x0=0.0, sigma=0.5, k0=5.0):
    """Gaussian wavepacket: localized in both position and momentum."""
    psi = (1 / (sigma * np.sqrt(np.pi))) ** 0.5 * np.exp(
        -((x - x0) ** 2) / (2 * sigma**2) + 1j * k0 * x
    )
    return psi


def box_eigenfunction(x, n, L=np.pi):
    """Normalized eigenfunction of the infinite square well."""
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L)


def momentum_wavefunction(p, x0=0.0, sigma=0.5, k0=5.0):
    """Fourier transform of the Gaussian wavepacket: psi(p) = <p|psi>."""
    return (sigma / np.sqrt(np.pi)) ** 0.5 * np.exp(
        -((p - k0) ** 2) * sigma**2 / 2 - 1j * (p - k0) * x0
    )


# --- Plot functions ---


def plot_basis_decomposition(save_as=None):
    """Show the step-by-step projection from the x-basis into the n-basis.

    Panel 1: the state psi(x) in the position basis.
    Panel 2: the weighted components c_n * phi_n(x) that sum to psi — the
             bridge from x-domain to n-domain, making the projection explicit.
    Panel 3: the resulting |c_n|^2 bar chart in the energy basis.
    """
    L = np.pi
    x = np.linspace(0, L, 500)

    coeffs = {1: 0.7, 2: 0.5, 3: 0.3, 5: 0.2}
    norm = np.sqrt(sum(c**2 for c in coeffs.values()))
    coeffs = {n: c / norm for n, c in coeffs.items()}

    psi = np.zeros_like(x)
    for n, c in coeffs.items():
        psi += c * box_eigenfunction(x, n, L)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))
    colors = sns.color_palette("deep")

    # Panel 1: psi(x) in the position basis
    ax1.plot(x, psi, color=colors[0], linewidth=2, label=r"$\psi(x) = \langle x | \psi \rangle$")
    ax1.fill_between(x, psi, alpha=0.2, color=colors[0])
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$\psi(x)$")
    ax1.set_title(r"Position basis: $\psi(x)$")
    ax1.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper right")

    # Panel 2: weighted basis components stacked vertically, summing to psi
    sorted_ns = sorted(coeffs.keys())
    offset_step = 1.1 * max(abs(c) * np.sqrt(2 / L) for c in coeffs.values())
    top_offset = (len(sorted_ns) + 1) * offset_step
    ax2.plot(x, psi + top_offset, color=colors[0], linewidth=2)
    ax2.fill_between(x, top_offset, psi + top_offset, alpha=0.2, color=colors[0])
    ax2.text(L + 0.05, top_offset, r"$\psi(x)$", va="center", fontsize=11, color=colors[0])

    # Draw a visual "=" separator
    ax2.text(
        L / 2, top_offset - 0.55 * offset_step, r"$=\ \sum_n c_n\, \phi_n(x)$",
        ha="center", va="center", fontsize=12, color="gray",
    )

    for idx, n in enumerate(sorted_ns):
        c = coeffs[n]
        component = c * box_eigenfunction(x, n, L)
        y_offset = (len(sorted_ns) - 1 - idx) * offset_step
        color = colors[(idx + 1) % len(colors)]
        ax2.plot(x, component + y_offset, color=color, linewidth=1.8)
        ax2.fill_between(x, y_offset, component + y_offset, alpha=0.2, color=color)
        ax2.axhline(y_offset, color="gray", linewidth=0.4, linestyle=":")
        ax2.text(
            L + 0.05, y_offset,
            rf"$c_{{{n}}}\,\phi_{{{n}}}(x),\ c_{{{n}}}={c:.2f}$",
            va="center", fontsize=10, color=color,
        )

    ax2.set_xlabel(r"$x$")
    ax2.set_xlim(0, L + 1.1)
    ax2.set_yticks([])
    ax2.set_title(r"Projection: $c_n = \langle n | \psi \rangle = \int \phi_n^*(x)\,\psi(x)\,dx$")
    ax2.grid(False)

    # Panel 3: |c_n|^2 in the energy basis
    n_max = 8
    probs = [abs(coeffs.get(n, 0)) ** 2 for n in range(1, n_max + 1)]
    ax3.bar(range(1, n_max + 1), probs, color=colors[1], edgecolor="white", alpha=0.85)
    for n in coeffs:
        if n <= n_max:
            ax3.text(
                n, abs(coeffs[n]) ** 2 + 0.01,
                rf"$|c_{{{n}}}|^2$", ha="center", fontsize=10,
            )
    ax3.set_xlabel(r"$n$")
    ax3.set_ylabel(r"$|\langle n | \psi \rangle|^2$")
    ax3.set_title(r"Energy basis: $P(n) = |c_n|^2$")
    ax3.set_xticks(range(1, n_max + 1))
    ax3.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_projection_operator(save_as=None):
    """Visualize the projection operator |n><n| acting on a state.

    Three panels: original state, projected component, remainder.
    """
    L = np.pi
    x = np.linspace(0, L, 500)

    # Superposition of first 5 eigenstates
    coeffs = [0.0, 0.5, 0.6, 0.3, 0.2, 0.4]  # index 0 unused
    norm = np.sqrt(sum(c**2 for c in coeffs[1:]))
    coeffs = [c / norm for c in coeffs]

    psi = sum(coeffs[n] * box_eigenfunction(x, n, L) for n in range(1, 6))

    # Project onto |2>
    n_proj = 2
    c_n = coeffs[n_proj]
    psi_proj = c_n * box_eigenfunction(x, n_proj, L)
    psi_remainder = psi - psi_proj

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 4.5))
    colors = sns.color_palette("deep")

    ax1.plot(x, psi, color=colors[0], linewidth=2)
    ax1.fill_between(x, psi, alpha=0.15, color=colors[0])
    ax1.set_title(r"$|\psi\rangle$")
    ax1.set_xlabel(r"$x$")
    ax1.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.grid(True, alpha=0.3)

    ax2.plot(x, psi_proj, color=colors[1], linewidth=2)
    ax2.fill_between(x, psi_proj, alpha=0.15, color=colors[1])
    ax2.set_title(
        rf"$|2\rangle\langle 2|\psi\rangle = c_2 |2\rangle$"
        rf"$\quad (c_2 = {c_n:.2f})$"
    )
    ax2.set_xlabel(r"$x$")
    ax2.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.grid(True, alpha=0.3)

    ax3.plot(x, psi_remainder, color=colors[2], linewidth=2)
    ax3.fill_between(x, psi_remainder, alpha=0.15, color=colors[2])
    ax3.set_title(r"$(1 - |2\rangle\langle 2|)|\psi\rangle$")
    ax3.set_xlabel(r"$x$")
    ax3.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax3.grid(True, alpha=0.3)

    # Match y-axis limits
    y_max = max(abs(psi).max(), abs(psi_proj).max(), abs(psi_remainder).max()) * 1.15
    for ax in (ax1, ax2, ax3):
        ax.set_ylim(-y_max, y_max)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_completeness(save_as=None):
    """Visualize the completeness relation: sum_n |n><n| = I.

    Shows partial sums of projections reconstructing the original state.
    """
    L = np.pi
    x = np.linspace(0, L, 500)

    # A non-trivial function to reconstruct
    psi = x * (np.pi - x)
    psi = psi / np.sqrt(np.trapezoid(psi**2, x))

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    colors = sns.color_palette("deep")

    for idx, n_max in enumerate([1, 3, 5, 15]):
        ax = axes[idx // 2, idx % 2]

        # Compute partial sum of projections
        reconstruction = np.zeros_like(x)
        for n in range(1, n_max + 1):
            phi_n = box_eigenfunction(x, n, L)
            c_n = np.trapezoid(phi_n * psi, x)
            reconstruction += c_n * phi_n

        ax.plot(x, psi, color="gray", linewidth=1.5, linestyle="--", label=r"$\psi(x)$")
        ax.plot(
            x,
            reconstruction,
            color=colors[0],
            linewidth=2,
            label=rf"$\sum_{{n=1}}^{{{n_max}}} |n\rangle\langle n|\psi\rangle$",
        )
        ax.fill_between(x, reconstruction, alpha=0.15, color=colors[0])
        ax.set_title(rf"$N = {n_max}$")
        ax.set_xlabel(r"$x$")
        ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.legend(loc="upper right", fontsize=9)
        ax.grid(True, alpha=0.3)

    plt.suptitle(
        r"Completeness: $\sum_{n=1}^{N} |n\rangle\langle n| \to \hat{I}$ as $N \to \infty$",
        fontsize=14,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_position_momentum(save_as=None):
    """Two-panel: same state in position and momentum representation.

    psi(x) = <x|psi> and phi(p) = <p|psi>, showing the Fourier duality.
    """
    x = np.linspace(-4, 4, 1000)
    p = np.linspace(-5, 15, 1000)

    psi_x = gaussian_wavepacket(x, x0=0, sigma=0.5, k0=5.0)
    psi_p = momentum_wavefunction(p, x0=0, sigma=0.5, k0=5.0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    colors = sns.color_palette("deep")

    # Position representation
    ax1.plot(x, np.real(psi_x), color=colors[0], linewidth=1.5, label=r"$\mathrm{Re}$")
    ax1.plot(
        x,
        np.imag(psi_x),
        color=colors[1],
        linewidth=1.5,
        linestyle="--",
        label=r"$\mathrm{Im}$",
    )
    ax1.plot(
        x, np.abs(psi_x), color="gray", linewidth=1, linestyle=":", label=r"$|\psi|$"
    )
    ax1.fill_between(x, np.abs(psi_x) ** 2, alpha=0.15, color=colors[0])
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$\psi(x) = \langle x | \psi \rangle$")
    ax1.set_title(r"Position representation")
    ax1.legend(loc="upper right")
    ax1.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax1.grid(True, alpha=0.3)

    # Momentum representation
    ax2.plot(p, np.real(psi_p), color=colors[0], linewidth=1.5, label=r"$\mathrm{Re}$")
    ax2.plot(
        p,
        np.imag(psi_p),
        color=colors[1],
        linewidth=1.5,
        linestyle="--",
        label=r"$\mathrm{Im}$",
    )
    ax2.plot(
        p,
        np.abs(psi_p),
        color="gray",
        linewidth=1,
        linestyle=":",
        label=r"$|\tilde\psi|$",
    )
    ax2.fill_between(p, np.abs(psi_p) ** 2, alpha=0.15, color=colors[1])
    ax2.set_xlabel(r"$p$")
    ax2.set_ylabel(r"$\tilde\psi(p) = \langle p | \psi \rangle$")
    ax2.set_title(r"Momentum representation")
    ax2.legend(loc="upper right")
    ax2.axhline(0, color="gray", linewidth=0.5, linestyle=":")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_matrix_elements(save_as=None):
    """Visualize operator matrix elements <m|A|n> as a heatmap.

    Uses the position operator x in the particle-in-a-box basis.
    """
    L = np.pi
    x = np.linspace(0, L, 1000)
    n_basis = 8

    # Compute <m|x|n> matrix
    matrix = np.zeros((n_basis, n_basis))
    for m in range(1, n_basis + 1):
        phi_m = box_eigenfunction(x, m, L)
        for n in range(1, n_basis + 1):
            phi_n = box_eigenfunction(x, n, L)
            matrix[m - 1, n - 1] = np.trapezoid(phi_m * x * phi_n, x)

    fig, ax = plt.subplots(figsize=(7, 6))
    vmax = np.abs(matrix).max()
    im = ax.imshow(
        matrix,
        cmap="twilight",
        vmin=-vmax,
        vmax=vmax,
        origin="lower",
        extent=[0.5, n_basis + 0.5, 0.5, n_basis + 0.5],
    )
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$m$")
    ax.set_title(r"Matrix elements $\langle m | \hat{x} | n \rangle$")
    ax.set_xticks(range(1, n_basis + 1))
    ax.set_yticks(range(1, n_basis + 1))
    fig.colorbar(im, ax=ax)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "basis": ("Basis decomposition", lambda: plot_basis_decomposition(save_as="dirac_basis_decomposition.png")),
        "projection": ("Projection operator", lambda: plot_projection_operator(save_as="dirac_projection.png")),
        "completeness": ("Completeness relation", lambda: plot_completeness(save_as="dirac_completeness.png")),
        "position_momentum": ("Position and momentum bases", lambda: plot_position_momentum(save_as="dirac_position_momentum.png")),
        "matrix_elements": ("Matrix elements", lambda: plot_matrix_elements(save_as="dirac_matrix_elements.png")),
    }

    parser = argparse.ArgumentParser(description="Dirac notation figures.")
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
