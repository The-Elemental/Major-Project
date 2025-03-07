from framework.BehaviourNode import BehaviourNode
from framework.Location import Location
from framework.NPC import NPC
from py2neo import Graph
import chromadb
import random

class World:
    """World object"""
    
    def __init__(self):
        # Initialise Graph
        self.graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
        
        # Initialise Database
        self.database = chromadb.Client().create_collection("npc_memory")
        
        # Values
        self.npcs = []
        self.locations = []
        
        # Location Generation
        location_id = 0
        start = Location("Start", location_id)
        location_id += 1
        self.locations.append(start)
        
        main_street = Location("Main Street", location_id)
        location_id += 1
        main_street.add_connection(start, 5)
        self.locations.append(main_street)
        
        work = Location("Work", location_id)
        location_id += 1
        work.add_connection(main_street, 5)
        self.locations.append(work)
        
        # NPC Generation
        for i in range(0, 30):
            new_npc = NPC("Name", 
                          round(random.uniform(0, 1), 1), 
                          round(random.uniform(0, 1), 1), 
                          round(random.uniform(0, 1), 1), 
                          round(random.uniform(0, 1), 1), 
                          round(random.uniform(0, 1), 1), 
                          round(random.uniform(0, 1), 1), 
                          i,
                          self.graph)
            self.npcs.append(new_npc)
        
        for i in range(0, 30):
            new_npc_house = Location(f"House {i}", location_id + i)
            self.npcs[i].move_to(new_npc_house)
            new_npc_house.add_connection(main_street, 5)
            self.locations.append(new_npc_house)
            
    def new_location(self, name, nodes):
        id = len(self.locations)
        new_location = Location(name, id, nodes)
        self.locations.append(new_location)
        return id
    
    def new_npc(self, name,  honesty, emotionality, extroversion, agreeableness, conscientiousness, openness):
        id = len(self.npcs)
        new_npc = NPC(name,  honesty, emotionality, extroversion, agreeableness, conscientiousness, openness, id, self.graph)
        self.npcs.append(new_npc)
        return id
    
    def next(self, current_time):
        for npc in self.npcs:
            npc.next(current_time)
        
    def get_start(self):
        return self.locations[0]