#Class for the player
class Player:
    def __init__(self, player_pos, pygame_instance, request_instance):
        # We init the player with a position, a pygame instance and a request instance
        self.id_player = 0
        self.player_pos = player_pos
        self.pygame_instance = pygame_instance
        self.request_instance = request_instance
        self.request_instance.post("player",{"x":self.player_pos.x,"y":self.player_pos.y})

    def draw(self, screen):
        # This function draw the player on the screen with a circle
        self.pygame_instance.draw.circle(screen, "red", self.player_pos, 40)
        
    def get_id(self):
        #Return the id of the player
        return self.id_player
    
    def get_pos(self):
        #Return the position of the player
        return self.player_pos
