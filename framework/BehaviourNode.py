from datetime import time

class BehaviourNode:
    """Base class for all behaviour nodes"""
    
    def __init__(self, name, honesty, emotionality, extroversion, agreeableness, conscientiousness, openness, 
                     happiness=0, sadness=0, anger=0, fear=0, disgust=0, surprise=0, love=0, jealousy=0, guilt=0, pride=0, stress=0, tags=[], start_time=time(0, 0), end_time=time(23, 59), active_days=[0, 1, 2, 3, 4, 5, 6]):
            self.name = name

            # HEXACO System
            self.honesty = honesty                      # Fairness
            self.emotionality = emotionality            # Emotional sensitivity
            self.extroversion = extroversion            # Social enthusiasm
            self.agreeableness = agreeableness          # Forgiveness and tolerance
            self.conscientiousness = conscientiousness  # Hardworking
            self.openness = openness                    # Creativity and curiosity

            # Mood
            self.happiness = happiness
            self.sadness = sadness
            self.anger = anger
            self.fear = fear
            self.disgust = disgust
            self.surprise = surprise
            self.love = love
            self.jealousy = jealousy
            self.guilt = guilt
            self.pride = pride
            self.stress = stress
            
            # Tags
            self.tags = tags
            
            # Time
            start_time = start_time
            end_time = end_time
            active_days = active_days