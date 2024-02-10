# Autor: LE TARNEC Thomas, MOLINIER Camille
import pygame
import random
from math import sqrt, pow
from Action.movement import Movement
from Entities.player import Player
from Entities.fish import Fish
from Entities.mine import Mine
from Requests.request import Request
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,45)
import json

class Interface:
    
    def sound_food(self, foods, player):
        # This function play a sound when the player eat a fish
        for food in foods:
            distfood=sqrt(pow((player.get_pos_x()-food['pos_x']),2)+pow((player.get_pos_y()-food['pos_y']),2))
            if distfood<12:
                pygame.mixer.Sound("src/Music/musicmiam.mp3").play()
                
    def sounf_mine(self, mines, player):
        # This function play a sound when the player eat a mines
        for mine in mines:
            distmine=sqrt(pow((player.get_pos_x()-mine['pos_x']),2)+pow((player.get_pos_y()-mine['pos_y']),2))
            if distmine<12:
                pygame.mixer.Sound("src/Music/explosion2.wav").play()
    
    def instanciation_player(self, screen, username):
        # This function instanciate the player and put it in a list to save their images
        initplayer = self.request.post("world/join", {"name": username})
        self.local_player = Player(initplayer['id'], initplayer['pos_x'], initplayer['pos_y'], username, pygame, self.request, screen)
         
    
    def instanciation_fish(self, fishs, screen):
        # This function instanciate the fishs and put it in a list to save their images
        List_fish=[]
        images=["fish1.png","fish2.png","fish3.png","fish4.png","fish5.png","fish6.png","fish7.png","fish8.png"]
        for fish in fishs:
            fish = Fish(fish['id'],fish['pos_x'],fish['pos_y'],images[random.randint(0,7)],pygame,screen)
            List_fish.append(fish)
        return List_fish
    
    def draw_fish(self, screen, fishs):
        for fish in fishs:
            if not any(f.id_fish == fish['id'] for f in self.list_fishs):
                self.list_fishs.append(Fish(fish['id'],fish['pos_x'],fish['pos_y'],self.random_image(),pygame,screen))
            next(filter(lambda f: f.id_fish == fish['id'], self.list_fishs), None).draw()

    def random_image(self):
        # This function return a random image for the fish
        images=["fish1.png","fish2.png","fish3.png","fish4.png","fish5.png","fish6.png","fish7.png","fish8.png"]
        return images[random.randint(0,7)]
    
    def instanciation_mine(self, screen):
        # This function instanciate the fishs and put it in a list to save their images
        mines = self.request.get("mine")
        List_mine=[]
        for mine in mines:
            mine = Mine(mine['id'],mine['pos_x'],mine['pos_y'],pygame,screen)
            List_mine.append(mine)
        return List_mine
    
    def draw_mines(self, screen, mines):
        for danger in mines:
            if not any(f.id_mine == danger['id'] for f in self.list_mines):
                self.list_mines.append(Mine(danger['id'],danger['pos_x'],danger['pos_y'],pygame,screen))
            next(filter(lambda f: f.id_mine == danger['id'], self.list_mines), None).draw()

    
    def function_listscores(self,scores,font,screen): 
        # We sort the list of score
        y=100
        list_scores=sorted(scores,key=lambda x: x[2], reverse=True)[:10]    # We only display the 10 first scores
        local_player_found=False
        for i, score in enumerate(list_scores[:10]):
            if(score[1]==self.local_player.name):
                local_player_found=True
            if(i==0):
                img_first = pygame.image.load("src/Images/Algue1.png")
                img_first = pygame.transform.scale(img_first, (20, 20))
                screen.blit(img_first, (630, y))
            elif(i==1):
                img_second = pygame.image.load("src/Images/Algue2.png")
                img_second = pygame.transform.scale(img_second, (20, 20))
                screen.blit(img_second, (630, y))
            elif(i==2):
                img_third = pygame.image.load("src/Images/Algue3.png")
                img_third = pygame.transform.scale(img_third, (20, 20))
                screen.blit(img_third, (630, y))
            text_surface = font.render(f" {score[1]} : {score[2]}", True, (211,211,211))
            screen.blit(text_surface, (650, y))
            y += 30
        if not local_player_found:
            text_surface = font.render(f"Local Player: {local_player_score}", True, (211, 211, 211))
            screen.blit(text_surface, (650, y))
    
    def screen_end(self,screen,events):
        # This function draw the end screen
        font=pygame.font.Font(None, 26)
        font_title=pygame.font.Font("src/Aquatico-Regular.otf", 40)
        text_surface = font.render("GAME OVER", True, (211,211,211))
        screen.blit(text_surface, (675, 450))
        button = pygame.Rect(675, 500, 100, 50)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    self.instanciation_player(screen,self.local_player.name)
                    self.list_fishs=self.instanciation_fish(self.request.get("food"),screen)
                    self.list_mines=self.instanciation_mine(screen,self.request,pygame)
        # Drawn the boarder of the button in black
        pygame.draw.rect(screen, (0, 0, 0), button, 2)
        # Fill the inside of the button in white
        pygame.draw.rect(screen, (211,211,211), button)
        button_text = font.render("Restart", True, "black")
        text_width, text_height = font.size("Restart")
        text_x = button.x + (button.width - text_width) // 2
        text_y = button.y + (button.height - text_height) // 2
        screen.blit(button_text, (text_x, text_y))
        
    
    def popup_username(self):
        # This function create a popup to ask the username of the player
        # We use the username to create the player instance
        # We send the username to the server
        pygame.init()
        screen = pygame.display.set_mode((400, 200))
        pygame.display.set_caption("Enter Username")
        background_image = pygame.image.load("src/Images/Enter.png")
        background_image = pygame.transform.scale(background_image, (400, 200))
        # Define the constants we need for the input box and button positions
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
                        if len(username) < 15:
                            username += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button.collidepoint(event.pos):
                        return username
            screen.blit(background_image, (0, 0))
            # Draw the border of the input box in black
            pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
            # Fill the inside of the input box in white
            pygame.draw.rect(screen, (211,211,211), input_box)
            # Draw the border of the button in black
            pygame.draw.rect(screen, (0, 0, 0), button, 2)
            # Fill the inside of the button in white
            pygame.draw.rect(screen, (211,211,211), button)
            # Print the username in the input box
            text_surface = font.render(username, True, 'black')
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

            # Print the button text
            
            button_text = font.render("Valider", True, "black")
            text_width, text_height = font.size("Valider")
            text_x = button.x + (button.width - text_width) // 2
            text_y = button.y + (button.height - text_height) // 2
            screen.blit(button_text, (text_x, text_y))
            pygame.display.flip()
            clock.tick(30)
        pygame.quit()
    
    
    def game(self,username):
        pygame.init()
        screen_info = pygame.display.Info()
        clock = pygame.time.Clock()
        screen=pygame.display.set_mode((self.world['y_dim']+250, self.world['x_dim']))
        self.list_fishs=self.instanciation_fish(self.request.get("food"),screen)
        self.list_mines=self.instanciation_mine(screen)
        font=pygame.font.Font(None, 26)
        # Init players (we draw local_player)
        self.instanciation_player(screen,username)
        self.local_player.draw(screen,"dark")
        running=True
        background_image = pygame.image.load("src/Images/background.png")
        background_image = pygame.transform.scale(background_image, (600, 600))
        movement=None
        music_path = "src/Music/musicshark.mp3"
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        previous_score=[]
        while running:
            # Events
            # pygame.QUIT event means the user clicked X to close your window
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.request.delete("player/"+str(self.local_player.get_id()))
                    running = False
            # We get the state of the game
            screen.fill((56,62,66))
            screen.blit(background_image, (0, 0))
            state=self.request.get("world/state")
            if(state):
                # The game is running
                
                # Update the food and draw it
                foods=self.request.get("food")
                self.draw_fish(screen,foods)
                #Update the mines and draw it
                
                mines=self.request.get("mine")
                self.draw_mines(screen,mines)   
                 
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
                        
                        keys = pygame.key.get_pressed()
                        if any(key !=0 for key in keys):
                            movement = Movement(player.get_pos_x(),player.get_pos_y(),pygame,self.request,player.get_id())
                            movement.move(keys)
                            
                    # We draw the player
                        if(movement!=None):
                            player.draw(screen,"blue",movement.reverse)
                        else:
                            player.draw(screen,"blue")
                    else:
                        player.draw(screen)
                    # We delete the player instance
                    del player
                previous_score=scores
                
            else:
                #The game is over
                # We draw the end screen
                end_screen=self.screen_end(screen,events)
            # We draw the score
            self.function_listscores(previous_score,font,screen)
            # We draw the title
            font_title=pygame.font.Font("src/Aquatico-Regular.otf", 40)
            text_surface = font_title.render("SHARKIO", True, (211,211,211))
            screen.blit(text_surface, (630, 30))
            
            # Flip
            pygame.display.flip()
            clock.tick(60)
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
        self.list_fishs = None
        self.list_mines = None

    
    def run(self):
        username = self.popup_username()
        if(username!=None):
            self.game(username)
        else:
            self.request.close()