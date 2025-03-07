from framework.Schedule import Schedule
from py2neo import Node, Relationship

class NPC:
    """Base node for NPC's"""
    
    def __init__(self, name,  honesty, emotionality, extroversion, agreeableness, conscientiousness, openness, id, graph):
        self.graph = graph
        self.name = name
        self.id = id
        self.schedule = Schedule()
        self.activity = None
        self.location = None
        
        # NPC information
        npc_node = Node("NPC",
            name=name,
            location_id=None,
            activity_id=None,
            id=id
        )
        
        # Hexaco System
        hexaco_node = Node("Hexaco", 
            honesty=honesty, 
            emotionality=emotionality, 
            extroversion=extroversion, 
            agreeableness=agreeableness, 
            conscientiousness=conscientiousness, 
            openness=openness
        )
        
        # Mood
        mood_node = Node("Mood", 
            happiness=0,
            sadness=0, 
            anger=0,
            fear=0, 
            disgust=0, 
            surprise=0, 
            love=0,
            jealousy=0, 
            guilt=0, 
            pride=0, 
            stress=0,
            fatigue=0
        )
        
        # Create relationships between NPC and Hexaco/Mood nodes
        hexaco_rel = Relationship(npc_node, "HAS_HEXACO", hexaco_node)
        mood_rel = Relationship(npc_node, "HAS_MOOD", mood_node)
        
        # Add nodes and relationships to the graph
        self.graph.create(npc_node)
        self.graph.create(hexaco_node)
        self.graph.create(mood_node)
        self.graph.create(hexaco_rel)
        self.graph.create(mood_rel)
        
    def move_to(self, new_location):
        """Moves NPC to a new location."""
        if self.location:
            self.location.npcs.remove(self)
        self.location = new_location
        self.location.npcs.append(self)
            
    def meet(self, npc, value):
        self_node = self.graph.match("NPC", id=self.id).first()
        npc_node = self.graph.match("NPC", id=npc.id).first()
        relationship = Relationship(self_node, "KNOWS", npc_node, known_by=[self.id, npc.id], value=value)
        self.graph.create(relationship)
        
    def knows(self, npc1, npc2):
        npc1_node = self.graph.nodes.match("NPC", id=npc1.id).first()
        npc2_node = self.graph.nodes.match("NPC", id=npc2.id).first()
        
        relationship = self.graph.match((npc1_node, npc2_node), "KNOWS").first()
        
        if self.id not in relationship["known_by"]:
            relationship["known_by"].append(self.id)
            self.graph.push(relationship)
            
    def next(self, current_time):
        self.schedule.next(current_time)

    def __repr__(self):
        return f"NPC({self.name}, Location: {self.location.name if self.location else 'None'})"
