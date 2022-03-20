
'''
Meta class holds meta information
'''
class Meta:
    def __init__(self):
        self.screen = Screen()
        self.game = Game()
    
    def __repr__(self):
        rep = str(type(self)) + ''
        for (k, v) in vars(self).items():
            rep += f'({k} = {v}), '
        return rep

'''
Meta Screen class holds meta infromation about the screen.
'''
class Screen(Meta):
    def __init__(self):
        self.WIDTH = 800 # default width
        self.HEIGHT = 600 # default height
        self.BACKGROUND_COLOR = (42, 42, 46)
        self._CELL_SIZE = 0.05 # 5% of width
        self.setup_cell_properties()

    def setup_cell_properties(self):
        self.ASPECT_RATIO = self.WIDTH / self.HEIGHT
        self.CELL_WIDTH = int(self.WIDTH * self._CELL_SIZE) # 5% of width
        self.CELL_HEIGHT = int(self.HEIGHT * self._CELL_SIZE * self.ASPECT_RATIO) # 5% of height

    def set_width(self, new_width):
        self.old_width = self.WIDTH
        self.WIDTH = new_width
        self.setup_cell_properties()
    
    def set_height(self, new_height):
        self.old_height = self.HEIGHT
        self.HEIGHT = new_height
        self.setup_cell_properties()

'''
Meta Game class holds meta infromation about the game.
fps = frames per second
'''
class Game(Meta):
    def __init__(self):
        self.fps = 60

meta = Meta()