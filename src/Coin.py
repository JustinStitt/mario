from Entity import Entity
from Collectable import Collectable

class Coin(Entity, Collectable):
    def __init__(self, game, pos=(0, 0)):
        Collectable.__init__(self)
        Entity.__init__(self,game=game,pos=pos, uses_gravity=False,
                    width=.65, height = .65,
                    uses_spritesheet=True,
                    animation_dict={
                        'idle': ['sprite10']
                    },
                    starting_animation_state='idle',
                    handle_collisions=True,
                    )
