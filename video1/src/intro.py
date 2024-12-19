import manim as m
import manim_physics as p


class MagneticFieldExmaple(m.Scene):
    def construct(self):
        # Load the image (use the image file name or full path)
        image = m.ImageMobject(
            "../bar-magnet-icon-n-pole-and-s-pole-magnets-png-3540789338.png"
        )
        image.rotate(-1 * (m.PI / 4))

        # Resize the image (optional)
        image.scale(0.4)  # Adjust the scale factor as needed

        # Position the image (optional)
        image.to_edge(m.UP)  # Moves the image to the top edge of the screen
        image.shift(m.UP * 0.5)

        # Adding the field lines
        wire = p.Wire(m.Circle(1).rotate(m.PI / 2, m.UP), current=4)
        mag_field = p.MagneticField(
            wire,
            x_range=[-10, 10],
            y_range=[-10, 10],
        )
        self.add(mag_field)
        # Add the image to the scene
        self.add(image)

        # Hold the image on screen for 3 seconds
        self.wait(3)


class AttractionRepulsion(m.Scene):
    def construct(self):
        # Create the first wire and position it to the left
        wire1 = p.Wire(m.Circle(radius=1).rotate(m.PI / 2, m.UP), current=4).shift(
            m.LEFT * 3
        )

        # Create the second wire and position it to the right
        wire2 = p.Wire(m.Circle(radius=1).rotate(m.PI / 2, m.UP), current=4).shift(
            m.RIGHT * 3
        )

        # Create the first image and set its properties
        img1 = m.ImageMobject(
            "../bar-magnet-icon-n-pole-and-s-pole-magnets-png-3540789338.png"
        )
        img1.rotate(-m.PI / 4)
        img1.scale(0.4)
        img1.to_edge(m.UP).shift(m.UP * 0.5 + m.RIGHT * 3)

        # Create the second image and set its properties
        img2 = m.ImageMobject(
            "../bar-magnet-icon-n-pole-and-s-pole-magnets-png-3540789338.png"
        )
        img2.rotate(-m.PI / 4)
        img2.scale(0.4)
        img2.to_edge(m.UP).shift(m.UP * 0.5 + m.LEFT * 3)

        # Create the magnetic field for the two wires
        magField = p.MagneticField(
            wire1,
            wire2,
            x_range=[-10, 10],
            y_range=[-10, 10],
        )

        # Add elements to the scene
        self.add(magField, img1, img2)

        # Define an updater function to update the magnetic field dynamically
        def update_field(mob):
            mob.become(
                p.MagneticField(
                    wire1,
                    wire2,
                    x_range=[-10, 10],
                    y_range=[-10, 10],
                )
            )

        magField.add_updater(update_field)

        # Animate the 180-degree rotation of img1 and wire2 simultaneously
        self.play(
            m.AnimationGroup(
                img1.animate.rotate(m.PI / 2),
                wire2.animate.rotate(m.PI / 2),
                lag_ratio=0,
            ),
        )
        self.wait(3)
        self.play(
            m.AnimationGroup(
                img1.animate.rotate(m.PI / 2),
                wire2.animate.rotate(m.PI / 2),
                lag_ratio=0,
            )
        )

        # Wait to display the final state
        self.wait(5)
