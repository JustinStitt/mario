from Entity import Entity
from Enemy import Enemy

class Goomba(Entity, Enemy):
    def __init__(self, game, pos=(0, 0)):
        Entity.__init__(self, game=game, pos=pos, 
                    uses_gravity=True,
                    handle_collisions=True,
                    width=.7, height=.8,
                    uses_spritesheet=True, 
                    animation_delay=10,
                    animation_dict={
                        'walk': ['goomba1', 'goomba2'],
                        'die': ['goomba4']
                    },
                    starting_animation_state='walk',)
        Enemy.__init__(self)
        self.velocity.x = 1
        self.alive = True
        self.kill_delay = 100
    
    def update(self):
        self.horizontal_movement()
        res = self.handle_horizontal_collisions()
        if res == True: self.velocity.x *= -1
        self.vertical_movement()
        self.handle_vertical_collisions()
        self.update_forces()
        self.animate()
        if not self.alive:
            self.kill_delay -= 1
            if self.kill_delay <= 0: self.kill()
    
    def die(self):
        print(f'Goomba defeated!', flush=True)
        self.animation_state = 'die'
        self.setup_image(.7, .4, pos=(self.rect.topleft[0]-5, self.rect.topleft[1] + 14))
        self.velocity.x = 0
        self.handle_collisions = False
        self.uses_gravity = False
        self.alive = False