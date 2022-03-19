from abstract import Updateable, Renderable
import pygame

'''
Entity class serves to provide basic functionality for
all entities within the game.
'''
class Entity(Updateable, Renderable, pygame.sprite.Sprite):
    def __init__(self, game, pos=(0, 0), width=10, height=10):
        Updateable.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.setup_image(width, height, pos=pos)
        self.velocity = pygame.math.Vector2(0 ,0)
        self.game = game

    def setup_image(self, *dims, pos):
        self.image = pygame.Surface(dims) # TO-DO: real images (from spritesheet)
        self.image.fill((255,0,0)) # default color
        self.rect = self.image.get_rect(topleft = pos)

    @Updateable._contingent_update
    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def render(self):
        pass