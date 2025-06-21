import numpy as np
from manim import *


class DoubleSlitStatic(Scene):
    def construct(self):
        # Parameter
        g = 3.0  # Spaltabstand
        alpha = 20 * DEGREES  # Ablenkwinkel
        slit_x = -3.0  # x-Position der Spaltebene
        plane_x = 6.0  # x-Position der Beobachtungsebene

        # Punkte S und T (Doppelspalt) und deren Mittelpunkt M
        S = np.array([slit_x, g / 2, 0])
        T = np.array([slit_x, -g / 2, 0])
        M = (S + T) / 2

        # Beobachtungspunkt A auf der Beobachtungsebene
        y_A = (plane_x - slit_x) * np.tan(alpha) + T[1]
        A = np.array([plane_x, y_A, 0])

        # Punkt F auf der Strecke TA so, dass AF = AS
        AS_len = np.linalg.norm(S - A)
        TA_len = np.linalg.norm(T - A)
        F = A + (AS_len / TA_len) * (T - A)

        # Zeichnen der optischen Achse (horizontal, gestrichelt)
        center_line = DashedLine(
            start=[slit_x, 0, 0],
            end=[6, 0, 0],
            dash_length=0.1,
            dashed_ratio=0.5,
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
        screen_line = Line(
            start=[plane_x, -4, 0],
            end=[plane_x, 4, 0],
        )
        screen_text = Text("Beobachtungsebene", font_size=24)
        screen_text.rotate(PI / 2).next_to(screen_line, UP, buff=0.2)

        # Punkte O, A und F markieren
        O = np.array([plane_x, 0, 0])
        O_dot = Dot(O)
        O_label = MathTex("O").next_to(O_dot, RIGHT)
        A_dot = Dot(A)
        A_label = MathTex("A").next_to(A_dot, RIGHT)
        F_dot = Dot(F)
        F_label = MathTex("F").next_to(F_dot, DOWN)

        # Strahlen von S und T nach A
        ray_S = Line(start=S, end=A, color=WHITE)
        ray_T = Line(start=T, end=A, color=WHITE)
        ray_S.set_color(BLUE)
        ray_T.set_color(RED)

        angle_ST = ray_T.get_angle() - ray_S.get_angle()
        rotation_overshoot = angle_ST * 0.3
        slit_screen_line_label = (
            MathTex("l").next_to(center_line, DOWN).shift(RIGHT * 2)
        )

        # Gleichschenkliges Dreieck S-A-F darstellen (AS = AF)
        tri_SF = DashedLine(start=S, end=F)
        tri_SF_arc = ArcBetweenPoints(
            start=S,
            end=F,
            radius=np.linalg.norm(S - A),  # radius = |AS|
        )
        # tri_AF = Line(start=A, end=F, color=BLUE)

        # Strecke M-A mit Beschriftung m
        ray_MA = Line(start=M, end=A)
        m_label = MathTex("m").next_to(ray_MA.point_from_proportion(0.5), UP)

        # Dreieck FSA
        triangle_FSA = Polygon(
            F_dot.get_center(),
            S_dot.get_center(),
            A_dot.get_center(),
            color=YELLOW,
            fill_opacity=0.3,
            stroke_width=2,
        )
        # Strecke T-A mit Beschriftung l
        # l_label = MathTex("l").next_to(ray_T.point_from_proportion(0.5), DOWN)

        # Winkel alpha am unteren Strahl darstellen
        angle_label_scale = 0.8
        angle_AMO = Angle(center_line, ray_MA, radius=1.6)
        AMO_label = MathTex(r"\alpha").next_to(angle_AMO, LEFT)
        angle_TSF = Angle(Line(S, T), Line(S, F), radius=2)
        TSF_label = (
            MathTex(r"\sphericalangle TSF")
            .next_to(angle_TSF, LEFT)
            .shift(RIGHT * 0.2)
            .scale(angle_label_scale)
        )
        angle_SAT = Angle(
            Line(A, S),
            Line(A, T),
            radius=2.5,  # TODO: make relative to distance slit <-> screen, so the angle still shows even when A is off-screen
        )
        SAT_label = (
            MathTex(r"\sphericalangle SAT")
            .next_to(angle_SAT, LEFT)
            .scale(angle_label_scale)
        )
        angle_ASF = Angle(Line(F, A), Line(F, S), radius=0.5)
        ASF_label = (
            MathTex(r"\sphericalangle AFS")
            .next_to(angle_ASF, RIGHT)
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
        self.play(
            Rotate(
                ray_S, (angle_ST + rotation_overshoot), about_point=A_dot.get_center()
            )
        )
        self.play(Rotate(ray_S, -rotation_overshoot, about_point=A_dot.get_center()))
        delta_s = Line(ray_T.get_start(), ray_S.get_start(), color=GREEN)
        delta_s_label = MathTex("\Delta s").next_to(delta_s, UP)
        self.wait(1)
        self.add(delta_s, delta_s_label)
        self.wait(1)
        self.remove(delta_s_label)
        self.add(F_dot, F_label)
        self.wait(1)
        self.play(Rotate(ray_S, -angle_ST, about_point=A_dot.get_center()))
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
        self.add(angle_ASF, ASF_label)
        self.wait(1)

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
