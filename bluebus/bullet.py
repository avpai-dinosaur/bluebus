import pygame
import math
import resources


class Bullet(pygame.sprite.Sprite):
    def __init__(self, filename, pos, owner, target):
        super().__init__()
        self.original_image, self.rect = resources.load_png(filename)
        self.pos = pygame.Vector2(pos)
        self.rect.center = self.pos
        self.owner = owner
        self.target = target
        
        # Rotate bullet
        self.trajectory = pygame.Vector2((self.target.pos[0] - self.pos[0], self.target.pos[1] - self.pos[1]))
        self.angle = math.degrees(math.atan2(-self.trajectory[1], self.trajectory[0]) - 90)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        
        # Bullet Characteristics
        self.speed = 7
        self.radius = 20

    def update(self):
        self.move(self.trajectory)

    def move(self, trajectory):
        x_dist = self.pos[0] - self.owner.pos[0]
        y_dist = self.pos[1] - self.owner.pos[1]
        distance = math.sqrt(x_dist ** 2 + y_dist ** 2)
        if pygame.sprite.collide_circle(self.target, self):
            self.kill()
        elif distance > self.owner.range:
            self.kill()
        else:
            self.pos += trajectory.normalize() * self.speed
        self.rect = self.image.get_rect()
        self.rect.center = self.pos