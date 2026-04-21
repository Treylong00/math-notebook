"""Probability and complex amplitudes: the Born rule, interference, and superposition."""

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


# --- Wavefunctions ---


def gaussian_wavepacket(x, x0=0.0, sigma=1.0, k0=5.0):
    """Normalized Gaussian wave packet: exp(ik0*x) * Gaussian envelope.

    Returns a complex-valued wavefunction centered at x0 with width sigma
    and carrier wavenumber k0.
    """
    norm = (2 * np.pi * sigma**2) ** (-0.25)
    return norm * np.exp(-((x - x0) ** 2) / (4 * sigma**2)) * np.exp(1j * k0 * x)


def particle_in_box(x, n, L=np.pi):
    """Normalized eigenstate of the particle in a box.

    psi_n(x) = sqrt(2/L) * sin(n*pi*x/L) for x in [0, L], zero elsewhere.
    """
    psi = np.sqrt(2 / L) * np.sin(n * np.pi * x / L)
    return np.where((x >= 0) & (x <= L), psi, 0.0)


# --- Plot functions ---


def plot_born_rule_panel(save_as=None):
    """Two-panel figure: complex wavefunction and its probability density.

    Left: Re(psi) and Im(psi) for a Gaussian wave packet.
    Right: |psi|^2 with shaded area representing total probability = 1.
    """
    x = np.linspace(-5, 5, 1000)
    psi = gaussian_wavepacket(x, x0=0.0, sigma=1.0, k0=5.0)
    prob = np.abs(psi) ** 2

    colors = sns.color_palette("deep")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left panel: Re and Im parts
    ax1.plot(
        x, np.real(psi), color=colors[0], linewidth=1.5, label=r"$\mathrm{Re}(\psi)$"
    )
    ax1.plot(
        x, np.imag(psi), color=colors[1], linewidth=1.5, label=r"$\mathrm{Im}(\psi)$"
    )
    ax1.plot(
        x,
        np.abs(psi),
        color="gray",
        linewidth=1.0,
        linestyle="--",
        label=r"$|\psi|$ (envelope)",
    )
    ax1.plot(x, -np.abs(psi), color="gray", linewidth=1.0, linestyle="--")
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$\psi(x)$")
    ax1.set_title(r"Complex wavefunction $\psi(x)$")
    ax1.legend(loc="upper right", fontsize=10)

    # Right panel: probability density
    ax2.plot(x, prob, color=colors[2], linewidth=1.8)
    ax2.fill_between(x, 0, prob, alpha=0.2, color=colors[2])
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$|\psi(x)|^2$")
    ax2.set_title(r"Probability density $|\psi(x)|^2$")
    ax2.annotate(
        r"$\int_{-\infty}^{\infty} |\psi|^2 \, dx = 1$",
        xy=(0.6, 0.85),
        xycoords="axes fraction",
        fontsize=13,
    )

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_interference_panel(save_as=None):
    """Three-panel figure showing interference of two wave packets.

    Panel 1: |psi_1|^2 alone.
    Panel 2: |psi_2|^2 alone.
    Panel 3: |psi_1 + psi_2|^2 compared to |psi_1|^2 + |psi_2|^2.
    """
    x = np.linspace(-6, 6, 1000)
    psi1 = gaussian_wavepacket(x, x0=-1.0, sigma=1.0, k0=5.0)
    psi2 = gaussian_wavepacket(x, x0=1.0, sigma=1.0, k0=5.0)

    prob1 = np.abs(psi1) ** 2
    prob2 = np.abs(psi2) ** 2
    prob_sum = prob1 + prob2
    prob_coherent = np.abs(psi1 + psi2) ** 2

    colors = sns.color_palette("deep")
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 4.5))

    # Panel 1: psi_1 alone
    ax1.plot(x, prob1, color=colors[0], linewidth=1.8)
    ax1.fill_between(x, 0, prob1, alpha=0.2, color=colors[0])
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$|\psi_1|^2$")
    ax1.set_title(r"Slit 1 alone")
    ax1.set_ylim(0, None)

    # Panel 2: psi_2 alone
    ax2.plot(x, prob2, color=colors[1], linewidth=1.8)
    ax2.fill_between(x, 0, prob2, alpha=0.2, color=colors[1])
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$|\psi_2|^2$")
    ax2.set_title(r"Slit 2 alone")
    ax2.set_ylim(0, None)

    # Panel 3: coherent sum vs incoherent sum
    ax3.plot(
        x,
        prob_sum,
        color="gray",
        linewidth=1.5,
        linestyle="--",
        label=r"$|\psi_1|^2 + |\psi_2|^2$ (classical)",
    )
    ax3.plot(
        x,
        prob_coherent,
        color=colors[3],
        linewidth=1.8,
        label=r"$|\psi_1 + \psi_2|^2$ (quantum)",
    )
    ax3.fill_between(x, 0, prob_coherent, alpha=0.15, color=colors[3])
    ax3.set_xlabel(r"$x$")
    ax3.set_ylabel("Probability density")
    ax3.set_title("Both slits open")
    ax3.legend(loc="upper right", fontsize=9)
    ax3.set_ylim(0, None)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_phase_matters_panel(save_as=None):
    """Two-panel figure: constructive vs destructive interference from phase shift.

    Left: |psi_1 + psi_2|^2 with relative phase 0 (constructive).
    Right: |psi_1 + e^{i*pi} psi_2|^2 (destructive).
    """
    x = np.linspace(-6, 6, 1000)
    psi1 = gaussian_wavepacket(x, x0=-1.0, sigma=1.0, k0=5.0)
    psi2 = gaussian_wavepacket(x, x0=1.0, sigma=1.0, k0=5.0)

    prob_constructive = np.abs(psi1 + psi2) ** 2
    prob_destructive = np.abs(psi1 + np.exp(1j * np.pi) * psi2) ** 2

    colors = sns.color_palette("deep")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: constructive (phase = 0)
    ax1.plot(x, prob_constructive, color=colors[0], linewidth=1.8)
    ax1.fill_between(x, 0, prob_constructive, alpha=0.2, color=colors[0])
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$|\psi_1 + \psi_2|^2$")
    ax1.set_title(r"Relative phase $\Delta\phi = 0$")
    ax1.set_ylim(0, None)

    # Right: destructive (phase = pi)
    ax2.plot(x, prob_destructive, color=colors[3], linewidth=1.8)
    ax2.fill_between(x, 0, prob_destructive, alpha=0.2, color=colors[3])
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$|\psi_1 + e^{i\pi}\psi_2|^2$")
    ax2.set_title(r"Relative phase $\Delta\phi = \pi$")
    ax2.set_ylim(0, None)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_superposition_panel(save_as=None):
    """Four-panel figure: particle-in-a-box superposition with different relative phases.

    Shows psi_1 + e^{i*phi} * psi_2 for phi = 0, pi/2, pi, 3*pi/2.
    Each panel shows the probability density |psi|^2.
    """
    x = np.linspace(-0.3, np.pi + 0.3, 1000)
    psi1 = particle_in_box(x, n=1).astype(complex)
    psi2 = particle_in_box(x, n=2).astype(complex)

    phases = [0, np.pi / 2, np.pi, 3 * np.pi / 2]
    phase_labels = [r"0", r"\pi/2", r"\pi", r"3\pi/2"]

    colors = sns.color_palette("deep")
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))

    for ax, phi, label in zip(axes.flat, phases, phase_labels):
        # Superposition with equal weights, normalized
        psi = (psi1 + np.exp(1j * phi) * psi2) / np.sqrt(2)
        prob = np.abs(psi) ** 2

        ax.plot(x, prob, color=colors[0], linewidth=1.8)
        ax.fill_between(x, 0, prob, alpha=0.2, color=colors[0])

        # Show the box boundaries
        ax.axvline(0, color="gray", linewidth=1, linestyle=":")
        ax.axvline(np.pi, color="gray", linewidth=1, linestyle=":")

        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$|\psi|^2$")
        ax.set_title(rf"$\phi = {label}$")
        ax.set_ylim(0, None)

    fig.suptitle(
        r"$\psi = \frac{1}{\sqrt{2}}(\psi_1 + e^{i\phi}\,\psi_2)$: "
        "relative phase shifts probability",
        fontsize=13,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "born_rule": ("Born rule probabilities", lambda: plot_born_rule_panel(save_as="prob_born_rule.png")),
        "interference": ("Quantum interference", lambda: plot_interference_panel(save_as="prob_interference.png")),
        "phase": ("Phase effects on amplitudes", lambda: plot_phase_matters_panel(save_as="prob_phase_matters.png")),
        "superposition": ("Superposition of states", lambda: plot_superposition_panel(save_as="prob_superposition.png")),
    }

    parser = argparse.ArgumentParser(description="Probability amplitude figures.")
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
