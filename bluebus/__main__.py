import pygame
import json
from world import World
from bus import Bus
from map import Map
import resources
import constants

# initialize screen
pygame.init()
screen = resources.init(pygame.Rect(0, 0, constants.SCREEN_WIDTH + constants.SIDE_PANEL, constants.SCREEN_HEIGHT))

# initialize map and load json data
with open("bluebus/assets/levels/basic-level.tmj") as file:
    map_data = json.load(file)
map = Map("basic-level.png", map_data)

# initialize world
world = World(map)

# initialize bus
speed = 2.3
bus = Bus("bus.png", map.waypoints)

# initialize sprites
bus_group = pygame.sprite.Group(bus)
turret_group = pygame.sprite.Group()

# draw everything to the screen
world.draw(screen)
pygame.display.flip()

# initialize clock
clock = pygame.time.Clock()

# Event loop
running = True
while running:
    clock.tick(constants.FPS)

    ###----------UPDATING SECTION----------###

    # poll for events
    # pygame.QUIT event means the user clicked X to close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            mouse_pos = pygame.mouse.get_pos()
            world.handle_mouse_click(mouse_pos)
    
    if world.menu.running_level:
        world.run_level(2)
    world.update()

    ###----------DRAW SECTION----------###

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey100")
    world.draw(screen)
    # map.draw_enemies_path()
    pygame.display.flip()

pygame.quit()
