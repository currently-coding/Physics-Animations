import numpy as np
from manim import *


class DoubleSlitFormula(ZoomedScene):
    def construct(self):
        # Parameter
        g = 3.0  # Spaltabstand
        alpha = 20 * DEGREES  # Ablenkwinkel
        slit_x = -3.0  # x-Position der Spaltebene
        screen_x = ValueTracker(6.0)  # x-Position der Beobachtungsebene
        original_screen_x = screen_x

        # Punkte S und T (Doppelspalt) und deren Mittelpunkt M
        S = np.array([slit_x, g / 2, 0])
        T = np.array([slit_x, -g / 2, 0])
        g_line = Line(S, T)
        M = (S + T) / 2

        # Beobachtungspunkt A auf der Beobachtungsebene

        # Zeichnen der optischen Achse (horizontal, gestrichelt)
        center_line = always_redraw(
            lambda: DashedLine(
                start=[slit_x, 0, 0],
                end=[screen_x.get_value(), 0, 0],
                dash_length=0.1,
                dashed_ratio=0.5,
            )
        )

        # Zeichnen der Spaltebene (vertikale Linie)
        slit_line = Line(
            start=[slit_x, g / 2 + 0.5, 0],
            end=[slit_x, -g / 2 - 0.5, 0],
        )

        # Punktquellen und Labels
        S_dot = Dot(S, color=YELLOW)
        T_dot = Dot(T, color=YELLOW)
        M_dot = Dot(M, color=WHITE)
        S_label = MathTex("S").next_to(S_dot, LEFT).shift(UP * 0.2)
        T_label = MathTex("T").next_to(T_dot, LEFT).shift(DOWN * 0.2)
        M_label = MathTex("M").next_to(M_dot, LEFT).shift(LEFT * 0.2)

        # Abstand g markieren
        g_arrow = BraceBetweenPoints(S_dot.get_center(), T_dot.get_center(), LEFT)
        g_label = MathTex("g").next_to(g_arrow, LEFT)

        screen_line = always_redraw(
            lambda: Line(
                start=[screen_x.get_value(), -4, 0],
                end=[screen_x.get_value(), 4, 0],
            )
        )

        # Punkte O, A und F markieren
        O = np.array([screen_x.get_value(), 0, 0])
        O_dot = always_redraw(lambda: Dot(np.array([screen_x.get_value(), 0, 0])))
        O_label = MathTex("O").next_to(O_dot, RIGHT)
        A_dot = always_redraw(
            lambda: Dot(
                np.array(
                    [
                        screen_x.get_value(),
                        (screen_x.get_value() - slit_x) * np.tan(alpha) + T[1],
                        0,
                    ]
                )
            )
        )
        A_label = always_redraw(lambda: MathTex("A").next_to(A_dot, RIGHT))

        a_k_brace = always_redraw(
            lambda: BraceBetweenPoints(A_dot.get_center(), O_dot.get_center(), RIGHT)
        ).shift(LEFT * 0.2)
        a_k_label = always_redraw(
            lambda: MathTex(r"a_{k}").next_to(a_k_brace, RIGHT).shift(LEFT * 0.1)
        )

        # F = A + (np.linalg.norm(S - A) / np.linalg.norm(T - A)) * (T - A)
        F_dot = always_redraw(
            lambda: Dot(
                A_dot.get_center()
                + (
                    np.linalg.norm(S_dot.get_center() - A_dot.get_center())
                    / np.linalg.norm(T_dot.get_center() - A_dot.get_center())
                )
                * (T_dot.get_center() - A_dot.get_center())
            )
        )
        F_label = always_redraw(
            lambda: MathTex("F").next_to(F_dot, RIGHT).shift(DOWN * 0.3)
        )

        # Strahlen von S und T nach A
        ray_S = always_redraw(
            lambda: Line(start=S_dot.get_center(), end=A_dot.get_center(), color=BLUE)
        )
        ray_T = always_redraw(
            lambda: Line(start=T_dot.get_center(), end=A_dot.get_center(), color=RED)
        )

        static_ray_S = Line(
            start=S_dot.get_center(), end=A_dot.get_center(), color=BLUE
        )
        static_ray_T = Line(start=T_dot.get_center(), end=A_dot.get_center(), color=RED)
        angle_ST = static_ray_T.get_angle() - static_ray_S.get_angle()
        rotation_overshoot = angle_ST * 0.3
        slit_screen_line_label = (
            MathTex("l").next_to(center_line, DOWN).shift(RIGHT * 2)
        )

        # Gleichschenkliges Dreieck S-A-F darstellen (AS = AF)
        tri_SF = always_redraw(
            lambda: DashedLine(start=S_dot.get_center(), end=F_dot.get_center())
        )
        tri_SF_arc = always_redraw(
            lambda: ArcBetweenPoints(
                start=S_dot.get_center(),
                end=F_dot.get_center(),
                radius=np.linalg.norm(
                    S_dot.get_center() - A_dot.get_center()
                ),  # radius = |AS|
            )
        )
        # tri_AF = Line(start=A, end=F, color=BLUE)

        # Strecke M-A mit Beschriftung m
        ray_MA = always_redraw(
            lambda: Line(start=M_dot.get_center(), end=A_dot.get_center())
        )
        m_label = always_redraw(
            lambda: MathTex("m").next_to(ray_MA.point_from_proportion(0.5), UP)
        )

        # Dreieck FSA
        triangle_FSA = always_redraw(
            lambda: Polygon(
                F_dot.get_center(),
                S_dot.get_center(),
                A_dot.get_center(),
                color=YELLOW,
                fill_opacity=0.3,
                stroke_width=2,
            )
        )
        triangle_FST = always_redraw(
            lambda: Polygon(
                F_dot.get_center(),
                S_dot.get_center(),
                T_dot.get_center(),
                color=BLUE,
                fill_opacity=0.3,
                stroke_width=2,
            )
        )

        # Winkel alpha am unteren Strahl darstellen
        angle_label_scale = 0.8
        angle_AMO = always_redraw(lambda: Angle(center_line, ray_MA, radius=1.6))
        AMO_label = always_redraw(lambda: MathTex(r"\alpha").next_to(angle_AMO, UP))
        angle_TSF = always_redraw(
            lambda: Angle(
                Line(S_dot.get_center(), T_dot.get_center()),
                Line(S_dot.get_center(), F_dot.get_center()),
                radius=2,
            )
        )
        TSF_label = always_redraw(
            lambda: MathTex(r"\alpha").next_to(angle_TSF, RIGHT).shift(DOWN * 0.1)
        )
        angle_SAT = always_redraw(
            lambda: Angle(
                Line(A_dot.get_center(), S_dot.get_center()),
                Line(A_dot.get_center(), T_dot.get_center()),
                radius=ray_S.get_length()
                - 2,  # BUG: the line jumps in the animation - pls fix :)
            )
        )
        SAT_label = always_redraw(
            lambda: MathTex(r"\sphericalangle SAT")
            .next_to(angle_SAT, RIGHT)
            .shift(LEFT * 0.2)
            .shift(UP * 0.75)
            .scale(angle_label_scale)
        )

        # Alle Elemente statisch hinzufügen
        self.play(FadeIn(slit_line, S_dot, T_dot, screen_line, S_label, T_label))
        self.wait(1)
        self.add(center_line, slit_screen_line_label)
        self.wait(1)
        self.add(g_label, g_arrow)
        self.wait(1)
        self.add(ray_T)
        self.wait(1)
        self.add(ray_S)
        self.wait(1)
        # switch to non always_redraw lines to show rotation
        self.remove(ray_T, ray_S)
        self.add(static_ray_T, static_ray_S)
        self.play(
            Rotate(
                static_ray_S,
                (angle_ST + rotation_overshoot),
                about_point=A_dot.get_center(),
            )
        )
        self.play(
            Rotate(static_ray_S, -rotation_overshoot, about_point=A_dot.get_center())
        )
        delta_s = always_redraw(
            lambda: Line(static_ray_T.get_start(), F_dot.get_center(), color=GREEN)
        )
        delta_s_label = always_redraw(
            lambda: MathTex("\\Delta s = \\text{ ?}")
            .next_to(delta_s, DOWN)
            .shift(RIGHT * 0.5)
            .shift(DOWN * 0.1)
        )

        delta_s_length = always_redraw(
            lambda: DecimalNumber(
                delta_s.get_length(), num_decimal_places=2, color=WHITE
            ).next_to(delta_s_label, RIGHT)
        )
        # (i'm sorry for the spaghetti code...)
        sin_alpha = (
            MathTex(r"\sin \alpha = \frac{\Delta s}{g}")
            .move_to(ORIGIN)
            .shift(LEFT * 1.5)
            .shift(UP * 3)
            .shift(LEFT * 3)
        )
        tan_alpha = (
            MathTex(r"\tan \alpha = \frac{a_{k}}{l}")
            .move_to(ORIGIN)
            .shift(RIGHT * 1.5)
            .shift(UP * 3)
            .shift(LEFT * 3)
        )
        tan_alpha_short = (
            MathTex(r"\tan^{-1} \alpha = ").next_to(g_label).shift(LEFT * 4).shift(DOWN)
        )
        tan_value = always_redraw(
            lambda: DecimalNumber(
                np.rad2deg(
                    np.arctan(
                        np.arctan(
                            Line(A_dot.get_center(), O_dot.get_center()).get_length()
                            / center_line.get_length()
                        )
                    )
                ),
                num_decimal_places=2,
                color=WHITE,
            ).next_to(tan_alpha_short, RIGHT)
        )
        tan_alpha_end = (
            MathTex(r"^{\circ}")
            .next_to(tan_value, buff=0)
            .shift(LEFT * 0.1)
            .shift(UP * 0.1)
        )
        tan = (
            VGroup(tan_alpha_short, tan_value, tan_alpha_end)
            .next_to(g_label, LEFT)
            .shift(DOWN * 1)
        )
        sin_alpha_short = (
            MathTex(r"\sin^{-1} \alpha = ").next_to(g_label).shift(LEFT * 4).shift(UP)
        )
        sin_value = always_redraw(
            lambda: DecimalNumber(
                np.rad2deg(np.arcsin(delta_s.get_length() / g_line.get_length())),
                num_decimal_places=2,
                color=WHITE,
            ).next_to(sin_alpha_short, RIGHT)
        )
        sin_alpha_end = (
            MathTex(r"^{\circ}")
            .next_to(sin_value, buff=0)
            .shift(UP * 0.1)
            .shift(LEFT * 0.1)
        )
        sin = (
            VGroup(sin_alpha_short, sin_value, sin_alpha_end)
            .next_to(g_label, LEFT)
            .shift(UP * 1)
        )
        alpha_short = MathTex(r"\alpha = ").next_to(g_label).shift(LEFT * 3)
        alpha_val = always_redraw(
            lambda: DecimalNumber(
                np.rad2deg(
                    np.arccos(
                        np.dot(ray_MA.get_vector(), center_line.get_vector())
                        / (
                            np.linalg.norm(ray_MA.get_vector())
                            * np.linalg.norm(center_line.get_vector())
                        )
                    )
                ),
                num_decimal_places=2,
                color=WHITE,
            ).next_to(alpha_short, RIGHT)
        )
        alpha_end = (
            MathTex(r"^{\circ}")
            .next_to(alpha_val, buff=0)
            .shift(LEFT * 0.1)
            .shift(UP * 0.1)
        )
        alpha_group = VGroup(alpha_short, alpha_val, alpha_end).next_to(g_label, LEFT)

        self.wait(1)
        self.add(F_dot, F_label)
        self.wait(1)
        self.add(delta_s, delta_s_label)
        self.wait(1)
        self.remove(static_ray_T, delta_s, static_ray_S)
        self.add(ray_T, static_ray_S)
        self.add(delta_s)
        self.wait(1)
        self.play(Rotate(static_ray_S, -angle_ST, about_point=A_dot.get_center()))
        self.remove(static_ray_S)
        self.add(ray_S)
        self.add(A_dot)
        self.add(A_label)
        self.wait(1)
        self.add(a_k_brace, a_k_label)
        self.wait(1)
        self.add(O_dot)
        self.wait(1)
        self.add(tri_SF)
        self.wait(1)
        self.add(
            M_dot, ray_MA
        )  # don't show M_label unless needed as it clutters the view
        self.wait(1)
        # self.wait(1)
        # self.add(sin_alpha)
        # self.play(FadeIn(triangle_FST))
        # self.wait(1)
        # self.add(angle_TSF, TSF_label)
        # self.wait(1)
        # self.play(FadeOut(triangle_FST))
        # self.wait(1)
        # self.add(tan_alpha)
        # self.play(FadeIn(triangle_FSA))
        # self.wait(1)
        # self.add(angle_AMO, AMO_label)
        # self.wait(1)
        # self.play(FadeOut(triangle_FSA))
        # self.wait(1)
        # self.add(sin, tan, alpha_group)
        #
        #
        self.add(angle_SAT, SAT_label)
        self.wait(1)
        self.camera.frame.save_state()
        self.wait(1)
        self.play(self.camera.frame.animate.set(width=slit_line.get_length() * 2))
        self.wait(1)
        self.play(screen_x.animate.set_value(100), run_time=10, rate_func=linear)
        self.wait(2)
        self.play(self.camera.frame.animate.restore())
        self.wait(1)
        self.play(screen_x.animate.set_value(6), run_time=5, rate_func=linear)
        self.wait(2)
        self.play(FadeIn(triangle_FST))
        self.wait(1)
        self.add(angle_TSF)
        self.wait(1)
        self.add(sin_alpha)
        self.wait(1)
        self.play(FadeOut(triangle_FST))
        self.wait(2)
        self.play(FadeIn(triangle_FSA))
        self.wait(1)
        self.add(angle_AMO)
        self.wait(1)
        self.add(tan_alpha)
        self.wait(1)
        self.play(FadeOut(triangle_FSA))
        self.wait(5)

        # Formelzauberei am Ende
        # Alle bisherigen Elemente ausblenden


# COMMENT OUT FOR FASTER RENDERING
# self.play(FadeOut(Group(*self.mobjects)))
#
# # Fortlaufende Umformung
# umf1 = MathTex(r"\sin(\alpha) = \tan(\alpha)").scale(1.3).move_to(ORIGIN)
# self.play(Write(umf1))
# self.wait(1)
# umf2 = MathTex(r"\frac{\Delta s}{g} = \frac{a_k}{l}").scale(1.3).move_to(ORIGIN)
# self.play(TransformMatchingTex(umf1, umf2))
# self.wait(1)
# umf3 = MathTex(r"a_k = \frac{l \cdot \Delta s}{g}").scale(1.3).move_to(ORIGIN)
# self.play(TransformMatchingTex(umf2, umf3))
# self.wait(1)
# umf4 = (
#     MathTex(r"a_k = \frac{l \cdot k \cdot \lambda}{g}")
#     .scale(1.3)
#     .move_to(ORIGIN)
# )
# self.play(TransformMatchingTex(umf3, umf4))
# self.wait(1)
# umf5 = (
#     MathTex(r"\lambda = \frac{a_k \cdot g}{l \cdot k}")
#     .scale(1.3)
#     .move_to(ORIGIN)
# )
# self.play(TransformMatchingTex(umf4, umf5))
# self.wait(3)
