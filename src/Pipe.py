from Entity import Entity

class Pipe(Entity):
    def __init__(self, game, pos=(0, 0), dest=(1, 2)):
        Entity.__init__(self, game=game, pos=pos,
                        handle_collisions=True,
                        uses_gravity=False,
                        uses_spritesheet=True,
                        animation_dict={
                            'idle': ['sprite34']
                        },
                        starting_animation_state='idle',
                        width = 2,
                        height=3,
                        )
        self.dest = dest