import pygame
import math
import resources
import constants
from bullet import Bullet


class Turret(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, pos):
        super().__init__()
        
        #animation variables
        self.sprite_sheet, _ = resources.load_png(sprite_sheet)
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # image stuff
        self.angle = 270
        self.original_image = self.animation_list[self.frame_index]
        self.rect = self.original_image.get_rect()
        self.image = self.original_image

        # positioning
        self.pos = pos
        self.tile_pos = (self.pos[0] // constants.COLS, self.pos[1] // constants.ROWS)
        self.rect.center = self.pos

        # Transparent Range background
        self.init_range_background(200, pos)

        # Target tracking and shooting
        self.target = None
        self.bullet_group = pygame.sprite.Group()
        self.just_shot = False

        # Turret characteristics
        self.cooldown = 1500
        self.last_shot = pygame.time.get_ticks()

    def init_range_background(self, range, pos):
        self.range = range
        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = pos
        self.selected = False

    def update(self, enemy_group):
        if self.target:
            if (pygame.time.get_ticks() - self.last_shot) > self.cooldown:
                self.play_animation()
                if (self.frame_index == 4) and (not self.just_shot):
                    self.shoot_target()
                    self.just_shot  = True
        else:
            self.just_shot = False
            if (pygame.time.get_ticks() - self.last_shot) > self.cooldown:
                self.pick_target(enemy_group)
        for bullet in self.bullet_group:
            bullet.update()

    def load_images(self):
        """Extract images from spritesheet."""
        size = self.sprite_sheet.get_height()
        animation_list = []
        for frame in range(0, constants.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(frame * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def play_animation(self):
        self.original_image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks()  - self.update_time > constants.ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                self.last_shot = pygame.time.get_ticks()
                self.target = None

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle - 270)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
        surface.blit(self.image, self.rect)
        self.bullet_group.draw(surface)

    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
        for enemy in enemy_group:
            x_dist = enemy.pos[0] - self.pos[0]
            y_dist = enemy.pos[1] - self.pos[1]
            dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
            if dist < self.range:
                self.target = enemy
                self.angle = math.degrees(math.atan2(-y_dist, x_dist))
    
    def shoot_target(self):
        trajectory = pygame.Vector2((self.target.pos[0] - self.pos[0], self.target.pos[1] - self.pos[1]))
        new_bullet = Bullet("football.png", self.pos, self, self.target, trajectory)
        self.bullet_group.add(new_bullet)