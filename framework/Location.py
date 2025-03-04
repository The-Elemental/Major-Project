class Location:
    """Base object for all locations"""
    
    def __init__(self, name, id, nodes=[]):
        self.name = name
        self.id = id
        self.nodes = nodes
        self.connections={}
        self.npcs = []
        
    def add_npc(self, npc):
        """Adds an NPC to this location."""
        self.npcs.append(npc)

    def remove_npc(self, npc):
        """Removes an NPC from this location."""
        if npc in self.npcs:
            self.npcs.remove(npc)
            
    def get_npcs(self):
        return self.npcs
            
    def get_connections(self):
        return self.connections
    
    def add_connection(self, location, distance):
        self.connections[location] = distance

    def __repr__(self):
        return f"Location({self.name}, NPCs: {[npc.name for npc in self.npcs]})"