from Entity import Entity
from Util import row_col_to_pos

class Block(Entity):
    def __init__(self, game, pos, width, height):
        self.pos = row_col_to_pos(*pos)
        Entity.__init__(self, game=game, pos=self.pos, width=width, height=height)
