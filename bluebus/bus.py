import pygame
from pygame import Vector2
import math
import resources


class Bus(pygame.sprite.Sprite):
    """Represents a bus."""

    def __init__(self, filename, waypoints):
        super().__init__()
        self.original_image, self.rect = resources.load_png(filename)
        self.image = self.original_image
        self.angle = 0
        self.speed = 2
        self.radius = 50
        self.waypoints = [Vector2(point) for point in waypoints]
        self.pos = self.waypoints[0]
        self.target_point = 1
        self.rect.center = self.pos
        self.area = pygame.display.get_surface().get_rect()
        self.health = 10
    
    def update(self):
        self.move()
        self.rotate()

    def move(self):
        if self.health <= 0:
            self.kill()
        elif self.target_point != len(self.waypoints):
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
            self.kill()

    def rotate(self):
        #use distance to calculate angle
        distance = self.target - self.pos
        self.angle = math.degrees(math.atan2(-distance[1], distance[0]))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos