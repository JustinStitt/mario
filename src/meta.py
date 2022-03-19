
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
        self.WIDTH = 800
        self.HEIGHT = 600
        self.BACKGROUND_COLOR = (42, 42, 46)

'''
Meta Game class holds meta infromation about the game.
fps = frames per second
'''
class Game(Meta):
    def __init__(self):
        self.fps = 60

meta = Meta()