# Autor: LE TARNEC Thomas, MOLINIER Camille
import pygame
import random
from Action.movement import Movement
from Entities.player import Player
from Entities.fish import Fish
from Requests.request import Request
import json

class Interface:
    
    def instanciation_player(self,screen,username):
        initplayer = self.request.post("world/join", {"name": username})
        self.local_player = Player(initplayer['id'], initplayer['pos_x'], initplayer['pos_y'], username, pygame, self.request, screen)
         
    
    def instanciation_fish(self,fishs,screen):
        # This function instanciate the fishs and put it in a list to save their images
        List_fish=[]
        images=["fish1.png","fish2.png","fish3.png","fish4.png","fish5.png","fish6.png","fish7.png","fish8.png"]
        for fish in fishs:
            fish = Fish(fish['id'],fish['pos_x'],fish['pos_y'],images[random.randint(0,7)],pygame,screen)
            List_fish.append(fish)
        return List_fish
    
    def function_listscores(self,scores,font,screen): 
        # We sort the list of score
        y=50
        list_scores=sorted(scores,key=lambda x: x[2], reverse=True)[:10]    # We only display the 10 first scores
        for score in list_scores:
            text_surface = font.render(f"Joueur {score[1]} : {score[2]}", True, "black")
            screen.blit(text_surface, (630, y))
            y += 30
            
    
    def popup_username(self):
        # This function create a popup to ask the username of the player
        # We use the username to create the player instance
        # We send the username to the server
        pygame.init()
        screen = pygame.display.set_mode((400, 200))
        pygame.display.set_caption("Zone d'input avec Pygame")
        # Définition des constantes pour les dimensions et les positions des éléments
        input_box = pygame.Rect(75, 50, 250, 30)
        button = pygame.Rect(150, 100, 100, 50)
        font = pygame.font.Font(None, 26)
        clock = pygame.time.Clock()
        running = True
        username = ""
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                        if username != "":
                            return username
                        else:
                            return None
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button.collidepoint(event.pos):
                        return username
            screen.fill("white")
            pygame.draw.rect(screen, 'black', input_box, 2)
            pygame.draw.rect(screen, 'black', button, 2)
            # Afficher le texte saisi dans la zone d'input
            text_surface = font.render(username, True, 'black')
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

            # Afficher le texte du bouton
            
            button_text = font.render("Valider", True, 'black')
            text_width, text_height = font.size("Valider")
            text_x = button.x + (button.width - text_width) // 2
            text_y = button.y + (button.height - text_height) // 2
            screen.blit(button_text, (text_x, text_y))
            pygame.display.flip()
            clock.tick(30)
        pygame.quit()
    
    
    def game(self,username):
        pygame.init()
        clock = pygame.time.Clock()
        screen=pygame.display.set_mode((self.world['y_dim']+250, self.world['x_dim']+50))
        list_fishs=self.instanciation_fish(self.request.get("food"),screen)
        font=pygame.font.Font(None, 36)
        # Init players (we draw local_player)
        self.instanciation_player(screen,username)
        self.local_player.draw(screen,"dark")
        running=True
        background_image = pygame.image.load("src/Images/background.png")
        background_image = pygame.transform.scale(background_image, (600, 600))
        while running:
            # Events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.request.delete("player/"+str(self.local_player.get_id()))
                    running = False

            # Update
            screen.fill("grey")
            screen.blit(background_image, (0, 0))
            
            # Update the food and draw it
            foods=self.request.get("food")
            for food in foods:
                next(filter(lambda fish: fish.id_fish == food['id'], list_fishs), None).draw()
            
            scores=[]
            #Update and check roleback
            players = self.request.get("player")
            for player in players:
                scores.append([player['id'],player['name'],player['score']])
                player = Player(player['id'],player['pos_x'],player['pos_y'],player['name'],pygame,self.request,screen)       
                # We check if the player is the local player
                if player.get_id() == self.local_player.get_id():
                    # We check if the position of the player is the same as the local player
                    # If not, it means that the server has rollback the player
                    if player.get_pos_x() != self.local_player.get_pos_x() or player.get_pos_y() != self.local_player.get_pos_y():
                        self.local_player.pos_x=player.get_pos_x()
                        self.local_player.pos_y=player.get_pos_y()
                # We move the player
                    movement=None
                    keys = pygame.key.get_pressed()
                    if any(key !=0 for key in keys):
                        movement = Movement(player.get_pos_x(),player.get_pos_y(),pygame,self.request,player.get_id())
                        movement.move(clock.tick(120) / 1000,keys)
                        
                # We draw the player
                    if(movement!=None):
                        player.draw(screen,"blue",movement.reverse)
                    else:
                        player.draw(screen,"blue")
                else:
                    player.draw(screen)
                # We delete the player instance
                del player
            
            # We draw the score
            self.function_listscores(scores,font,screen)
            
            # Flip
            pygame.display.flip()
            clock.tick(120)
        self.request.close()
        pygame.quit()
        
        
    def __init__(self):
        # Init pygame and window size 
        # We request the world to the server
        
        self.request = Request()
        # We get the world instance (the size of the window)
        self.clock = pygame.time.Clock()
        self.world=self.request.get("world")
        self.local_player = None

    
    def run(self):
        username = self.popup_username()
        if(username!=None):
            self.game(username)
        else:
            self.request.close()