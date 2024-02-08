class Movement:
    def __init__(self, player_pos_x,player_pos_y, pygame_instance,request_instance,id_player):
        self.request_instance = request_instance
        self.player_pos_x = player_pos_x
        self.player_pos_y = player_pos_y
        self.pygame_instance = pygame_instance
        self.id_player = id_player

    def move(self, dt, keys):
        # Founction for the movement of the player
        # We use the key pressed to move the player
        # We send the new position of the player to the server
        data={'newX':self.player_pos_x,'newY':self.player_pos_y,'dt':dt}

        if keys[self.pygame_instance.K_z]:
            data={'newX':self.player_pos_x,'newY':(self.player_pos_y-300*dt),'dt':dt}
            self.player_pos_y -= 300 * dt
        if keys[self.pygame_instance.K_s]:
            data={'newX':self.player_pos_x,'newY':(self.player_pos_y+300*dt),'dt':dt}
            self.player_pos_y += 300 * dt
        if keys[self.pygame_instance.K_q]:
            data={'newX':(self.player_pos_x-300*dt),'newY':self.player_pos_y,'dt':dt}
            self.player_pos_x -= 300 * dt
        if keys[self.pygame_instance.K_d]:
            data={'newX':(self.player_pos_x+300*dt),'newY':self.player_pos_y,'dt':dt}
            self.player_pos_x += 300 * dt
        self.request_instance.put("player/"+str(self.id_player)+"/move",data)
