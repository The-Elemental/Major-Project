from py2neo import Graph, Node, Relationship
class GraphConnection:
    """Centralized Graph Connection Singleton"""
    def __init__(self):
        # This is where the graph connection is initialized.
        self.graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

    def get_graph(self):
        return self.graph