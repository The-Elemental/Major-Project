from procedural_generation.World import World

class Game:
    """Running game object"""
    
    def __init__(self):
        self.world = World()
        self.current_location = self.world.get_start_location()
        
    def next(self):
        self.world.next()
        
    def play(self):
        print("-" * 23)
        print(f"Current Location: {self.current_location}")
        print(f"NPC's at current location: {self.current_location.get_npcs()}")
        print("1) Talk")
        print("2) Travel")
        
game = Game()
game.play()