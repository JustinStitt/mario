from Entity import Entity

class Flagpole(Entity):
    def __init__(self, game, pos=(0,0)):
        Entity.__init__(self, game=game, pos=pos,
                        handle_collisions=True,
                        uses_gravity=False,
                        uses_spritesheet=True,
                        animation_dict={
                            'idle': ['flag']
                        },
                        starting_animation_state='idle',
                        width = 1,
                        height=10.5,
                        )