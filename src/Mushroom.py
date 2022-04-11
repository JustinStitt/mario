from Entity import Entity
from Collectable import Collectable

class Mushroom(Entity, Collectable):
    def __init__(self, game, pos=(0, 0)):
        Entity.__init__(self, game=game, pos=pos, 
                    uses_gravity=True,
                    handle_collisions=True,
                    width=.7, height=.82,
                    uses_spritesheet=True, 
                    animation_delay=10,
                    animation_dict={
                        'idle': ['sprite23'],
                    },
                    starting_animation_state='idle',)
        Collectable.__init__(self)
        self.velocity.x = 1