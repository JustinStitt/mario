import pygame
from abstract import Updateable, Renderable
from Force import Force

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
        self.forces = []
        self.speed_multiplier = 1.0 # default speed multi is 1.0 (100% of normal speed)

    def setup_image(self, *dims, pos):
        self.image = pygame.Surface(dims) # TO-DO: real images (from spritesheet)
        self.image.fill((255,0,0)) # default color
        self.rect = self.image.get_rect(topleft = pos)

    @Updateable._contingent_update
    def update(self):
        self.rect.x += self.velocity.x * self.speed_multiplier
        self.rect.y += self.velocity.y * self.speed_multiplier
        self.apply_force()

    def render(self):
        pass

    def collideswith(self):
        collides = pygame.sprite.spritecollide(self, self.game.entities, False)
        print(f'{collides=}', flush=True)
        for collision in collides:
            pass
        # idea, each entity has an array of FORCE objects that can decay overtime 
    
    '''
    add force to entity force list
    usage: self.add_force([10, 0], 5)
    '''
    def add_force(self, force, duration):
        force = pygame.math.Vector2(force)
        self.forces.append(Force(force, duration))
    
    def apply_force(self):
        for force in self.forces:
            force.update()
            self.rect.x += force.x
            self.rect.y += force.y

        # cleanup forces (remove expired ones)
        self.forces = [f for f in self.forces if not force.expired]