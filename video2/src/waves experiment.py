import math
from manim import *
import numpy as np

def resulting_wave(u, v, t, wave_sources):
    """
    Compute the resulting wave height at point (u, v) and time t.
    
    wave_sources: list of tuples (x, y, amplitude, k, omega, phase)
    """
    z = 0
    for x, y, amplitude, k, omega, phase in wave_sources:
        r = np.sqrt((u - x)**2 + (v - y)**2)
        z += amplitude * np.sin(k * r - omega * t + phase)
    return z

class Animate3DFunction(ThreeDScene):
    def construct(self):
        # Set up the 3D axes
        
        # Create a ValueTracker for the time parameter
        time_tracker = ValueTracker(0)
        
        # constants
        wavelength = 1

        # Define default wave sources at (-1, 0) and (1, 0) with equal standard parameters:
        # amplitude = 1, k = 2, omega = 1, phase = 0
        # z=A⋅sin(kr+ωt+ϕ)
        wave_sources = [
            (-1, 0, 0.1, 2 * PI / wavelength, 2, 0),
            (1, 0, 0.1, 2 * PI / wavelength, 2, 0)
        ]
        
        # Define the dynamic wave surface using the resulting_wave function
        wave_surface = always_redraw(lambda: Surface(
            lambda u, v: np.array([
                u, 
                v, 
                resulting_wave(u, v, time_tracker.get_value(), wave_sources)
            ]),
            u_range=[-3*PI, 3*PI],
            v_range=[0, 3*PI],
            resolution=(100, 100),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D],
        ))
        
        # Create red dots for each wave source
        red_dots = VGroup(*[
            Dot3D(point=np.array([x, y, 0]), color=RED, radius=0.1)
            for (x, y, _, _, _, _) in wave_sources
        ])
        
        # Add a vertical wall at the x-coordinate of the dots
        def my_surface(u_range):
            return Surface(
                lambda u, v: np.array([u, 0, v]),
                u_range=u_range,
                v_range=[-3, 3],
                resolution=(10, 10),
                fill_opacity=1,
                checkerboard_colors=[GRAY],
            )

        wall1 = my_surface([-3*PI, -1.2])
        wall2 = my_surface([-0.8, 0.8])
        wall3 = my_surface([1.2, 3*PI])
        
        def curve_fun(n):
            # Define the constant c
            c = wavelength / 2 * n
            # Define the curve (1 - 4/c^2)x^2 + 2y = c^2/4 - 1
            if n == 0:
                return ParametricFunction(
                    lambda t: np.array([
                        0,  # x = t
                        t,  # y as a function of x
                        0   # z = 0 (2D curve in the xy-plane)
                    ]),
                    t_range= (0, 10),
                    color=YELLOW,
                    stroke_width=4
                )
            return ParametricFunction(
                lambda t: np.array([
                    t,  # x = t
                    0 if c == 0 else np.sqrt((c**2 - 4)*(c**2 - 4*t**2) / (4*c**2)),  # y as a function of x
                    0   # z = 0 (2D curve in the xy-plane)
                ]),
                t_range= (-10, -c/2) if n > 0 else (-c/2, 10),
                color=YELLOW,
                stroke_width=4
            )
        
        def point_from_wavelength(l1, l2):
            d1 = l1 * wavelength
            d2 = l2 * wavelength
            x = (d2**2 - d1**2) / 4
            y = np.sqrt(d1**2 - (x-1)**2)
            return Dot3D(point=np.array([x, y, 0]), color=YELLOW, radius=0.1)
        
        point = point_from_wavelength(3, 2)
        
        # Calculate the range of n based on the condition |c| < 2
        max_n = math.ceil(4 / wavelength) - 1 # Maximum value of n
        n_range = range(-max_n, max_n + 1)  # Range of n values

        # Create a family of curves for integer n such that |c| < 2
        curves = VGroup()
        for n in n_range:  # Explicit loop over n
            curve = curve_fun(n)  # Generate the curve using curve_fun
            curve.set_color(RED if n % 2 != 0 else GREEN)  # Red for odd n, Green for even n
            curves.add(curve)  # Add the curve to the group

        # Define the red points (wave sources)
        red_point1 = np.array([-1, 0, 0])  # First red point
        red_point2 = np.array([1, 0, 0])   # Second red point

        # Define the yellow point (already calculated)
        yellow_point = point.get_center()

        # Create dark gray lines connecting the yellow point to the red points
        line1 = Line(start=point, end=red_point1, color=DARK_GRAY, stroke_width=4)
        line2 = Line(start=point, end=red_point2, color=DARK_GRAY, stroke_width=4)

        # Add the dark gray lines to the scene
        self.add(line1, line2)

        # Create ValueTrackers for the progression of yellow color
        progress1 = ValueTracker(0)  # Progress along line1 (0 to 1)
        progress2 = ValueTracker(0)  # Progress along line2 (0 to 1)

        # Function to create the yellow progression line
        def get_progress_line(start, end, progress):
            return Line(
                start=start,
                end=start + (end - start) * progress.get_value(),
                color=YELLOW,
                stroke_width=4
            )

        # Create yellow progression lines
        progress_line1 = always_redraw(lambda: get_progress_line(yellow_point, red_point1, progress1))
        progress_line2 = always_redraw(lambda: get_progress_line(yellow_point, red_point2, progress2))

        # Create labels to show the distance traveled in multiples of wavelength
        distance_label1 = always_redraw(lambda: MathTex(
            f"{progress1.get_value() * np.linalg.norm(red_point1 - yellow_point) / wavelength:.1f}\\lambda"
        ).next_to(red_point1, DOWN).rotate(PI).rotate(axis=RIGHT, angle=-30*DEGREES))

        distance_label2 = always_redraw(lambda: MathTex(
            f"{progress2.get_value() * np.linalg.norm(red_point2 - yellow_point) / wavelength:.1f}\\lambda"
        ).next_to(red_point2, DOWN).rotate(PI).rotate(axis=RIGHT, angle=-30*DEGREES))

        

        # Set a good camera orientation to view the 3D object
        self.set_camera_orientation(phi=30 * DEGREES, theta= 90 * DEGREES, zoom=1)
        
        # Add the axes, wave surface, red dots, wall, and wavefronts to the scene
        #self.add(wave_surface, red_dots, wall1, wall2, wall3, curves)
        self.add(red_dots, curves, point)

        # Here animation

        # Add the yellow progression lines and labels to the scene
        self.add(progress_line1, progress_line2, distance_label1, distance_label2)

        # Animate the yellow progression along the lines
        self.play(
            progress1.animate.set_value(1),  # Animate yellow progression along line1
            run_time=3
        )
        self.wait(0.5)

        self.play(
            progress2.animate.set_value(1),  # Animate yellow progression along line2
            run_time=3
        )
        self.wait(0.5)

        # Optionally, add a title as a fixed (non-moving) overlay
        #title = Text("Resulting 3D Wave").to_corner(UL)
        #self.add_fixed_in_frame_mobjects(title)
        
        # Animate the wave by updating the time parameter
        # self.play(time_tracker.animate.increment_value(2 * PI), run_time=0.01, rate_func=linear)
        self.wait()
