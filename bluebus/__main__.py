import pygame
import json
import objects
import resources
import constants

# initialize screen
screen = resources.init(pygame.Rect(0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

# initialize map and load json data
with open("bluebus/assets/levels/basic-level.tmj") as file:
    map_data = json.load(file)
map = objects.Map("basic-level.png", map_data)

# initialize world
world = objects.World(map)

# initialize bus
speed = 2.3
bus = objects.Bus("bus.png", map.waypoints)

# initialize sprites
bus_group = pygame.sprite.Group(bus)

# draw everything to the screen
world.draw(screen)
pygame.display.flip()

# initialize clock
clock = pygame.time.Clock()

# Event loop
running = True
while running:
    clock.tick(constants.FPS)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey100")

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    world.draw(screen)
    bus_group.update()
    bus_group.draw(screen)
    map.draw_enemies_path()

    # flip() the display to put your work on screen
    pygame.display.flip()
pygame.quit()
