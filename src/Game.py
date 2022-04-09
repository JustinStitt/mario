import pygame, sys, os, math
from Camera import Camera
from abstract import Updateable, Renderable
from Entity import Entity
from Player import Player
from meta import meta
from LevelParser import LevelParser
from LevelBuilder import LevelBuilder

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
        self.screen = pygame.Surface(
            meta.screen.WORLD_DIMS,
        )
        self.camera = Camera(self.screen)

        pygame.display.set_caption('Mario')
        self.setup_background()
        self.clock = pygame.time.Clock()
    
    def setup_background(self):
        border_buffer = 100
        #self.background = pygame.Surface(
        #    [meta.screen.WIDTH+border_buffer, meta.screen.HEIGHT+border_buffer]
        #)
        self.background_img = pygame.image.load('../resources/level_bgs/level_bg_1-01.png')
        self.background_img = pygame.transform.scale(self.background_img, (3568*2.67, 239*2.67))
        self.background = pygame.Surface((self.background_img.get_rect().width, 
                                                self.background_img.get_rect().height+meta.screen.WORLD_DIMS[1]))
        self.background.fill((0,0,0))#172, 200, 252))
        self.background.blit(self.background_img, (0, 0))
        self.screen.blit(self.background, (0, 0))


    @Updateable._contingent_update
    def update(self):
        if self.tileset is None: print('No level found...'); return
        self.check_events()
        for e in self.entities: e.update()
        for t in self.tileset: t.update()
        self.player.sprite.update()

    def render(self):
        #self.draw_static_background()
        #self.draw_grid()
        self.player.clear(self.screen, self.background)
        self.player.draw(self.screen)
        self.entities.clear(self.screen, self.background)
        self.entities.draw(self.screen)
        self.camera.follow_player(self.player.sprite.rect)
        self.camera.render_to_camera()
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
        if key == pygame.K_k:
            self.player.sprite.add_force([10, 0], duration=10)

    def handle_mouse(self, event):
        self.player.sprite.handle_mouse(event)
        print(f'{self.tileset=}', flush=True)

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
        for e in (*self.entities.sprites(), self.player.sprite, *self.tileset):
            wpercent, hpercent = (sw - e.rect.x) / sw, (sh - e.rect.y) / sh
            new_x, new_y = w - (w*wpercent), nh - (nh*hpercent)
            e.setup_image(e.width, e.height, pos=(new_x, new_y))
        self.player.sprite.adjust_speed()
        meta.physics.GRAVITY = meta.screen.CELL_HEIGHT * .01

        # setup screen again
        self.screen = pygame.display.set_mode((nw, nh), pygame.RESIZABLE)

    def draw_static_background(self):
        #self.background.fill(meta.screen.BACKGROUND_COLOR)
        #self.screen.blit(self.background, (0, 0))
        try:
            self.partial_background = pygame.Surface.copy(
                pygame.Surface.subsurface(self.background, 
                            (self.camera.x, self.camera.y, meta.screen.WIDTH+25, meta.screen.HEIGHT+25))
                )
            self.screen.blit(self.partial_background, (self.camera.x, self.camera.y))
        except: pass

    def add_entity(self, to_add):
        if not isinstance(to_add, Entity): raise TypeError
        self.entities.add(to_add)
    
    def add_player(self, player):
        if not isinstance(player, Player): raise TypeError
        self.player.add(player)

    def load_level(self, world_id, level_id):
        path = f'../levels/{world_id}-{level_id if level_id > 9 else f"0{level_id}"}.level'
        level = LevelParser.load_level(path)
        self.tileset = LevelBuilder.build_level(self, level)
        self.tileset.draw(self.screen)


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
