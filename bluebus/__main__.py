import pygame
import objects
import resources
import constants

# initialize screen
screen = resources.init(pygame.Rect(0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

# initialize map
waypoints = [
    (0, constants.SCREEN_HEIGHT),
    (256, 711),
    (480, 500),
    (680, 480),
    (1050, 450),
    (1100, 400),
    (1240, 120),
    (1240, 0)
]
map = objects.Map("map.png", waypoints)

# initialize bus
speed = 2.3
bus = objects.Bus("bus.png", waypoints, (0.47, speed))

# initialize sprites
bus_group = pygame.sprite.Group(bus)

# blit everything to the screen
screen.blit(map.image, (0, 0))
pygame.display.flip()

# initialize clock
clock = pygame.time.Clock()

# Event loop
running = True
while running:
    clock.tick(constants.FPS)

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.blit(map.image, (0, 0))
    bus_group.update()
    bus_group.draw(screen)
    map.draw_enemies_path()

    # flip() the display to put your work on screen
    pygame.display.flip()
pygame.quit()
