from framework.NPC import NPC
from datetime import time
class Location:
    """Base object for all locations"""
    
    def __init__(self, name:str, id:int, nodes:set=set()):
        self.name = name
        self.id = id
        self.nodes = nodes
        self.connections={}
        self.npcs = set()
        
    def add_connection(self, location:"Location", distance:int):
        self.connections[location] = distance
        location.connections[self] = distance

    def get_best_node(self, required_tags:set, npc:NPC, current_time:time):
        node_val = {}
        for x in self.nodes:
            node_val = {}
            if required_tags.issubset(x.tags) and current_time.weekday() in x.active_days and x.start_time <= current_time.time() <= x.end_time:
                # Calculate how the current node would affect the NPC's mood
                mood_change = x.get_change(npc)
                
                # Define which moods are considered positive and negative
                positive_emotions = {'happiness', 'love', 'pride', 'surprise'}
                negative_emotions = {'stress', 'anger', 'fear', 'disgust', 'jealousy', 'guilt', 'fatigue', 'sadness', 'anxiety'}

                # Initialize the overall behavior value
                overall_value = 0

                # Iterate through the mood_change dictionary
                for emotion, change_value in mood_change.items():
                    if emotion in positive_emotions:
                        overall_value += change_value  # Add for positive emotions
                    elif emotion in negative_emotions:
                        overall_value -= change_value  # Subtract for negative emotions
                        
                node_val[x] = overall_value
                
        return max(node_val, key=node_val.get)
        
    def __repr__(self):
        return f"Location({self.name}, NPCs: {[npc.name for npc in self.npcs]})"