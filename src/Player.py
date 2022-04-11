from Entity import Entity, pygame
from meta import meta
from Fireball import Fireball

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
        elif keys[pygame.K_DOWN] and self.on_top_of_pipe:
            self.enter_pipe()
            self.can_enter_pipe = False
        elif keys[pygame.K_s]:
            self.shoot()
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
        self.kill_delay = 100
        self.on_top_of_pipe = False
        self.can_enter_pipe = True
        self.pipe_dest = (1, 1)
        self.hp = 1
        self.use_iframes = False
        self.iframe_duration = 300
        self.iframe_count = 0
        self.facing_right = True

        self.has_fireflower = False
        self.fireflower_animation_dict = {
            'idle': ['sprite8'],
            'run': ['sprite31', 'sprite49', 'sprite62'],
            'jump': ['sprite91'],
            'die': ['sprite8']
        }
        self.shoot_cd = 30
        self.current_shoot_cd = 0
        self.shooting = False

    def setup_sounds(self):
        self.jump_sound = pygame.mixer.Sound('../resources/sounds/mario_jump_01.mp3')
        self.die_sound = pygame.mixer.Sound('../resources/sounds/mario_die.mp3')
        self.collect_coin_sound = pygame.mixer.Sound('../resources/sounds/collect_coin.mp3')
        self.enter_pipe_sound = pygame.mixer.Sound('../resources/sounds/pipe_enter.mp3')
        self.collect_mushroom_sound = pygame.mixer.Sound('../resources/sounds/mushroom_collect.wav')
        pygame.mixer.Sound.set_volume(self.jump_sound, 0.01)
        pygame.mixer.Sound.set_volume(self.die_sound, 0.07)
        pygame.mixer.Sound.set_volume(self.collect_coin_sound, 0.085)
        pygame.mixer.Sound.set_volume(self.enter_pipe_sound, 0.3)
        pygame.mixer.Sound.set_volume(self.collect_mushroom_sound, 0.3)


    def update(self):
        super().update()
        self.get_input()
        if self.on_ground and self.animation_state == 'jump': self.animation_state = 'idle'
        if abs(self.velocity.x) > 0 and self.animation_state != 'jump': self.animation_state = 'run'
        elif self.animation_state == 'run': self.animation_state = 'idle'
        if not self.alive: self.kill_delay -= 1
        if self.kill_delay <= 0: self.kill(); self.game.reset_game()
        if self.use_iframes:
            self.iframe_count += 1
            if self.iframe_count > self.iframe_duration: 
                self.use_iframes = False; self.iframe_count = 0
                self.toggle_alpha(255)
            if self.iframe_count % 10 == 0:
                self.toggle_alpha(50)
            if self.iframe_count % 20 == 0:
                self.toggle_alpha(255)
        if self.shooting:
            self.current_shoot_cd += 1
            if self.current_shoot_cd >= self.shoot_cd:
                self.shooting = False; self.current_shoot_cd = 0
                

    def toggle_alpha(self, alpha=255):
        for (state, img_list) in self.animation_dict.items():
            for x in range(len(img_list)):
                img_list[x].set_alpha(alpha)

    def jump(self):
        self.velocity.y = -self.jump_height
        self.on_ground = False
        self.animation_state = 'jump'
        pygame.mixer.Sound.play(self.jump_sound)
        self.can_enter_pipe = True

    def collect_collectable(self, collectable):
        n = type(collectable).__name__
        if n == 'Mushroom':
            self.collect_mushroom()
        elif n == 'Fireflower':
            self.collect_fireflower()
        elif n == 'Coin':
            self.collect_coin()

    def collect_fireflower(self):
        self.has_fireflower = True
        self.temp_anim_dict = self.animation_dict.copy()
        self.animation_dict = self.fireflower_animation_dict
        self.load_images()
        self.hp = 3
        self.height = 1.8
        self.setup_image(self.width, self.height, pos=self.rect.topleft)
        pygame.mixer.Sound.play(self.collect_mushroom_sound)

    def collect_coin(self):
        self.game.score += 100
        pygame.mixer.Sound.play(self.collect_coin_sound)
    
    def die(self):
        if self.use_iframes: return
        if self.hp > 1:
            self.hp -= 1
            if self.has_fireflower:
                self.has_fireflower = False
                self.animation_dict = self.temp_anim_dict
                self.hp = 2
                self.height = 1.8
                self.setup_image(self.width, self.height, pos=self.rect.topleft)
            self.use_iframes = True
            if self.hp == 1:
                self.height = 1
                self.setup_image(self.width, self.height, pos=self.rect.topleft)
            return
        self.animation_state = 'die'
        self.handle_collisions = False
        self.alive = False
        pygame.mixer.Sound.play(self.die_sound)
        self.velocity = pygame.Vector2(0, 0)
        self.game.save_highscore()
        self.game.score = 0
    
    def enter_pipe(self):
        if not self.can_enter_pipe: return
        pygame.mixer.Sound.play(self.enter_pipe_sound)
        self.game.load_level(*self.pipe_dest)
    
    def collect_mushroom(self):
        self.hp = 2
        self.height = 1.8
        self.setup_image(self.width, self.height, pos=self.rect.topleft)
        pygame.mixer.Sound.play(self.collect_mushroom_sound)
    
    def shoot(self):
        if not self.has_fireflower or self.shooting: return
        self.shooting = True
        self.game.add_entity(
            Fireball(game=self.game, pos=(self.rect.topleft[0], self.rect.topleft[1]-15))
        )

    
    
