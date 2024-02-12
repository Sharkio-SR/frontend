#Class Fish 
# This class allows to instantiate the mines which symbolize the danger for the players

class Mine:
    
    def __init__(self, id, pos_x, pos_y, pygame, screen):
        self.id_mine= id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pygame_instance = pygame
        self.screen_instance=screen
        self.image_mine = self.pygame_instance.image.load("src/Images/mines.png")
        self.image_mine = self.pygame_instance.transform.scale(self.image_mine, (20, 20))
    
    
    def draw(self):
        # We draw the mine on the screen
        self.screen_instance.blit(self.image_mine,(self.pos_x-10,self.pos_y-10))
        