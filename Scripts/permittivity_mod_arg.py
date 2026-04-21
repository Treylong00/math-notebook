"""Visualizing complex permittivity of non-resonant, Drude, and Lorentzian materials.

Plots mod(eps) and arg(eps) as functions of frequency for each model,
plus contour maps in the complex plane.
"""

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


# --- Permittivity models ---


def eps_non_resonant(omega, eps_inf=2.25):
    """Non-resonant dielectric: constant real permittivity (e.g., glass in the visible).

    eps(omega) = eps_inf (purely real, no dispersion).
    """
    return np.full_like(omega, eps_inf, dtype=complex)


def eps_drude(omega, eps_inf=1.0, omega_p=1.0, gamma=0.05):
    """Drude model: free-electron response (metals, doped semiconductors).

    eps(omega) = eps_inf - omega_p^2 / (omega^2 + i*gamma*omega)
    """
    return eps_inf - omega_p**2 / (omega**2 + 1j * gamma * omega)


def eps_lorentz(omega, eps_inf=1.0, omega_0=1.0, omega_p=0.5, gamma=0.05):
    """Lorentz oscillator: bound-charge resonance (phonons, excitons).

    eps(omega) = eps_inf + omega_p^2 / (omega_0^2 - omega^2 - i*gamma*omega)
    """
    return eps_inf + omega_p**2 / (omega_0**2 - omega**2 - 1j * gamma * omega)


# --- Plotting ---


def plot_permittivity_components(save_as=None):
    """Three-panel: eps' and eps'' vs frequency for each model."""
    omega = np.linspace(0.01, 3.0, 1000)
    colors = sns.color_palette("deep")

    models = [
        (eps_non_resonant, "Non-resonant dielectric", {}),
        (eps_drude, "Drude (metal)", {"omega_p": 1.0, "gamma": 0.1}),
        (
            eps_lorentz,
            "Lorentz (resonance)",
            {"omega_0": 1.0, "omega_p": 0.5, "gamma": 0.1},
        ),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for ax, (model, title, kwargs) in zip(axes, models):
        eps = model(omega, **kwargs)
        ax.plot(
            omega, np.real(eps), color=colors[0], linewidth=2, label=r"$\varepsilon'$"
        )
        ax.plot(
            omega,
            np.imag(eps),
            color=colors[1],
            linewidth=2,
            linestyle="--",
            label=r"$\varepsilon''$",
        )
        ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.set_xlabel(r"$\omega / \omega_0$")
        ax.set_ylabel(r"$\tilde{\varepsilon}$")
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_permittivity_mod_arg(save_as=None):
    """Three-panel: |eps| and arg(eps) vs frequency for each model."""
    omega = np.linspace(0.01, 3.0, 1000)
    colors = sns.color_palette("deep")

    models = [
        (eps_non_resonant, "Non-resonant", {}),
        (eps_drude, "Drude", {"omega_p": 1.0, "gamma": 0.1}),
        (eps_lorentz, "Lorentz", {"omega_0": 1.0, "omega_p": 0.5, "gamma": 0.1}),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(16, 9))

    for col, (model, title, kwargs) in enumerate(models):
        eps = model(omega, **kwargs)

        # Top row: modulus
        axes[0, col].plot(omega, np.abs(eps), color=colors[0], linewidth=2)
        axes[0, col].set_ylabel(r"$|\tilde{\varepsilon}|$")
        axes[0, col].set_title(title)
        axes[0, col].grid(True, alpha=0.3)

        # Bottom row: argument
        axes[1, col].plot(omega, np.angle(eps), color=colors[1], linewidth=2)
        axes[1, col].set_xlabel(r"$\omega / \omega_0$")
        axes[1, col].set_ylabel(r"$\arg(\tilde{\varepsilon})$")
        axes[1, col].set_ylim(-np.pi, np.pi)
        axes[1, col].grid(True, alpha=0.3)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_permittivity_complex_plane(save_as=None):
    """Three-panel: trajectory of eps(omega) in the complex plane, colored by frequency."""
    omega = np.linspace(0.01, 3.0, 1000)

    models = [
        (eps_non_resonant, "Non-resonant", {}),
        (eps_drude, "Drude", {"omega_p": 1.0, "gamma": 0.1}),
        (eps_lorentz, "Lorentz", {"omega_0": 1.0, "omega_p": 0.5, "gamma": 0.1}),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    for ax, (model, title, kwargs) in zip(axes, models):
        eps = model(omega, **kwargs)

        # Color by frequency
        points = ax.scatter(
            np.real(eps), np.imag(eps), c=omega, cmap="rocket", s=3, alpha=0.8
        )
        fig.colorbar(points, ax=ax, label=r"$\omega$")

        # Mark key points
        ax.plot(
            np.real(eps[0]),
            np.imag(eps[0]),
            "o",
            color="white",
            markersize=6,
            markeredgecolor="black",
            zorder=5,
        )
        ax.plot(
            np.real(eps[-1]),
            np.imag(eps[-1]),
            "s",
            color="white",
            markersize=6,
            markeredgecolor="black",
            zorder=5,
        )

        ax.axhline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.axvline(0, color="gray", linewidth=0.5, linestyle=":")
        ax.set_xlabel(r"$\varepsilon'$")
        ax.set_ylabel(r"$\varepsilon''$")
        ax.set_title(title)
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_permittivity_contour(save_as=None):
    """2x3 contour panel: |eps| and arg(eps) over (omega, gamma) parameter space.

    Columns: non-resonant, Drude, Lorentz.
    Top row: |eps(omega, gamma)|.
    Bottom row: arg(eps(omega, gamma)).
    """
    omega = np.linspace(0.01, 3.0, 500)
    gamma_vals = np.linspace(0.01, 0.5, 500)
    OMEGA, GAMMA = np.meshgrid(omega, gamma_vals)

    models = [
        ("Non-resonant", lambda w, g: eps_non_resonant(w, eps_inf=2.25)),
        ("Drude", lambda w, g: eps_drude(w, omega_p=1.0, gamma=g)),
        ("Lorentz", lambda w, g: eps_lorentz(w, omega_0=1.0, omega_p=0.5, gamma=g)),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    for col, (title, model_fn) in enumerate(models):
        eps = model_fn(OMEGA, GAMMA)
        mod = np.abs(eps)
        arg = np.angle(eps)

        # Top: modulus
        c_top = axes[0, col].contourf(OMEGA, GAMMA, mod, levels=100, cmap="rocket")
        axes[0, col].contour(
            OMEGA, GAMMA, mod, levels=10, colors="k", linewidths=0.3, alpha=0.3
        )
        axes[0, col].set_title(rf"{title} — $|\tilde{{\varepsilon}}|$")
        axes[0, col].set_ylabel(r"$\gamma$")
        fig.colorbar(c_top, ax=axes[0, col])

        # Bottom: argument
        c_bot = axes[1, col].contourf(
            OMEGA, GAMMA, arg, levels=100, cmap="twilight", vmin=-np.pi, vmax=np.pi
        )
        axes[1, col].set_title(rf"{title} — $\arg(\tilde{{\varepsilon}})$")
        axes[1, col].set_xlabel(r"$\omega / \omega_0$")
        axes[1, col].set_ylabel(r"$\gamma$")
        fig.colorbar(c_bot, ax=axes[1, col])

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "components": ("Re/Im permittivity vs frequency", lambda: plot_permittivity_components(save_as="permittivity_components.png")),
        "mod_arg": ("Mod and arg of permittivity", lambda: plot_permittivity_mod_arg(save_as="permittivity_mod_arg.png")),
        "complex_plane": ("Permittivity in the complex plane", lambda: plot_permittivity_complex_plane(save_as="permittivity_complex_plane.png")),
        "contour": ("Contour map of permittivity", lambda: plot_permittivity_contour(save_as="permittivity_contour.png")),
    }

    parser = argparse.ArgumentParser(description="Complex permittivity visualizations.")
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
