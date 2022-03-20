import pygame, sys, os, math
from abstract import Updateable, Renderable
from Entity import Entity
from Player import Player
from meta import meta

'''
Main game object (should theoretically be a singleton)
handles main game logic and execution flow.
'''
class Game(Updateable, Renderable):
    def __init__(self):
        self.setup_pygame()
        Updateable.__init__(self)
        self.entities = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
    
    def setup_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            [meta.screen.WIDTH, meta.screen.HEIGHT],
            pygame.RESIZABLE,
        )
        pygame.display.set_caption('Mario')
        self.setup_background()
        self.clock = pygame.time.Clock()
    
    def setup_background(self):
        self.background = pygame.Surface(
            [meta.screen.WIDTH, meta.screen.HEIGHT]
        )

    @Updateable._contingent_update
    def update(self):
        self.check_events()
        for e in self.entities: e.update()
        self.player.sprite.update()

    def render(self):
        self.draw_static_background()
        self.draw_grid()
        self.player.draw(self.screen)
        self.entities.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.go:
            self.update()
            self.render()
            self.clock.tick(meta.game.fps)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_key(event.key)
            elif event.type == pygame.KEYUP:
                self.handle_key(event.key, dir='up')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse(event)
            elif event.type == pygame.VIDEORESIZE:
                self.handle_window_resize(event)

    def handle_key(self, key, dir='down'):
        if dir == 'down':
            self.player.sprite.handle_keydown(key)
        else:
            self.player.sprite.handle_keyup(key) 

    def handle_mouse(self, event):
        self.player.sprite.handle_mouse(event)

    def handle_window_resize(self, event):
        w, h = event.size
        # maintain aspect ratio
        aspect_ratio = meta.screen.ASPECT_RATIO = 1.333
        nw = w
        nh = int(nw / aspect_ratio)
        meta.screen.set_width(nw)
        meta.screen.set_height(nh)
        self.setup_background()
        # resize entities to match the new size
        sw, sh = meta.screen.old_width, meta.screen.old_height
        for e in (*self.entities.sprites(), self.player.sprite):
            wpercent, hpercent = (sw - e.rect.x) / sw, (sh - e.rect.y) / sh
            new_x, new_y = w - (w*wpercent), nh - (nh*hpercent)
            e.setup_image(e.width, e.height, pos=(new_x, new_y))
        self.player.sprite.adjust_speed()

        # setup screen again
        self.screen = pygame.display.set_mode((nw, nh), pygame.RESIZABLE)

    def draw_static_background(self):
        self.background.fill(meta.screen.BACKGROUND_COLOR)
        self.screen.blit(self.background, (0, 0))
    
    def add_entity(self, to_add):
        if not isinstance(to_add, Entity): raise TypeError
        self.entities.add(to_add)
    
    def add_player(self, player):
        if not isinstance(player, Player): raise TypeError
        self.player.add(player)

    '''
    debug method for drawing grid lines to screen
    '''
    def draw_grid(self):
        color = pygame.Color(25, 25, 25, 128) # grid line color
        w, h = meta.screen.WIDTH, meta.screen.HEIGHT
        cw, ch = meta.screen.CELL_WIDTH, meta.screen.CELL_HEIGHT

        # draw rows
        for y in range(0, h, ch):
            pygame.draw.line(self.screen, color, (0, y), (w, y), width=1)
        
        # draw cols
        for x in range(0, w, cw):
            pygame.draw.line(self.screen, color, (x, 0), (x, h), width=1)


game = Game()
