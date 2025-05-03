from manim import *
import numpy as np

class DoubleSlitStatic(Scene):
    def construct(self):
        # Parameter
        g = 3.0                          # Spaltabstand
        alpha = 20 * DEGREES            # Ablenkwinkel
        slit_x = -3.0                   # x-Position der Spaltebene
        plane_x = 6.0                   # x-Position der Beobachtungsebene

        # Punkte S und T (Doppelspalt) und deren Mittelpunkt M
        S = np.array([slit_x,  g/2, 0])
        T = np.array([slit_x, -g/2, 0])
        M = (S + T) / 2

        # Beobachtungspunkt A auf der Beobachtungsebene
        y_A = (plane_x - slit_x) * np.tan(alpha) + T[1]
        A = np.array([plane_x, y_A, 0])

        # Punkt F auf der Strecke TA so, dass AF = AS
        AS_len = np.linalg.norm(S - A)
        TA_len = np.linalg.norm(T - A)
        F = A + (AS_len / TA_len) * (T - A)

        # Zeichnen der optischen Achse (horizontal, gestrichelt)
        axis = DashedLine(
            start=[-6, 0, 0],
            end=[ 6, 0, 0],
            dash_length=0.1,
            dashed_ratio=0.5,
        )

        # Zeichnen der Spaltebene (vertikale Linie)
        slit_line = Line(
            start=[slit_x,  g/2 + 0.5, 0],
            end=[slit_x, -g/2 - 0.5, 0],
        )

        # Punktquellen und Labels
        S_dot = Dot(S, color=YELLOW)
        T_dot = Dot(T, color=YELLOW)
        M_dot = Dot(M, color=YELLOW)
        S_label = MathTex("S").next_to(S_dot, LEFT)
        T_label = MathTex("T").next_to(T_dot, LEFT)
        M_label = MathTex("M").next_to(M_dot, LEFT)

        # Abstand g markieren
        g_arrow = DoubleArrow(
            start=[slit_x - 1.2, -g/2, 0],
            end=[slit_x - 1.2,  g/2, 0]
        )
        g_label = MathTex("g").next_to(g_arrow, LEFT)

        # Zeichnen der Beobachtungsebene
        plane_line = Line(
            start=[plane_x, -4, 0],
            end=[plane_x,  4, 0],
        )
        plane_text = Text("Beobachtungsebene", font_size=24)
        plane_text.rotate(PI/2).next_to(plane_line, UP, buff=0.2)

        # Punkte O, A und F markieren
        O = np.array([plane_x, 0, 0])
        O_dot = Dot(O)
        O_label = MathTex("O").next_to(O_dot, RIGHT)
        A_dot = Dot(A)
        A_label = MathTex("A").next_to(A_dot, RIGHT)
        F_dot = Dot(F)
        F_label = MathTex("F").next_to(F_dot, DOWN)

        # Strahlen von S und T nach A
        ray_S = Line(start=S, end=A, color=RED)
        ray_T = Line(start=T, end=A, color=RED)

        # Gleichschenkliges Dreieck S-A-F darstellen (AS = AF)
        tri_SF = DashedLine(start=S, end=F)
        #tri_AF = Line(start=A, end=F, color=BLUE)

        # Strecke M-A mit Beschriftung m
        ray_MA = Line(start=M, end=A)
        m_label = MathTex("m").next_to(ray_MA.point_from_proportion(0.5), UP)

        # Strecke T-A mit Beschriftung l
        l_label = MathTex("l").next_to(ray_T.point_from_proportion(0.5), DOWN)

        # Winkel alpha am unteren Strahl darstellen
        angle_arc = Angle(axis, ray_MA, radius=1.6, other_angle=False)
        alpha_label = MathTex("\\alpha").next_to(angle_arc, LEFT)

        # Alle Elemente statisch hinzufügen
        self.add(
            axis, slit_line,
            S_dot, T_dot, M_dot, S_label, T_label, M_label,
            g_arrow, g_label,
            plane_line, plane_text,
            O_dot, O_label, A_dot, A_label, F_dot, F_label,
            ray_S, ray_T,
            tri_SF,
            ray_MA, m_label,
            l_label, angle_arc, alpha_label
        )
