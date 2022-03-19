import pygame, sys, os, math
from abstract import Updateable, Renderable
from Entity import Entity
from meta import meta

'''
Main game object (should theoretically be a singleton)
handles main game logic and execution flow.
'''
class Game(Updateable, Renderable):
    def __init__(self):
        Updateable.__init__(self)
        self.setup_pygame()
        self.entities = pygame.sprite.Group()
    
    def setup_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            [meta.screen.WIDTH, meta.screen.HEIGHT]
        )
        pygame.display.set_caption('Mario')
        self.background = pygame.Surface(
            [meta.screen.WIDTH, meta.screen.HEIGHT]
        )
        self.clock = pygame.time.Clock()

    @Updateable._contingent_update
    def update(self):
        self.check_events()
        for e in self.entities: e.update()

    def render(self):
        self.draw_static_background()
        self.entities.draw(self.screen)
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse(event)
    
    def handle_keydown(self, key):
        print(f'{key=}')

    def handle_mouse(self, event):
        print(f'{event.pos=}')

    def draw_static_background(self):
        self.background.fill(meta.screen.BACKGROUND_COLOR)
        self.screen.blit(self.background, (0, 0))
    
    def add_entity(self, to_add):
        if not isinstance(to_add, Entity): raise TypeError
        self.entities.add(to_add)
