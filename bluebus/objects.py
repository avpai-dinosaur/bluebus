import pygame
from pygame.math import Vector2
from copy import copy
import math
import resources
import constants


class World():
    """Top level class to keep track of all game objects."""

    def __init__(self, map):
        self.map = map
        self.menu = Menu("menu.png", (constants.SCREEN_WIDTH, 0))
        self.enemies = 0
        self.bus_group = pygame.sprite.Group()
        self.turret_group = pygame.sprite.Group()
        self.selected_turret = None
    
    def update(self):
        self.bus_group.update()
        self.turret_group.update(self.bus_group)

    def draw(self, surface):
        surface.blit(self.map.image, (0, 0))
        self.menu.draw(surface)
        self.bus_group.draw(surface)
        for turret in self.turret_group:
            turret.draw(surface)
    
    def handle_mouse_click(self, mouse_pos):
        if (mouse_pos[0] in range(0, constants.SCREEN_WIDTH) and 
                mouse_pos[1] in range(0, constants.SCREEN_HEIGHT)):
                self.clear_selections()
                if self.menu.placing_turrets:
                    self.spawn_turret(mouse_pos)
                else:
                    self.selected_turret = self.select_turret(mouse_pos)

    def spawn_enemy(self):
        if self.enemies == 0:
            new_bus = Bus("bus.png", self.map.waypoints)
            self.bus_group.add(new_bus)
            self.enemies += 1

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
                new_turret = Turret("nerd.png", snapped_pos)
                self.turret_group.add(new_turret)
                print("created turret", new_turret)
    
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
        #use distance to calculate angle
        distance = self.target - self.pos
        self.angle = math.degrees(math.atan2(-distance[1], distance[0]))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


class Turret(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, pos):
        super().__init__()
        
        #animation variables
        self.sprite_sheet, _ = resources.load_png(sprite_sheet)
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # image stuff
        self.original_image = self.animation_list[self.frame_index]
        self.rect = self.original_image.get_rect()
        self.image = self.original_image

        # positioning
        self.pos = pos
        self.tile_pos = (self.pos[0] // constants.COLS, self.pos[1] // constants.ROWS)
        self.rect.center = self.pos

        # Transparent Range background
        self.init_range_background(200, pos)

        # Target tracking
        self.target = None

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
        if (pygame.time.get_ticks() - self.last_shot) > self.cooldown:
            self.play_animation()
        self.pick_target(enemy_group)

    def load_images(self):
        """Extract images from spritesheet."""
        size = self.sprite_sheet.get_height()
        animation_list = []
        for frame in range(0, constants.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(frame * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def play_animation(self):
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks()  - self.update_time > constants.ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                self.last_shot = pygame.time.get_ticks()

    def draw(self, surface):
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
        surface.blit(self.image, self.rect)

    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
        for enemy in enemy_group:
            x_dist = enemy.pos[0] - self.pos[0]
            y_dist = enemy.pos[1] - self.pos[1]
            dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
            if dist < self.range:
                self.target = enemy
                print("target selected")


class Menu():
    def __init__(self, filename, pos):
        self.image, self.rect = resources.load_png(filename)
        self.pos = pos
        self.rect.topleft = self.pos
        self.buttons = [Button("tower-buy-button.png", (constants.SCREEN_WIDTH, constants.HEADER_HEIGHT))]
        self.cancel_button = Button("cancel.png", (constants.SCREEN_WIDTH + 50, constants.HEADER_HEIGHT))
        self.placing_turrets = False
        self.clicked_button = None

    def add_button(self, button):
        self.buttons.append(button)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.placing_turrets:
            if self.clicked_button:
                cursor_pos = pygame.mouse.get_pos()
                cursor_rect = self.clicked_button.image.get_rect()
                cursor_rect.center = cursor_pos
                if (cursor_pos[0] in range(0, constants.SCREEN_WIDTH) and
                    cursor_pos[1] in range(0, constants.SCREEN_HEIGHT)):
                    surface.blit(self.clicked_button.image, cursor_rect)
            self.placing_turrets = not self.cancel_button.draw(surface)
        else:
            for button in self.buttons:
                if button.draw(surface):
                    self.placing_turrets = True
                    self.clicked_button = copy(button)


class Button():
    def __init__(self, filename, pos, single_click=True):
        self.image, self.rect = resources.load_png(filename)
        self.pos = pos
        self.rect.topleft = self.pos
        self.clicked = False
        self.single_click = single_click
    
    def draw(self, surface):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if (pygame.mouse.get_pressed()[0]) and (not self.clicked):
                action = True
                if self.single_click:
                    self.clicked = True
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        surface.blit(self.image, self.rect)
        return action