class Location:
    """Base object for all locations"""
    
    def __init__(self, name, id, nodes=[]):
        self.name = name
        self.id = id
        self.nodes = nodes
        self.connections={}
        self.npcs = []
        
    def add_connection(self, location, distance):
        self.connections[location] = distance
        location.connections[self] = distance

    def get_best_node(self, required_tags, npc):
        ## DO THE LOGIC FOR DETERMINING THE MOST VALUIEABLE NODE
        return "best_node"
        
    def __repr__(self):
        return f"Location({self.name}, NPCs: {[npc.name for npc in self.npcs]})"