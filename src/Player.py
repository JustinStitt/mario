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

    def handle_keydown(self, key):
        diff = pygame.math.Vector2(0, 0)
        ms = self.move_speed
        if key in self.up: diff.y = -ms
        elif key in self.down: diff.y = ms
        elif key in self.left: diff.x = -ms
        elif key in self.right: diff.x = ms
        self.velocity += diff

    def handle_keyup(self, key):
        diff = pygame.math.Vector2(0, 0)
        ms = self.move_speed
        if key in self.up: diff.y = ms
        elif key in self.down: diff.y = -ms
        elif key in self.left: diff.x = ms
        elif key in self.right: diff.x = -ms
        self.velocity += diff


    def handle_mouse(self, event):
        self.collideswith()

class Player(Entity, PlayerControlled):
    def __init__(self, game, pos = (0, 0), width=.8, height=2):
        Entity.__init__(self, game=game, pos=pos, width=width, height=height)
        PlayerControlled.__init__(self)
