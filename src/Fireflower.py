from Entity import Entity
from Collectable import Collectable

class Fireflower(Entity, Collectable):
    def __init__(self, game, pos=(0, 0)):
        Entity.__init__(self, game=game, pos=pos, 
                    uses_gravity=True,
                    handle_collisions=True,
                    width=.7, height=.9,
                    uses_spritesheet=True, 
                    animation_delay=10,
                    animation_dict={
                        'idle': ['sprite57'],
                    },
                    starting_animation_state='idle',)
        Collectable.__init__(self)