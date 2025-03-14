from framework import Schedule
from framework import Location
from py2neo import Node, Relationship
from datetime import datetime
import sys

class NPC:
    """Base node for NPC's"""
    
    def __init__(self, name:str, honesty:int, emotionality:int, extroversion:int, agreeableness:int, conscientiousness:int, openness:int, id:int, graph, database):
        self.graph = graph
        self.database = database
        self.name = name
        self.id = id
        self.schedule = Schedule()
        self.activity = None
        self.event = None
        self.location = None
        
        # NPC information
        npc_node = Node("NPC",
            name=name,
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
            anxiety=0,
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
        
    def move_to(self, new_location:Location):
        """Moves NPC to a new location."""
        if self.location:
            self.location.npcs.remove(self)
        self.location = new_location
        self.location.npcs.append(self)
            
    def meet(self, npc:"NPC", value:int):
        self_node = self.graph.match("NPC", id=self.id).first()
        npc_node = self.graph.match("NPC", id=npc.id).first()
        relationship = Relationship(self_node, "KNOWS", npc_node, known_by=[self.id, npc.id], value=value)
        self.graph.create(relationship)
        
    def knows(self, npc1:"NPC", npc2:"NPC"):
        npc1_node = self.graph.nodes.match("NPC", id=npc1.id).first()
        npc2_node = self.graph.nodes.match("NPC", id=npc2.id).first()
        
        relationship = self.graph.match((npc1_node, npc2_node), "KNOWS").first()
        
        if self.id not in relationship["known_by"]:
            relationship["known_by"].append(self.id)
            self.graph.push(relationship)
            
    def next(self, current_time:datetime):
        if self.activity:
            metadata = {
                "npc_id": self.id,
                "npc_name": self.name,
                "type": "activity"
            }
            
            query = """
            MATCH (npc:NPC)-[:HAS_MOOD]->(mood:Mood)
            WHERE npc.id = $npc_id
            RETURN mood
            """
            result = self.graph.run(query, npc_id=self.id).data()
            mood_values = result[0]['mood']
            
            document = {
                "activity_id": self.activity.id,
                "location_id": self.location.id,
                "timestamp": int(current_time.timestamp()),
                "mood": mood_values
            }
            self.database.add(
                documents=document,
                metadata=metadata
            )
            
        self.event = self.schedule.next(current_time)
        if self.event:
            self.location = self.event.location
            if self.event.behaviour_tag:
                self.activity = self.location.get_best_node(self.event.behaviour_tag, self, current_time)
            elif self.event.behaviour_node:
                self.activity = self.event.behaviour_node
            else:
                print("Error, exiting")
                sys.exit(1)
        
        mood_change = self.activity.get_change(self)
        for key, value in mood_change.items():
            self.mood[key] = max(0, min(100, self.mood[key] + value))

    def __repr__(self):
        return f"NPC({self.name}, Location: {self.location.name if self.location else 'None'})"
