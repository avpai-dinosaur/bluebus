import pygame
from copy import copy
import resources
import constants
import turret_data
from button import Button


class Menu():
    def __init__(self, filename, pos):
        self.image, self.rect = resources.load_png(filename)
        self.pos = pos
        self.rect.topleft = self.pos
        self.buttons = self.load_buttons()
        self.cancel_button = Button(turret_data.T_CANCEL, (constants.SCREEN_WIDTH + constants.SIDE_PANEL / 2, constants.SCREEN_HEIGHT / 2))
        self.placing_turrets = False
        self.clicked_button = None

    def load_buttons(self):
        buttons = [Button(turret_data.T_NERD, (constants.SCREEN_WIDTH, constants.HEADER_HEIGHT)),
                   Button(turret_data.T_JOCK, (constants.SCREEN_WIDTH + 50, constants.HEADER_HEIGHT)),
                   Button(turret_data.T_SCHLISSEL, (constants.SCREEN_WIDTH + 100, constants.HEADER_HEIGHT))]
        return buttons

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