import pygame

# Import helper functions.
from helpers import *

# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite

pygame.init()

# Main group of sprites to display.
all_sprites = pygame.sprite.Group()
all_sprites.add(
    ImageSprite(300, 225, 'w.png'),
    ButtonSprite(50, 50, 'Splice!', switch_to_screen, ['splicer_screen']),
    ButtonSprite(50, 100, 'QUIT', quit_game, []),
)

def workshop_loop(game_state):
    """The workshop screen loop.
    """

    # Want to move these elsewhere/design them away.
    dragging = False
    dragged_sprite = None

    game_surface = game_state.get('game_surface')

    # Want to refactor this body into seperate functions.
    while not game_state.get('screen_done'):

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                s = top_draggable_sprite_at_point(all_sprites, event.pos)
                if s:
                    dragging = True
                    dragged_sprite = s
                    all_sprites.remove(s)
                    all_sprites.add(s)
                
                b = button_at_point(all_sprites, event.pos)
                if b:
                    game_state = b.on_click(game_state)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    dragged_sprite = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dragged_sprite.move(event.rel)

        # Display.
        game_surface.fill((0, 0, 0))
        all_sprites.draw(game_surface)
        pygame.display.update()

    return game_state
