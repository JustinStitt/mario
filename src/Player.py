from Entity import Entity, pygame
from meta import meta

class PlayerControlled():
    def __init__(self, move_speed=.1):
        self.base_speed = move_speed
        self.adjust_speed()
        self.left = [pygame.K_LEFT, pygame.K_a]
        self.right = [pygame.K_RIGHT, pygame.K_d]
        self.up = [pygame.K_UP, pygame.K_w]
        self.down = [pygame.K_DOWN, pygame.K_s]
        self.facing_right = True

    def adjust_speed(self):
        self.move_speed = meta.screen.CELL_WIDTH * self.base_speed + 1
        self.jump_height = meta.screen.CELL_HEIGHT / 4

    def get_input(self):
        if not self.alive: return
        ms = self.move_speed
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_RIGHT]:
            self.velocity.x = ms
            if not self.facing_right:
                self.flip_animation()
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.velocity.x = -ms
            if self.facing_right:
                self.flip_animation()
            self.facing_right = False
        else:
            self.velocity.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def handle_mouse(self, event):
        self.collideswith()

    def flip_animation(self):
        for (state, img_list) in self.animation_dict.items():
                    for x in range(len(img_list)):
                        img_list[x] = pygame.transform.flip(img_list[x], True, False)

class Player(Entity, PlayerControlled):
    def __init__(self, game, pos = (0, 0), width=.8, height=1):
        Entity.__init__(self, game=game, pos=pos, width=width, 
                          height=height, uses_gravity=True, 
                            handle_collisions=True, uses_spritesheet=True, 
                            animation_delay = 5,
                            animation_dict={
                                'idle': ['mario_idle'],
                                'run': ['mario_run3', 'mario_run2', 'mario_run1'],
                                'jump': ['mario_jump'],
                                'die': ['mario_die']
                                },
                            starting_animation_state='idle')
        PlayerControlled.__init__(self)
        self.adjust_speed()
        self.setup_sounds()
        self.alive = True

    def setup_sounds(self):
        self.jump_sound = pygame.mixer.Sound('../resources/sounds/mario_jump_01.mp3')
        self.die_sound = pygame.mixer.Sound('../resources/sounds/mario_die.mp3')
        pygame.mixer.Sound.set_volume(self.jump_sound, 0.01)
        pygame.mixer.Sound.set_volume(self.die_sound, 0.07)

    def update(self):
        super().update()
        self.get_input()
        if self.on_ground and self.animation_state == 'jump': self.animation_state = 'idle'
        if abs(self.velocity.x) > 0 and self.animation_state != 'jump': self.animation_state = 'run'
        elif self.animation_state == 'run': self.animation_state = 'idle'

    def jump(self):
        self.velocity.y = -self.jump_height
        self.on_ground = False
        self.animation_state = 'jump'
        pygame.mixer.Sound.play(self.jump_sound)
        print(f'player jump!', flush=True)
    
    def die(self):
        self.animation_state = 'die'
        self.handle_collisions = False
        self.alive = False
        pygame.mixer.Sound.play(self.die_sound)
        self.velocity = pygame.Vector2(0, 0)
    
    
    
