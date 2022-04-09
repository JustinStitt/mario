import pygame
from abstract import Updateable, Renderable
from Force import Force
from meta import meta

'''
Entity class serves to provide basic functionality for
all entities within the game.
'''
class Entity(Updateable, Renderable, pygame.sprite.Sprite):
    def __init__(self, game, pos=(0, 0), width=1, height=1,
                         uses_gravity=False, handle_collisions=False, 
                            image_list=None, animation_delay = 25):
        Updateable.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = width, height
        self.load_images(image_list)
        self.setup_image(width, height, pos=pos, images=self.images)
        self.velocity = pygame.math.Vector2(0 ,0)
        self.game = game
        self.forces = []
        self.speed_multiplier = 1.0 # default speed multi is 1.0 (100% of normal speed)
        self.uses_gravity = uses_gravity
        self.handle_collisions = True
        self.on_ground = False
        self.animation_timer, self.animation_index = 0, 0
        self.animation_delay = animation_delay
        self.do_update = True

    def load_images(self, image_list):
        if image_list is None: self.images = None; return
        self.images = [pygame.image.load(img) for img in image_list]

    def setup_image(self, *dims, pos, images):
        self.w = int(meta.screen.CELL_WIDTH * dims[0])
        self.h = int(meta.screen.CELL_HEIGHT * dims[1])
        if images is None: 
            self.image = pygame.Surface((self.w, self.h))
            self.image.fill((255,0,0)) # default color
        else:
            for x in range(len(self.images)):
                self.images[x] = pygame.transform.scale(self.images[x], (self.w, self.h))
            self.image = self.images[0]
        self.rect = self.image.get_rect(topleft = pos)

    def animate(self):
        if self.images is None or len(self.images) < 2: return
        self.animation_timer += 1
        if self.animation_timer < self.animation_delay: return
        self.animation_timer = 0
        self.animation_index = (self.animation_index + 1) % len(self.images)
        self.image = self.images[self.animation_index]

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
        if not len(collisions): return
        for collision in collisions:
            if self.velocity.x > 0:  # Hit tile moving right
                self.rect.x = collision.rect.left - self.rect.w
            elif self.velocity.x < 0:  # Hit tile moving left
                self.rect.x = collision.rect.right
    
    def handle_vertical_collisions(self):
        if self.on_ground and self.velocity.y != 0: self.on_ground = False
        collisions = self.collideswith()
        for collision in collisions:
            if not len(collisions): return
            if self.velocity.y > 0: 
                self.rect.bottom = collision.rect.top
                self.velocity.y = 0
                self.on_ground = True
            elif self.velocity.y < 0:
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