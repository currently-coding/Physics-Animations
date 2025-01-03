import manim as m
import manim_physics as p


class MagneticFieldExmaple(m.Scene):
    def bar_magnet_field_lines(self):
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

        north = (
            m.Rectangle(m.BLACK, height=0.8, width=1.5)
            .shift(m.LEFT * 0.5)
            .set_fill(m.GREEN, opacity=100)
        )
        south = m.Rectangle(m.BLACK, height=0.8, width=1.5).set_fill(m.RED, opacity=100)
        south.next_to(north, buff=0)

        # Adding the field lines
        wire1 = p.Wire(m.Circle(1).rotate(m.PI / 2, m.UP), current=2).shift(
            m.RIGHT * 0.41
        )
        wire5 = p.Wire(m.Circle(1).rotate(m.PI / 2, m.UP), current=2).shift(
            m.RIGHT * 0.2
        )
        wire2 = p.Wire(m.Circle(1).rotate(m.PI / 2, m.UP), current=2).shift(
            m.LEFT * 0.41
        )
        wire4 = p.Wire(m.Circle(1).rotate(m.PI / 2, m.UP), current=2).shift(
            m.LEFT * 0.2
        )
        wire3 = p.Wire(m.Circle(1).rotate(m.PI / 2, m.UP), current=2)
        wires = [wire1, wire2, wire3, wire4, wire5]
        mag_field = p.MagneticField(
            *wires,
            x_range=[-10, 10],
            y_range=[-10, 10],
        )
        self.add(mag_field)
        # Add the image to the scene
        self.add(image)
        self.add(south, north)
        return (image, mag_field)

    def construct(self):
        self.add(*self.bar_magnet_field_lines())
