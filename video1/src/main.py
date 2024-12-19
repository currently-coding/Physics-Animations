from manim import Scene, Text, MathTex, VGroup, Write, config, UP, DOWN, FadeOut, Tex, SVGMobject, Vector, LEFT, RIGHT, GREEN, BLUE, RED, UL, DL, FadeIn, UR, ORIGIN, TransformMatchingTex, Arrow, Create, Transform

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

        self.play(FadeOut(eqn1), FadeOut(text_group))
