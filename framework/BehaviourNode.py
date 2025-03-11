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