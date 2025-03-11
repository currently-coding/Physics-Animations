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
        z += amplitude * np.sin(k * r + omega * t + phase)
    return z

class Animate3DFunction(ThreeDScene):
    def construct(self):
        # Set up the 3D axes
        axes = ThreeDAxes()
        
        # Create a ValueTracker for the time parameter
        time_tracker = ValueTracker(0)
        
        # Define default wave sources at (-1, 0) and (1, 0) with equal standard parameters:
        # amplitude = 1, k = 2, omega = 1, phase = 0
        # z=A⋅sin(kr+ωt+ϕ)
        wave_sources = [
            (-1, -PI, 0.1, 4, 2, 0),
            (1, -PI, 0.1, 4, 2, 0)
        ]
        
        # Define the dynamic wave surface using the resulting_wave function
        wave_surface = always_redraw(lambda: Surface(
            lambda u, v: np.array([
                u, 
                v, 
                resulting_wave(u, v, time_tracker.get_value(), wave_sources)
            ]),
            u_range=[-PI, PI],
            v_range=[-PI, PI],
            resolution=(100, 100),
            fill_opacity=0.8,
            checkerboard_colors=[BLUE_D],
        ))
        
        # Create red dots for each wave source
        red_dots = VGroup(*[
            Dot3D(point=np.array([x, y, 0]), color=RED, radius=0.1)
            for (x, y, _, _, _, _) in wave_sources
        ])
        
        # Set a good camera orientation to view the 3D object
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        # Add the axes, wave surface, and red dots to the scene
        self.add(axes, wave_surface, red_dots)
        
        # Optionally, add a title as a fixed (non-moving) overlay
        title = Text("Resulting 3D Wave").to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        
        # Animate the wave by updating the time parameter
        self.play(time_tracker.animate.increment_value(2 * PI), run_time=2, rate_func=linear)
        self.wait()
