import pygame
from pathlib import Path

def init(screen_rect):
    """Initialize pygame."""
    pygame.init()
    screen = pygame.display.set_mode(size=screen_rect.size)
    pygame.display.set_caption("BLUE BUS")
    pygame.mixer.pre_init(
        frequency=44100,
        size=32,
        # N.B.: 2 here means stereo, not the number of channels to use
        # in the mixer
        channels=2,
        buffer=512,
    )
    pygame.font.init()
    return screen

def load_png(name):
    """Load image and return image object."""
    fullname = Path("bluebus/assets/images/") / name
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image, image.get_rect()