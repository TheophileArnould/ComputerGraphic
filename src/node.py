from glm import identity, mat4

class Node:
    """ Scene graph node """
    def __init__(self, children=(), transform=identity(mat4)):
        self.transform = transform
        self.children = list(iter(children))

    def add(self, *drawables):
        """ Add drawables to this node, simply updating children list """
        self.children.extend(drawables)

    def draw(self, model, view, projection):
        """ Recursive draw, passing down updated model matrix. """
        for child in self.children:
            child.draw(model @ self.transform, view, projection)

    def key_handler(self, key):
        """ Dispatch keyboard events to children with key handler """
        for child in (c for c in self.children if hasattr(c, 'key_handler')):
            child.key_handler(key)