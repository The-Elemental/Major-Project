from framework import BehaviourNode
from framework import Location
from framework import NPC
from py2neo import Graph
from datetime import datetime
import chromadb
import random
import sys

class World:
    """World object"""
    
    def __init__(self):
        # Initialise Graph
        try:
            self.graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
            print("✅ Connected to Neo4j successfully!")
        except:
            print("⚠️ Could not connect to Neo4j. Please start the Neo4j database and try again.")
            sys.exit(1)
        
        # Clear Previous Instances
        result = self.graph.run("MATCH (n) RETURN count(n) AS count").data()
        node_count = result[0]["count"] if result else 0
        if node_count > 0:
            print(f"Graph contains {node_count} nodes. Clearing previous session")
            self.graph.run("MATCH (n) DETACH DELETE n")
        
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
                          self.graph,
                          self.database)
            self.npcs.append(new_npc)
        
        for i in range(0, 30):
            new_npc_house = Location(f"House {i}", location_id + i)
            self.npcs[i].move_to(new_npc_house)
            new_npc_house.add_connection(main_street, 5)
            self.locations.append(new_npc_house)
            
    def new_location(self, name:str, nodes:set):
        id = len(self.locations)
        new_location = Location(name, id, nodes)
        self.locations.append(new_location)
        return id
    
    def new_npc(self, name:str, honesty:int, emotionality:int, extroversion:int, agreeableness:int, conscientiousness:int, openness:int):
        id = len(self.npcs)
        new_npc = NPC(name,  honesty, emotionality, extroversion, agreeableness, conscientiousness, openness, id, self.graph, self.database)
        self.npcs.append(new_npc)
        return id
    
    def next(self, current_time:datetime):
        for npc in self.npcs:
            npc.next(current_time)
            
    def exit(self):
        self.graph.run("MATCH (n) DETACH DELETE n")
        
    def get_start(self):
        return self.locations[0]