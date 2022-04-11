from Entity import Entity
from Mushroom import Mushroom
from meta import meta

class SpecialBlock(Entity):
    def __init__(self, game, pos=(0,0), reward=Mushroom, hit_count=1):
        Entity.__init__(self, game=game, pos=pos,
                        handle_collisions=True,
                        uses_gravity=False,
                        uses_spritesheet=True,
                        animation_dict={
                            'idle': ['sprite64', 'sprite73'],
                            'depleted': ['sprite99']
                        },
                        starting_animation_state='idle',
                        width = 1,
                        height= 1,
                        )
        self.reward = reward
        self.hit_count = hit_count

    def trigger(self):
        if self.hit_count <= 0:
            return
        self.hit_count -= 1
        if self.hit_count == 0:
            self.animation_state = 'depleted'
            self.animation_delay = 0
        self.game.add_entity(self.reward(
            game=self.game, 
            pos=(self.rect.topleft[0]+1, self.rect.topleft[1]-meta.screen.CELL_HEIGHT-1))
            )