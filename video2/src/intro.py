from manim import (
    Circle,
    Dot,
    VGroup,
    MovingCameraScene,
    linear,
    RIGHT,
    LEFT,
    UP,
    DOWN,
    IN,
    OUT,
    Line,
    Scene,
    Axes,
    ValueTracker,
    PI,
    always_redraw,
    BLUE,
    GREEN,
    YELLOW,
    YELLOW_A,
    YELLOW_B,
    YELLOW_C,
    YELLOW_D,
    YELLOW_E,
    WHITE,
    BLACK,
    GREY,
    camera,
)

import numpy as np


class SineCurveUnitCircle(Scene):
    # contributed by heejin_park, https://infograph.tistory.com/230
    def construct(self):
        self.origin_point = np.array([-3.5, 0, 0])
        self.curve_start = np.array([-7, 0, 0])
        self.move_dot_and_draw_curve()
        self.wait()

    def move_dot_and_draw_curve(self, amplitude=1):
        orbit = Circle(radius=amplitude).move_to(self.origin_point)
        origin_point = self.origin_point

        # DONT REMOVE THE DOT OR IT ALL WILL BREAK->see line updater
        height_tracer = Dot(radius=0.000001, color=YELLOW)
        height_tracer.move_to(orbit.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        def go_around_circle(mob, dt):
            self.t_offset += dt * rate
            # print(self.t_offset)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(origin_point, height_tracer.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = height_tracer.get_center()[1]
            return Line(
                height_tracer.get_center(),
                np.array([x, y, 0]),
                color=YELLOW_A,
                stroke_width=2,
            )

        self.curve = VGroup()
        self.curve.add(Line(self.curve_start, self.curve_start))

        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = height_tracer.get_center()[1]
            new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=YELLOW_D)
            self.curve.add(new_line)
            return self.curve

        self.line = VGroup()
        self.line.add(Line(self.curve_start, self.curve_start))

        def get_line():
            last_line = self.line[-1]
            x = self.curve_start[0] + self.t_offset * 4
            new_line = Line(last_line.get_end(), np.array([x, 0, 0]), color=YELLOW_D)
            self.line.add(new_line)
            return self.line

        height_tracer.add_updater(go_around_circle)

        line_along_sine = always_redraw(get_line)
        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        # you have to first add the elements to trigger the movements (i think)
        self.add(height_tracer)
        self.add(
            line_along_sine,
            origin_to_circle_line,
            dot_to_curve_line,
            sine_curve_line,
        )
        self.remove(origin_to_circle_line, dot_to_curve_line)

        self.wait(10.05)

        height_tracer.remove_updater(go_around_circle)
