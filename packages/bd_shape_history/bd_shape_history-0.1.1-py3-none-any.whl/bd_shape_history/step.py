import json
from typing import List, Self

from ocp_tessellate import convert

from .types import Part, Shape, Face, Edge

COLOR_FACE_DEFAULT = 'Gray'
COLOR_FACE_ADDED = 'Green'
COLOR_FACE_MODIFIED = 'DarkOliveGreen'

COLOR_EDGE_DEFAULT = 'Black'
COLOR_EDGE_ADDED = 'LimeGreen'
COLOR_EDGE_MODIFIED = 'Olive'

TESSELATION_TOLERANCE = 0.1
FLOAT_MULTIPLIER = 1000


class Step:
    def __init__(self, label: str, obj: Part, tesselate_hash=False) -> None:
        self.label = label
        self.object = obj
        self.tesselate_hash = tesselate_hash

        self.faces = {self.get_id(f): f for f in obj.faces()}
        self.edges = {self.get_id(e): e for e in obj.edges()}
        self.vertices = {self.get_id(v): v for v in obj.vertices()}

        Step.labelise({**self.faces, **self.edges, **self.vertices})

    @staticmethod
    def labelise(shapes_dict):
        for shape_label, shape in shapes_dict.items():
            shape.label = shape_label

    def hash(self, shape) -> int:
        if not self.tesselate_hash:
            return hash(shape)

        shapes = convert.tessellate_group(*convert.to_ocpgroup(shape))[1]
        d = convert.numpy_to_buffer_json(shapes)
        return hash(json.dumps(d))

    def get_id(self, shape: Shape) -> str:
        return hex(self.hash(shape))[2:]

    def get_faces(self) -> List[Face]:
        return list(self.faces.values())

    def get_edges(self) -> List[Edge]:
        return list(self.edges.values())

    def get_faces_and_edges(self) -> List[Edge|Face]:
        return self.get_faces() + self.get_edges()

    def is_very_new_face(self, step: Self, face: Face) -> bool:
        for edge in face.edges():
            if self.get_id(edge) in step.edges:
                return False
        return True

    def is_very_new_edge(self, step: Self, edge: Edge):
        for vertex in edge.vertices():
            if self.get_id(vertex) in step.vertices:
                return False
        return True

    def colorize_faces_diff(self, that_step: Self|None) -> None:
        for face_label, face in self.faces.items():
            if not that_step:
                face.color = COLOR_FACE_ADDED
            elif face_label in that_step.faces:
                face.color = COLOR_FACE_DEFAULT
            elif self.is_very_new_face(that_step, face):
                face.color = COLOR_FACE_ADDED
            else:
                face.color = COLOR_FACE_MODIFIED

    def colorize_edges_diff(self, that_step: Self|None) -> None:
        for edge_label, edge in self.edges.items():
            if not that_step:
                edge.color = COLOR_EDGE_ADDED
            elif edge_label in that_step.edges:
                edge.color = COLOR_EDGE_DEFAULT
            elif self.is_very_new_edge(that_step, edge):
                edge.color = COLOR_EDGE_ADDED
            else:
                edge.color = COLOR_EDGE_MODIFIED
