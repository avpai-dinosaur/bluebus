import pygame
from pygame.math import Vector2
from copy import copy
import math
import resources
import constants
import turret_data
import enemy_data
from turret import Turret
from bus import Bus
from map import Map
from menu import Menu
from button import Button


class World():
    """Top level class to keep track of all game objects."""

    def __init__(self, map):
        # map stuff
        self.map = map
        self.menu = Menu("menu.png", (constants.SCREEN_WIDTH, 0))
        self.game_over_img, _ = resources.load_png("game-over.png")

        # level info
        self.num_levels = len(enemy_data.ENEMY_SPAWN_DATA)
        self.spawned_enemies = 0
        self.bus_group = pygame.sprite.Group()
        self.turret_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.last_enemy_spawn = None

        # state variables
        self.selected_turret = None

        # game info
        self.game_over = False
        self.game_outcome = 0

    def update(self):
        self.bus_group.update()
        self.turret_group.update(self.bus_group)

    def draw(self, surface):
        surface.blit(self.map.image, (0, 0))
        self.menu.draw(surface)
        self.bus_group.draw(surface)
        for turret in self.turret_group:
            turret.draw(surface)
        if self.game_outcome == -1:
            surface.blit(self.game_over_img, (constants.SCREEN_WIDTH / 4, constants.SCREEN_HEIGHT / 4))
    
    def handle_mouse_click(self, mouse_pos):
        if (mouse_pos[0] in range(0, constants.SCREEN_WIDTH) and 
                mouse_pos[1] in range(0, constants.SCREEN_HEIGHT)):
                self.clear_selections()
                if self.menu.placing_turrets:
                    self.spawn_turret(mouse_pos)
                else:
                    self.selected_turret = self.select_turret(mouse_pos)

    def spawn_enemy(self, enemy_type):
        if self.last_enemy_spawn:
            if (pygame.time.get_ticks() - self.last_enemy_spawn) > constants.SPAWN_COOLDOWN: 
                new_bus = Bus(self, enemy_type, self.map.waypoints)
                self.bus_group.add(new_bus)
                self.last_enemy_spawn = pygame.time.get_ticks()
                self.spawned_enemies += 1
        else:
            new_bus = Bus(self, enemy_type, self.map.waypoints)
            self.bus_group.add(new_bus)
            self.last_enemy_spawn = pygame.time.get_ticks()
            self.spawned_enemies += 1

    def process_enemy_list(self, spawn_dict):
        enemies = []
        for enemy_type in spawn_dict:
            num_type = spawn_dict[enemy_type]
            for _ in range(0, num_type):
                enemies.append(enemy_type)
        return enemies

    def run_next_level(self):
        spawn_list = self.process_enemy_list(enemy_data.ENEMY_SPAWN_DATA[self.menu.level - 1])
        num_enemies = len(spawn_list)
        if self.spawned_enemies >= num_enemies:
            if len(self.bus_group.sprites()) == 0:
                self.menu.running_level = False
                self.spawned_enemies = 0
                self.menu.money += 100 + 20 * (self.menu.level - 1)
                self.menu.level += 1
        else:
            self.spawn_enemy(spawn_list[self.spawned_enemies])

    def spawn_turret(self, mouse_pos):
        # snap mouse click to the grid
        index, snapped_pos = resources.grid_snap(mouse_pos)
        # check that tile is not road
        if (self.map.tile_data[index] == constants.BUILDABLE):
            is_occupied = False
            for turret in self.turret_group:
                if turret.pos == snapped_pos:
                    is_occupied = True
            if not is_occupied and self.menu.placing_turrets:
                new_turret = Turret(self.menu.clicked_button.type, snapped_pos)
                if self.menu.money >= new_turret.cost:
                    self.turret_group.add(new_turret)
                    self.menu.money -= new_turret.cost
    
    def select_turret(self, mouse_pos):
        tile_pos = (mouse_pos[0] // constants.COLS, mouse_pos[1] // constants.ROWS)
        for turret in self.turret_group:
            if tile_pos == turret.tile_pos:
                if turret.selected:
                    turret.selected = False
                    return None
                else:
                    turret.selected = True
                    return turret
        return None

    def clear_selections(self):
        self.selected_turret = None
        for turret in self.turret_group:
            turret.selected = False