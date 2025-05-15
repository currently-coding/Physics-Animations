from manim import (
    FadeIn,
    Text,
    DecimalNumber,
    LEFT,
    Tex,
    VGroup,
    ValueTracker,
    Transform,
    GREEN,
    YELLOW,
    RED,
    MathTex,
    Create,
    Write,
    linear,
    RIGHT,
    UP,
    DOWN,
    Line,
    Scene,
    Axes,
    PI,
    BLUE,
    WHITE,
)

import numpy as np


class SineCurve(Scene):
    def construct(self):
        # Define the start and end of the curve
        x_start = 0
        x_end = 4 * np.pi  # Customize this as needed

        # Create the axes
        axes = Axes(
            x_range=[x_start, x_end, PI / 2],
            y_range=[-2.2, 2.2, 1],
            axis_config={
                "color": BLUE,
            },
            # x_axis_config={"x_range":[0, 4*PI, PI]}
        )

        axes.x_axis.add_labels(
            {
                PI: MathTex(r"\pi"),
                2 * PI: MathTex(r"2\pi"),
                3 * PI: MathTex(r"3\pi"),
                4 * PI: MathTex(r"4\pi"),
            }
        )

        axes.y_axis.add_numbers()
        # Define the sine curve with custom range
        sine_curve = axes.plot(lambda x: np.sin(x), color=WHITE)

        # Highlight one period of the sine curve (you can change these values)
        period_start = 0  # Custom start of period
        period_end = 2 * np.pi  # Custom end of period

        # Label the axes
        axes_labels = axes.get_axis_labels("x", "y")

        # Create labels for amplitude and period
        period_label = (
            Tex("$T$", font_size=90)
            .next_to(axes.c2p(period_end, 0), DOWN)
            .shift(RIGHT * 0.2)
            .shift(DOWN * 0.3)
        )
        period_line = Line(start=axes.c2p(0, 0), end=axes.c2p(2 * PI, 0), color=RED)
        frequency_label = Tex("$ = \\frac{1}{f}$", font_size=90).next_to(period_label)
        period_curve = axes.plot(
            lambda x: np.sin(x), color=RED, x_range=[period_start, period_end]
        )
        phase_speed_label = (
            Tex("c", font_size=90)
            .next_to(axes.c2p(0, 0), DOWN)
            .shift(RIGHT * 0.3)
            .shift(DOWN * 1.5)
        )
        phase_speed_label_formula = Tex(
            r"$=\frac{\Delta x}{\Delta t}=\frac{\lambda}{T}$", font_size=90
        ).next_to(phase_speed_label, RIGHT)

        amplitude_line = Line(
            start=axes.c2p(2.5 * PI, 0), end=axes.c2p(2.5 * PI, 1), color=RED
        )
        amplitude_label = (
            Tex("A", font_size=90).next_to(amplitude_line).shift(UP).shift(RIGHT * 0.2)
        )

        wave_length_line = Line(
            start=axes.c2p(2.5 * PI, 1), end=axes.c2p(0.5 * PI, 1), color=RED
        )
        wave_length_label = (
            Tex(r"$\lambda$", font_size=90)
            .next_to(wave_length_line.get_center())
            .shift(UP * 0.5)
        )

        # ---
        self.play(Create(axes), Write(axes_labels))

        # Animate the sine curve developing over time
        self.play(FadeIn(sine_curve))

        self.wait(2)
        # ---
        self.play(Create(wave_length_label), Write(wave_length_line))
        self.wait(2)
        self.remove(wave_length_line, wave_length_label)

        self.wait(1)
        self.play(Create(amplitude_line), Write(amplitude_label))
        self.wait(2)
        self.remove(amplitude_label, amplitude_line)
        # ---
        # ---
        timer_tracker = ValueTracker(0)

        timer_display = DecimalNumber(0, num_decimal_places=2)
        timer_display.next_to(amplitude_label)
        # FIX: s is centered next to the num so it needs to be shifted down a little
        timer_label = Tex("$s$").next_to(timer_display, RIGHT, buff=0.1)
        timer = VGroup(timer_display, timer_label).shift(LEFT * 6)

        # Updater that reads the tracker value
        timer_display.add_updater(lambda m: m.set_value(timer_tracker.get_value()))

        # Manim only calls update(dt) on Mobjects in the scene, so we attach an updater to tracker
        def update_timer(mob, dt):
            timer_tracker.set_value(
                timer_tracker.get_value() + dt
            )  # increment by frame delta

        timer_tracker.add_updater(update_timer)
        self.add(
            timer, timer_tracker
        )  # tracker must be added to the scene for updater to work
        # ANIMATION HERE ---

        self.play(
            Create(period_curve),
            Write(period_label),
            run_time=1,
            rate_func=linear,
        )
        # ------------------

        timer_tracker.clear_updaters()
        timer_display.clear_updaters()
        self.wait(3)
        self.remove(timer, timer_tracker)
        self.wait(1)
        self.play(Write(frequency_label))
        self.wait(2)
        self.remove(period_label, period_curve, frequency_label)
        self.wait(1)
        period_curve.set_color(YELLOW)
        self.play(
            Create(period_line),
            Create(period_curve),
            Write(phase_speed_label),
            run_time=1,
            rate_func=linear,
        )
        self.wait(1)
        self.play(Write(phase_speed_label_formula))
        self.wait(3)
