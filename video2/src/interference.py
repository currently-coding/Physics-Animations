from manim import *


class SineWavesScene(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 14, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_numbers": False},
        ).add_coordinates()

        wave1 = lambda x, t: 0.5 * np.sin(2 * PI * (0.5 * x - 0.2 * t))  # Moving right
        wave2 = lambda x, t: 0.5 * np.sin(2 * PI * (0.5 * x + 0.2 * t))  # Moving left
        wave_sum = lambda x, t: wave1(x, t) + wave2(x, t)

        def get_wave_graph(func):
            return ax.plot(lambda x: func(x, 0), color=BLUE)

        wave1_graph = always_redraw(
            lambda: ax.plot(lambda x: wave1(x, self.time), color=BLUE)
        )
        wave2_graph = always_redraw(
            lambda: ax.plot(lambda x: wave2(x, self.time), color=RED)
        )
        sum_graph = always_redraw(
            lambda: ax.plot(lambda x: wave_sum(x, self.time), color=YELLOW)
        )

        self.t = ValueTracker(0)
        self.add(ax, wave1_graph, wave2_graph, sum_graph)
        self.play(self.t.animate.set_value(10), run_time=10, rate_func=linear)
        self.wait(3)
