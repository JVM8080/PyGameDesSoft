import pygame
from pygame import mixer
from config import HEIGHT, FPS, SOUND_VOLUME_SFX
from src.utils.asset_loader import load_image
from src.objects.projectile import Projectile, EnergyBall

JUMP_SOUND = None
TELEPORT_SOUND = None
DAMAGE_SOUND = None

class Player:
    def __init__(self, x, y):
        global JUMP_SOUND
        global TELEPORT_SOUND
        global DAMAGE_SOUND
        self.image = load_image("dipper/dipper_parado.png", size=(50, "auto"))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_y = 0
        self.speed = 2
        self.jump_force = -8
        self.gravity = 0.3
        self.on_ground = False
        self.facing_right = True

        self.teleporting = False
        self.teleport_target_x = None
        self.teleport_frames = 0
        self.teleport_duration = 10
        self.visible = True
        self.blink_timer = 0
        self.has_teleported_in_air = False
        self.teleport_cooldown = 0
        self.teleport_cooldown_max = FPS/3

        self.projectiles = []
        self.special_attacks = []
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 20
        self.special_cooldown = 0
        self.special_cooldown_max = 30

        self.use_special_attack = False
        self.prev_toggle_input = False

        self.aim_direction = pygame.math.Vector2(1, 0)  
        self.aim_locked = False  

        self.invulnerable = False

        self.invulnerable_timer = 0
        self.invulnerable_duration = 500  
        
        if not JUMP_SOUND:
            JUMP_SOUND = mixer.Sound("assets/sounds/dipper-jump.mp3")
            
        if not TELEPORT_SOUND:
            TELEPORT_SOUND = mixer.Sound("assets/sounds/dipper-teleport.mp3")
            
        if not DAMAGE_SOUND:
            DAMAGE_SOUND = mixer.Sound("assets/sounds/dipper-death.mp3")

            
        self.image_idle = load_image("dipper/dipper_parado.png", size=(40, "auto"))
        self.anim_right = load_image("dipper/dipper_indo_pra_direita.png")
        self.anim_left = load_image("dipper/dipper_indo_pra_esquerda.png")

        self.frame_width = self.anim_right.get_width() // 3
        self.frame_height = self.anim_right.get_height()

        self.walk_right_frames = [
            self.anim_right.subsurface(i * self.frame_width, 0, self.frame_width, self.frame_height)
            for i in range(3)
        ]
        self.walk_left_frames = [
            self.anim_left.subsurface(i * self.frame_width, 0, self.frame_width, self.frame_height)
            for i in range(3)
        ]

        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_interval = 100 
        
        self.teleport_anim = load_image("dipper/dipper_teleport.png", size=(40*5,40))
        self.teleport_frame_count = 5
        self.teleport_frame_width = self.teleport_anim.get_width() // self.teleport_frame_count
        self.teleport_frame_height = self.teleport_anim.get_height()

        self.teleport_frames_list = [
            self.teleport_anim.subsurface(i * self.teleport_frame_width, 0,
                                        self.teleport_frame_width, self.teleport_frame_height)
            for i in [1, 4]
        ]

        self.current_teleport_frame = 0
        self.teleport_anim_timer = 0
        self.teleport_anim_interval = 5 
        
        self.damage_sheet = load_image("dipper/dipper-death.png", size=(3 * 80, 80))  
        self.damage_frames = []
        for i in range(3):
            frame = self.damage_sheet.subsurface((i * 80, 0, 80, 80))  
            self.damage_frames.append(frame)

        self.playing_damage_animation = False
        self.damage_frame_index = 0
        self.damage_frame_timer = 0
        self.damage_frame_interval = 5  


    def update(self, keys=None, joystick=None, platforms=None):
        if self.playing_damage_animation:
            self.damage_frame_timer += 1
            if self.damage_frame_timer >= self.damage_frame_interval:
                self.damage_frame_timer = 0
                self.damage_frame_index += 1
                if self.damage_frame_index >= len(self.damage_frames):
                    self.playing_damage_animation = False
                    self.damage_frame_index = 0

        dx = 0

        if keys:
            if keys[pygame.K_LEFT]:
                dx = -self.speed
                self.facing_right = False
            if keys[pygame.K_RIGHT]:
                dx = self.speed
                self.facing_right = True

        if joystick:
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)
            self.aim_locked = joystick.get_button(5)  

            movement_vector = pygame.math.Vector2(axis_x, axis_y)

            if movement_vector.length_squared() > 0.1:
                self.aim_direction = self._normalize_to_8_directions(movement_vector)
            else:
                if abs(self.aim_direction.x) < 1 or abs(self.aim_direction.y) > 0:
                    self.aim_direction = pygame.math.Vector2(1 if self.facing_right else -1, 0)


            if not self.aim_locked and abs(axis_x) > 0.1:
                dx = axis_x * self.speed * 2
                self.facing_right = axis_x > 0

            if joystick.get_button(0) and self.on_ground:
                self.vel_y = self.jump_force
                self.on_ground = False
                self.has_teleported_in_air = False
                JUMP_SOUND.set_volume(SOUND_VOLUME_SFX)
                JUMP_SOUND.play()

            if joystick.get_button(3) and not self.teleporting and (self.on_ground or not self.has_teleported_in_air):
                self.activate_teleport()


        self.vel_y += self.gravity
        dy = self.vel_y

        self.rect.x += dx
        self.rect.y += dy
        
        if platforms:
            platform_hits = pygame.sprite.spritecollide(self, platforms, False)
            for platform in platform_hits:
                if self.vel_y >= 0 and self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
        else:
            if self.rect.bottom >= HEIGHT - 50:
                self.rect.bottom = HEIGHT - 50
                self.vel_y = 0
                self.on_ground = True
        
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(800, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(600, self.rect.bottom)

        self.handle_teleport()
        
        now = pygame.time.get_ticks()
        moving = abs(dx) > 0.1
        
        if self.teleporting:
            self.image = self.teleport_frames_list[self.current_teleport_frame]
        elif moving:
            if now - self.last_update > self.frame_interval:
                self.last_update = now
                self.frame_index = (self.frame_index + 1) % len(self.walk_right_frames)

            if self.facing_right:
                self.image = self.walk_right_frames[self.frame_index]
            else:
                self.image = self.walk_left_frames[self.frame_index]
        else:
            self.image = self.image_idle


        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vel_y = 0
            self.on_ground = True
            self.has_teleported_in_air = False

        self.handle_cooldowns()
        self.handle_attacks(keys, joystick)
        self.update_projectiles()
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= 1
        
        if self.invulnerable:
            if pygame.time.get_ticks() - self.invulnerable_timer >= self.invulnerable_duration:
                self.invulnerable = False
                self.visible = True  
            else:
                if not self.teleporting:
                    if pygame.time.get_ticks() - self.blink_timer >= 100:
                        self.visible = not self.visible
                        self.blink_timer = pygame.time.get_ticks()
                else:
                    self.visible = True


    def play_damage_animation(self):
        self.playing_damage_animation = True
        self.damage_frame_index = 0
        self.damage_frame_timer = 0
        DAMAGE_SOUND.set_volume(SOUND_VOLUME_SFX)
        DAMAGE_SOUND.play()


    def activate_invulnerability(self):
        self.invulnerable = True
        self.invulnerable_timer = pygame.time.get_ticks()

    def _normalize_to_8_directions(self, vector):
        x, y = vector.x, vector.y
        direction = pygame.math.Vector2(0, 0)

        if abs(x) > 0.3:
            direction.x = 1 if x > 0 else -1
        if abs(y) > 0.3:
            direction.y = 1 if y > 0 else -1

        if direction.length_squared() > 0:
            return direction.normalize()
        else:
            return pygame.math.Vector2(0, 0)


    def activate_teleport(self):
        if self.teleport_cooldown > 0:
            return  

        offset = 120
        self.teleport_target_x = self.rect.x + (offset if self.facing_right else -offset)
        self.teleport_frames = 0
        self.teleporting = True
        self.teleport_cooldown = self.teleport_cooldown_max 

        if not self.on_ground:
            self.has_teleported_in_air = True
        TELEPORT_SOUND.set_volume(SOUND_VOLUME_SFX)
        TELEPORT_SOUND.play()

        self.activate_invulnerability()

    def handle_teleport(self):
        if self.teleporting:
            self.teleport_frames += 1

            if self.teleport_frames % self.teleport_anim_interval == 0:
                self.current_teleport_frame = (self.current_teleport_frame + 1) % len(self.teleport_frames_list)

            if self.teleport_frames >= self.teleport_duration:
                self.rect.x = self.teleport_target_x
                self.teleporting = False
                self.current_teleport_frame = 0
            else:
                start_x = self.rect.x
                end_x = self.teleport_target_x
                self.rect.x = start_x + (end_x - start_x) * 0.1
                


    def handle_cooldowns(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.special_cooldown > 0:
            self.special_cooldown -= 1

    def handle_attacks(self, keys, joystick):
        toggle_key = keys and keys[pygame.K_a]
        toggle_button = joystick and joystick.get_button(4)  

        toggle_input = toggle_key or toggle_button
        if toggle_input and not self.prev_toggle_input:
            self.use_special_attack = not self.use_special_attack
        self.prev_toggle_input = toggle_input

        shoot_key = keys and keys[pygame.K_z]
        shoot_button = joystick and joystick.get_button(2)

        if shoot_key or shoot_button:
            if self.use_special_attack and self.special_cooldown == 0:
                self.special_attack()
                self.special_cooldown = self.special_cooldown_max
            elif not self.use_special_attack and self.shoot_cooldown == 0:
                self.shoot()
                self.shoot_cooldown = self.shoot_cooldown_max


    def shoot(self):
        if self.aim_direction.length_squared() == 0:
            self.aim_direction = pygame.math.Vector2(1 if self.facing_right else -1, 0)
        x = self.rect.centerx
        y = self.rect.centery
        self.projectiles.append(Projectile(x, y, self.aim_direction))

    def special_attack(self):
        if self.aim_direction.length_squared() == 0:
            self.aim_direction = pygame.math.Vector2(1 if self.facing_right else -1, 0)
        x = self.rect.centerx
        y = self.rect.centery
        self.special_attacks.append(EnergyBall(x, y, self.aim_direction))

    def update_projectiles(self):
        self.projectiles[:] = [p for p in self.projectiles if not p.update()]
        self.special_attacks[:] = [s for s in self.special_attacks if not s.update()]

    def reset_position(self):
        self.rect.topleft = (100, HEIGHT - 150)
        self.has_teleported_in_air = False
        self.projectiles = []
        self.special_attacks = []

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)
        
        if self.teleporting:
            effect_image = self.teleport_frames_list[self.current_teleport_frame]
            effect_rect = effect_image.get_rect(center=self.rect.center)
            screen.blit(effect_image, effect_rect)

        if self.playing_damage_animation:
            damage_image = self.damage_frames[self.damage_frame_index]
            damage_rect = damage_image.get_rect(center=self.rect.center)
            screen.blit(damage_image, damage_rect)

        for projectile in self.projectiles:
            projectile.draw(screen)
        for special in self.special_attacks:
            special.draw(screen)