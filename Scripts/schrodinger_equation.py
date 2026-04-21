"""The Schrodinger equation: particle in a box, harmonic oscillator,
time evolution, and the uncertainty principle.
"""

import math
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


# --- Particle in a box ---


def box_eigenfunction(x, n, L):
    """Normalized eigenfunction for particle in a box of length L.

    psi_n(x) = sqrt(2/L) * sin(n * pi * x / L)
    """
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L)


def box_energy(n, L):
    """Energy eigenvalue for particle in a box (natural units hbar=1, m=1/2).

    E_n = n^2 * pi^2 / L^2
    """
    return n**2 * np.pi**2 / L**2


def plot_particle_box_panel(save_as=None):
    """Multi-panel: first 4 eigenfunctions psi_n(x) and probability densities |psi_n|^2
    for the particle in a box, with energy levels marked.
    """
    L = 1.0
    x = np.linspace(0, L, 500)
    colors = sns.color_palette("deep")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    for n in range(1, 5):
        psi = box_eigenfunction(x, n, L)
        E_n = box_energy(n, L)

        # Offset by energy level for stacking
        ax1.plot(
            x, psi * 0.3 + E_n, color=colors[n - 1], linewidth=2, label=rf"$n = {n}$"
        )
        ax1.axhline(E_n, color=colors[n - 1], linewidth=0.5, alpha=0.4, linestyle="--")

        ax2.plot(
            x,
            np.abs(psi) ** 2 * 0.3 + E_n,
            color=colors[n - 1],
            linewidth=2,
            label=rf"$n = {n}$",
        )
        ax2.fill_between(
            x, E_n, np.abs(psi) ** 2 * 0.3 + E_n, color=colors[n - 1], alpha=0.15
        )
        ax2.axhline(E_n, color=colors[n - 1], linewidth=0.5, alpha=0.4, linestyle="--")

    # Draw box walls
    for ax in (ax1, ax2):
        ax.axvline(0, color="k", linewidth=2)
        ax.axvline(L, color="k", linewidth=2)
        ax.set_xlabel(r"$x$")
        ax.set_xlim(-0.05, L + 0.05)
        ax.legend(loc="upper right", fontsize=10)

    ax1.set_ylabel(r"$E_n$")
    ax1.set_title(r"Wavefunctions $\psi_n(x)$")
    ax2.set_ylabel(r"$E_n$")
    ax2.set_title(r"Probability densities $|\psi_n(x)|^2$")

    fig.suptitle("Particle in a Box", fontsize=14, y=1.01)
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- Quantum harmonic oscillator ---


def hermite(x, n):
    """Physicist's Hermite polynomial H_n(x) via recurrence.

    H_0 = 1, H_1 = 2x, H_{n+1} = 2x H_n - 2n H_{n-1}
    """
    if n == 0:
        return np.ones_like(x)
    if n == 1:
        return 2 * x
    h_prev2 = np.ones_like(x)
    h_prev1 = 2 * x
    for k in range(2, n + 1):
        h_curr = 2 * x * h_prev1 - 2 * (k - 1) * h_prev2
        h_prev2 = h_prev1
        h_prev1 = h_curr
    return h_prev1


def ho_eigenfunction(x, n, omega=1.0):
    """Normalized eigenfunction of the quantum harmonic oscillator.

    Uses natural units (hbar=1, m=1/2), so alpha = sqrt(m*omega/hbar) = sqrt(omega/2).
    psi_n(x) = (alpha/pi)^{1/4} * (1/sqrt(2^n n!)) * H_n(alpha*x) * exp(-alpha*x^2/2)
    """
    alpha = np.sqrt(omega / 2)
    xi = np.sqrt(alpha) * x
    # Normalization: (alpha/pi)^{1/4} / sqrt(2^n * n!)
    norm = (alpha / np.pi) ** 0.25 / np.sqrt(2**n * math.factorial(n))
    return norm * hermite(xi, n) * np.exp(-(xi**2) / 2)


def ho_energy(n, omega=1.0):
    """Energy eigenvalue of the harmonic oscillator (natural units hbar=1).

    E_n = omega * (n + 1/2)
    """
    return omega * (n + 0.5)


def plot_harmonic_oscillator_panel(save_as=None):
    """First 4 eigenfunctions of the harmonic oscillator superimposed on the
    parabolic potential V(x), offset by their energy levels.
    """
    omega = 1.0
    x = np.linspace(-5, 5, 1000)
    colors = sns.color_palette("deep")

    # Potential: V(x) = (1/2) m omega^2 x^2 = (omega^2 / 4) x^2 in natural units (m=1/2)
    V = 0.25 * omega**2 * x**2

    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw potential
    ax.plot(x, V, color="gray", linewidth=2, alpha=0.5, label=r"$V(x)$")
    ax.fill_between(x, 0, V, alpha=0.05, color="gray")

    for n in range(4):
        psi = ho_eigenfunction(x, n, omega)
        E_n = ho_energy(n, omega)
        scale = 0.5  # scale wavefunctions for visibility

        ax.plot(
            x,
            psi * scale + E_n,
            color=colors[n],
            linewidth=2,
            label=rf"$n = {n}$, $E_{n} = {E_n:.1f}$",
        )
        ax.fill_between(x, E_n, psi * scale + E_n, color=colors[n], alpha=0.15)
        ax.axhline(E_n, color=colors[n], linewidth=0.5, alpha=0.4, linestyle="--")

    ax.set_xlabel(r"$x$")
    ax.set_ylabel("Energy")
    ax.set_title("Quantum Harmonic Oscillator Eigenstates")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-0.2, ho_energy(4, omega) + 0.5)
    ax.legend(loc="upper right", fontsize=10)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- Time evolution ---


def plot_time_evolution_panel(save_as=None):
    """Snapshots of |psi(x,t)|^2 at different times for a superposition
    of particle-in-a-box states, showing probability sloshing.

    Uses psi(x,0) = (1/sqrt(2))(psi_1 + psi_2) and natural units.
    """
    L = 1.0
    x = np.linspace(0, L, 500)
    colors = sns.color_palette("deep")

    # Period of oscillation: T = 2*pi / (E2 - E1)
    E1 = box_energy(1, L)
    E2 = box_energy(2, L)
    T = 2 * np.pi / (E2 - E1)

    times = [0, T / 4, T / 2, 3 * T / 4]
    time_labels = [r"$t = 0$", r"$t = T/4$", r"$t = T/2$", r"$t = 3T/4$"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    psi_1 = box_eigenfunction(x, 1, L)
    psi_2 = box_eigenfunction(x, 2, L)

    for ax, t, label in zip(axes.flat, times, time_labels):
        # psi(x,t) = (1/sqrt(2)) * (psi_1 * e^{-iE_1 t} + psi_2 * e^{-iE_2 t})
        psi_t = (psi_1 * np.exp(-1j * E1 * t) + psi_2 * np.exp(-1j * E2 * t)) / np.sqrt(
            2
        )
        prob = np.abs(psi_t) ** 2

        ax.plot(x, prob, color=colors[0], linewidth=2)
        ax.fill_between(x, 0, prob, color=colors[0], alpha=0.2)
        ax.axvline(0, color="k", linewidth=2)
        ax.axvline(L, color="k", linewidth=2)
        ax.set_title(label, fontsize=13)
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$|\psi(x, t)|^2$")
        ax.set_ylim(0, 3.5)
        ax.set_xlim(-0.02, L + 0.02)

    fig.suptitle(
        r"Time evolution: $\psi = \frac{1}{\sqrt{2}}(\psi_1 + \psi_2)$",
        fontsize=14,
        y=1.01,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


# --- Uncertainty principle ---


def plot_uncertainty_panel(save_as=None):
    """Two-panel: narrow vs wide Gaussian wavepacket in position space
    and their Fourier transforms (momentum space), illustrating the
    uncertainty trade-off.
    """
    x = np.linspace(-6, 6, 1000)
    k = np.linspace(-6, 6, 1000)
    colors = sns.color_palette("deep")

    sigmas = [0.5, 2.0]
    labels_x = [r"Narrow ($\sigma_x = 0.5$)", r"Wide ($\sigma_x = 2.0$)"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    for i, sigma in enumerate(sigmas):
        # Position space: Gaussian wavepacket |psi(x)|^2
        psi_x = np.exp(-(x**2) / (4 * sigma**2)) / (2 * np.pi * sigma**2) ** 0.25
        prob_x = np.abs(psi_x) ** 2

        # Momentum space: FT of Gaussian is Gaussian with sigma_k = 1/(2*sigma)
        sigma_k = 1 / (2 * sigma)
        psi_k = np.exp(-(k**2) / (4 * sigma_k**2)) / (2 * np.pi * sigma_k**2) ** 0.25
        prob_k = np.abs(psi_k) ** 2

        ax1.plot(x, prob_x, color=colors[i], linewidth=2, label=labels_x[i])
        ax1.fill_between(x, 0, prob_x, color=colors[i], alpha=0.15)

        ax2.plot(
            k,
            prob_k,
            color=colors[i],
            linewidth=2,
            label=rf"$\sigma_k = {sigma_k:.2f}$",
        )
        ax2.fill_between(k, 0, prob_k, color=colors[i], alpha=0.15)

    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$|\psi(x)|^2$")
    ax1.set_title("Position space")
    ax1.legend(fontsize=11)

    ax2.set_xlabel(r"$k$")
    ax2.set_ylabel(r"$|\tilde{\psi}(k)|^2$")
    ax2.set_title("Momentum space")
    ax2.legend(fontsize=11)

    fig.suptitle(
        r"Uncertainty principle: $\Delta x \cdot \Delta p \geq \frac{1}{2}$"
        "\n(narrow in $x$ = wide in $k$, and vice versa)",
        fontsize=13,
        y=1.04,
    )
    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "particle_box": ("Particle in a box eigenstates", lambda: plot_particle_box_panel(save_as="schrodinger_particle_box.png")),
        "harmonic_oscillator": ("Quantum harmonic oscillator", lambda: plot_harmonic_oscillator_panel(save_as="schrodinger_harmonic_oscillator.png")),
        "time_evolution": ("Wavepacket time evolution", lambda: plot_time_evolution_panel(save_as="schrodinger_time_evolution.png")),
        "uncertainty": ("Uncertainty principle", lambda: plot_uncertainty_panel(save_as="schrodinger_uncertainty.png")),
    }

    parser = argparse.ArgumentParser(description="Schrodinger equation figures.")
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
