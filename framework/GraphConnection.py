from py2neo import Graph

class GraphConnection:
    """Centralized Graph Connection Singleton"""

    # Store the graph connection at the class level
    _graph = None

    @staticmethod
    def get_graph():
        # Initialize the graph connection only if it's not already created
        if GraphConnection._graph is None:
            GraphConnection._graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
        return GraphConnection._graph
