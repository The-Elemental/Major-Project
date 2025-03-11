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
        query = """
        MATCH (npc:NPC {id: $npc_id}) 
        OPTIONAL MATCH (npc)-[:HAS_MOOD]->(mood:Mood)
        OPTIONAL MATCH (npc)-[:HAS_HEXACO]->(hexaco:HEXACO)
        RETURN npc, mood, hexaco
        """
        result = self.graph.run(query, npc_id=npc.id).data()

        if not result:
            print("Error: NPC not found when attempting location.get_best_node()")
            return None
        
        mood = dict(result[0]["mood"]) if result[0]['mood'] else {}
        hexaco = dict(result[0]["hexaco"]) if result[0]['hexaco'] else {}
        
        node_val = {}
        for x in self.nodes:
            node_val = {}
            # first need to calculate the change in current mood
            # then apply weighting and diminishing returns # adding later
            # then the difference in this nodes hexaco and npcs hexaco
            # then use the difference to create additional mood changes
            #   difference mapping:
            #   openness -> ^ stress + ^ fear + ^ anxiety
            #   conscientiousness -> ^ stress + ^ disgust
            #   agreeableness -> ^ anger + ^ stress
            #   emotionality -> ^ sadness + ^ fear + ^ stress + ^ anxiety
            #   extroversion -> ^ stress + ^ anxiety
            #   honesty -> ^ disgust + ^ stress + ^ pride + ^ guilt
            if required_tags.issubset(x.tags) and current_time.weekday() in x.active_days and x.start_time <= current_time.time() <= x.end_time:
                hexaco_difference = {
                    key: (hexaco[key] - behavior_value)  # Calculate the difference
                    for key, behavior_value in x.hexaco.items()
                    if behavior_value != 0  # Skip behavior nodes with value 0
                }
                mood_change = x.mood
                # stress : openess, conscientiousness, agreeableness, emotionality, extroversion, honesty
                stress_change = (hexaco_difference['openness'] * 5) * max(5, mood['stress'])
                stress_change += (hexaco_difference['conscientiousness'] * 5) * max(5, mood['stress'])
                stress_change += (hexaco_difference['agreeableness'] * 5) * max(5, mood['stress'])
                stress_change += (hexaco_difference['emotionality'] * 5) * max(5, mood['stress'])
                stress_change += (hexaco_difference['extroversion'] * 5) * max(5, mood['stress'])
                stress_change += (hexaco_difference['honesty'] * 5) * max(5, mood['stress'])
                mood_change['stress'] += stress_change
                # fear: openness, emotionality, 
                fear_change = (hexaco_difference['openness'] * 5) * max(5, mood['fear'])
                fear_change += (hexaco_difference['emotionality'] * 5) * max(5, mood['fear'])
                mood_change['fear'] += fear_change
                # anxiety: openness, emotionality, extroversion
                anxiety_change = (hexaco_difference['openness'] * 5) * max(5, mood['anxiety'])
                anxiety_change += (hexaco_difference['emotionality'] * 5) * max(5, mood['anxiety'])
                anxiety_change += (hexaco_difference['extroversion'] * 5) * max(5, mood['anxiety'])
                mood_change['anxiety'] += anxiety_change
                # disgust: conscientiousness, honesty
                disgust_change = (hexaco_difference['conscientiousness'] * 5) * max(5, mood['disgust'])
                disgust_change += (hexaco_difference['honesty'] * 5) * max(5, mood['disgust'])
                mood_change['disgust'] += disgust_change
                # anger: agreeableness
                mood_change['anger'] += (hexaco_difference['agreeableness'] * 5) * max(5, mood['anger'])
                # sadness: emotionality
                mood_change['sadness'] += (hexaco_difference['emotionality'] * 5) * max(5, mood['sadness'])
                # pride : honesty
                mood_change['pride'] += (hexaco_difference['honesty'] * max(5, 100 - mood['pride']))
                # guilt : honesty
                mood_change['guilt'] += (hexaco_difference['honesty'] * max(5, mood['guilt']))
                
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