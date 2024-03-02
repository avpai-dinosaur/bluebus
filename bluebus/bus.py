import pygame
from pygame import Vector2
import math
import constants
import resources
import enemy_data


class Bus(pygame.sprite.Sprite):
    """Represents a bus."""

    def __init__(self, world, type, waypoints):
        super().__init__()
        self.world = world
        self.type = type
        self.data = enemy_data.ENEMY_DATA[self.type]

        #animation variables
        self.sprite_sheet, _ = resources.load_png(self.data["img"])
        self.animation_list = resources.load_animation(self.sprite_sheet, 
                                                       self.sprite_sheet.get_height() * 2,
                                                       self.sprite_sheet.get_height())
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # image stuff
        self.original_image = self.animation_list[self.frame_index]
        self.rect = self.original_image.get_rect()
        self.image = self.original_image
        self.angle = 0

        # bus characteristics
        self.speed = self.data["speed"]
        self.radius = 50
        self.health = self.data["health"]
        self.money_return = self.health

        # waypoint following
        self.waypoints = [Vector2(point) for point in waypoints]
        self.pos = self.waypoints[0]
        self.target_point = 1
        self.rect.center = self.pos
    
    def update(self):
        if self.health <= 0:
            self.world.menu.money += self.money_return
            self.kill()
        else:
            self.play_animation()
            self.move()
            self.rotate()

    def move(self):
        if self.target_point != len(self.waypoints):
            self.target = self.waypoints[self.target_point]
            self.movement = self.target - self.pos

            # calculate distance to next waypoint
            distance = self.movement.length()
            if distance >= self.speed:
                self.pos += self.movement.normalize() * self.speed
            else:
                if distance != 0:
                    self.pos += self.movement.normalize() * distance
                self.target_point += 1
        else:
            self.world.menu.health -= self.health
            self.kill()

    def rotate(self):
        #use distance to calculate angle
        distance = self.target - self.pos
        self.angle = math.degrees(math.atan2(-distance[1], distance[0]))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    def play_animation(self):
        self.original_image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks()  - self.update_time > constants.ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0