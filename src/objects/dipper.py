import pygame
from config import HEIGHT
from src.utils.asset_loader import load_image
from pygame import mixer
import random

JUMP_SOUND = None

class Player:
    def __init__(self, x, y):
        global JUMP_SOUND
        self.image = load_image("player.png", size=(40, 40))
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
        self.visible = True  # Para el efecto de parpadeo
        self.blink_timer = 0
        self.has_teleported_in_air = False  

        if not JUMP_SOUND:
            JUMP_SOUND = mixer.Sound("assets/sounds/jump.mp3")

    def update(self, keys=None, joystick=None):
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
            if abs(axis_x) > 0.1:
                dx = axis_x * self.speed * 2
                self.facing_right = axis_x > 0

            if joystick.get_button(0) and self.on_ground:
                self.vel_y = self.jump_force
                self.on_ground = False
                self.has_teleported_in_air = False  
                JUMP_SOUND.play()
                
            if joystick.get_button(3) and not self.teleporting and (self.on_ground or not self.has_teleported_in_air):
                offset = 120  
                self.teleport_target_x = self.rect.x + (offset if self.facing_right else -offset)
                self.teleport_frames = 0
                self.teleporting = True
                self.blink_timer = 0
                
                if not self.on_ground:
                    self.has_teleported_in_air = True  

        self.vel_y += self.gravity
        dy = self.vel_y

        self.rect.x += dx
        self.rect.y += dy
        
        if self.teleporting:
            self.teleport_frames += 1
            self.blink_timer += 1
            
            # Efecto de parpadeo
            if self.blink_timer >= 2:
                self.visible = not self.visible
                self.blink_timer = 0
                
            progress = self.teleport_frames / self.teleport_duration
            if progress >= 1:
                self.rect.x = self.teleport_target_x
                self.teleporting = False
                self.visible = True
            else:
                # Movimiento suave
                start_x = self.rect.x
                end_x = self.teleport_target_x
                self.rect.x = start_x + (end_x - start_x) * 0.1

        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vel_y = 0
            self.on_ground = True
            self.has_teleported_in_air = False
            
    def reset_position(self):
        self.rect.topleft = (100, HEIGHT - 150)
        self.has_teleported_in_air = False  

    def draw(self, screen):
        if self.visible or not self.teleporting:  
            screen.blit(self.image, self.rect)