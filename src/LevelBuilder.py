import pygame
from Block import Block
from Goomba import Goomba
from Mushroom import Mushroom
from Fireflower import Fireflower
from SpecialBlock import SpecialBlock
from Muncher import Muncher
from Flagpole import Flagpole
from Coin import Coin
from Pipe import Pipe
from meta import meta
from Util import row_col_to_pos

class LevelBuilder():
    @classmethod
    def build_level(self, game, level_matrix) -> pygame.sprite.Group:
        m = level_matrix
        tileset = pygame.sprite.Group()
        for r in range(len(m)):
            for c in range(len(m[r])):
                block_id = m[r][c]
                if '0' <= block_id <= '9': block_id = int(block_id)
                if block_id == 0: continue # don't draw air block
                x, y = row_col_to_pos(c, r)
                if block_id == 9: # dealing with goomba
                    game.add_entity(Goomba(game=game, pos=(x, y)))
                elif block_id == 8: # muncher
                    game.add_entity(Muncher(game=game, pos=(x, y)))
                elif block_id == 7: # flagpole
                    x, y = row_col_to_pos(c, r-10.5)
                    game.add_entity(Flagpole(game=game, pos=(x, y)))
                elif block_id == 5: # coin
                    game.add_entity(Coin(game=game, pos=(x, y)))
                elif block_id == 4: # pipe
                    x, y = row_col_to_pos(c, r-2)
                    game.add_entity(Pipe(game=game, pos=(x,y), dest=(1, 2))) # how to encode dest??
                elif block_id == 3: # pipe to overworld
                    x, y = row_col_to_pos(c, r-2)
                    game.add_entity(Pipe(game=game, pos=(x,y), dest=(1, 1))) # how to encode dest??
                elif block_id == 'S': # block with mushroom
                    game.add_entity(
                        SpecialBlock(game=game, pos=(x,y), reward=Mushroom
                        ))
                elif block_id == 'F': # block with fireflower
                    game.add_entity(
                        SpecialBlock(game=game, pos=(x,y), reward=Fireflower
                        ))
                else:
                    new_block = Block(game, (c, r), width=1, height=1, id=block_id)
                    new_block.do_update = False
                    tileset.add(new_block)
        return tileset