class Node:
    def __init__(self):
        self.children = []
        self.parent: Node = None

    def add_child(self, node):
        self.children.append(node)
        node.parent = self


class PanNode(Node):
    parent: 'PanNode'

    def __init__(self):
        super().__init__()
        self.value = 0

    def final_value(self):
        range_min = -1
        range_max = +1

        parent = self.parent
        while parent:
            if parent.value > 0:
                pass
            parent = parent.parent

        range_length = range_max - range_min
        range_ratio = (self.value + 1)/2

        return range_min + (range_ratio * range_length)