"""Fourier analysis: series, transforms, and energy conservation."""

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
    """Create a 1D linspace over [a, b] with n points."""
    return np.linspace(a, b, n)


def _save_fig(fig, save_as):
    """Save a figure to the Figures/ directory."""
    if save_as:
        fig.savefig(
            os.path.join(FIGURES_DIR, save_as), dpi=SAVE_DPI, bbox_inches="tight"
        )


# --- Signal definitions ---


def square_wave(x):
    """Unit square wave with period 2*pi: +1 on (0, pi), -1 on (pi, 2*pi)."""
    return np.sign(np.sin(x))


def fourier_partial_sum(x, n_terms):
    """Partial sum of the Fourier series for the square wave.

    S_N(x) = sum_{k=0}^{N-1} (4/pi) * sin((2k+1)x) / (2k+1)
    """
    result = np.zeros_like(x)
    for k in range(n_terms):
        m = 2 * k + 1
        result += np.sin(m * x) / m
    return result * 4 / np.pi


def gaussian(x, sigma):
    """Gaussian: (1 / (sigma * sqrt(2*pi))) * exp(-x^2 / (2*sigma^2))."""
    return np.exp(-(x**2) / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))


def gaussian_ft(xi, sigma):
    """Fourier transform of a Gaussian with std dev sigma.

    The FT of (1/(sigma*sqrt(2*pi))) * exp(-x^2/(2*sigma^2))
    is exp(-2*pi^2*sigma^2*xi^2).
    """
    return np.exp(-2 * np.pi**2 * sigma**2 * xi**2)


# --- Fourier coefficient computation ---


def square_wave_coefficients(n_max):
    """Compute complex Fourier coefficients c_n for the square wave.

    For the square wave, c_n = -2i/(n*pi) for odd n, 0 for even n.
    Returns arrays of indices, magnitudes, and phases for n in [-n_max, n_max].
    """
    ns = np.arange(-n_max, n_max + 1)
    magnitudes = np.zeros(len(ns))
    phases = np.zeros(len(ns))

    for i, n in enumerate(ns):
        if n == 0:
            magnitudes[i] = 0.0
            phases[i] = 0.0
        elif n % 2 != 0:
            # c_n = -2i / (n*pi)
            c_n = -2j / (n * np.pi)
            magnitudes[i] = np.abs(c_n)
            phases[i] = np.angle(c_n)
        else:
            magnitudes[i] = 0.0
            phases[i] = 0.0

    return ns, magnitudes, phases


# --- Plot functions ---


def plot_square_wave_panel(save_as=None):
    """Four-panel figure showing Fourier partial sums converging to a square wave.

    Panels show N = 1, 3, 5, 15 terms of the series.
    """
    x = make_grid(-2 * np.pi, 2 * np.pi, 2000)
    exact = square_wave(x)
    n_values = [1, 3, 5, 15]

    colors = sns.color_palette("deep")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    for ax, n in zip(axes.flat, n_values):
        ax.plot(x, exact, color="gray", linewidth=1, alpha=0.5, label="Square wave")
        approx = fourier_partial_sum(x, n)
        ax.plot(x, approx, color=colors[0], linewidth=1.5, label=f"$N = {n}$")
        ax.set_title(rf"$N = {n}$ term{'s' if n > 1 else ''}")
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$S_N(x)$")
        ax.set_ylim(-1.5, 1.5)
        ax.legend(loc="upper right", fontsize=10)

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_complex_coefficients(save_as=None):
    """Two-panel stem plot: magnitude and phase of Fourier coefficients for the square wave."""
    ns, magnitudes, phases = square_wave_coefficients(15)

    colors = sns.color_palette("deep")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))

    # Magnitude
    markerline, stemlines, baseline = ax1.stem(
        ns, magnitudes, linefmt="-", markerfmt="o", basefmt="k-"
    )
    plt.setp(stemlines, color=colors[0], linewidth=1.2)
    plt.setp(markerline, color=colors[0], markersize=4)
    ax1.set_xlabel(r"$n$")
    ax1.set_ylabel(r"$|c_n|$")
    ax1.set_title("Fourier coefficient magnitudes (square wave)")

    # Phase (only for nonzero coefficients)
    nonzero = magnitudes > 1e-10
    phase_display = np.where(nonzero, phases, 0.0)
    markerline2, stemlines2, baseline2 = ax2.stem(
        ns, phase_display, linefmt="-", markerfmt="o", basefmt="k-"
    )
    plt.setp(stemlines2, color=colors[1], linewidth=1.2)
    plt.setp(markerline2, color=colors[1], markersize=4)
    ax2.set_xlabel(r"$n$")
    ax2.set_ylabel(r"$\arg(c_n)$")
    ax2.set_title("Fourier coefficient phases (square wave)")
    ax2.set_yticks([-np.pi / 2, 0, np.pi / 2])
    ax2.set_yticklabels([r"$-\pi/2$", r"$0$", r"$\pi/2$"])

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_transform_gaussian(save_as=None):
    """Two-panel: a Gaussian in the time domain and its Fourier transform.

    Shows two widths (narrow and wide) to illustrate the uncertainty trade-off.
    """
    x = make_grid(-5, 5, 1000)
    xi = make_grid(-3, 3, 1000)

    sigmas = [0.5, 1.5]
    colors = sns.color_palette("deep")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    for i, sigma in enumerate(sigmas):
        ax1.plot(
            x,
            gaussian(x, sigma),
            color=colors[i],
            linewidth=1.8,
            label=rf"$\sigma = {sigma}$",
        )
        ax2.plot(
            xi,
            gaussian_ft(xi, sigma),
            color=colors[i],
            linewidth=1.8,
            label=rf"$\sigma = {sigma}$",
        )

    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$f(x)$")
    ax1.set_title("Gaussian in time/space domain")
    ax1.legend()

    ax2.set_xlabel(r"$\xi$")
    ax2.set_ylabel(r"$\hat{f}(\xi)$")
    ax2.set_title("Fourier transform (frequency domain)")
    ax2.legend()

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def plot_parseval(save_as=None):
    """Two-panel: a signal and its power spectrum, illustrating Parseval's theorem.

    Uses a sum of sinusoids as the signal. Shows that total energy
    (area under |f|^2) equals total spectral energy (area under |F|^2).
    """
    n = 4096
    dt = 1 / 256
    t = np.arange(n) * dt

    # Signal: sum of three sinusoids with different frequencies and amplitudes
    def signal(t):
        """Test signal: three sinusoidal components."""
        return (
            1.5 * np.sin(2 * np.pi * 5 * t)
            + 0.8 * np.sin(2 * np.pi * 12 * t)
            + 0.4 * np.sin(2 * np.pi * 25 * t)
        )

    f = signal(t)
    f_power = f**2

    # Compute FFT
    f_hat = np.fft.fft(f) * dt
    freqs = np.fft.fftfreq(n, d=dt)

    # Power spectrum (only positive frequencies for display)
    pos = freqs > 0
    power_spectrum = np.abs(f_hat[pos]) ** 2 / dt

    # Compute energies for annotation
    time_energy = np.sum(f_power) * dt
    # Parseval: sum |f|^2 dt = sum |F|^2 df (double positive freqs to account for symmetry)
    freq_energy_display = np.sum(np.abs(f_hat[pos]) ** 2) * 2 / (n * dt)

    colors = sns.color_palette("deep")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Time domain
    ax1.plot(t[:512], f[:512], color=colors[0], linewidth=0.8)
    ax1.fill_between(t[:512], 0, f_power[:512], alpha=0.15, color=colors[0])
    ax1.set_xlabel(r"$t$")
    ax1.set_ylabel(r"$f(t)$")
    ax1.set_title("Signal and $|f(t)|^2$")
    ax1.annotate(
        rf"$\int |f|^2 \, dt \approx {time_energy:.2f}$",
        xy=(0.55, 0.92),
        xycoords="axes fraction",
        fontsize=12,
    )

    # Frequency domain
    ax2.plot(freqs[pos], power_spectrum, color=colors[1], linewidth=0.8)
    ax2.fill_between(freqs[pos], 0, power_spectrum, alpha=0.15, color=colors[1])
    ax2.set_xlabel(r"$\xi$ (frequency)")
    ax2.set_ylabel(r"$|\hat{f}(\xi)|^2$")
    ax2.set_title("Power spectrum $|\\hat{f}(\\xi)|^2$")
    ax2.set_xlim(0, 40)
    ax2.annotate(
        rf"$\int |\hat{{f}}|^2 \, d\xi \approx {freq_energy_display:.2f}$",
        xy=(0.45, 0.92),
        xycoords="axes fraction",
        fontsize=12,
    )

    plt.tight_layout()
    _save_fig(fig, save_as)
    plt.show()


def main():
    import argparse

    figures = {
        "square_wave": ("Square wave Fourier series", lambda: plot_square_wave_panel(save_as="fourier_square_wave.png")),
        "coefficients": ("Complex Fourier coefficients", lambda: plot_complex_coefficients(save_as="fourier_complex_coefficients.png")),
        "transform": ("Gaussian Fourier transform", lambda: plot_transform_gaussian(save_as="fourier_transform_gaussian.png")),
        "parseval": ("Parseval's theorem", lambda: plot_parseval(save_as="fourier_parseval.png")),
    }

    parser = argparse.ArgumentParser(description="Fourier analysis visualizations.")
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
