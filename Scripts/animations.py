"""Animations for the mathematical notebook using manim."""

import os
import shutil

import numpy as np
from manim import (
    UP,
    DOWN,
    LEFT,
    RIGHT,
    UL,
    UR,
    GRAY,
    GRAY_A,
    GRAY_B,
    WHITE,
    PI,
    Axes,
    Circle,
    DecimalNumber,
    Dot,
    Integer,
    Line,
    MathTex,
    Scene,
    Text,
    VGroup,
    VMobject,
    ValueTracker,
    always_redraw,
    linear,
    smooth,
    tempconfig,
)

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "Figures")

# Seaborn "deep" palette
DEEP_BLUE = "#4C72B0"
DEEP_ORANGE = "#DD8452"


def _eps_phonon(omega, eps_inf, omega_to, omega_lo, gamma=4.0):
    """Lorentz phonon permittivity for a single resonance."""
    return (
        eps_inf
        * (omega_lo**2 - omega**2 - 1j * gamma * omega)
        / (omega_to**2 - omega**2 - 1j * gamma * omega)
    )


def render_scene(scene_class, filename):
    """Render a manim Scene as GIF to Figures/."""
    media_dir = os.path.join(os.path.dirname(__file__), ".manim_media")
    # Remove stale GIFs but keep TeX cache
    if os.path.exists(media_dir):
        for root, _, files in os.walk(media_dir):
            for f in files:
                if f.endswith(".gif"):
                    os.remove(os.path.join(root, f))
    with tempconfig(
        {
            "format": "gif",
            "pixel_height": 600,
            "pixel_width": 800,
            "frame_rate": 20,
            "media_dir": media_dir,
            "disable_caching": True,
            "preview": False,
            "verbosity": "WARNING",
        }
    ):
        scene = scene_class()
        scene.render()
    dest = os.path.join(FIGURES_DIR, filename)
    for root, _, files in os.walk(media_dir):
        for f in files:
            if f.endswith(".gif"):
                shutil.copy2(os.path.join(root, f), dest)
                print(f"  Saved: {filename}")
                return
    print(f"  ERROR: No GIF found for {scene_class.__name__}")


# --- 1. Fourier series convergence ---


class FourierConvergence(Scene):
    """Fourier partial sums converging to a square wave, term by term."""

    def construct(self):
        axes = Axes(
            x_range=[-2 * PI, 2 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={"color": GRAY_B, "include_ticks": False},
            tips=False,
        )
        title = Text("Fourier Series Convergence", font_size=28).to_edge(UP)

        exact = axes.plot(
            lambda x: float(np.sign(np.sin(x))),
            x_range=[-2 * PI + 0.01, 2 * PI - 0.01, 0.001],
            discontinuities=[k * PI for k in range(-2, 3)],
            color=GRAY,
            stroke_width=1.5,
            stroke_opacity=0.5,
        )

        n_tracker = ValueTracker(1)

        def get_curve():
            n = int(n_tracker.get_value())

            def f(x):
                return (
                    sum(np.sin((2 * k + 1) * x) / (2 * k + 1) for k in range(n))
                    * 4
                    / np.pi
                )

            return axes.plot(
                f, x_range=[-2 * PI, 2 * PI, 0.02], color=DEEP_BLUE, stroke_width=2.5
            )

        curve = always_redraw(get_curve)

        n_prefix = (
            MathTex("N =", font_size=36).to_corner(UR).shift(DOWN * 0.8 + LEFT * 0.5)
        )
        n_number = Integer(1, font_size=36).next_to(n_prefix, RIGHT, buff=0.1)
        n_number.add_updater(lambda d: d.set_value(int(n_tracker.get_value())))
        n_number.add_updater(lambda d: d.next_to(n_prefix, RIGHT, buff=0.1))

        self.add(axes, title, exact, curve, n_prefix, n_number)
        self.wait(0.5)
        self.play(n_tracker.animate(rate_func=linear).set_value(30), run_time=6)
        self.wait(1)


# --- 2. Conformal mapping z -> z^2 ---


class ConformalMapping(Scene):
    """Grid deforming under the conformal map z -> z^2."""

    def construct(self):
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=6.5,
            y_length=6.5,
            axis_config={"color": GRAY_B, "include_ticks": False},
            tips=False,
        )
        title = MathTex(r"z \to z^2", font_size=32).to_edge(UP)

        t_tracker = ValueTracker(0)

        # Precompute z-values for grid lines
        h_z = [np.linspace(-1.5, 1.5, 120) + 1j * y for y in np.linspace(-1.5, 1.5, 11)]
        v_z = [x + 1j * np.linspace(-1.5, 1.5, 120) for x in np.linspace(-1.5, 1.5, 11)]

        def make_grid():
            t = t_tracker.get_value()
            lines = VGroup()
            for z_arr in h_z:
                w = (1 - t) * z_arr + t * z_arr**2
                pts = [axes.c2p(wi.real, wi.imag) for wi in w]
                line = VMobject().set_points_as_corners(pts)
                line.set_stroke(DEEP_BLUE, width=1.2, opacity=0.7)
                lines.add(line)
            for z_arr in v_z:
                w = (1 - t) * z_arr + t * z_arr**2
                pts = [axes.c2p(wi.real, wi.imag) for wi in w]
                line = VMobject().set_points_as_corners(pts)
                line.set_stroke(DEEP_ORANGE, width=1.2, opacity=0.7)
                lines.add(line)
            return lines

        grid = always_redraw(make_grid)

        t_prefix = MathTex("t =", font_size=30).to_corner(UR).shift(DOWN * 0.5)
        t_number = DecimalNumber(0, num_decimal_places=2, font_size=30)
        t_number.next_to(t_prefix, RIGHT, buff=0.1)
        t_number.add_updater(lambda d: d.set_value(t_tracker.get_value()))
        t_number.add_updater(lambda d: d.next_to(t_prefix, RIGHT, buff=0.1))

        self.add(axes, title, grid, t_prefix, t_number)
        self.wait(0.5)
        self.play(t_tracker.animate(rate_func=smooth).set_value(1), run_time=4)
        self.wait(1)


# --- 3. Wavepacket evolution in a box ---


class WavefunctionEvolution(Scene):
    """Gaussian wavepacket bouncing inside a particle-in-a-box potential."""

    def construct(self):
        L = np.pi
        n_modes = 50
        x_arr = np.linspace(0, L, 500)

        # Precompute eigenstates
        phis = np.zeros((n_modes, len(x_arr)))
        energies = np.zeros(n_modes)
        for n in range(1, n_modes + 1):
            phis[n - 1] = np.sqrt(2 / L) * np.sin(n * np.pi * x_arr / L)
            energies[n - 1] = (n * np.pi / L) ** 2

        # Initial Gaussian wavepacket
        x0, sigma, k0 = L / 3, L / 12, 20.0
        psi0 = np.exp(-((x_arr - x0) ** 2) / (2 * sigma**2)) * np.exp(1j * k0 * x_arr)
        psi0 /= np.sqrt(np.trapezoid(np.abs(psi0) ** 2, x_arr))

        c_n = np.array([np.trapezoid(phis[n] * psi0, x_arr) for n in range(n_modes)])

        axes = Axes(
            x_range=[0, PI, PI / 4],
            y_range=[-4, 8, 2],
            x_length=10,
            y_length=5,
            axis_config={"color": GRAY_B, "include_ticks": False},
            tips=False,
        )
        title = Text("Wavepacket evolution in a box", font_size=28).to_edge(UP)
        left_wall = Line(axes.c2p(0, -4), axes.c2p(0, 8), color=WHITE, stroke_width=3)
        right_wall = Line(axes.c2p(L, -4), axes.c2p(L, 8), color=WHITE, stroke_width=3)

        t_tracker = ValueTracker(0)
        t_total = 0.5
        step = 3  # subsample x_arr for performance

        def get_curves():
            t = t_tracker.get_value()
            phases = np.exp(-1j * energies * t)
            psi = np.sum(c_n[:, None] * phis * phases[:, None], axis=0)
            prob = np.abs(psi) ** 2
            re = np.real(psi) * 3

            prob_pts = [axes.c2p(x_arr[i], prob[i]) for i in range(0, len(x_arr), step)]
            re_pts = [axes.c2p(x_arr[i], re[i]) for i in range(0, len(x_arr), step)]

            prob_curve = VMobject().set_points_as_corners(prob_pts)
            prob_curve.set_stroke(DEEP_BLUE, width=2.5)
            re_curve = VMobject().set_points_as_corners(re_pts)
            re_curve.set_stroke(DEEP_ORANGE, width=1.5, opacity=0.5)
            return VGroup(prob_curve, re_curve)

        curves = always_redraw(get_curves)

        t_prefix = MathTex("t =", font_size=30).to_corner(UR).shift(DOWN * 0.5)
        t_number = DecimalNumber(0, num_decimal_places=3, font_size=30)
        t_number.next_to(t_prefix, RIGHT, buff=0.1)
        t_number.add_updater(lambda d: d.set_value(t_tracker.get_value()))
        t_number.add_updater(lambda d: d.next_to(t_prefix, RIGHT, buff=0.1))

        self.add(axes, title, left_wall, right_wall, curves, t_prefix, t_number)
        self.wait(0.3)
        self.play(t_tracker.animate(rate_func=linear).set_value(t_total), run_time=5)
        self.wait(0.5)


# --- 4. Isofrequency contour transition ---


class IsofrequencyTransition(Scene):
    """Isofrequency contour morphing from elliptic to hyperbolic as eps_z sweeps."""

    def construct(self):
        eps_perp = 2.25

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=6.5,
            y_length=6.5,
            axis_config={"color": GRAY_B, "include_ticks": False},
            tips=False,
        )
        x_lab = axes.get_x_axis_label(MathTex(r"k_x", font_size=24), direction=DOWN)
        y_lab = axes.get_y_axis_label(MathTex(r"k_z", font_size=24), direction=LEFT)
        title = Text("Isofrequency contour transition", font_size=26).to_edge(UP)

        # Vacuum circle
        r = np.linalg.norm(axes.c2p(1, 0) - axes.c2p(0, 0))
        vacuum = Circle(radius=r).move_to(axes.c2p(0, 0))
        vacuum.set_stroke(GRAY, width=1, opacity=0.4)
        vacuum.set_fill(opacity=0)

        eps_tracker = ValueTracker(5.0)

        def get_contour():
            ez = eps_tracker.get_value()
            group = VGroup()
            if abs(ez) < 0.1:
                return group

            if ez > 0:
                a, b = np.sqrt(ez), np.sqrt(eps_perp)
                theta = np.linspace(0, 2 * np.pi, 300)
                pts = [axes.c2p(a * np.cos(t), b * np.sin(t)) for t in theta]
                curve = VMobject().set_points_as_corners(pts)
                curve.set_stroke(DEEP_BLUE, width=2.5)
                group.add(curve)
            else:
                a = np.sqrt(abs(ez))
                b = np.sqrt(eps_perp)
                t_max = np.arcsinh(5.0 / a) if a > 0.01 else 4.0
                t_arr = np.linspace(-t_max, t_max, 300)
                for sign in [1, -1]:
                    pts = [
                        axes.c2p(a * np.sinh(t), sign * b * np.cosh(t)) for t in t_arr
                    ]
                    curve = VMobject().set_points_as_corners(pts)
                    curve.set_stroke(DEEP_BLUE, width=2.5)
                    group.add(curve)
            return group

        contour = always_redraw(get_contour)

        eps_prefix = (
            MathTex(r"\varepsilon_z =", font_size=28)
            .to_corner(UL)
            .shift(DOWN * 0.5 + RIGHT * 0.3)
        )
        eps_number = DecimalNumber(
            5.0, num_decimal_places=1, font_size=28, include_sign=True
        )
        eps_number.next_to(eps_prefix, RIGHT, buff=0.1)
        eps_number.add_updater(lambda d: d.set_value(eps_tracker.get_value()))
        eps_number.add_updater(lambda d: d.next_to(eps_prefix, RIGHT, buff=0.1))

        regime_text = Text("(elliptic)", font_size=20, color=GRAY_A)
        regime_text.next_to(eps_prefix, DOWN, aligned_edge=LEFT)

        def update_regime(mob):
            ez = eps_tracker.get_value()
            label = "(elliptic)" if ez > 0 else "(hyperbolic)"
            new_mob = Text(label, font_size=20, color=GRAY_A)
            new_mob.next_to(eps_prefix, DOWN, aligned_edge=LEFT)
            mob.become(new_mob)

        regime_text.add_updater(update_regime)

        self.add(
            axes,
            x_lab,
            y_lab,
            title,
            vacuum,
            contour,
            eps_prefix,
            eps_number,
            regime_text,
        )
        self.wait(0.5)
        self.play(eps_tracker.animate(rate_func=linear).set_value(0.15), run_time=2.5)
        eps_tracker.set_value(-0.15)
        self.wait(0.1)
        self.play(eps_tracker.animate(rate_func=linear).set_value(-5), run_time=2.5)
        self.wait(1)


# --- 5. Complex permittivity trajectory ---


class PermittivityTrajectory(Scene):
    """Point tracing the Lorentz permittivity through the complex plane."""

    def construct(self):
        n_pts = 200
        omega = np.linspace(0.01, 3.0, n_pts)
        eps_inf, omega_0, omega_p, gamma = 1.0, 1.0, 0.5, 0.1
        eps = eps_inf + omega_p**2 / (omega_0**2 - omega**2 - 1j * gamma * omega)
        re_vals, im_vals = np.real(eps), np.imag(eps)

        margin = 0.3
        x_min, x_max = float(np.min(re_vals)) - margin, float(np.max(re_vals)) + margin
        y_min, y_max = float(np.min(im_vals)) - margin, float(np.max(im_vals)) + margin

        axes = Axes(
            x_range=[x_min, x_max, 0.5],
            y_range=[y_min, y_max, 0.5],
            x_length=9,
            y_length=5.5,
            axis_config={"color": GRAY_B, "include_ticks": False},
            tips=False,
        )
        x_lab = axes.get_x_axis_label(
            MathTex(r"\varepsilon'", font_size=24), direction=DOWN
        )
        y_lab = axes.get_y_axis_label(
            MathTex(r"\varepsilon''", font_size=24), direction=LEFT
        )
        title = MathTex(
            r"\text{Lorentz } \tilde{\varepsilon}(\omega)",
            font_size=26,
        ).to_edge(UP)

        # Full trajectory (faint reference)
        full_pts = [axes.c2p(re_vals[i], im_vals[i]) for i in range(n_pts)]
        full_curve = VMobject().set_points_as_corners(full_pts)
        full_curve.set_stroke(GRAY, width=0.8, opacity=0.3)

        idx_tracker = ValueTracker(0)

        def get_trail():
            idx = max(2, min(int(idx_tracker.get_value()), n_pts - 1))
            pts = [axes.c2p(re_vals[i], im_vals[i]) for i in range(idx)]
            trail = VMobject().set_points_as_corners(pts)
            trail.set_stroke(DEEP_ORANGE, width=2.5, opacity=0.8)
            return trail

        trail = always_redraw(get_trail)

        dot = Dot(radius=0.08, color=DEEP_ORANGE)
        dot.add_updater(
            lambda d: d.move_to(
                axes.c2p(
                    re_vals[min(int(idx_tracker.get_value()), n_pts - 1)],
                    im_vals[min(int(idx_tracker.get_value()), n_pts - 1)],
                )
            )
        )

        omega_prefix = (
            MathTex(r"\omega / \omega_0 =", font_size=26)
            .to_corner(UR)
            .shift(DOWN * 0.5 + LEFT * 0.3)
        )
        omega_number = DecimalNumber(omega[0], num_decimal_places=2, font_size=26)
        omega_number.next_to(omega_prefix, RIGHT, buff=0.1)
        omega_number.add_updater(
            lambda d: d.set_value(omega[min(int(idx_tracker.get_value()), n_pts - 1)])
        )
        omega_number.add_updater(lambda d: d.next_to(omega_prefix, RIGHT, buff=0.1))

        self.add(
            axes,
            x_lab,
            y_lab,
            title,
            full_curve,
            trail,
            dot,
            omega_prefix,
            omega_number,
        )
        self.wait(0.3)
        self.play(
            idx_tracker.animate(rate_func=linear).set_value(n_pts - 1), run_time=5
        )
        self.wait(1)


# --- 6. MoO3 in-plane isofrequency sweep ---


class MoO3Isofrequency(Scene):
    """In-plane isofrequency contours for MoO3 sweeping through frequency."""

    def construct(self):
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=6.5,
            y_length=6.5,
            axis_config={"color": GRAY_B, "include_ticks": False},
            tips=False,
        )
        x_lab = axes.get_x_axis_label(MathTex(r"k_x", font_size=24), direction=DOWN)
        y_lab = axes.get_y_axis_label(MathTex(r"k_y", font_size=24), direction=LEFT)
        title = MathTex(
            r"\text{MoO}_3 \text{ in-plane isofrequency}", font_size=26
        ).to_edge(UP)

        freq_tracker = ValueTracker(400)

        def get_contour():
            freq = freq_tracker.get_value()
            w = np.array([freq])
            ex = np.real(_eps_phonon(w, 4.0, 820, 972))[0]
            ey = np.real(_eps_phonon(w, 5.2, 545, 851))[0]

            safe_ex = ex if abs(ex) > 0.05 else 0.05 * (1 if ex >= 0 else -1)
            safe_ey = ey if abs(ey) > 0.05 else 0.05 * (1 if ey >= 0 else -1)

            group = VGroup()

            if safe_ex > 0 and safe_ey > 0:
                # Ellipse: kx^2/ey + ky^2/ex = 1
                a, b = np.sqrt(safe_ey), np.sqrt(safe_ex)
                theta = np.linspace(0, 2 * np.pi, 300)
                pts = [axes.c2p(a * np.cos(t), b * np.sin(t)) for t in theta]
                curve = VMobject().set_points_as_corners(pts)
                curve.set_stroke(DEEP_BLUE, width=2.5)
                group.add(curve)
            elif safe_ex > 0 and safe_ey < 0:
                # Opens along ky: ky^2/ex - kx^2/|ey| = 1
                a, b = np.sqrt(abs(safe_ey)), np.sqrt(safe_ex)
                t_max = np.arcsinh(6.0 / a) if a > 0.01 else 4.0
                t_arr = np.linspace(-t_max, t_max, 300)
                for sign in [1, -1]:
                    pts = [
                        axes.c2p(a * np.sinh(t), sign * b * np.cosh(t)) for t in t_arr
                    ]
                    curve = VMobject().set_points_as_corners(pts)
                    curve.set_stroke(DEEP_BLUE, width=2.5)
                    group.add(curve)
            elif safe_ex < 0 and safe_ey > 0:
                # Opens along kx: kx^2/ey - ky^2/|ex| = 1
                a, b = np.sqrt(safe_ey), np.sqrt(abs(safe_ex))
                t_max = np.arcsinh(6.0 / b) if b > 0.01 else 4.0
                t_arr = np.linspace(-t_max, t_max, 300)
                for sign in [1, -1]:
                    pts = [
                        axes.c2p(sign * a * np.cosh(t), b * np.sinh(t)) for t in t_arr
                    ]
                    curve = VMobject().set_points_as_corners(pts)
                    curve.set_stroke(DEEP_BLUE, width=2.5)
                    group.add(curve)
            # Both negative: no propagation, empty group
            return group

        contour = always_redraw(get_contour)

        # Info labels: static prefixes + dynamic numbers
        freq_prefix = (
            MathTex(r"\omega =", font_size=24)
            .to_corner(UR)
            .shift(DOWN * 0.3 + LEFT * 0.2)
        )
        freq_number = DecimalNumber(400, num_decimal_places=0, font_size=24)
        freq_number.next_to(freq_prefix, RIGHT, buff=0.1)
        freq_number.add_updater(lambda d: d.set_value(freq_tracker.get_value()))
        freq_number.add_updater(lambda d: d.next_to(freq_prefix, RIGHT, buff=0.1))
        freq_unit = MathTex(r"\text{ cm}^{-1}", font_size=24)
        freq_unit.next_to(freq_number, RIGHT, buff=0.05)
        freq_unit.add_updater(lambda d: d.next_to(freq_number, RIGHT, buff=0.05))

        # Epsilon and regime labels (dynamic)
        eps_x_prefix = MathTex(r"\varepsilon_x =", font_size=22)
        eps_x_prefix.next_to(freq_prefix, DOWN, buff=0.25, aligned_edge=LEFT)
        eps_x_num = DecimalNumber(
            0, num_decimal_places=1, font_size=22, include_sign=True
        )
        eps_x_num.next_to(eps_x_prefix, RIGHT, buff=0.1)

        def update_eps_x(d):
            freq = freq_tracker.get_value()
            ex = np.real(_eps_phonon(np.array([freq]), 4.0, 820, 972))[0]
            d.set_value(ex)
            d.next_to(eps_x_prefix, RIGHT, buff=0.1)

        eps_x_num.add_updater(update_eps_x)

        eps_y_prefix = MathTex(r"\varepsilon_y =", font_size=22)
        eps_y_prefix.next_to(eps_x_prefix, DOWN, buff=0.15, aligned_edge=LEFT)
        eps_y_num = DecimalNumber(
            0, num_decimal_places=1, font_size=22, include_sign=True
        )
        eps_y_num.next_to(eps_y_prefix, RIGHT, buff=0.1)

        def update_eps_y(d):
            freq = freq_tracker.get_value()
            ey = np.real(_eps_phonon(np.array([freq]), 5.2, 545, 851))[0]
            d.set_value(ey)
            d.next_to(eps_y_prefix, RIGHT, buff=0.1)

        eps_y_num.add_updater(update_eps_y)

        regime_text = Text("(elliptic)", font_size=18, color=GRAY_A)
        regime_text.next_to(eps_y_prefix, DOWN, buff=0.15, aligned_edge=LEFT)

        def update_regime(mob):
            freq = freq_tracker.get_value()
            w = np.array([freq])
            ex = np.real(_eps_phonon(w, 4.0, 820, 972))[0]
            ey = np.real(_eps_phonon(w, 5.2, 545, 851))[0]
            if ex > 0 and ey > 0:
                label = "(elliptic)"
            elif ex < 0 and ey < 0:
                label = "(no propagation)"
            elif ex * ey < 0:
                label = "(hyperbolic)"
            else:
                label = "(degenerate)"
            new_mob = Text(label, font_size=18, color=GRAY_A)
            new_mob.next_to(eps_y_prefix, DOWN, buff=0.15, aligned_edge=LEFT)
            mob.become(new_mob)

        regime_text.add_updater(update_regime)

        self.add(
            axes,
            x_lab,
            y_lab,
            title,
            contour,
            freq_prefix,
            freq_number,
            freq_unit,
            eps_x_prefix,
            eps_x_num,
            eps_y_prefix,
            eps_y_num,
            regime_text,
        )
        self.wait(0.3)
        self.play(freq_tracker.animate(rate_func=linear).set_value(1100), run_time=6)
        self.wait(1)


# --- 7. Eigenfunction expansion convergence ---


class EigenfunctionExpansion(Scene):
    """Eigenfunction partial sums converging to a triangle wave."""

    def construct(self):
        L = np.pi
        x_arr = np.linspace(0, L, 500)
        target = 1 - 2 * np.abs(x_arr / L - 0.5)

        n_max = 30
        coeffs = []
        for n in range(1, n_max + 1):
            basis = np.sin(n * np.pi * x_arr / L)
            c = (2 / L) * np.trapezoid(target * basis, x_arr)
            coeffs.append(c)

        axes = Axes(
            x_range=[0, PI, PI / 4],
            y_range=[-0.2, 1.2, 0.2],
            x_length=10,
            y_length=5,
            axis_config={"color": GRAY_B, "include_ticks": False},
            tips=False,
        )
        title = Text("Eigenfunction expansion convergence", font_size=28).to_edge(UP)

        step = 3
        target_pts = [axes.c2p(x_arr[i], target[i]) for i in range(0, len(x_arr), step)]
        target_curve = VMobject().set_points_as_corners(target_pts)
        target_curve.set_stroke(GRAY, width=1.5, opacity=0.5)

        n_tracker = ValueTracker(1)

        def get_partial():
            n = int(n_tracker.get_value())
            partial = np.zeros_like(x_arr)
            for i in range(n):
                partial += coeffs[i] * np.sin((i + 1) * np.pi * x_arr / L)
            pts = [axes.c2p(x_arr[j], partial[j]) for j in range(0, len(x_arr), step)]
            curve = VMobject().set_points_as_corners(pts)
            curve.set_stroke(DEEP_BLUE, width=2.5)
            return curve

        curve = always_redraw(get_partial)

        n_prefix = (
            MathTex("N =", font_size=36).to_corner(UR).shift(DOWN * 0.8 + LEFT * 0.5)
        )
        n_number = Integer(1, font_size=36).next_to(n_prefix, RIGHT, buff=0.1)
        n_number.add_updater(lambda d: d.set_value(int(n_tracker.get_value())))
        n_number.add_updater(lambda d: d.next_to(n_prefix, RIGHT, buff=0.1))

        self.add(axes, title, target_curve, curve, n_prefix, n_number)
        self.wait(0.5)
        self.play(n_tracker.animate(rate_func=linear).set_value(30), run_time=6)
        self.wait(1)


# --- CLI ---

ANIMATIONS = {
    "fourier": (
        "Fourier series convergence",
        FourierConvergence,
        "anim_fourier_convergence.gif",
    ),
    "conformal": (
        "Conformal mapping z -> z^2",
        ConformalMapping,
        "anim_conformal_mapping.gif",
    ),
    "wavefunction": (
        "Wavepacket evolution",
        WavefunctionEvolution,
        "anim_wavefunction_evolution.gif",
    ),
    "isofrequency": (
        "Elliptic to hyperbolic",
        IsofrequencyTransition,
        "anim_isofrequency_transition.gif",
    ),
    "permittivity": (
        "Lorentz permittivity",
        PermittivityTrajectory,
        "anim_permittivity_trajectory.gif",
    ),
    "moo3": (
        "MoO3 isofrequency",
        MoO3Isofrequency,
        "anim_moo3_isofrequency.gif",
    ),
    "eigenfunction": (
        "Eigenfunction expansion",
        EigenfunctionExpansion,
        "anim_eigenfunction_expansion.gif",
    ),
}


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate notebook animations as GIFs using manim."
    )
    parser.add_argument(
        "names", nargs="*", help="animations to generate (omit for all)"
    )
    parser.add_argument(
        "--list", "-l", action="store_true", help="list available animations"
    )
    args = parser.parse_args()

    if args.list:
        for name, (desc, _, _) in ANIMATIONS.items():
            print(f"  {name:30s}  {desc}")
        return

    selected = args.names or list(ANIMATIONS.keys())
    for name in selected:
        if name not in ANIMATIONS:
            print(f"Unknown animation '{name}'. Use --list to see options.")
            return
        desc, scene_cls, filename = ANIMATIONS[name]
        print(f"Rendering: {name}")
        render_scene(scene_cls, filename)


if __name__ == "__main__":
    main()
