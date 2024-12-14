try:

    import build123d as bd

    Part = bd.Part
    Shape = bd.Shape
    Edge = bd.Edge
    Face = bd.Face
    Vertex = bd.Vertex

except ImportError:

    Part = object
    Shape = object
    Edge = object
    Face = object
    Vertex = object
