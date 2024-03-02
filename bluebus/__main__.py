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
with open("bluebus/assets/levels/purple-road.tmj") as file:
    map_data = json.load(file)
map = Map("purple-road.png", map_data)

# initialize world
world = World(map)

# draw everything to the screen
world.draw(screen)
pygame.display.flip()

# initialize clock
clock = pygame.time.Clock()

# Event loop
running = True
while running:
    clock.tick(constants.FPS)

    # poll for events
    # pygame.QUIT event means the user clicked X to close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            mouse_pos = pygame.mouse.get_pos()
            world.handle_mouse_click(mouse_pos)
    
    # check if game is over
    if not world.game_over:
        if world.menu.running_level and world.menu.level <= world.num_levels:
            world.run_next_level()
        world.update()
        if world.menu.health <= 0:
            world.game_over = True
            world.game_outcome = -1
        elif world.menu.level > world.num_levels:
            world.game_over = True
            world.game_outcome = 1

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey100")
    world.draw(screen)
    pygame.display.flip()

pygame.quit()
