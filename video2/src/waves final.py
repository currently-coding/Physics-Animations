from manim import *
import numpy as np
import math


class InterferenceDemo(ThreeDScene):
    """Visualizes two-point-source water‑wave interference in 3‑D."""

    # ---------------------------------------------------------------------
    # Wave model helpers
    # ---------------------------------------------------------------------
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wavelength = 1  # base wavelength λ
        # Each source is defined as (x, y, amplitude, k, ω, phase)
        self.wave_sources = [
            (-1, 0, 0.1, 2 * PI / self.wavelength, 2, 0),
            (1, 0, 0.1, 2 * PI / self.wavelength, 2, 0),
        ]
        self.time_tracker = ValueTracker(0)

    def resulting_wave(self, u: float, v: float, t: float) -> float:
        """Return the superposed wave height z(u, v, t)."""
        z = 0
        for x, y, amp, k, omega, phase in self.wave_sources:
            r = np.hypot(u - x, v - y)  # radial distance from source
            z += amp * np.sin(k * r - omega * t + phase)
        return z

    # ---------------------------------------------------------------------
    # Dynamic surface
    # ---------------------------------------------------------------------
    def get_wave_surface(self):
        """Surface object that updates its z‑values with self.time_tracker."""
        return Surface(
            lambda u, v: np.array(
                [
                    u,
                    v,
                    self.resulting_wave(u, v, self.time_tracker.get_value()),
                ]
            ),
            u_range=[-3 * PI, 3 * PI],
            v_range=[0, 3 * PI],
            resolution=(200, 200),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D],
            stroke_width=0,
        )

    # ---------------------------------------------------------------------
    # Scene construction
    # ---------------------------------------------------------------------
    def construct(self):
        # Main dynamic objects
        wave_surface = always_redraw(self.get_wave_surface)
        source_dots = VGroup(
            *[Dot3D([x, y, 0], color=RED, radius=0.1) for x, y, *_ in self.wave_sources]
        )

        # Static decorations: three vertical “walls” and curves of equal
        # path‑length difference (interference fringes)
        walls = VGroup(
            self.make_wall([-3 * PI, -1.2]),
            self.make_wall([-0.8, 0.8]),
            self.make_wall([1.2, 3 * PI]),
        )
        fringes = self.build_constant_path_difference_curves()

        # Camera & assembly
        self.set_camera_orientation(phi=30 * DEGREES, theta=90 * DEGREES, zoom=1)
        self.play(FadeIn(walls))
        self.play(Create(source_dots))
        self.play(FadeIn(wave_surface))

        # Wave propagation (advance time by 2π)
        self.play(
            self.time_tracker.animate.increment_value(4 * PI),
            run_time=2,
            rate_func=linear,
        )

        # self.play(
        #    wave_surface.animate.set_fill(opacity=0.4),
        #    run_time=1
        # )

        # wave_surface.set_fill(opacity=0.4)

        self.play(Create(fringes))

        self.length_animation(3, 2)
        self.length_animation(3, 2.5)

        self.wait()

    # ------------------------------------------------------------------
    # Helper builders
    # ------------------------------------------------------------------
    def make_wall(self, u_range):
        """Return a simple vertical surface acting as a ‘wall’."""
        return Surface(
            lambda u, v: np.array([u, 0, v]),
            u_range=u_range,
            v_range=[-3, 3],
            resolution=(1, 1),
            fill_opacity=1,
            checkerboard_colors=[GRAY],
        )

    def build_constant_path_difference_curves(self):
        """Fringes where |d₁ – d₂| = n λ / 2 for integer n."""
        curves = VGroup()
        max_n = math.ceil(4 / self.wavelength) - 1  # ensures |c| < 2
        for n in range(-max_n, max_n + 1):
            c = self.wavelength / 2 * n
            if n == 0:
                curve = ParametricFunction(
                    lambda t: np.array([0, t, 0]),
                    t_range=(0, 10),
                    stroke_width=4,
                )
            else:
                curve = ParametricFunction(
                    lambda t: np.array(
                        [
                            t,
                            np.sqrt((c**2 - 4) * (c**2 - 4 * t**2) / (4 * c**2)),
                            0,
                        ]
                    ),
                    t_range=(-10, -c / 2) if n > 0 else (-c / 2, 10),
                    stroke_width=4,
                )
            curve.set_color(RED if n % 2 else GREEN)
            curves.add(curve)
        return curves

    # ------------------------------------------------------------------
    # Path‑length animation
    # ------------------------------------------------------------------
    def point_from_wavelength(self, l1, l2):
        """Coordinates of a point with d₁ = l₁ λ, d₂ = l₂ λ (from sources)."""
        d1, d2 = l1 * self.wavelength, l2 * self.wavelength
        x = (d2**2 - d1**2) / 4
        y = np.sqrt(max(d1**2 - (x - 1) ** 2, 0))
        return np.array([x, y, 0])

    def length_animation(self, l1, l2):
        """Grow yellow segments from an interference point back to each source."""
        yellow_pt = Dot3D(self.point_from_wavelength(l1, l2), color=YELLOW, radius=0.1)
        src1, src2 = np.array([-1, 0, 0]), np.array([1, 0, 0])

        # Static reference lines (dark grey)
        line1 = Line(yellow_pt.get_center(), src1, color=DARK_GRAY, stroke_width=4)
        line2 = Line(yellow_pt.get_center(), src2, color=DARK_GRAY, stroke_width=4)

        # Trackers governing the growth of bright yellow segments
        prog1, prog2 = ValueTracker(0), ValueTracker(0)

        def growing_line(start, end, tracker):
            return always_redraw(
                lambda: Line(
                    start,
                    start + (end - start) * tracker.get_value(),
                    color=YELLOW,
                    stroke_width=4,
                )
            )

        growing1 = growing_line(yellow_pt.get_center(), src1, prog1)
        growing2 = growing_line(yellow_pt.get_center(), src2, prog2)

        # Dynamic labels showing travelled distance in multiples of λ
        label1 = always_redraw(
            lambda: MathTex(
                f"{prog1.get_value() * np.linalg.norm(src1 - yellow_pt.get_center()) / self.wavelength:.1f}\\lambda"
            )
            .next_to(src1, DOWN)
            .rotate(PI)
            .rotate(axis=RIGHT, angle=-30 * DEGREES)
        )

        label2 = always_redraw(
            lambda: MathTex(
                f"{prog2.get_value() * np.linalg.norm(src2 - yellow_pt.get_center()) / self.wavelength:.1f}\\lambda"
            )
            .next_to(src2, DOWN)
            .rotate(PI)
            .rotate(axis=RIGHT, angle=-30 * DEGREES)
        )

        # Animations (moved to the end)
        self.play(Create(yellow_pt))
        self.play(
            Create(line1), Create(growing1), Create(label1)
        )  # Create first static line and label
        self.play(
            prog1.animate.set_value(1), run_time=3
        )  # Animate growth of first yellow segment

        self.play(Create(line2), Create(growing2), Create(label2))
        self.play(
            prog2.animate.set_value(1), run_time=3
        )  # Animate growth of second yellow segment

        eq = (
            MathTex(
                rf"{float(l1):.{1}f}\lambda",
                " - ",
                rf"{float(l2):.{1}f}\lambda",
                " = ",
                rf"{float(l1 - l2):.{1}f}\lambda",
            )
            .rotate(PI)
            .rotate(axis=RIGHT, angle=-30 * DEGREES)
            .move_to(3 * DOWN)
        )
        self.play(Write(eq))  # Write the equation

        self.wait(1)

        frac = (
            (l1 - l2) % 1
        )  # fractional part of l1-l2        eq = MathTex(f"{label1}"," - ", f"{label2}", " = ", {l1-l2}\lambda").rotate(PI).rotate(axis=RIGHT, angle=-30 * DEGREES).move_to(3*DOWN)

        if abs(frac) < 1e-6:  # ≡ 0  (integer multiple)
            out_tex = rf"\Delta s = n\lambda"
        elif abs(frac - 0.5) < 1e-6:  # ≡ 0.5 (half-integer multiple)
            out_tex = rf"\Delta s = \frac{'{2n+1}{2}'}\lambda"

        final_eq = (
            MathTex(out_tex)
            .rotate(PI)
            .rotate(axis=RIGHT, angle=-30 * DEGREES)
            .move_to(eq)
        )
        self.play(Transform(eq, final_eq))

        self.wait(1)

        self.remove(eq, line1, line2)  # Remove the original labels
        # Uncreate all objects
        self.play(
            Uncreate(yellow_pt),
            Uncreate(growing1),
            Uncreate(growing2),
            Unwrite(final_eq),
            Unwrite(label1),
            Unwrite(label2),
        )
        self.wait(1)

