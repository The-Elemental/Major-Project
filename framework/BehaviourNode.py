from datetime import time

class BehaviourNode:
    """Base class for all behaviour nodes"""
    
    def __init__(self, name, honesty, emotionality, extroversion, agreeableness, conscientiousness, openness, 
                     happiness=0, sadness=0, anger=0, fear=0, disgust=0, surprise=0, love=0, jealousy=0, guilt=0, pride=0, stress=0, anxiety=0, fatigue=0, 
                     tags=[], start_time=time(0, 0), end_time=time(23, 59), active_days=[0, 1, 2, 3, 4, 5, 6], duration=0):
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
            start_time = start_time
            end_time = end_time
            active_days = active_days