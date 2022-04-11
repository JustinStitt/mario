import pygame
from meta import meta

class GUI(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.dest = self.game.camera.camera
        self.WHITE = pygame.Color(255, 255, 255)
        self.image = pygame.Surface((meta.screen.WIDTH, meta.screen.HEIGHT), pygame.SRCALPHA, 32)
        #self.rect = pygame.Rect(0, 0, meta.screen.WIDTH, meta.screen.HEIGHT//8)
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.elements = dict()
        self.setup_elements()

    def setup_elements(self):
        self.elements['score'] = ('Score', self.get_text_element(text='Score', value='0'))
        self.elements['hiscore'] = ('HScore', self.get_text_element(text='Hscore', value='0', pos=(10, 30)))
        self.elements['time'] = ('Time', self.get_text_element(text='Time', value='300', pos=(300, 0)))
        self.elements['world'] = ('World', self.get_text_element(text='WORLD', value='1-1', pos=(605, 0)))

    def update_element(self, id, value):
        elem = self.elements[id]
        self.elements[id] = (elem[0], self.get_text_element(text=elem[0], value=value, pos=elem[1][1]))

    def render(self):
        self.image.fill((255, 0, 0, 0))
        for (_, details) in self.elements.values():
            self.image.blit(*details)
        self.flip()

    def flip(self):
        self.dest.blit(self.image, (0, 0))

    def get_text_element(self, text, value='', pos=(10, 0), size=32, color=None):
        font_obj = self.font(size=size)
        text_obj = font_obj.render(text + f': {value}' if len(value) else '', True, self.WHITE if not color else color)
        return (text_obj, pos)

    def font(self, name='freesansbold', size=108, ext='ttf'):
        return pygame.font.Font(f'{name}.{ext}', size)
    

    
