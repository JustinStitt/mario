import pygame
from Block import Block
from Goomba import Goomba
from Muncher import Muncher
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
                if block_id == 0: continue # don't draw air block
                x, y = row_col_to_pos(c, r)
                if block_id == 9: # dealing with goomba
                    game.add_entity(Goomba(game=game, pos=(x, y)))
                elif block_id == 8: # muncher
                    game.add_entity(Muncher(game=game, pos=(x, y)))
                else:
                    new_block = Block(game, (c, r), width=1, height=1, id=block_id)
                    new_block.do_update = False
                    tileset.add(new_block)
        return tileset