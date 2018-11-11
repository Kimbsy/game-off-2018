import pygame

# Import helper functions.
from helpers import *

# Import sprites.
from sprites.base_sprites import BaseSprite, ImageSprite, ButtonSprite

pygame.init()

class NewspaperSprite(BaseSprite):
    """This sprite contains the reviews of the product.
    """

    def __init__(self, x, y):
        # Call the parent constructor
        super(NewspaperSprite, self).__init__(x, y)

    def init_image(self):
        self.image = pygame.Surface((200, 150))
        self.image.fill((150, 150, 150))

def result_loop(game_state):
    """The result screen loop.
    """

    # Main group of sprites to display.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(
        NewspaperSprite(100, 200),
        ButtonSprite(50, 50, 'Awesome!', switch_to_screen, ['workshop_screen']),
    )

    game_surface = game_state.get('game_surface')

    # Want to refactor this body into seperate functions.
    while not game_state.get('screen_done'):

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:                
                b = button_at_point(all_sprites, event.pos)
                if b:
                    game_state = b.on_click(game_state)

        # Display.
        game_surface.fill((0, 0, 0))
        all_sprites.draw(game_surface)
        pygame.display.update()

    return game_state
