# Autor: LE TARNEC Thomas, MOLINIER Camille
import pygame
import random
from Action.movement import Movement
from Entities.player import Player
from Entities.fish import Fish
from Requests.request import Request
import json

class Interface:
    def instanciation_fish(self,fishs):
        # This function instanciate the fishs and put it in a list to save their images
        List_fish=[]
        images=["fish1.png","fish2.png","fish3.png","fish4.png","fish5.png","fish6.png","fish7.png","fish8.png"]
        for fish in fishs:
            fish = Fish(fish['id'],fish['pos_x'],fish['pos_y'],images[random.randint(0,7)],pygame,self.screen)
            List_fish.append(fish)
        return List_fish
        
            
        
    def __init__(self):
        # Init pygame and window size 
        # We request the world to the server
        pygame.init()
        self.request = Request()
        # We get the world instance (the size of the window)
        self.world=self.request.get("world")
        
        self.screen = pygame.display.set_mode((self.world['y_dim']+250, self.world['x_dim']+50))
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.running = True
        
        #We request the fishs(food) to the server
        self.foods=self.request.get("food")
        self.list_fishs=self.instanciation_fish(self.foods)
        
        # We request the local player to the server (the player that we control)
        # We get a player instance
        self.initplayer=self.request.get("world/join")
        self.local_player=Player(self.initplayer['id'],self.initplayer['pos_x'],self.initplayer['pos_y'],pygame,self.request,self.screen)
    
        

    def run(self):
        
        background_image = pygame.image.load("src/Images/background.png")
        background_image = pygame.transform.scale(background_image, (600, 600))
        
        # Init players (we draw local_player)
        self.local_player.draw(self.screen,"dark")
            
        while self.running:
            # Events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.request.delete("player/"+str(self.local_player.get_id()))
                    self.running = False

            # Update
            self.screen.fill("grey")
            self.screen.blit(background_image, (0, 0))
            
            # Update the food and draw it
            foods=self.request.get("food")
            for food in foods:
                next(filter(lambda fish: fish.id_fish == food['id'], self.list_fishs), None).draw()
            
            #Update and check roleback
            self.players = self.request.get("player")
            scores=[]
            for player in self.players:
                scores.append((player['id'],player['score']))
                player = Player(player['id'],player['pos_x'],player['pos_y'],pygame,self.request,self.screen)       
                # We check if the player is the local player
                if player.get_id() == self.local_player.get_id():
                    # We check if the position of the player is the same as the local player
                    # If not, it means that the server has rollback the player
                    if player.get_pos_x() != self.local_player.get_pos_x() or player.get_pos_y() != self.local_player.get_pos_y():
                        self.local_player.pos_x=player.get_pos_x()
                        self.local_player.pos_y=player.get_pos_y()
                # We move the player
                    keys = pygame.key.get_pressed()
                    if any(key !=0 for key in keys):
                        movement = Movement(player.get_pos_x(),player.get_pos_y(),pygame,self.request,player.get_id())
                        movement.move(self.clock.tick(120) / 1000,keys)
                # We draw the player
                    player.draw(self.screen,"blue")
                else:
                    player.draw(self.screen)
                # We delete the player instance
                del player
            
            # We sort the list of score
            y=50
            list_scores=sorted(scores,key=lambda x: x[1], reverse=True)
            for score in list_scores:
                text_surface = self.font.render(f"Joueur {score[0]} : {score[1]}", True, "black")
                self.screen.blit(text_surface, (630, y))
                y += 30
            
            # Flip
            pygame.display.flip()
            self.clock.tick(120)
        self.request.close()
        pygame.quit()

    
