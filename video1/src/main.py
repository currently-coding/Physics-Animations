from dataclasses import field
from manim_physics import Wire, MagneticField
from manim import (
    TracedPath,
    Rectangle,
    BLACK,
    GREEN,
    RED,
    BLUE,
    ORANGE,
    TEAL,
    PURPLE,
    MAROON,
    ImageMobject,
    Line,
    Scene,
    Square,
    Text,
    MathTex,
    WHITE,
    ThreeDScene,
    VGroup,
    Write,
    config,
    UP,
    DOWN,
    FadeOut,
    Tex,
    SVGMobject,
    Vector,
    LEFT,
    RIGHT,
    GREEN,
    BLUE,
    RED,
    UL,
    DL,
    FadeIn,
    UR,
    ORIGIN,
    TransformMatchingTex,
    Arrow,
    Create,
    Transform,
    Dot,
    VMobject,
    MoveAlongPath,
    DEGREES,
    YELLOW,
    ArrowSquareTip,
    linear,
    Circle,
    PI,
)
import numpy as np
from pathops import NumberOfPointsError


class LorentzKraftVideo(Scene):
    def construct(self):
        # Titel der Präsentation
        title = Text("Die Lorentzkraft", font_size=72)
        subtitle = Text("erklärt am magnetohydrodynamischen Antrieb", font_size=36)
        subtitle.next_to(title, DOWN)
        title_group = VGroup(title, subtitle)

        # Versuchsankündigung
        experiment_note = Text(
            "Von oben gefilmter Versuch mit Pfeilen erklärt", font_size=36
        )
        # Definition und Formel
        definition_header = Text("Definition:", font_size=48).to_edge(UP, buff=2)

        definition_text = Text(
            "Die Lorentzkraft ist die Kraft, die auf bewegte\n"
            "elektrische Ladungen in einem Magnetfeld wirkt.",
            font_size=42,
            line_spacing=1.2,
        ).move_to(ORIGIN)

        lorentz_eqn = MathTex(
            r"\vec{F}_L", r"=", r"q(", r"\vec{v}", r"\times", r"\vec{B}", r")"
        ).scale(1.2)
        lorentz_eqn.next_to(definition_text, DOWN, buff=1.5)

        # Farbkodierung
        for tex, color in [
            (r"\vec{v}", GREEN),
            (r"\vec{B}", BLUE),
            (r"\vec{F}_L", RED),
        ]:
            lorentz_eqn.set_color_by_tex(tex, color)

        # Gruppierung
        definition_group = VGroup(definition_header, definition_text, lorentz_eqn)
        definition_group.move_to(ORIGIN)
        # ---- Aufbau ----
        #
        # Hier Magnet einleitung
        self.bar_magnet_field_lines()

        #
        # TODO: Hier Probemagnet hinzufuegen und hervorheben
        #
        # Hier lorentz_particle_comparison() zeigen und definieren
        self.particle_deflection()
        self.play(Write(definition_group))
        self.wait(5)
        self.play(FadeOut(definition_group))
        #
        # TODO: Hier Lorentz zeigen(Bild von ihm)
        #
        # Hier Formel zeigen
        self.play(
            lorentz_eqn.animate.to_edge(UR),
        )
        #
        # Hier Kreuzprodukt aufloesen
        #
        # Hier beziehungen zeigen
        # Mathematical derivation
        eqn = (
            MathTex(r"\vec{F}_L", r"=", r"q(", r"\vec{v}", r"\times", r"\vec{B}", r")")
            .scale(1.2)
            .move_to(ORIGIN)
        )

        # Color coding
        for tex, color in [
            (r"\vec{v}", GREEN),
            (r"\vec{B}", BLUE),
            (r"\vec{F}_L", RED),
        ]:
            eqn.set_color_by_tex(tex, color)

        self.play(Write(eqn))
        self.wait()

        # Mathematical derivation
        eqn1 = (
            MathTex(r"F_L", r"=", r"q", r"v", r"B", r"\sin(\theta)")
            .scale(1.2)
            .to_edge(UP, buff=1)
        )  # Reduced buffer to move everything up

        # Color coding for equation
        for tex, color in [(r"v", GREEN), (r"B", BLUE), (r"F_L", RED)]:
            eqn1.set_color_by_tex(tex, color)

        # Create and position text elements relative to equation
        header = Text("Die Lorentzkraft ist umso größer, je...", font_size=36).next_to(
            eqn1, DOWN, buff=0.8
        )  # Slightly reduced buffer

        points = [
            "• größer die Ladung q ist",
            "• schneller sich die Ladung bewegt (v)",
            "• stärker das Magnetfeld ist (B)",
            "• mehr die Bewegungsrichtung senkrecht",
            "• zum Magnetfeld steht (sin θ)",
        ]

        bullet_points = VGroup(
            *[Text(point, font_size=32) for point in points]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

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

        self.lorentz_particle()
        self.lorentz_particle(B_strength=2)
        self.lorentz_particle(velocity=1)
        self.lorentz_particle(charge=1.5)
        #
        # Hier 3-Finger Regel zeigen
        #
        hand = SVGMobject("svg/right-hand-rule.svg").scale(2)
        v_vector = Vector(0.5 * RIGHT + 2.5 * UP).set_color(GREEN)
        v_label = Tex(r"$\vec{v}$").set_color(GREEN).next_to(v_vector, UP)

        B_vector = Vector(3 * LEFT + 0.75 * UP).set_color(BLUE)
        B_label = (
            Tex(r"$\vec{B}$")
            .move_to(B_vector.get_end())
            .shift(UL * 0.5)
            .set_color(BLUE)
        )

        F_vector = Vector(2.5 * LEFT + 1 * DOWN).set_color(RED)
        F_label = (
            Tex(r"$\vec{F}_L$")
            .move_to(F_vector.get_end())
            .shift(DL * 0.5)
            .set_color(RED)
        )

        self.play(Write(hand))
        self.play(Write(v_vector), Write(B_vector))
        self.play(FadeIn(v_label, B_label))
        self.play(Write(F_vector))
        self.play(FadeIn(F_label))
        self.wait()
        self.play(
            FadeOut(
                v_label,
                B_label,
                F_label,
                lorentz_eqn,
                hand,
                v_vector,
                B_vector,
                F_vector,
            )
        )
        # TODO: Hier Versuch mit Pfeilen zeigen
        #
        # Fertig!
        # (evtl code scroll down zeigen)
        # ----- Ende -----

        # Animation Sequenz
        #
        #
        # self.play(Write(title_group))
        # self.wait(2)
        # self.play(FadeOut(title_group))

        # self.play(Write(experiment_note))
        # self.wait(2)
        # self.play(FadeOut(experiment_note))

        self.wait(3)

        # Right-hand rule demonstration

        # Application placeholder
        application_text = Text("Anwendung auf den Versuch", font_size=36).move_to(
            ORIGIN
        )

        self.play(Write(application_text))
        self.wait(2)
        self.play(FadeOut(application_text))

    def bar_magnet_field_lines(self):
        # Load the image (use the image file name or full path)
        image = ImageMobject(
            "../bar-magnet-icon-n-pole-and-s-pole-magnets-png-3540789338.png"
        )
        image.rotate(-1 * (PI / 4))

        # Resize the image (optional)
        image.scale(0.4)  # Adjust the scale factor as needed

        # Position the image (optional)
        image.to_edge(UP)  # Moves the image to the top edge of the screen
        image.shift(UP * 0.5)

        north = (
            Rectangle(BLACK, height=0.8, width=1.5)
            .shift(LEFT * 0.5)
            .set_fill(GREEN, opacity=100)
        )
        south = Rectangle(BLACK, height=0.8, width=1.5).set_fill(RED, opacity=100)
        south.next_to(north, buff=0)

        # Adding the field lines
        wire3 = Wire(Circle(1).rotate(PI / 2, UP), current=2)
        mag_field = MagneticField(
            wire3,
            x_range=[-10, 10],
            y_range=[-10, 10],
        )
        self.add(image)
        self.play(FadeIn(mag_field))
        # Add the image to the scene
        # self.add(south, north)
        self.wait(3)
        self.play(FadeOut(mag_field, image))

    def lorentz_particle(
        self, charge=1.0, velocity=2.0, B_strength=1.2, angle_degrees=45
    ):
        # -------- PARAMETERS (adjust here) --------

        # -------- SETUP --------
        angle = angle_degrees * DEGREES  # Convert to radians
        force = charge * velocity * B_strength  # * sin(90)

        # -------- MAGNETIC FIELD --------
        B_field = VGroup(*[Text("×", font_size=24) for _ in range(64)]).arrange_in_grid(
            8, 8, buff=0.7
        )
        B_field.set_color(BLUE)

        # -------- PARTICLE --------

        # -------- LABELS --------
        B_label = (
            Tex(r"$\vec{B}$").set_color(BLUE).next_to(B_field, UP, buff=0.2)
        )  # B vector above field
        q_label = Tex(f"q = {charge} e").set_color(RED if charge > 0 else BLUE)
        v_label = Tex(r"$v = " + str(velocity) + r"\,\mathrm{\frac{m}{s}}$").set_color(
            GREEN
        )

        # Label positioning
        q_label.to_corner(UL)
        v_label.next_to(q_label, DOWN)

        def get_B_field_bounds(B_field):
            """Get the bounds (left, right, top, bottom) of the B_field."""
            left = B_field.get_left()[0]  # x-coordinate of the leftmost point
            right = B_field.get_right()[0]  # x-coordinate of the rightmost point
            top = B_field.get_top()[1]  # y-coordinate of the topmost point
            bottom = B_field.get_bottom()[1]  # y-coordinate of the bottommost point
            return left, right, top, bottom

        field_bounds = get_B_field_bounds(B_field)
        field_center = np.array(
            [
                (field_bounds[1] + field_bounds[0]) / 2,
                (field_bounds[2] + field_bounds[3]) / 2,
                0,
            ]
        )
        # spawns center of b_field
        radius = abs(velocity * charge / B_strength)
        circle = Circle(radius=radius, color=YELLOW).move_to(field_center)
        particle = (
            Dot(color=RED if charge > 0 else BLUE)
            .move_to(field_center)
            .shift(RIGHT * radius)
        )
        center_offset = radius * np.array(
            [-np.sin(angle), np.cos(angle), 0]
        )  # BUG: incorrect calculation leads to errors pointing wrong directions

        # Time for exactly one rotation
        omega = velocity / radius  # Angular frequency
        t_max = 2 * np.pi / omega  # Time for one full rotation

        # Create and rotate circle
        # circle = Circle(radius=radius, color=YELLOW).move_to(center_offset) circle already at correct position
        # circle.rotate(
        # -angle, about_point=center_offset
        # )  # BUG: no clue why that is here, seems to mess stuff up
        circle.set_stroke(opacity=0.3)

        # -------- FORCE VECTOR --------
        # Scaling factors
        force_scale = 0.5
        velocity_scale = 0.5

        # Standard values for all arrows
        arrow_kwargs = {
            "tip_length": 0.4,  # Same tip size for all arrows
            "max_tip_length_to_length_ratio": 0.4,
        }

        force_vector = Arrow(start=ORIGIN, end=RIGHT, color=RED, **arrow_kwargs)

        velocity_vector = Arrow(start=ORIGIN, end=RIGHT, color=GREEN, **arrow_kwargs)

        def update_force_vector(arrow):
            # Calculate new start and end points
            start = particle.get_center()
            direction = center_offset - start
            direction = direction / np.linalg.norm(direction) * force * force_scale
            # Update existing arrow
            arrow.put_start_and_end_on(start, start + direction)

        def update_velocity_vector(arrow):
            # Calculate new start and end points
            start = particle.get_center()
            # Vector from circle center to particle
            radial = start - center_offset
            # Tangential vector (90° rotation)
            tangent = np.array([-radial[1], radial[0], 0])
            # Normalize and scale
            tangent = tangent / np.linalg.norm(tangent) * velocity * velocity_scale
            # Update existing arrow
            arrow.put_start_and_end_on(start, start + tangent)

        # Füge den Updater hinzu
        force_vector.add_updater(update_force_vector)
        velocity_vector.add_updater(update_velocity_vector)

        # -------- ANIMATION --------
        self.play(
            FadeIn(B_field),
            Write(B_label),
            FadeIn(particle),
            Write(q_label),
            Write(v_label),
        )
        self.wait()

        rate = lambda t: min(max(3 * t - 1, 0), 1)

        self.play(
            MoveAlongPath(particle, circle, rate_func=linear),
            FadeIn(circle, rate_func=rate),
            FadeIn(velocity_vector, rate_func=rate),
            FadeIn(force_vector, rate_func=rate),
            run_time=t_max,
        )
        self.wait()

        # Aufräumen
        self.play(
            *[
                FadeOut(mob)
                for mob in [
                    B_field,
                    B_label,
                    particle,
                    q_label,
                    v_label,
                    circle,
                    force_vector,
                    velocity_vector,
                ]
            ]
        )

    def lorentz_particle_comparison(
        self, charge=1.0, velocity=2.0, B_strength=1.2, angle_degrees=45
    ):
        # -------- PARAMETERS (adjust here) --------

        # -------- SETUP --------
        angle = angle_degrees * DEGREES  # Convert to radians
        force = charge * velocity * B_strength  # * sin(90)

        # -------- MAGNETIC FIELD --------
        B_field = (
            VGroup(*[Text("×", font_size=24) for _ in range(30)])
            .arrange_in_grid(5, 6, buff=0.7)
            .shift(RIGHT * 2)
        )
        B_field.set_color(BLUE)

        # -------- PARTICLE --------
        # needs to be right by one radius of circle
        particle = Dot(color=RED if charge > 0 else BLUE).center()

        # -------- LABELS --------
        B_label = (
            Tex(r"$\vec{B}$").set_color(BLUE).next_to(B_field, UP, buff=0.2)
        )  # B vector above field
        q_label = Tex(f"q = {charge} e").set_color(RED if charge > 0 else BLUE)
        v_label = Tex(r"$v = " + str(velocity) + r"\,\mathrm{\frac{m}{s}}$").set_color(
            GREEN
        )

        # Label positioning
        q_label.to_corner(UL)
        v_label.next_to(q_label, DOWN)

        def get_B_field_bounds(B_field):
            """Get the bounds (left, right, top, bottom) of the B_field."""
            left = B_field.get_left()[0]  # x-coordinate of the leftmost point
            right = B_field.get_right()[0]  # x-coordinate of the rightmost point
            top = B_field.get_top()[1]  # y-coordinate of the topmost point
            bottom = B_field.get_bottom()[1]  # y-coordinate of the bottommost point
            return left, right, top, bottom

        field_bounds = get_B_field_bounds(B_field)
        field_center = np.array(
            [
                abs(field_bounds[1] + field_bounds[0]) / 2,
                abs(field_bounds[2] + field_bounds[3]) / 2,
                0,
            ]
        )
        # spawns center of b_field
        radius = abs(velocity * charge / B_strength)
        circle = Circle(radius=radius, color=YELLOW).move_to(field_center)
        # circle.rotate(-angle, about_point=center_offset)
        circle.set_stroke(opacity=0.3)

        # -------- TRAJECTORY CALCULATION --------
        # circle center needs to be in field
        center_offset = field_center + radius * np.array(
            [-np.sin(angle), np.cos(angle), 0]
        )
        particle.move_to(field_center).shift(RIGHT * radius)
        # particle2.move_to(-field_center)

        # Time for exactly one rotation
        omega = velocity / radius  # Angular frequency
        t_max = 2 * np.pi / omega  # Time for one full rotation

        # -------- FORCE VECTOR --------
        # Scaling factors
        force_scale = 0.5
        velocity_scale = 0.5

        # Standard values for all arrows
        arrow_kwargs = {
            "tip_length": 0.4,  # Same tip size for all arrows
            "max_tip_length_to_length_ratio": 0.4,
        }

        force_vector = Arrow(start=ORIGIN, end=RIGHT, color=RED, **arrow_kwargs)

        velocity_vector = Arrow(start=ORIGIN, end=RIGHT, color=GREEN, **arrow_kwargs)

        def update_force_vector(arrow):
            # Calculate new start and end points
            start = particle.get_center()
            direction = center_offset - start
            direction = direction / np.linalg.norm(direction) * force * force_scale
            # Update existing arrow
            arrow.put_start_and_end_on(start, start + direction)

        def update_velocity_vector(arrow):
            # Calculate new start and end points
            start = particle.get_center()
            # Vector from circle center to particle
            radial = start - center_offset
            # Tangential vector (90° rotation)
            tangent = np.array([-radial[1], radial[0], 0])
            # Normalize and scale
            tangent = tangent / np.linalg.norm(tangent) * velocity * velocity_scale
            # Update existing arrow
            arrow.put_start_and_end_on(start, start + tangent)

        # Füge den Updater hinzu
        force_vector.add_updater(update_force_vector)
        velocity_vector.add_updater(update_velocity_vector)
        circle_circumference = radius * 2 * PI

        particle2 = (
            Dot(color=RED if charge > 0 else BLUE)
            .shift((circle_circumference / 4) * DOWN)
            .shift(LEFT * 4)
        )
        end2 = Dot().shift(circle_circumference / 2 * UP).shift(LEFT * 4)
        rate = lambda t: min(max(3 * t - 1, 0), 1)
        path2 = Line(start=particle2.get_center(), end=end2.get_center())

        # -------- ANIMATION --------

        self.play(
            FadeIn(particle2),
            FadeIn(B_field),
            FadeIn(particle),
            FadeIn(velocity_vector, rate_func=rate),
        )
        self.wait()

        self.play(
            MoveAlongPath(particle, circle),
            MoveAlongPath(particle2, path2),
            FadeIn(circle, rate_func=rate),
            FadeIn(force_vector, rate_func=rate),
            rate_func=linear,
            run_time=t_max,
        )
        self.wait()

        # Aufräumen
        self.play(
            *[
                FadeOut(mob)
                for mob in [
                    B_field,
                    # B_label,
                    particle,
                    # q_label,
                    # v_label,
                    circle,
                    # force_vector,
                    velocity_vector,
                ]
            ]
        )

    def particle_deflection(self, velocity=1, field_strength=0.5, number_of_objects=1):
        # used for smoother movements
        oversampling = max(1, int(100 / config.frame_rate))
        height, width = 3, 3
        number_of_objects = 5
        field = Rectangle(height=height, width=width)
        magnet_field = VGroup(
            *[Text("×", font_size=24) for _ in range(width * height * 4)]
        ).arrange_in_grid(height * 2, width * 2, buff=0.35)
        magnet_field.set_color(BLUE)
        dots = VGroup()
        speeds = [0.5 + a / 2 for a in range(number_of_objects)]
        for idx in range(number_of_objects):
            dot = Dot(
                point=[-3, field.get_center()[1] - 1, 0],
                color=RED,
            )
            # dot velocity
            dot.v = np.array([np.random.uniform(0.5, 2), 0, 0])

            def dotupdater(mobj, dt):
                if dt > 0:
                    ddt = dt / oversampling
                    for _ in range(oversampling):
                        p = mobj.get_center()
                        if (field.get_left()[0] < p[0] < field.get_right()[0]) and (
                            field.get_bottom()[1] < p[1] < field.get_top()[1]
                        ):
                            mobj.v += (
                                field_strength
                                * ddt
                                * np.matmul(
                                    np.array([[0, -1, 0], [1, 0, 0], [0, 0, 0]]), mobj.v
                                )
                            )
                        mobj.shift(ddt * mobj.v)

            dot.add_updater(dotupdater)
            dots += dot
        traces = VGroup(
            *[TracedPath(dot.get_center, stroke_color=dot.get_color()) for dot in dots]
        )
        self.add(magnet_field, field)
        self.wait(3)
        self.add(dots, traces)
        self.wait(10)


class Testing(ThreeDScene):
    def construct(self):
        # self.lorentz_particle_comparison(velocity=1.5)
        self.particle_deflection()

    def particle_deflection(self, velocity=1, field_strength=0.5, number_of_objects=1):
        # used for smoother movements
        oversampling = max(1, int(100 / config.frame_rate))
        height, width = 3, 3
        number_of_objects = 5
        field = Rectangle(height=height, width=width)
        magnet_field = VGroup(
            *[Text("×", font_size=24) for _ in range(width * height * 4)]
        ).arrange_in_grid(height * 2, width * 2, buff=0.35)
        magnet_field.set_color(BLUE)
        dots = VGroup()
        speeds = [0.5 + a / 2 for a in range(number_of_objects)]
        for idx in range(number_of_objects):
            dot = Dot(
                point=[-3, field.get_center()[1] - 1, 0],
                color=RED,
            )
            # dot velocity
            dot.v = np.array([np.random.uniform(0.5, 2), 0, 0])

            def dotupdater(mobj, dt):
                if dt > 0:
                    ddt = dt / oversampling
                    for _ in range(oversampling):
                        p = mobj.get_center()
                        if (field.get_left()[0] < p[0] < field.get_right()[0]) and (
                            field.get_bottom()[1] < p[1] < field.get_top()[1]
                        ):
                            mobj.v += (
                                field_strength
                                * ddt
                                * np.matmul(
                                    np.array([[0, -1, 0], [1, 0, 0], [0, 0, 0]]), mobj.v
                                )
                            )
                        mobj.shift(ddt * mobj.v)

            dot.add_updater(dotupdater)
            dots += dot
        traces = VGroup(
            *[TracedPath(dot.get_center, stroke_color=dot.get_color()) for dot in dots]
        )
        self.add(magnet_field, field)
        self.wait(3)
        self.add(dots, traces)

        # self.set_camera_orientation(phi=55 * DEGREES, theta=-45 * DEGREES)
        self.wait(5)
