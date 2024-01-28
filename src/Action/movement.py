#Importation



#Class for the movement of the player
class Movement:
    def __init__(self, player_pos, pygame_instance,request_instance,id_player):
        self.request_instance = request_instance
        self.player_pos = player_pos
        self.pygame_instance = pygame_instance
        self.id_player = id_player

    def move(self, dt):
        # Founction for the movement of the player
        # We use the key pressed to move the player
        # We send the new position of the player to the server
        keys = self.pygame_instance.key.get_pressed()
        if keys[self.pygame_instance.K_z]:
            self.request_instance.put(self.id_player,{"x":self.player_pos.x,"y":self.player_pos.y-300*dt})
            self.player_pos.y -= 300 * dt
        if keys[self.pygame_instance.K_s]:
            self.request_instance.put(self.id_player,{"x":self.player_pos.x,"y":self.player_pos.y+300*dt})
            self.player_pos.y += 300 * dt
        if keys[self.pygame_instance.K_q]:
            self.request_instance.put(self.id_player,{"x":self.player_pos.x-300*dt,"y":self.player_pos.y})
            self.player_pos.x -= 300 * dt
        if keys[self.pygame_instance.K_d]:
            self.request_instance.put(self.id_player,{"x":self.player_pos.x+300*dt,"y":self.player_pos.y})
            self.player_pos.x += 300 * dt