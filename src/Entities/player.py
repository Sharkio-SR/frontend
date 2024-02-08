#Class for the player
class Player:
    def __init__(self, id,pos_x,pos_y, name, pygame_instance, request_instance, screen):
        # We init the player with a position, a pygame instance and a request instance
        self.id_player = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.name = name
        self.pygame_instance = pygame_instance
        self.screen_instance=screen
        self.request_instance = request_instance
        self.image_player = self.pygame_instance.image.load("src/Images/sharkplayer.png")
        self.image_player = self.pygame_instance.transform.scale(self.image_player, (60, 34))
        self.player_rect=self.image_player.get_rect()
        self.image_opponent = self.pygame_instance.image.load("src/Images/sharkopp.png")
        self.image_opponent = self.pygame_instance.transform.scale(self.image_opponent, (60, 34))
        self.opponent_rect=self.image_opponent.get_rect()
        #Image player
        

    def draw(self, screen,color="red",reverse=False):
        # This function draw the player on the screen with a circle
        self.player_rect.x = self.pos_x
        self.player_rect.y = self.pos_y
        flipped_image_vertical = self.image_player
        if(color=="blue"):
            self.player_rect.x = self.pos_x
            self.player_rect.y = self.pos_y
            flipped_image_vertical = self.pygame_instance.transform.flip(self.image_player, reverse, False)
            self.screen_instance.blit(flipped_image_vertical,(self.player_rect.x-30,self.player_rect.y-17))
        else:
            self.opponent_rect.x = self.pos_x
            self.opponent_rect.y = self.pos_y
            self.screen_instance.blit(self.image_opponent,(self.opponent_rect.x-30,self.opponent_rect.y-17))
        
    def get_id(self):
        #Return the id of the player
        return self.id_player
    
    def get_pos_x(self):
        #Return the position of the player
        return self.pos_x
    
    def get_pos_y(self):
        #Return the position of the player
        return self.pos_y
    
    
    def set_pos_x(self, new_pos_x):
        #Set the position of the player
        self.pos_x = new_pos_x
    
    def set_pos_y(self, new_pos_y):
        #Set the position of the player
        self.pos_y = new_pos_y
        
