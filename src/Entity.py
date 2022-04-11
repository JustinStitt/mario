import pygame
from abstract import Updateable, Renderable
from Collectable import Collectable
from Force import Force
from meta import meta
from Enemy import Enemy
from Util import get_image

'''
Entity class serves to provide basic functionality for
all entities within the game.
'''
class Entity(Updateable, Renderable, pygame.sprite.Sprite):
    def __init__(self, game, pos=(0, 0), width=1, height=1,
                         uses_gravity=False, handle_collisions=False, 
                            image_list=None, animation_delay = 25, 
                            uses_spritesheet=False,
                            animation_dict={},
                            starting_animation_state='state'): # state: list[imgs]
        Updateable.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = width, height
        self.uses_spritesheet = uses_spritesheet
        self.animation_dict = animation_dict
        self.animation_state = starting_animation_state
        self.load_images()
        self.setup_image(width, height, pos=pos)
        self.velocity = pygame.math.Vector2(0 ,0)
        self.game = game
        self.forces = []
        self.speed_multiplier = 1.0 # default speed multi is 1.0 (100% of normal speed)
        self.uses_gravity = uses_gravity
        self.handle_collisions = handle_collisions
        self.on_ground = False
        self.animation_timer, self.animation_index = 0, 0
        self.animation_delay = animation_delay
        self.do_update = True
        self.alive = True

    def load_images(self):
        for (state, img_list) in self.animation_dict.items():
            for x in range(len(img_list)):
                if self.uses_spritesheet:
                    img_list[x] = get_image(img_list[x])
                else:
                    img_list[x] = pygame.image.load(img_list[x])
        if len(self.animation_dict.keys()) < 1: self.images = None; return

    def setup_image(self, *dims, pos):
        self.w = int(meta.screen.CELL_WIDTH * dims[0])
        self.h = int(meta.screen.CELL_HEIGHT * dims[1])
        if len(self.animation_dict.keys()) < 1: 
            self.image = pygame.Surface((self.w, self.h))
            self.image.fill((255,0,0)) # default color
        else:
            for (state, img_list) in self.animation_dict.items():
                for x in range(len(img_list)):
                    img_list[x] = pygame.transform.scale(img_list[x], (self.w, self.h))
            self.image = img_list[0]
        self.rect = self.image.get_rect(topleft = pos)

    def animate(self):
        #if len(self.animation_dict[self.animation_state]) < 2: return
        self.animation_timer += 1
        if self.animation_timer < self.animation_delay: return
        self.animation_timer = 0
        self.animation_index = (self.animation_index + 1) % len(self.animation_dict[self.animation_state])
        self.image = self.animation_dict[self.animation_state][self.animation_index]

    @Updateable._contingent_update
    def update(self):
        if not self.do_update: return
        self.horizontal_movement()
        if self.handle_collisions:
            self.handle_horizontal_collisions()
        self.vertical_movement()
        if self.handle_collisions:
            self.handle_vertical_collisions()
        self.update_forces()
        self.animate()

    def apply_gravity(self):
        if not self.uses_gravity: return
        self.velocity.y += meta.physics.GRAVITY

    def render(self):
        pass

    def collideswith(self):
        collides = pygame.sprite.spritecollide(self, [*self.game.entities,*self.game.tileset], False)
        collides = [x for x in collides if hasattr(x, 'alive') and x.alive]
        collides = [x for x in collides if x.handle_collisions]
        return collides

    def horizontal_movement(self):
        self.rect.x += self.velocity.x * self.speed_multiplier
        horizontal_forces = [f for f in self.forces if f.x != 0]
        self.rect.x += sum([f.x for f in horizontal_forces])
    
    def vertical_movement(self):
        self.rect.y += self.velocity.y * self.speed_multiplier
        vertical_forces = [f for f in self.forces if f.y != 0]
        self.rect.y += sum([f.y for f in vertical_forces])
        self.apply_gravity()

    def handle_horizontal_collisions(self):
        collisions = self.collideswith()
        did_hit = False
        if not len(collisions): return False
        for collision in collisions:
            if collision is self: continue
            is_player = type(self).__name__ == 'Player'
            if is_player and type(collision).__name__ == 'Fireball': continue
            if type(self).__name__ == 'Fireball' and isinstance(collision, Collectable): continue
            if type(self).__name__ == 'Fireball' and isinstance(collision, Enemy): 
                collision.die()
                self.kill()
            if type(self).__name__ == 'Fireball' and type(collision).__name__ == 'Block': continue
            if isinstance(self, Collectable) and isinstance(collision, Collectable): continue

            if is_player and isinstance(collision, Collectable):
                collision.kill()
                self.collect_collectable(collision)
                continue
            if is_player and isinstance(collision, Enemy):
                if abs(self.rect.topleft[1] - collision.rect.topleft[1]) < 55:
                    self.die()
            if is_player and type(collision).__name__ == 'Flagpole': self.game.win(); continue
            did_hit = True
            if self.velocity.x > 0:  # Hit tile moving right
                if type(self).__name__ == 'Fireball':
                    self.kill()
                self.rect.x = collision.rect.left - self.rect.w
            elif self.velocity.x < 0:  # Hit tile moving left
                self.rect.x = collision.rect.right
                if type(self).__name__ == 'Fireball':
                    self.kill()

        return did_hit
    
    def handle_vertical_collisions(self):
        if self.on_ground and self.velocity.y != 0: self.on_ground = False
        collisions = self.collideswith()
        pipe_status = False
        is_player = type(self).__name__ == 'Player'
        for collision in collisions:
            if type(self).__name__ == 'Fireball' and isinstance(collision, Collectable): continue
            if isinstance(self, Collectable) and isinstance(collision, Collectable): continue
            if is_player and type(collision).__name__ == 'Fireball': continue
            if type(self).__name__ == 'Fireball' and isinstance(collision, Enemy):
                collision.die()
                self.kill()
            if collision is self: continue
            if is_player and type(collision).__name__== 'Pipe':
                self.pipe_dest = collision.dest
                self.on_top_of_pipe = True
                pipe_status = True
            elif pipe_status == False:
                self.on_top_of_pipe = False
            if is_player and isinstance(collision, Collectable):
                collision.kill()
                self.collect_collectable(collision)
                continue
            if is_player and isinstance(collision, Enemy):
                if collision.boppable == True:
                    collision.die()
                    self.jump()
                    break
                else:
                    self.die()
            is_special = type(collision).__name__ == 'SpecialBlock'
            if not len(collisions): return
            if self.velocity.y > 0:
                self.rect.bottom = collision.rect.top
                self.velocity.y = 0
                self.on_ground = True
                if type(self).__name__ == 'Fireball':
                    self.velocity.y -= 10
            elif self.velocity.y < 0:
                if is_special:
                    collision.trigger() 
                self.rect.top = collision.rect.bottom
                self.velocity.y = 0
                self.on_ceiling = True
        
    '''
    add force to entity force list
    usage: self.add_force([10, 0], 5)
    '''
    def add_force(self, force, duration):
        force = pygame.math.Vector2(force)
        self.forces.append(Force(force, duration))
    
    def update_forces(self):
        for force in self.forces:
            force.update()

        # cleanup forces (remove expired ones)
        self.forces = [f for f in self.forces if not force.expired]
