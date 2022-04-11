from Entity import Entity

class Fireball(Entity):
    def __init__(self, game, pos=(0, 0)):
        Entity.__init__(self, game=game, pos=pos, 
                    uses_gravity=True,
                    handle_collisions=True,
                    width=.45, height=.45,
                    uses_spritesheet=True, 
                    animation_delay=10,
                    animation_dict={
                        'idle': ['sprite117']
                    },
                    starting_animation_state='idle',)
        self.velocity.x = 5 * (1 if self.game.player.sprite.facing_right else -1)