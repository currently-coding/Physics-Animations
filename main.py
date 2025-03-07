from PIL.Image import new
from manim import *
from manim.utils.color.X11 import MAGENTA
import numpy as np


class ExperimentSetup(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi=0 * DEGREES, theta=-90 * DEGREES, gamma=0 * DEGREES
        )
        # self.play(self.camera.frame.animate.rotate(PI / 4))
        data = self.double_slit_structure(num_slits=2, slit_width=0.6)

        for elem in data:
            if len(elem) == 0:
                self.add(elem)
            else:
                for e in elem:
                    self.add(e)
        self.wait()

        return
        self.sine_from_light(
            start=np.array([0, 0, 0]), end=data[2].get_center(), freq=PI, amplitude=1
        )
        self.wait(2)

        middle_slits = []
        assert len(data[1]) >= 2
        print("Elements")
        for elem in data[1]:
            print(elem.get_center())
        for idx in range(len(data[1][:-1])):  # loop through slit walls
            center_current = data[1][idx].get_center()
            center_next = data[1][idx + 1].get_center()
            middle = (center_current[1] + center_next[1]) / 2
            middle_slits.append(
                np.array(
                    [data[1][idx].get_center()[0], middle, data[1][idx].get_center()[2]]
                )
            )
        print("Calculations")
        for elem in middle_slits:
            print(elem)

        self.explain_formula(
            middle_slits=middle_slits,
            screen=data[-1],
        )

    # ----- ENDE ------

    def double_slit_structure(
        self,
        num_slits=2,
        slit_width=0.2,
        slit_distance=1.2,
        total_distance=35,
        height=2,
    ):
        # BUG: only works good for even numbers
        # odd numbers will shift everything to one side
        # vars

        light = (
            Sphere(
                radius=0.2,
                resolution=(15, 15),
            )
            .shift(LEFT * 3)
            .set_color(YELLOW)
        )
        slits = self.get_wall_with_n_slits(
            num_slits=num_slits,
            slit_width=slit_width,
            slit_distance=slit_distance,
            total_distance=total_distance,
            height=height,
        )
        print("Slit: ", slits[0].get_center())
        print("Slit: ", slits[1].get_center())
        print("Slit: ", slits[2].get_center())
        wall = (
            Cube()
            .scale(np.array([3, 0.1, 7]))
            .set_color(GREY_D)
            .shift(5 * RIGHT)
            .rotate(90 * DEGREES, LEFT)
            .rotate(90 * DEGREES, DOWN)
        )

        # doppelspalt

        return (light, slits, wall)

    def get_wall_with_n_slits(
        self,
        num_slits=2,
        slit_width=0.2,
        slit_distance=1.2,
        total_distance=35,
        height=2,
    ):
        # TODO: extend to cover the total_distance, not just the bare minimum
        parts = []
        distance = 0
        distance_prev = 0
        for slit in range(1, num_slits + 2):
            cube = (
                Cube().scale(np.array([height, slit_distance, 0.05])).set_color(GREY_B)
            ).rotate(PI / 2, UP)
            if slit % 2:
                cube.shift((distance) * UP)
            else:
                # only update every 2 walls
                distance = distance_prev + 2 * slit_distance + slit_width
                cube.shift((distance) * DOWN)
                distance_prev = distance
            parts.append(cube)
        parts.sort(key=lambda x: x.get_center()[1])
        return parts

    def sine_from_light(self, start, end, freq=PI, amplitude=1, rotation_angle=10):
        # TODO: https://www.youtube.com/watch?v=EmKQsSDlaa4&t=863s
        #
        # BUG: this code is not sufficient
        #
        amplitude /= 3
        freq *= 2

        # Generate the sine curve between the points
        sine_curve = ParametricFunction(
            lambda t: np.array(
                [t, amplitude * np.sin(t * freq), 0]
            ),  # Parametric sine curve
            t_range=[0, 2 * PI],  # Range of t
            color=BLUE,
        ).rotate(90 * DEGREES, LEFT)

        # Add the sine curve to the scene
        # self.add(sine_curve)

    def waves(self, start):
        # TODO: https://www.youtube.com/watch?v=EmKQsSDlaa4&t=814s
        pass

    def explain_formula(self, middle_slits, screen):
        # self.camera.frame.save_state()  # save state to later zoom out to this again
        (lines, animations) = self.get_parts_for_explanation(
            middle_slits,
            start=screen.get_center() + np.array([0, 3.8, 0]),
            end=screen.get_center() + np.array([0, -3.8, 0]),
        )
        self.move_camera(zoom=0.5, run_time=2) # camera.frame is deprecated | Zoom in (reduce the scale)
        # center_dot = Dot(np.array([0, 0, 0])) # was used for centering the cam
        # TODO: zoom in on start of lines
        # TODO: show rotation of angled line overlaps with 2nd line

        self.add(*lines)
        end = lines[0].get_end() + np.array([0, 1, 0])

        self.play(*animations, run_time=2)
        self.wait(2)

    def get_parts_for_explanation(self, middle_slits, start, end):
        # draw lines from each slit to center of screen
        lines = [Line(start=middle, end=start) for middle in middle_slits]
        # correctly draws lines from middle of each slit to a custom point
        # ----
        # Animation
        animations = [
            line.animate.put_start_and_end_on(line.get_start(), end) for line in lines
        ]
        #
        # swipes lines from slit to screen across entire screen
        # to show that the following is true for all segmants of the wave
        # ----
        # one line straight, one angled: |\
        #                                | \
        #                                x  x
        # rotate angled line around end
        # show right triangle
        # done!
        return (lines, animations)
