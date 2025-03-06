from framework.World import World

class Game:
    """Running game object"""
    
    def __init__(self):
        self.world = World()
        self.current_location = self.world.get_start()
        
    def next(self):
        self.world.next()
        
    def converse(self, npc):
        print("I be talking here")
    
    def travel(self, location):
        self.current_location = location
    
    def play(self):
        while True:
            print("-" * 23)
            print(f"Current Location: {self.current_location.name}")
            index = 1
            for x in self.current_location.npcs:
                print(f"{index}) Talk to {x.name}")
                index += 1
            for x in self.current_location.connections:
                print(f"{index}) Travel to {x.name}")
                index += 1
            print(f"{index}) Exit")
            user_input = input("->: ")
            try:
                user_input = int(user_input)
                if user_input < len(self.current_location.npcs):
                    self.converse(self.current_location.npcs[user_input - 1])
                elif user_input < index:
                    dict_items = list(self.current_location.connections.items())
                    key, value = dict_items[user_input - 1 - len(self.current_location.npcs)]
                    self.travel(key)
                elif user_input == index:
                    break
                else:
                    print("Please choose an option in the list.")
            except ValueError as e:
                print(f"Please enter a valid number. Error: {e}")
        
game = Game()
game.play()