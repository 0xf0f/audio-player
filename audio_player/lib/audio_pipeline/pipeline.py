from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .pipeline_node import PipelineNode


class Pipeline:
    def __init__(self):
        self.nodes: List['PipelineNode'] = []

    def start(self):
        for node in self.nodes:
            node.start()

    # def add_node(self, node: 'PipelineNodeV2'):
    #     self.nodes.append(node)
    #     return node

    def add_node(self, node: 'PipelineNode', parent: 'PipelineNode'=None):
        if parent:
            parent.output.connect(node.input)

        elif self.nodes:
            self.nodes[-1].output.connect(node.input)

        self.nodes.append(node)
        return node

    def input(self, item):
        self.nodes[0].input(item)

    def __call__(self, item):
        self.nodes[0].input(item)

    def wait(self):
        for node in self.nodes:
            node.wait()
