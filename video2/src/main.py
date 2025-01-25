from math import degrees
from manim import (
    GREY,
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
)
import numpy as np


class Video(ThreeDScene):
    def construct(self):
        data = self.doppelspalt_aufbau(num_slits=2)
        for elem in data:
            if len(elem) == 0:
                self.add(elem)
            else:
                for e in elem:
                    self.add(e)
        self.wait()
        self.move_camera(
            theta=25 * DEGREES, phi=-90 * DEGREES, frame_center=data[1][0]
        )  # unten
        self.wait()

    def doppelspalt_aufbau(self, num_slits=2):
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
        slits = self.get_wall_with_slits(num_slits=num_slits)
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

    def get_wall_with_slits(
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
