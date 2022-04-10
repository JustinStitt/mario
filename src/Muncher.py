from Entity import Entity
from Enemy import Enemy

class Muncher(Entity, Enemy):
    def __init__(self, game, pos=(0, 0)):
        Entity.__init__(self, game=game, pos=pos, 
                    uses_gravity=True,
                    handle_collisions=True,
                    width=.7, height=1.5,
                    uses_spritesheet=True, 
                    animation_delay=10,
                    animation_dict={
                        'chomp': ['muncher1', 'muncher2']
                    },
                    starting_animation_state='chomp',)
        Enemy.__init__(self)
        self.boppable = False
    