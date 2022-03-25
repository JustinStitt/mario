from Entity import Entity, pygame
from meta import meta

class PlayerControlled():
    def __init__(self, move_speed=.1):
        self.base_speed = move_speed
        self.adjust_speed()
        self.left = [pygame.K_LEFT, pygame.K_a]
        self.right = [pygame.K_RIGHT, pygame.K_d]
        self.up = [pygame.K_UP, pygame.K_w]
        self.down = [pygame.K_DOWN, pygame.K_s]

    def adjust_speed(self):
        self.move_speed = meta.screen.CELL_WIDTH * self.base_speed + 1
        self.jump_height = meta.screen.CELL_HEIGHT / 4

    def get_input(self):
        ms = self.move_speed
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.velocity.x = ms
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.velocity.x = -ms
            self.facing_right = False
        else:
            self.velocity.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def handle_mouse(self, event):
        self.collideswith()

class Player(Entity, PlayerControlled):
    def __init__(self, game, pos = (0, 0), width=.8, height=2):
        Entity.__init__(self, game=game, pos=pos, width=width, 
                          height=height, uses_gravity=True, 
                            handle_collisions=True)
        PlayerControlled.__init__(self)
        self.adjust_speed()

    def update(self):
        super().update()
        self.get_input()

    def jump(self):
        self.velocity.y = -self.jump_height
        self.on_ground = False
        
    
    
    
