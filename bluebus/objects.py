import pygame
from pygame.math import Vector2
import math
import resources

class World():
    """Top level class to load levels and maps."""

    def __init__(self, map):
        self.map = map
        self.enemies = 0
        self.bus_group = pygame.sprite.Group()
        self.turret_group = pygame.sprite.Group()
    
    def update(self):
        self.bus_group.update()
        self.turret_group.update()

    def draw(self, surface):
        surface.blit(self.map.image, (0, 0))
        self.bus_group.draw(surface)
        self.turret_group.draw(surface)
    
    def spawn_enemy(self):
        if self.enemies == 0:
            new_bus = Bus("bus.png", self.map.waypoints)
            self.bus_group.add(new_bus)
            self.enemies += 1

    def spawn_turret(self, mouse_pos):
        new_turret = Turret("tower.png", mouse_pos)
        self.turret_group.add(new_turret)



class Map(pygame.sprite.Sprite):
    """Represents a map in the game."""

    def __init__(self, filename, map_data):
        super().__init__()
        self.image, self.rect = resources.load_png(filename)
        self.area = pygame.display.get_surface().get_rect()
        self.map_data = map_data
        self.waypoints = []
        self.process_data()

    def process_data(self):
        """Processes json map_data and creates waypoint list"""
        for layer in self.map_data["layers"]:
            if layer["name"] == "waypoints":
                waypoint_data = layer["objects"][0]["polyline"]
                self.process_waypoints(waypoint_data)

    def process_waypoints(self, waypoint_data):
        """Helper function for process_data. 
        Processes list of dictionaries of waypoint coordinates"""
        for datum in waypoint_data:
            self.waypoints.append(Vector2((datum.get("x"), datum.get("y"))))

    def draw_enemies_path(self):
        screen = pygame.display.get_surface()
        pygame.draw.lines(screen, (0, 0, 0), False, self.waypoints)


class Bus(pygame.sprite.Sprite):
    """Represents a bus."""

    def __init__(self, filename, waypoints):
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
        #use distance to calculate angle
        self.angle = math.degrees(math.atan2(-distance[1], distance[0]))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

class Turret(pygame.sprite.Sprite):
    def __init__(self, filename, pos):
        super().__init__()
        self.original_image, self.rect = resources.load_png(filename)
        self.image = self.original_image
        self.pos = pos
        self.rect.center = self.pos