from build123d import (
    BuildPart,
    Cylinder,
    Locations,
    Location,
    Pos,
    Rot,
    Circle,
    Axis,
    Sphere,
    Part,
    Compound,
    ExportSVG,
    LineType,
    Mesher,
)
from build123d import export_stl, revolve, export_gltf
from math import cos, sin, radians
from dataclasses import dataclass


@dataclass
class BearingConfig:
    number_of_balls: int = 8
    circle_radius: float = 20
    ball_diameter: float = 4.1
    thickness: float = 4


class BearingBuilder:
    def __init__(self, config: BearingConfig):
        self.config = config
        self.balls = None
        self.ball_track_ring = None
        self.top_track = None
        self.bottom_track = None
        self.center_wheel = None
        self.outer_wheel = None

    def build_balls(self):
        # place balls in a circle based on the number of balls and
        # the diameter of the circle_radius
        with BuildPart() as balls:
            for i in range(self.config.number_of_balls):
                angle = radians(i * 360 / self.config.number_of_balls)
                x = self.config.circle_radius * cos(angle)
                y = self.config.circle_radius * sin(angle)
                with Locations((x, y, 0)):
                    Sphere(radius=self.config.ball_diameter / 2)
        self.balls = balls.part
        return self

    def build_segments(self):
        # segments are the negative that the balls could roll within
        # there are 1 segment every 2 balls and they can be thought of as
        # pill shaped segments of a torus
        segments = Part()
        ball_sketch = Pos(0, self.config.circle_radius, 0) * Circle(
            self.config.ball_diameter / 2
        )
        deg = 360 / self.config.number_of_balls

        for i in range(self.config.number_of_balls):
            if i % 2 != 0:
                bearing = Rot(0, 0, i * deg) * (
                    Rot(0, 90)
                    * revolve(axis=Axis.X, profiles=ball_sketch, revolution_arc=deg)
                )
                segments += bearing

        self.ball_track_ring = segments + self.balls
        return self

    def build_tracks(self):
        # tracks are the positive space around the segments, and are the wells in which the balls roll
        outer_circle = Cylinder(self.config.circle_radius + 1.25, self.config.thickness)
        inner_circle = Cylinder(self.config.circle_radius - 1.25, self.config.thickness)
        outer_circle_part = outer_circle - inner_circle

        full_track = (Location((0, 0, 1)) * outer_circle_part) - self.ball_track_ring

        self.top_track = full_track
        self.bottom_track = Rot(0, 180, 180) * full_track
        return self

    def build_wheels(self):
        # build ball well. we have a single negative space torus that represents the
        # full area the balls could travel in. This is used to subtract from the inner and
        # outer wheels to create the wells for the balls
        ball_well = Pos(0, self.config.circle_radius, 0) * Circle(
            self.config.ball_diameter / 2
        )
        ball_well_donut = Rot(0, 0, 0) * (
            Rot(0, 90) * revolve(axis=Axis.X, profiles=ball_well, revolution_arc=360)
        )

        # build center wheel
        self.center_wheel = (
            Cylinder(self.config.circle_radius - 1.5, self.config.thickness + 2)
            - ball_well_donut
        )

        # build outer wheel
        self.outer_wheel = (
            Cylinder(self.config.circle_radius + 1.5 + 2, self.config.thickness + 2)
            - Cylinder(self.config.circle_radius + 1.5, self.config.thickness + 2)
            - ball_well_donut
        )
        return self

    def export_stl(self, directory="out"):
        export_stl(self.outer_wheel, f"{directory}/outer_wheel.stl")
        export_stl(self.center_wheel, f"{directory}/center_wheel.stl")
        export_stl(self.top_track, f"{directory}/top_track.stl")
        export_stl(self.bottom_track, f"{directory}/bottom_track.stl")
        return self

    def export_gtlf(self, directory="out"):
        # combine all parts into a single part
        bearing = (
            self.top_track + self.bottom_track + self.center_wheel + self.outer_wheel
        )
        export_gltf(bearing, f"{directory}/bearing.gltf")
        return self

    def export_svg(self, directory="out"):
        view_port_origin = (-100, -50, 30)
        bearing = (
            self.top_track + self.bottom_track + self.center_wheel + self.outer_wheel
        )
        visible, hidden = bearing.project_to_viewport(view_port_origin)
        max_dimension = max(*Compound(children=visible + hidden).bounding_box().size)
        exporter = ExportSVG(scale=100 / max_dimension)
        exporter.add_layer("Visible")
        exporter.add_layer(
            "Hidden", line_color=(99, 99, 99), line_type=LineType.ISO_DOT
        )
        exporter.add_shape(visible, layer="Visible")
        exporter.add_shape(hidden, layer="Hidden")
        exporter.write("bearing.svg")
        return self

    def export_3mf(self, directory="out"):
        exporter = Mesher()

        # Improve the layout of the parts in the 3mf file
        # - move top track 50mm on the x axis and flip 180 degrees to avoid floating parts
        # - move bottom track 50mm on the x axis
        # - move outer wheel 50mm on both x and y axis
        # - center stays in origin
        top_track = Location((0, 50, 0)) * Rot(0, 180, 0) * self.top_track
        bottom_track = Location((50, 0, 0)) * self.bottom_track
        outer_wheel = Location((50, 50, 0)) * self.outer_wheel

        exporter.add_shape(top_track, part_number="top_track")
        exporter.add_shape(bottom_track, part_number="bottom_track")
        exporter.add_shape(self.center_wheel, part_number="center_wheel")
        exporter.add_shape(outer_wheel, part_number="outer_wheel")
        exporter.add_code_to_metadata()
        exporter.write("example.3mf")
        return self

    def build(self):
        return self.build_balls().build_segments().build_tracks().build_wheels()
