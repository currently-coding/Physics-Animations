from manim import *
import numpy as np


class SineWavesScene(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 14, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_numbers": False},
        ).add_coordinates()
        labels = ax.get_axis_labels(Tex("X").scale(0.7), Text("Y").scale(0.45))

        def wave1(x, t):
            return np.sin(1.2 * x - t)  # Moving right

        def wave2(x, t):
            return np.sin(1.2 * x + t)  # Moving left

        def wave_sum(x, t):
            return wave1(x, t) + wave2(x, t)

        t = ValueTracker(0)  # fixed: using local ValueTracker

        wave1_graph = always_redraw(
            lambda: ax.plot(lambda x: wave1(x, t.get_value()), color=BLUE)
        )  # fixed: use t.get_value()
        wave2_graph = always_redraw(
            lambda: ax.plot(lambda x: wave2(x, t.get_value()), color=RED)
        )  # fixed
        sum_graph = always_redraw(
            lambda: ax.plot(lambda x: wave_sum(x, t.get_value()), color=YELLOW)
        )  # fixed

        self.play(FadeIn(ax, labels))
        self.add(wave1_graph, wave2_graph)
        self.play(
            t.animate.set_value(5), run_time=5, rate_func=linear
        )  # Animate wave movement
        self.add(sum_graph)
        self.play(
            t.animate.set_value(10), run_time=5, rate_func=linear
        )  # Continue animation
        self.play(
            t.animate.set_value(15), run_time=5, rate_func=linear
        )  # Continue animation
        self.play(
            t.animate.set_value(20), run_time=5, rate_func=linear
        )  # Continue animation
        self.play(
            t.animate.set_value(25), run_time=5, rate_func=linear
        )  # Continue animation
