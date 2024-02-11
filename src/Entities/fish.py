#Class Fish 
#Cette classe permet d'instancier les poissons qui symbolise la nourriture/score pour les joueurs
import random

class Fish:
    
    def __init__(self, id, pos_x, pos_y, image, pygame, screen):
        self.id_fish = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pygame_instance = pygame
        self.screen_instance=screen
        self.image_fish = self.pygame_instance.image.load("src/Images/"+image)
        self.image_fish = self.pygame_instance.transform.scale(self.image_fish, (20, 20))
    
    def draw(self):
        # We draw the fish on the screen
        #self.fish_rect=self.image_fish.get_rect()
        #self.fish_rect.x = self.pos_x
        #self.fish_rect.y = self.pos_y
        self.screen_instance.blit(self.image_fish,(self.pos_x-10,self.pos_y-10))
    
    def find_fish_by_id(fish_list, target_id):
        for fish in fish_list:
            if fish.id == target_id:
                return fish
        return None
        