from framework.Schedule import Schedule
from framework.GraphConnection import GraphConnection
from framework.BehaviourNode import BehaviourNode
from framework.Location import Location
from py2neo import Graph, Node, Relationship

class NPC:
    """Base node for NPC's"""
    
    def __init__(self, name,  honesty, emotionality, extroversion, agreeableness, conscientiousness, openness, id, graph):
        self.graph = graph
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
        node = self.graph.node.get(self.id)
        if node:
            if node['location']:
                node['location'].remove_npc(self)
            new_location.add_npc(self)

    def __repr__(self):
        return f"NPC({self.name}, Location: {self.location.name if self.location else 'None'})"
