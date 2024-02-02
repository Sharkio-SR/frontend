#Class for the player
class Player:
    def __init__(self, id,pos_x,pos_y, pygame_instance, request_instance):
        # We init the player with a position, a pygame instance and a request instance
        self.id_player = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pygame_instance = pygame_instance
        self.request_instance = request_instance

    def draw(self, screen,color="red"):
        # This function draw the player on the screen with a circle
        self.player_pos=(self.pos_x,self.pos_y)
        self.pygame_instance.draw.circle(screen, color, self.player_pos, 15)
        
    def get_id(self):
        #Return the id of the player
        return self.id_player
    
    def get_pos_x(self):
        #Return the position of the player
        return self.pos_x
    
    def get_pos_y(self):
        #Return the position of the player
        return self.pos_y
