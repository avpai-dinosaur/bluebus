import pygame
from copy import copy
import resources
import constants
import turret_data
from button import Button


class Menu():
    """Represents in-game menu from which to buy/sell turrets and start levels."""
    def __init__(self, filename, pos):
        # image stuff
        self.image, self.rect = resources.load_png(filename)
        self.pos = pos
        self.rect.topleft = self.pos

        # fonts
        self.text_font = pygame.font.SysFont("Consolas", 20, bold=True)
        self.large_font = pygame.font.SysFont("Consolas", 36, bold=False)

        # butons
        self.turret_buttons = self.load_turret_buttons()
        self.start_level_button = Button(constants.B_START, 
                                         (constants.SCREEN_WIDTH + 50, constants.HEADER_HEIGHT + 550))
        self.cancel_button = Button(constants.B_CANCEL, 
                                    (constants.SCREEN_WIDTH + 250, constants.HEADER_HEIGHT + 550))
        self.restart_button = Button(constants.B_RESTART, 
                                     (constants.SCREEN_WIDTH + constants.SIDE_PANEL / 2, constants.SCREEN_HEIGHT / 2))
        
        # State variables
        self.placing_turrets = False
        self.running_level = False
        self.clicked_button = None
        self.hovered_button = None

        # Game info
        self.health = constants.HEALTH
        self.money = constants.MONEY
        self.level = 1

    def load_turret_buttons(self):
        buttons = [Button(turret_data.T_NERD, (constants.SCREEN_WIDTH + 50, constants.HEADER_HEIGHT + 50)),
                   Button(turret_data.T_JOCK, (constants.SCREEN_WIDTH + 150, constants.HEADER_HEIGHT + 50)),
                   Button(turret_data.T_SCHLISSEL, (constants.SCREEN_WIDTH + 250, constants.HEADER_HEIGHT + 50))]
        return buttons

    def create_turret_range_image(self, range):
        range_img = pygame.Surface((range * 2, range * 2))
        range_img.fill((0, 0, 0))
        range_img.set_colorkey((0, 0, 0))
        pygame.draw.circle(range_img, "grey100", (range, range), range)
        range_img.set_alpha(100)
        range_rect = range_img.get_rect()
        return (range_img, range_rect)

    def draw_buttons(self, surface):
        if self.placing_turrets:
            for button in self.turret_buttons:
                button.draw(surface)
            if self.clicked_button:
                cursor_pos = pygame.mouse.get_pos()
                cursor_rect = self.clicked_button.image.get_rect()
                cursor_rect.center = cursor_pos
                turret_range = turret_data.TURRET_DATA[self.clicked_button.type]["upgrades"][0]["range"]
                range_img, range_rect = self.create_turret_range_image(turret_range)
                if (cursor_pos[0] in range(0, constants.SCREEN_WIDTH) and
                    cursor_pos[1] in range(0, constants.SCREEN_HEIGHT)):
                    range_rect.center = cursor_pos
                    surface.blit(range_img, range_rect)
                    surface.blit(self.clicked_button.image, cursor_rect)
            self.placing_turrets = not self.cancel_button.draw(surface)[0]
        else:
            for button in self.turret_buttons:
                if button.draw(surface)[0]:
                    self.placing_turrets = True
                    self.clicked_button = copy(button)
                elif button.draw(surface)[1]:
                    self.hovered_button = copy(button)
            if not self.running_level:
                if self.start_level_button.draw(surface)[0]:
                    self.running_level = True

    def draw_text(self, surface, text, font, color, pos):
        img = font.render(text, True, color)
        surface.blit(img, pos)

    def draw_tower_info(self, surface, type, font, color, pos):
        self.draw_text(surface, str(type), font, color, pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_buttons(surface)
        self.draw_text(surface, str(self.health), self.text_font, (0, 0, 0), (constants.SCREEN_WIDTH + 50, 15))
        self.draw_text(surface, str(self.money), self.text_font, (0, 0, 0), (constants.SCREEN_WIDTH + 50, 60))
        self.draw_text(surface, str(self.level), self.large_font, (0, 0, 0), 
                       (constants.SCREEN_WIDTH + 140, constants.HEADER_HEIGHT + 530))
        if self.hovered_button:
            self.draw_tower_info(surface, self.hovered_button.type, self.text_font, (0, 0, 0), (constants.SCREEN_WIDTH + 10, constants.HEADER_HEIGHT + 210))