import pygame
from pygame import Vector2
import math
import resources
import enemy_data


class Bus(pygame.sprite.Sprite):
    """Represents a bus."""

    def __init__(self, world, type, waypoints):
        super().__init__()
        self.world = world
        self.type = type
        self.data = enemy_data.ENEMY_DATA[self.type]

        # image stuff
        self.original_image, self.rect = resources.load_png(self.data["img"])
        self.image = self.original_image
        self.angle = 0

        # bus characteristics
        self.speed = self.data["speed"]
        self.radius = 50
        self.health = self.data["health"]

        # waypoint following
        self.waypoints = [Vector2(point) for point in waypoints]
        self.pos = self.waypoints[0]
        self.target_point = 1
        self.rect.center = self.pos
    
    def update(self):
        if self.health <= 0:
            self.kill()
        else:
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