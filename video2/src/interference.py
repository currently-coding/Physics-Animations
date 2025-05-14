from manim import *


class SineWavesScene(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 14, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_numbers": False},
        ).add_coordinates()
        labels = ax.get_axis_labels(Tex("X").scale(0.7), Text("Y").scale(0.45))

        def wave1(x, t):
            return 1 * np.sin(2 * PI * (0.2 * x - 0.13 * t))  # Moving right

        def wave2(x, t):
            return 1 * np.sin(2 * PI * (0.2 * x + 0.35 * t))  # Moving left

        def wave_sum(x, t):
            return wave1(x, t) + wave2(x, t)

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

        self.play(FadeIn(ax, labels))
        self.add(wave1_graph, wave2_graph)
        self.play(
            self.t.animate.set_value(6), run_time=6, rate_func=linear
        )  # Animate first 3 seconds
        self.add(sum_graph)  # Show sum graph
        self.play(
            self.t.animate.set_value(17), run_time=11, rate_func=linear
        )  # Continue animation
        self.remove(wave1_graph, wave2_graph, sum_graph)
        current_time = self.time
        static_wave1 = ax.plot(lambda x: wave1(x, current_time), color=BLUE)
        static_wave2 = ax.plot(lambda x: wave2(x, current_time), color=RED)
        static_sum = ax.plot(lambda x: wave_sum(x, current_time), color=YELLOW)
        self.add(static_wave1, static_wave2, static_sum)
        self.wait(2)
        x = ax.c2p(7.6, 0)
        y1 = ax.c2p(7.6, wave1(7.6, current_time))
        y2 = ax.c2p(7.6, wave2(7.6, current_time))
        wave1_amplitude = Line(x, x, color=GREEN)
        wave2_amplitude = Line(x, x, color=GREEN)
        self.add(wave1_amplitude)
        self.add(wave2_amplitude)
        self.play(
            wave1_amplitude.animate.put_start_and_end_on(x, y1),
        )
        self.wait(1.5)
        self.play(
            wave2_amplitude.animate.put_start_and_end_on(x, y2),
        )
        self.wait(1.5)
        self.play(
            wave1_amplitude.animate.put_start_and_end_on(x, x),
            wave2_amplitude.animate.put_start_and_end_on(x, x),
        )
        self.wait(5)
