import pygame, sys, os, math
from Camera import Camera
from Mushroom import Mushroom
from abstract import Updateable, Renderable
from Entity import Entity
from Player import Player
from meta import meta
from GUI import GUI
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
        self.start_music('1-01-theme')
        self.use_underground_filter = False
        self.score = 0
    
    def setup_pygame(self):
        pygame.init()
        self.screen = pygame.Surface(
            meta.screen.WORLD_DIMS, pygame.SRCALPHA, 32
        )
        self.camera = Camera(self.screen)

        pygame.display.set_caption('Mario')
        self.setup_background()
        self.clock = pygame.time.Clock()
        self.gui = GUI(self)
        self.gui_sprite = pygame.sprite.GroupSingle()
        self.gui_sprite.add(self.gui)

    
    def setup_background(self, world_id=1, level_id=1):
        border_buffer = 100
        #self.background = pygame.Surface(
        #    [meta.screen.WIDTH+border_buffer, meta.screen.HEIGHT+border_buffer]
        #)
        # fix bug with double digit level_ids for background imgs (not crucial atm)
        self.background_img = pygame.image.load(f'../resources/level_bgs/level_bg_{world_id}-0{level_id}.png')
        irect = self.background_img.get_rect()
        self.background_img = pygame.transform.scale(self.background_img, (irect[2]*2.67, irect[3]*2.67))
        self.background = pygame.Surface((self.background_img.get_rect().width, 
                                                self.background_img.get_rect().height+meta.screen.WORLD_DIMS[1]))
        self.background.fill((0,0,0))#172, 200, 252))
        self.background.blit(self.background_img, (0, 0))
        self.screen.blit(self.background, (0, 0))

    def start_music(self, name):
        self.background_music = pygame.mixer.music.load(f'../resources/sounds/{name}.mp3')
        pygame.mixer.music.set_volume(.07)
        pygame.mixer.music.play(-1)

    @Updateable._contingent_update
    def update(self):
        if self.tileset is None: print('No level found...'); return
        self.check_events()
        for e in self.entities: e.update()
        for t in self.tileset: t.update()
        self.player.sprite.update()
        if self.frame % 60 == 0: self.time_left -= 1

    def render(self):
        #self.draw_static_background()
        #self.draw_grid()
        self.camera.follow_player(self.player.sprite.rect)
        self.camera.render_to_camera()
        self.entities.clear(self.screen, self.background)
        self.gui_sprite.clear(self.camera.camera, self.background)
        self.player.clear(self.screen, self.background)
        if self.use_underground_filter == True:
            self.player.clear(self.screen, self.underground_filter)
            self.entities.clear(self.screen, self.underground_filter)
        self.gui.render()
        self.entities.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.go:
            self.update()
            self.render()
            self.clock.tick(meta.game.fps)
            self.update_gui()

    def update_gui(self):
        self.gui.update_element('score', str(self.score))
        self.gui.update_element('time', str(self.time_left))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
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
            #self.load_level(1, 2)
            #self.player.sprite.get_mushroom()
            self.add_entity(Mushroom(game=self, pos=(200, 25)))

    def save_highscore(self):
        hiscore_file = open('../resources/highscore.dat', 'r+')
        current_hiscore = hiscore_file.readlines()[0]
        current_hiscore = str(max(int(current_hiscore, 10), self.score))
        hiscore_file.seek(0)
        hiscore_file.write(current_hiscore)
        self.gui.update_element('hiscore', value=current_hiscore)
    
    def reset_game(self):
        self.add_player(Player(self))
        for e in self.entities: e.kill()
        self.load_level(1, 1)

    def handle_mouse(self, event):
        self.player.sprite.handle_mouse(event)
        print(f'{self.tileset=}', flush=True)

    def win(self):
        self.camera.show_win()

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
        #self.screen = pygame.display.set_mode((nw, nh), pygame.RESIZABLE)

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
        self.setup_background(world_id=world_id, level_id=level_id)
        self.player.empty()
        self.entities.empty()
        self.add_player(Player(self))
        self.gui.update_element('world', f'{world_id}-{level_id}')
        self.time_left = 300
        path = f'../levels/{world_id}-{level_id if level_id > 9 else f"0{level_id}"}.level'
        level = LevelParser.load_level(path)
        self.tileset = LevelBuilder.build_level(self, level)
        self.tileset.draw(self.screen)
        if world_id == 1 and level_id == 2:
            self.use_underground_filter = True
            self.underground_filter = pygame.Surface(meta.screen.WORLD_DIMS, pygame.SRCALPHA, 32)
            self.underground_filter.fill((12, 15, 199, 200))
            self.screen.blit(self.underground_filter, (0, 0))
        else:
            self.use_underground_filter = False
        self.save_highscore()

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
