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
        self.local_player=self.request.get("world/join")
        self.screen = pygame.display.set_mode((self.world['y_dim'], self.world['x_dim']))
        self.clock = pygame.time.Clock()
        self.running = True
    
        

    def run(self):
        #Init player (temporary)
        self.player_pos = pygame.Vector2(random.randint(0, self.screen.get_width()), random.randint(0, self.screen.get_height()))
        self.player = Player(self.player_pos,pygame,self.request)
        
        # Init players (we get player instances)
        self.players = self.request.get("player")
        print("######################")
        print(self.players)
        print("######################")
        # Before the server is implemented, we create a list of players to test the interface
        #self.players = [Player(pygame.Vector2(100,100),pygame,self.request),Player(pygame.Vector2(200,200),pygame,self.request),self.player]
            
        while self.running:
            # Events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update
            self.screen.fill("white")
            
            # Draw Player
            #self.player.draw(self.screen)

            # Movement
            movement = Movement(self.local_player.get_pos(),pygame,self.request,self.player.get_id())
            movement.move(self.clock.tick(60) / 1000)
            #self.players[2]=self.player
            
            #Update and check roleback
            self.players = self.request.get("/world/players")
            for player in self.players:
                # We check if the player is the local player
                if player.get_id() == self.local_player.get_id():
                    # We check if the position of the player is the same as the local player
                    # If not, it means that the server has rollback the player
                    if player.get_pos().x != self.player.get_pos().x or player.get_pos().y != self.player.get_pos().y:
                        self.player_pos=player.get_pos()
                # We draw the player
                    player.draw(self.screen,"blue")
                else:
                    player.draw(self.screen)
                    
                        
            
            # Flip
            pygame.display.flip()
            self.clock.tick(60)
        self.request.close()
        pygame.quit()

