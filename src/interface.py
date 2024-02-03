# Autor: LE TARNEC Thomas, MOLINIER Camille
import pygame
import random
from Action.movement import Movement
from Entities.player import Player
from Requests.request import Request
import json

class Interface:
        
        
    def __init__(self):
        # Init pygame and window size 
        # We request the world to the server
        pygame.init()
        self.request = Request()
        # We get the world instance (the size of the window)
        self.world=self.request.get("world")
        print("######################")
        print(self.world)
        print("######################")
        
        # We request the local player to the server (the player that we control)
        # We get a player instance
        self.initplayer=self.request.get("world/join")
        self.local_player=Player(self.initplayer['id'],self.initplayer['pos_x'],self.initplayer['pos_y'],pygame,self.request)
        print("######################")
        print(self.initplayer)
        print("######################")
        
        
        self.screen = pygame.display.set_mode((self.world['y_dim'], self.world['x_dim']))
        self.clock = pygame.time.Clock()
        self.running = True
    
        

    def run(self):
        
        # Init players (we draw local_player)
        self.local_player.draw(self.screen,"blue")
            
        while self.running:
            # Events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update
            self.screen.fill("white")
            
            #Update and check roleback
            self.players = self.request.get("player")
            
            for player in self.players:
                player = Player(player['id'],player['pos_x'],player['pos_y'],pygame,self.request)
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
                        movement.move(self.clock.tick(60) / 1000,keys)
                # We draw the player
                    player.draw(self.screen,"blue")
                else:
                    player.draw(self.screen)
                # We delete the player instance
                del player
            
            # Flip
            pygame.display.flip()
            self.clock.tick(60)
        self.request.close()
        pygame.quit()

    
