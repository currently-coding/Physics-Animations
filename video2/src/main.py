from manim import (
    GREY,
    linear,
    WHITE,
    Arc,
    ValueTracker,
    VGroup,
    ORIGIN,
    GREY_B,
    Rectangle,
    ApplyMethod,
    ThreeDScene,
    Cube,
    GREY_D,
    Sphere,
    BLACK,
    GREY_A,
    GRAY_B,
    GRAY_C,
    Camera,
    DEGREES,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    BLUE,
    GREEN,
    RED,
    YELLOW,
    interpolate_color,
    Surface,
    Scene,
    config,
    Dot,
    Create,
    FadeIn,
    Line,
    PI,
    ParametricFunction,
)
import numpy as np


class Video(ThreeDScene):
    def construct(self):
        data = self.double_slit_structure(num_slits=2, slit_width=0.6)
        self.move_camera(
            theta=90 * DEGREES, phi=-90 * DEGREES, frame_center=data[1][0]
        )  # unten
        for elem in data:
            if len(elem) == 0:
                self.add(elem)
            else:
                for e in elem:
                    self.add(e)
        self.wait()
        self.sine_from_light(
            start=np.array([0, 0, 0]), end=data[2].get_center(), freq=PI, amplitude=1
        )
        self.wait(2)

        middle_slits = []
        assert len(data[1]) >= 2
        for idx in range(len(data[1][:-1])):  # loop through slit walls
            center_current = data[1][idx].get_center()
            center_next = data[1][idx + 1].get_center()
            print(center_current, center_next)
            middle = (center_current[1] + center_next[1]) / 2
            middle_slits.append(
                np.array(
                    [data[1][idx].get_center()[0], middle, data[1][idx].get_center()[2]]
                )
            )

        self.explain_formula(screen=data[-1], middle_slits=middle_slits)

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
        self.add(sine_curve)

    def waves(self, start):
        # TODO: https://www.youtube.com/watch?v=EmKQsSDlaa4&t=814s
        pass

    def explain_formula(self, middle_slits, screen):
        result = self.get_parts_for_explanation(middle_slits, screen)
        for elem in result:
            self.add(elem)

        self.move_camera(
            theta=-90 * DEGREES, phi=1 * DEGREES, frame_center=screen
        )  # unten
        print("did it")
        self.wait(2)

    def get_parts_for_explanation(self, middle_slits, screen):
        # draw lines from each slit to center of screen
        lines = []
        for middle in middle_slits:
            lines.append(Line(start=middle, end=screen.get_center()))
        # one line straight, one angled: |\
        #                                | \
        #                                x  x
        # rotate angled line around end
        # show right triangle
        # done!
        return lines
