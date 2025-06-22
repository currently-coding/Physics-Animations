import numpy as np
from manim import *


class DoubleSlitStatic(ZoomedScene):
    def construct(self):
        # Parameter
        g = 3.0  # Spaltabstand
        alpha = 20 * DEGREES  # Ablenkwinkel
        slit_x = -3.0  # x-Position der Spaltebene
        screen_x = ValueTracker(6.0)  # x-Position der Beobachtungsebene

        # Punkte S und T (Doppelspalt) und deren Mittelpunkt M
        S = np.array([slit_x, g / 2, 0])
        T = np.array([slit_x, -g / 2, 0])
        M = (S + T) / 2
        y_A = (screen_x.get_value() - slit_x) * np.tan(alpha) + T[1]

        # Beobachtungspunkt A auf der Beobachtungsebene
        A = np.array(
            [
                screen_x.get_value(),
                y_A,
                0,
            ]
        )

        F = A + (np.linalg.norm(S - A) / np.linalg.norm(T - A)) * (T - A)

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
        S_label = MathTex("S").next_to(S_dot, LEFT)
        T_label = MathTex("T").next_to(T_dot, LEFT)
        M_label = MathTex("M").next_to(M_dot, LEFT)

        # Abstand g markieren
        g_arrow = DoubleArrow(
            start=[slit_x - 1.2, -g / 2 - 0.25, 0], end=[slit_x - 1.2, g / 2 + 0.25, 0]
        )
        g_label = MathTex("g").next_to(g_arrow, LEFT)

        # Zeichnen der Beobachtungsebene
        screen_line = always_redraw(
            lambda: Line(
                start=[screen_x.get_value(), -4, 0],
                end=[screen_x.get_value(), 4, 0],
            )
        )
        screen_text = Text("Beobachtungsebene", font_size=24)
        screen_text.rotate(PI / 2).next_to(screen_line, UP, buff=0.2)

        # Punkte O, A und F markieren
        O = np.array([screen_x.get_value(), 0, 0])
        O_dot = always_redraw(lambda: Dot(np.array([screen_x.get_value(), 0, 0])))
        O_label = MathTex("O").next_to(O_dot, RIGHT)
        A_dot = always_redraw(
            lambda: Dot(
                np.array(
                    [
                        screen_x.get_value(),
                        y_A,
                        0,
                    ]
                )
            )
        )
        A_label = always_redraw(lambda: MathTex("A").next_to(A_dot, RIGHT))
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
        F_label = always_redraw(lambda: MathTex("F").next_to(F_dot, DOWN))

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
        # Strecke T-A mit Beschriftung l
        # l_label = MathTex("l").next_to(ray_T.point_from_proportion(0.5), DOWN)

        # Winkel alpha am unteren Strahl darstellen
        angle_label_scale = 0.8
        angle_AMO = always_redraw(lambda: Angle(center_line, ray_MA, radius=1.6))
        AMO_label = always_redraw(lambda: MathTex(r"\alpha").next_to(angle_AMO, RIGHT))
        angle_TSF = always_redraw(
            lambda: Angle(
                Line(S_dot.get_center(), T_dot.get_center()),
                Line(S_dot.get_center(), F_dot.get_center()),
                radius=2,
            )
        )
        TSF_label = always_redraw(
            lambda: MathTex(r"\sphericalangle TSF")
            .next_to(angle_TSF, LEFT)
            .shift(RIGHT * 0.2)
            .scale(angle_label_scale)
        )
        angle_SAT = always_redraw(
            lambda: Angle(
                Line(A_dot.get_center(), S_dot.get_center()),
                Line(A_dot.get_center(), T_dot.get_center()),
                radius=2.5,  # TODO: make relative to distance slit <-> screen, so the angle still shows even when A is off-screen
            )
        )
        SAT_label = always_redraw(
            lambda: MathTex(r"\sphericalangle SAT")
            .next_to(angle_SAT, LEFT)
            .scale(angle_label_scale)
        )
        angle_SFA = always_redraw(
            lambda: Angle(
                Line(F_dot.get_center(), A_dot.get_center()),
                Line(F_dot.get_center(), S_dot.get_center()),
                radius=0.5,
            )
        )
        SFA_label = always_redraw(
            lambda: MathTex(r"\sphericalangle AFS")
            .next_to(angle_SFA, RIGHT)
            .shift(UP * 0.5)
            .shift(LEFT * 0.2)
            .scale(angle_label_scale)
        )

        # Alle Elemente statisch hinzufügen
        self.play(
            FadeIn(slit_line, S_dot, T_dot, screen_line, screen_text, S_label, T_label)
        )
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
        delta_s = Line(static_ray_T.get_start(), static_ray_S.get_start(), color=GREEN)
        delta_s_label = MathTex("\\Delta s").next_to(delta_s, UP)
        self.wait(1)
        self.add(delta_s, delta_s_label)
        self.wait(1)
        self.remove(delta_s_label, delta_s)
        self.remove(static_ray_T)
        self.add(ray_T)
        self.add(F_dot, F_label)
        self.wait(1)
        self.play(Rotate(static_ray_S, -angle_ST, about_point=A_dot.get_center()))
        self.remove(static_ray_S)
        self.add(ray_S)
        self.add(A_dot)
        self.wait(1)
        self.add(A_label)
        self.wait(1)
        self.play(FadeIn(triangle_FSA))
        self.wait(1)
        self.add(tri_SF, tri_SF_arc)
        self.play(FadeOut(triangle_FSA))
        self.wait(1)
        self.add(M_dot, M_label, ray_MA)
        self.wait(1)
        self.add(angle_AMO, AMO_label)
        self.wait(1)
        self.add(angle_TSF, TSF_label)
        self.wait(1)
        self.add(angle_SAT, SAT_label)
        self.wait(1)
        self.add(angle_SFA, SFA_label)
        self.play(screen_x.animate.set_value(100), run_time=15)
        self.wait(1)
        self.play(self.camera.frame.animate.move_to(ORIGIN))
        self.wait(5)

        # self.add(M_dot)
        # self.wait(1)
        # self.add(M_label)
        # self.wait(1)
        # self.add(g_arrow)
        # self.wait(1)
        # self.add(g_label)
        # self.wait(1)
        # self.add(O_dot)
        # self.wait(1)
        # self.add(O_label)
        # self.wait(1)
        # self.add(tri_SF_arc)
        # self.wait(1)
        # self.add(tri_SF)
        # self.wait(1)
        # self.add(ray_MA)
        # self.wait(1)
        # self.add(m_label)
        # self.wait(1)
        # self.add(slit_screen_line_label)
        # self.wait(1)
        # self.add(angle_arc)
        # self.wait(1)
        # self.add(alpha_label)
        # (self.wait(1))
