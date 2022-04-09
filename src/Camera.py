from meta import meta
import pygame

class Camera():
    def __init__(self, screen):
        self.camera = pygame.display.set_mode((meta.screen.WIDTH, meta.screen.HEIGHT))
        self.x, self.y = 0, 0
        self.screen = screen
        self.right_scroll_threshold = .7
        self.left_scroll_threshold = .3
        self.down_scroll_threshold = .65
        self.up_scroll_threshold = .2

    def follow_player(self, prect):
        px, py = prect.topleft[0], prect.topleft[1]
        right_threshold = meta.screen.WIDTH * self.right_scroll_threshold + self.x
        left_threshold = meta.screen.WIDTH * self.left_scroll_threshold + self.x
        if px > right_threshold: self.x += px-right_threshold
        elif px < left_threshold: self.x -= left_threshold-px

        self.x = max(1, self.x)
        self.x = min(self.x, meta.screen.WORLD_DIMS[0]-meta.screen.WIDTH+1)

        up_threshold = meta.screen.HEIGHT * self.up_scroll_threshold + self.y
        down_threshold = meta.screen.HEIGHT * self.down_scroll_threshold + self.y
        if py < up_threshold: self.y -= up_threshold-py
        elif py > down_threshold: self.y += py-down_threshold
        self.y = max(1, self.y)
        self.y = min(self.y, meta.screen.WORLD_DIMS[1]-meta.screen.HEIGHT +1)

    def render_to_camera(self):
        try:
            self.camera.blit(self.get_subsurface(), (0, 0))
        except: pass
    
    def get_subsurface(self):
        try:
            self.subsurface = pygame.Surface.copy(
                    pygame.Surface.subsurface(
                            self.screen, 
                            (self.x, self.y, meta.screen.WIDTH, meta.screen.HEIGHT)
                        )
                )
            return self.subsurface
        except: pass

