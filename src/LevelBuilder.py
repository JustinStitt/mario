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
                if m[r][c] != 1: continue
                new_block = Block(game, (c, r), width=1, height=1)
                tileset.add(new_block)
        return tileset