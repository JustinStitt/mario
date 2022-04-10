from Entity import Entity
from Util import row_col_to_pos
from dataclasses import dataclass

@dataclass
class BlockId:
    name: list[str]
    ext: str = 'png'

    @property
    def path(self) -> str:
        paths = []
        for img in self.name:
            a = f'../resources/blocks/{img}.{self.ext}'
            paths.append(a)
        return paths

BLOCK_IDS = {
    1: BlockId(['red_brick']), 
    2: BlockId(['stair_brick']),
}

class Block(Entity):
    def __init__(self, game, pos, width, height, id):
        global BLOCK_IDS
        self.pos = row_col_to_pos(*pos)
        self.id = id
        Entity.__init__(self, game=game, pos=self.pos, 
                          width=width, height=height,
                            animation_dict={'state': BLOCK_IDS[id].path})
