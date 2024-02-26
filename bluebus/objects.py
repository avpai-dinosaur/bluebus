import pygame
from pygame.math import Vector2
import math
import resources

class Map(pygame.sprite.Sprite):
    """Represents a map in the game."""

    def __init__(self, filename, waypoints):
        super().__init__()
        self.image, self.rect = resources.load_png(filename)
        self.area = pygame.display.get_surface().get_rect()
        self.waypoints = [Vector2(point) for point in waypoints]
    
    def draw_enemies_path(self):
        screen = pygame.display.get_surface()
        pygame.draw.lines(screen, (0, 0, 0), False, self.waypoints)


class Bus(pygame.sprite.Sprite):
    """Represents a bus."""

    def __init__(self, filename, waypoints, vector):
        super().__init__()
        self.original_image, self.rect = resources.load_png(filename)
        self.image = self.original_image
        self.angle = 0
        self.speed = 2
        self.waypoints = [Vector2(point) for point in waypoints]
        self.pos = self.waypoints[0]
        self.target_point = 1
        self.rect.center = self.pos
        self.area = pygame.display.get_surface().get_rect()
    
    def update(self):
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
            self.kill()

    def rotate(self):
        distance = self.target - self.pos
        self.angle = distance.angle_to(Vector2(0, 0))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
