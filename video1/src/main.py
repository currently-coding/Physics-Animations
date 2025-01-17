from manim_physics import (
    Wire,
    MagneticField,
)
from manim import (
    TracedPath,
    GrowArrow,
    Rectangle,
    BLACK,
    GREEN,
    RED,
    BLUE,
    ImageMobject,
    Scene,
    Text,
    MathTex,
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
    ORIGIN,
    Arrow,
    Transform,
    Dot,
    MoveAlongPath,
    DEGREES,
    YELLOW,
    linear,
    Circle,
    PI,
)
import numpy as np


class LorentzKraftVideo(Scene):
    def construct(self):
        # Titel der Präsentation
        title = Text("Die Lorentzkraft", font_size=72)
        subtitle = Text("erklärt am magnetohydrodynamischen Antrieb", font_size=36)
        subtitle.next_to(title, DOWN)

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
            (r"\vec{F}_L", YELLOW),
        ]:
            lorentz_eqn.set_color_by_tex(tex, color)

        # Gruppierung
        definition_group = VGroup(definition_header, definition_text, lorentz_eqn)
        definition_group.move_to(ORIGIN)

        #
        #
        #
        #
        #
        #
        #
        # ---- Aufbau ----
        #
        # INITIAL wait
        self.wait(40)  # end at 0:40
        # Hier Magnet einleitung
        self.bar_magnet_field_lines()  # end at 1:04
        self.wait(4)  # til 1:08

        # Hier lorentz_particle_comparison() zeigen und definieren
        self.particle_deflection(
            velocity=2, initial_wait=1, animation_time=4
        )  # start at 1:11
        self.particle_deflection(initial_wait=2, animation_time=8)
        self.play(Write(definition_group))  # start at 1:26
        self.wait(34)
        self.play(FadeOut(definition_group))  # end at 2:00
        
        self.properties()  # start at 2:00
        self.wait(2)  # wait before animation
        #
        self.lorentz_particle(velocity=1)
        self.lorentz_particle(velocity=2)
        self.wait()  # til 3:10
        # #
        # # Hier 3-Finger Regel zeigen
        # #
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

        F_vector = Vector(2.5 * LEFT + 1 * DOWN).set_color(YELLOW)
        F_label = (
            Tex(r"$\vec{F}_L$")
            .move_to(F_vector.get_end())
            .shift(DL * 0.5)
            .set_color(YELLOW)
        )

        self.play(Write(hand))
        self.wait(2)  # til 3:13
        self.play(Write(v_vector), Write(B_vector))
        self.play(FadeIn(v_label, B_label))
        self.wait(15)  # til 3:28
        self.play(Write(F_vector))
        self.play(FadeIn(F_label))
        self.wait(7)  # til 3:35
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
        self.wait(3)  # til 3:40
        self.explain_picture()
        self.wait(5)

    def bar_magnet_field_lines(self):
        # Load the image (use the image file name or full path)
        image = ImageMobject(
            "../bar-magnet-icon-n-pole-and-s-pole-magnets-png-3540789338.png"
        )
        image.rotate(-1 * (PI / 4))

        # Resize the image (optional)
        image.scale(0.47)  # Adjust the scale factor as needed

        # Position the image (optional)
        image.move_to(ORIGIN)

        north = (
            Rectangle(BLACK, height=0.8, width=1.5)
            .shift(LEFT * 0.5)
            .set_fill(GREEN, opacity=100)
        )
        south = Rectangle(BLACK, height=0.8, width=1.5).set_fill(RED, opacity=100)
        south.next_to(north, buff=0)

        # Adding the field lines
        wire3 = Wire(Circle(1).rotate(PI / 2, UP), current=7).shift(LEFT * 0.0001)
        mag_field = MagneticField(
            wire3,
            x_range=[-10, 10],
            y_range=[-10, 10],
        )
        self.add(image)  # 0:37
        self.wait(8)  # til 0.45
        # swap image to front and mag field to back
        self.remove(image)
        self.add(mag_field)
        self.add(image)  # til 1:09
        self.wait(24)
        self.remove(mag_field, image)

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
        center = particle
        center_offset = ORIGIN  # fixed a so-called bug utilizing advanced linear algebra and vector calculus

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

        force_vector = Arrow(start=ORIGIN, end=RIGHT, color=YELLOW, **arrow_kwargs)

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

    def particle_deflection(
        self,
        velocity=1,
        field_strength=0.5,
        number_of_objects=1,
        initial_wait=0,
        animation_time=10,
    ):
        # used for smoother movements
        oversampling = max(1, int(100 / config.frame_rate))
        text = MathTex("v = ", velocity, r"\frac{m}{s}").to_edge(UP).shift(DOWN * 0.5)
        height, width = 3, 3
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
            dot.v = np.array([np.random.uniform(velocity, velocity + 0.1), 0, 0])

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
        self.wait(initial_wait)
        self.add(text)
        self.wait(0.5)
        self.add(dots, traces)
        self.wait(animation_time)
        self.remove(magnet_field, dots, traces, field, text)

    def properties(self):
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
            (r"\vec{F}_L", YELLOW),
        ]:
            eqn.set_color_by_tex(tex, color)

        # self.play(Write(eqn)) # i think this is the orphan formula

        # Mathematical derivation
        eqn1 = (
            MathTex(r"F_L", r"=", r"q", r"v", r"B", r"\sin(\alpha)")
            .scale(1.2)
            .to_edge(UP, buff=1)
        )  # Reduced buffer to move everything up

        # Color coding for equation
        for tex, color in [(r"v", GREEN), (r"B", BLUE), (r"F_L", YELLOW)]:
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
            "  zum Magnetfeld steht (sin α)",
        ]

        bullet_points = VGroup(
            *[Text(point, font_size=32) for point in points]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        # Position bullet points relative to header
        bullet_points.next_to(header, DOWN, buff=0.5)

        # Aliwgn last line with bullet points
        bullet_points[-1].align_to(bullet_points[-2], LEFT)

        # Group all text elements
        text_group = VGroup(header, bullet_points)

        # Animation sequence
        self.play(Transform(eqn, eqn1))  # at 2:01
        self.wait(9)  # til 2:10
        self.play(Write(text_group))  # at 2:08
        self.wait(3)  # til 2:42
        self.play(FadeOut(eqn), FadeOut(text_group))

    def explain_picture(self):
        # starts at 3:40
        pic1 = "../before_ink.jpg"
        pic2 = "../after_ink.jpg"
        before_ink = ImageMobject(pic1)
        after_ink = ImageMobject(pic2)
        scale_factor = 1
        before_ink.scale(scale_factor)
        after_ink.scale(scale_factor)

        # Define magnet center
        magnet_center = [0, -2.5, 0]

        arrow_length = 1.7
        # Create arrows originating from magnet_center
        velocity_arrow = Arrow(
            start=magnet_center,
            end=magnet_center + np.array([arrow_length, 0, 0]),
            color=YELLOW,
        )  # Right
        field_arrow = Arrow(
            start=magnet_center,
            end=magnet_center + np.array([0, -arrow_length, 0]),
            color=BLUE,
        )  # Up
        current_arrow = Arrow(
            start=magnet_center,
            end=magnet_center + np.array([-0.5, -0.7, arrow_length]),
            color=GREEN,
        )  # Into picture

        # Add elements to the scene
        # starts at 3:40
        self.add(before_ink)
        self.wait()  # til 3:52
        self.play(GrowArrow(field_arrow))
        # self.wait()  # til 3:53
        self.play(GrowArrow(current_arrow))
        self.wait(17)  # til 4:10
        self.play(GrowArrow(velocity_arrow))
        self.wait(21)  # til 4:31

        self.remove(before_ink)
        self.remove(after_ink, velocity_arrow, field_arrow, current_arrow)
        self.add(after_ink)  # at 4:32
        self.wait(3)
