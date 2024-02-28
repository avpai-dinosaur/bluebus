import pygame
import resources


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