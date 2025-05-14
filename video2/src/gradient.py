from manim import *
import numpy as np


class FillByValueExample(MovingCameraScene):
    def construct(self):
        resolution_fa = 34
        axes = ThreeDAxes(
            x_range=(0, 8.5, 1), y_range=(0, 8.5, 1), z_range=(-1, 1, 0.5)
        )

        # bump_centers has to be sorted center out
        # bump_centers = [(1.5, 3), (3.5, 3)]  # centers of the bumps
        bump_centers_interference = [
            (5, 3),
            (6.5, 3),
            (3.5, 3),
            (2, 3),
            (8, 3),
        ]
        bump_centers_2_dots = [(5, 3), (3, 3), (7, 3)]
        bump_centers_falloff = [(5, 3)]

        bump_height = 0.05  # individual bump height
        bump_sigma = 0.3  # controls bump "spread"
        bump_falloff = 0.05

        def param_surface_falloff(u, v):
            bump_sigma = 1  # controls bump "spread"
            sum = 0
            for idx, (cx, cy) in enumerate(bump_centers_falloff):
                sum += bump_height * np.exp(
                    -((u - cx) ** 2 + (v - cy) ** 2) / (2 * bump_sigma**2)
                )
            return sum

        def param_surface_2_dots(u, v):
            bump_sigma = 0.5
            sum = 0
            for idx, (cx, cy) in enumerate(bump_centers_2_dots[1:]):
                sum += bump_height * np.exp(
                    -((u - cx) ** 2 + (v - cy) ** 2) / (2 * bump_sigma**2)
                )
            return sum

        def param_surface_interference(u, v):
            sum = 0
            bump_subtract = 0
            for idx, (cx, cy) in enumerate(bump_centers_interference):
                if bump_subtract == 0:
                    bump_subtract = bump_falloff
                else:
                    bump_subtract = 0
                sum += bump_height * np.exp(
                    -((u - cx) ** 2 + (v - cy) ** 2)
                    / (2 * (bump_sigma - (bump_falloff * idx - bump_subtract)) ** 2)
                )

            return sum

        surface_plane = Surface(
            lambda u, v: axes.c2p(u, v, param_surface_interference(u, v)),
            resolution=(resolution_fa, resolution_fa),
            v_range=[0, 8.5],  # updated to match axes
            u_range=[0, 8.5],  # updated to match axes
        )
        surface_plane.set_style(fill_opacity=1)
        surface_plane.set_fill_by_value(
            axes=axes, colorscale=[(BLACK, 0), (RED, 0.05)], axis=2
        )
        # center image
        first_bump = bump_centers_interference[0]
        shift_vector = axes.c2p(*first_bump, 0)  # get the 3D point of the bump
        surface_plane.shift(-shift_vector)  # shift the whole surface
        # final image
        self.camera.frame.scale(2)
        self.add(surface_plane)
