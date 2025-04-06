from manim import *
import numpy as np


class SineCurve3D(ThreeDScene):
    def construct(self):
        start = np.array([-1, -2, 0])  # Replace with your [x, y, z]
        start2 = np.array([-1, 2, 0])  # Replace with your [x, y, z]
        end = np.array([4, 0, 2])  # Replace with your [x2, y2, z2]
        freq = 8 * PI  # Frequency of sine wave
        amp = 0.5  # Amplitude of sine wave
        steps = 100

        # Direction vector from start to end
        direction = end - start
        direction2 = end - start2

        def sine_curve1(t):
            point = start + t * direction
            sine_offset = amp * np.sin(freq * t)
            return point + np.array([0, sine_offset, 0])  # Add sine in y-direction

        def sine_curve2(t):
            point = start2 + t * direction2
            sine_offset = amp * np.sin(freq * t)
            return point + np.array([0, sine_offset, 0])  # Add sine in y-direction

        curve1 = ParametricFunction(sine_curve1, t_range=[-1, 1], color=BLUE)
        curve2 = ParametricFunction(sine_curve2, t_range=[-1, 1], color=BLUE)

        self.play(Create(curve1, rate_func=linear), Create(curve2, rate_func=linear))
        self.wait(5)
