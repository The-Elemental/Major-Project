from framework.NPC import NPC
from datetime import time

class BehaviourNode:
    """Base class for all behaviour nodes"""
    
    def __init__(self, name:str, honesty:float, emotionality:float, extroversion:float, agreeableness:float, conscientiousness:float, openness:float, 
                     happiness:int=0, sadness:int=0, anger:int=0, fear:int=0, disgust:int=0, surprise:int=0, love:int=0, jealousy:int=0, guilt:int=0, pride:int=0, stress:int=0, anxiety:int=0, fatigue:int=0, 
                     tags:set=set(), start_time:time=time(0, 0), end_time:time=time(23, 59), active_days:set=set([0, 1, 2, 3, 4, 5, 6]), duration:int=0):
        self.name = name

        self.hexaco = {
            "honesty": honesty,                      # Fairness
            "emotionality": emotionality,            # Emotional sensitivity
            "extroversion": extroversion,            # Social enthusiasm
            "agreeableness": agreeableness,          # Forgiveness and tolerance
            "conscientiousness": conscientiousness,  # Hardworking
            "openness": openness                     # Creativity and curiosity
        }

            # Mood
        self.mood = {
            "happiness": happiness,
            "sadness": sadness,
            "anger": anger,
            "fear": fear,
            "disgust": disgust,
            "surprise": surprise,
            "love": love,
            "jealousy": jealousy,
            "guilt": guilt,
            "pride": pride,
            "stress": stress,
            "anxiety": anxiety,
            "fatigue": fatigue
        }
            
            # Tags
        self.tags = tags
        
        # Time
        self.start_time = start_time
        self.end_time = end_time
        self.active_days = active_days
        self.duration = duration
            
    def get_change(self, npc:NPC):
        query = """
        MATCH (npc:NPC {id: $npc_id}) 
        OPTIONAL MATCH (npc)-[:HAS_MOOD]->(mood:Mood)
        OPTIONAL MATCH (npc)-[:HAS_HEXACO]->(hexaco:HEXACO)
        RETURN npc, mood, hexaco
        """
        result = npc.graph.run(query, npc_id=npc.id).data()

        if not result:
            print("Error: NPC not found when attempting location.get_best_node()")
            return None
        
        mood = dict(result[0]["mood"]) if result[0]['mood'] else {}
        hexaco = dict(result[0]["hexaco"]) if result[0]['hexaco'] else {}
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
        hexaco_difference = {
            key: (hexaco[key] - behavior_value)  # Calculate the difference
            for key, behavior_value in self.hexaco.items()
            if behavior_value != 0  # Skip behavior nodes with value 0
        }
        mood_change = npc.mood.copy()
        # stress : openness, conscientiousness, agreeableness, emotionality, extroversion, honesty
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
        
        return mood_change