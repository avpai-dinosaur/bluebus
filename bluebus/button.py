import pygame
import resources


class Button():
    def __init__(self, type, pos, single_click=True):
        self.type = type
        self.image = self.load_image(self.type + ".png")
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.clicked = False
        self.single_click = single_click

    def load_image(self, filename):
        """Extract first frame from spritesheet."""
        sprite_sheet, _ = resources.load_png(filename)
        size = sprite_sheet.get_height()
        img = sprite_sheet.subsurface(0, 0, size, size)
        return img
    
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