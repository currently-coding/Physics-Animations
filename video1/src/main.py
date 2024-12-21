from manim import Scene, Text, MathTex, VGroup, Write, config, UP, DOWN, FadeOut, Tex, SVGMobject, Vector, LEFT, RIGHT, GREEN, BLUE, RED, UL, DL, FadeIn, UR, ORIGIN, TransformMatchingTex, Arrow, Create, Transform, Dot, VMobject, MoveAlongPath, DEGREES, YELLOW, ArrowSquareTip, linear, Circle, PI
import numpy as np

class LorentzKraftVideo(Scene):
    def construct(self):
        # Titel der Präsentation
        title = Text("Die Lorentzkraft", font_size=72)
        subtitle = Text("erklärt am magnetohydrodynamischen Antrieb", font_size=36)
        subtitle.next_to(title, DOWN)
        title_group = VGroup(title, subtitle)
        
        # Versuchsankündigung
        experiment_note = Text(
            "Von oben gefilmter Versuch mit Pfeilen erklärt",
            font_size=36
        )

        # Definition und Formel
        definition_header = Text("Definition:", font_size=48).to_edge(UP, buff=2)
        
        definition_text = Text(
            "Die Lorentzkraft ist die Kraft, die auf bewegte\n"
            "elektrische Ladungen in einem Magnetfeld wirkt.",
            font_size=42,
            line_spacing=1.2
        ).move_to(ORIGIN)
        
        lorentz_eqn = MathTex(
            r"\vec{F}_L", r"=", r"q(", r"\vec{v}", r"\times", r"\vec{B}", r")"
        ).scale(1.2)
        lorentz_eqn.next_to(definition_text, DOWN, buff=1.5)
        
        # Farbkodierung
        for tex, color in [(r"\vec{v}", GREEN), (r"\vec{B}", BLUE), (r"\vec{F}_L", RED)]:
            lorentz_eqn.set_color_by_tex(tex, color)
        
        # Gruppierung
        definition_group = VGroup(definition_header, definition_text, lorentz_eqn)
        definition_group.move_to(ORIGIN)
        
        # Animation Sequenz
        self.play(Write(title_group))
        self.wait(2)
        self.play(FadeOut(title_group))
        
        self.play(Write(experiment_note))
        self.wait(2)
        self.play(FadeOut(experiment_note))
        
        self.play(Write(definition_group))
        self.wait(3)
        self.play(
            FadeOut(definition_header),
            FadeOut(definition_text),
            lorentz_eqn.animate.to_edge(UR)
        )

        # Right-hand rule demonstration
        hand = SVGMobject("svg/right-hand-rule.svg").scale(2)
        v_vector = Vector(0.5*RIGHT+2.5*UP).set_color(GREEN)
        v_label = Tex(r"$\vec{v}$").set_color(GREEN).next_to(v_vector,UP)

        B_vector = Vector(3*LEFT+0.75*UP).set_color(BLUE)
        B_label = Tex(r"$\vec{B}$").move_to(B_vector.get_end()).shift(UL*0.5).set_color(BLUE)

        F_vector = Vector(2.5*LEFT+1*DOWN).set_color(RED)
        F_label = Tex(r"$\vec{F}_L$").move_to(F_vector.get_end()).shift(DL*0.5).set_color(RED)

        self.play(Write(hand))
        self.play(Write(v_vector), Write(B_vector))
        self.play(FadeIn(v_label, B_label))
        self.play(Write(F_vector))
        self.play(FadeIn(F_label))
        self.wait()
        self.play(FadeOut(v_label, B_label, F_label, lorentz_eqn, hand, v_vector, B_vector, F_vector))
        
        # Application placeholder
        application_text = Text(
            "Anwendung auf den Versuch",
            font_size=36
        ).move_to(ORIGIN)
        
        self.play(Write(application_text))
        self.wait(2)
        self.play(FadeOut(application_text))
        
        # Mathematical derivation
        eqn = MathTex(
            r"\vec{F}_L", r"=", r"q(", r"\vec{v}", r"\times", r"\vec{B}", r")"
        ).scale(1.2).move_to(ORIGIN)
        
        # Color coding
        for tex, color in [(r"\vec{v}", GREEN), (r"\vec{B}", BLUE), (r"\vec{F}_L", RED)]:
            eqn.set_color_by_tex(tex, color)
        
        self.play(Write(eqn))
        self.wait()
        
        # Mathematical derivation
        eqn1 = MathTex(
            r"F_L", r"=", r"q", r"v", r"B", r"\sin(\theta)"
        ).scale(1.2).to_edge(UP, buff=1)  # Reduced buffer to move everything up

        # Color coding for equation
        for tex, color in [(r"v", GREEN), (r"B", BLUE), (r"F_L", RED)]:
            eqn1.set_color_by_tex(tex, color)

        # Create and position text elements relative to equation
        header = Text(
            "Die Lorentzkraft ist umso größer, je...",
            font_size=36
        ).next_to(eqn1, DOWN, buff=0.8)  # Slightly reduced buffer

        points = [
            "• größer die Ladung q ist",
            "• schneller sich die Ladung bewegt (v)",
            "• stärker das Magnetfeld ist (B)",
            "• mehr die Bewegungsrichtung senkrecht",
            "  zum Magnetfeld steht (sin θ)"
        ]

        bullet_points = VGroup(*[
            Text(point, font_size=32)
            for point in points
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        # Position bullet points relative to header
        bullet_points.next_to(header, DOWN, buff=0.5)
        
        # Align last line with bullet points
        bullet_points[-1].align_to(bullet_points[-2], LEFT)

        # Group all text elements
        text_group = VGroup(header, bullet_points)

        # Animation sequence
        self.play(Transform(eqn, eqn1))
        self.play(Write(text_group))
        self.wait(3)

        self.play(FadeOut(eqn), FadeOut(text_group))

        self.lorentz_particle(charge=1.0, velocity=1.0)
        self.lorentz_particle(charge=1.0, velocity=2.0)

    def lorentz_particle(self, charge, velocity, B_strength=1.2, angle_degrees=45):
        # -------- SETUP --------
        angle = angle_degrees * DEGREES  # Umrechnung in Radianten
        force = charge * velocity * B_strength # * sin(90)
        
        # -------- MAGNETFELD --------
        B_field = VGroup(*[
            Text("×", font_size=24)
            for _ in range(64)
        ]).arrange_in_grid(8, 8, buff=0.7)
        B_field.set_color(BLUE)
        
        # -------- TEILCHEN --------
        particle = Dot(color=RED if charge > 0 else BLUE)
        
        # -------- BESCHRIFTUNGEN --------
        B_label = Tex(r"$\vec{B}$").set_color(BLUE).next_to(B_field, UP, buff=0.2)  # B-Vektor über dem Feld
        q_label = Tex(f"q = {charge} e").set_color(RED if charge > 0 else BLUE)
        v_label = Tex(r"$v = " + str(velocity) + r"\,\mathrm{\frac{m}{s}}$").set_color(GREEN)
        
        # Positionierung der Labels
        q_label.to_corner(UL)
        v_label.next_to(q_label, DOWN)
        
        # -------- BAHNBERECHNUNG --------
        radius = abs(velocity * charge / B_strength)
        center_offset = radius * np.array([-np.sin(angle), np.cos(angle), 0])
        
        # Zeit für genau eine Rotation
        omega = velocity / radius  # Kreisfrequenz
        t_max = 2 * np.pi / omega  # Zeit für eine volle Rotation
        
        # Kreis erstellen und rotieren
        circle = Circle(radius=radius, color=YELLOW).move_to(center_offset)
        circle.rotate(-angle, about_point=center_offset)  # Rotation um 90° (oder einen anderen Winkel)
        circle.set_stroke(opacity=0.3)
        
        # -------- KRAFTVEKTOR --------
        # Skalierungsfaktoren
        force_scale = 0.5
        velocity_scale = 0.5
        
        # Standardwerte für alle Pfeile
        arrow_kwargs = {
            "tip_length": 0.4,  # Same tip size for all arrows
            "max_tip_length_to_length_ratio": 0.4
        }
        
        force_vector = Arrow(
            start=ORIGIN, 
            end=RIGHT, 
            color=RED,
            **arrow_kwargs
        )

        
        velocity_vector = Arrow(
            start=ORIGIN,
            end=RIGHT,
            color=GREEN,
            **arrow_kwargs
        )
        
        def update_force_vector(arrow):
            # Berechne neue Start- und Endpunkte
            start = particle.get_center()
            direction = center_offset - start
            direction = direction / np.linalg.norm(direction) * force * force_scale
            # Aktualisiere den existierenden Pfeil
            arrow.put_start_and_end_on(
                start,
                start + direction
            )
            
        def update_velocity_vector(arrow):
            # Berechne neue Start- und Endpunkte
            start = particle.get_center()
            # Vektor vom Kreismittelpunkt zum Teilchen
            radial = start - center_offset
            # Tangentialvektor (90° gedreht)
            tangent = np.array([-radial[1], radial[0], 0])  # Rotation um 90°
            # Normieren und skalieren
            tangent = tangent / np.linalg.norm(tangent) * velocity * velocity_scale
            # Aktualisiere den existierenden Pfeil
            arrow.put_start_and_end_on(
                start,
                start + tangent
            )
        
        # Füge den Updater hinzu
        force_vector.add_updater(update_force_vector)
        velocity_vector.add_updater(update_velocity_vector)
        
        # -------- ANIMATION --------
        self.play(
            FadeIn(B_field),
            Write(B_label),
            FadeIn(particle),
            Write(q_label),
            Write(v_label)
        )
        self.wait()

        rate = lambda t: min(max(3*t-1, 0), 1)

        self.play(
            MoveAlongPath(particle, circle, rate_func=linear),
            FadeIn(circle, rate_func=rate), 
            FadeIn(velocity_vector, rate_func=rate), FadeIn(force_vector, rate_func=rate),
            run_time=t_max
        )
        self.wait()
        
        # Aufräumen
        self.play(
            *[FadeOut(mob) for mob in [B_field, B_label,
                                     particle, q_label, v_label, circle, 
                                     force_vector, velocity_vector]]
        )