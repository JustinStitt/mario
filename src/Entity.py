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
        self.image = pygame.Surface((width, height))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(topleft = pos)
        self.velocity = pygame.math.Vector2(1, 1)
        self.game = game

    @Updateable._contingent_update
    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def render(self):
        self.draw(self.game.screen)
