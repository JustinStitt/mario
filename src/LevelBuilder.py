import pygame
from Block import Block
from meta import meta

class LevelBuilder():
    @classmethod
    def build_level(self, game, level_matrix) -> pygame.sprite.Group:
        m = level_matrix
        tileset = pygame.sprite.Group()
        for r in range(len(m)):
            for c in range(len(m[r])):
                block_id = m[r][c]
                if block_id == 0: continue # don't draw air block
                new_block = Block(game, (c, r), width=1, height=1, id=block_id)
                tileset.add(new_block)
        return tileset