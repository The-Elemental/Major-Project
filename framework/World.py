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
        self.NPCs = []
        self.locations = []
        
        # Location Generation
        start = Location("Start", 32)
        self.locations.append(start)
        
        main_street = Location("Main Street", 30)
        main_street.add_connection(start, 5)
        self.locations.append(main_street)
        
        work = Location("Work", 31)
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
            #testing location
            new_npc.move_to(start)
            self.NPCs.append(new_npc)
        
        for i in range(0, 30):
            new_npc_house = Location(f"House {i}", i)
            new_npc_house.add_connection(main_street, 5)
            self.locations.append(new_npc_house)
            
    def get_start(self):
        return self.locations[0]