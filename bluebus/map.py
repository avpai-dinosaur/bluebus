import pygame
from pygame import Vector2
import resources


class Map(pygame.sprite.Sprite):
    """Represents a map in the game."""

    def __init__(self, filename, map_data):
        super().__init__()
        self.image, self.rect = resources.load_png(filename)
        self.area = pygame.display.get_surface().get_rect()
        self.map_data = map_data
        self.tile_data = []
        self.waypoints = []
        self.process_data()

    def process_data(self):
        """Processes json map_data and creates waypoint list"""
        for layer in self.map_data["layers"]:
            if layer["name"] == "Tile Layer 1":
                self.tile_data = layer["data"]
            elif layer["name"] == "waypoints":
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
