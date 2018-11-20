import pygame, os, random, string

# Import helper functions.
from helpers import *


# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite, button_at_point

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit() # Hack to stop sound lagging.
pygame.mixer.init(22050, -16, 2, 1024)

def start_game(game_state):
    game_state.update({
        'active_music': 'Komiku_School.mp3',
        'music_done': True,
    })
    return switch_to_screen(game_state, 'workshop_screen')

def main_menu_loop(game_state):
    """The main menu screen loop.
    """

    game_surface = game_state.get('game_surface')
    clock = game_state.get('clock')
    click = game_state.get('click_sound')
    screen_size = game_state.get('screen_size')
    screen_width = screen_size[0]
    screen_height = screen_size[1]

    toast_stack = game_state.get('toast_stack')

    # Main group of sprites to display.
    all_sprites = pygame.sprite.OrderedUpdates()
    all_sprites.add(
        ButtonSprite(
            (screen_width * 0.5),
            (screen_height * 0.4),
            'Play!',
            start_game,
            [],
        ),
        ButtonSprite(
            (screen_width * 0.5),
            (screen_height * 0.5),
            'Quit',
            quit_game,
            [],
        ),
    )

    # Want to refactor this body into seperate functions.
    while not game_state.get('screen_done'):

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:                
                b = button_at_point(all_sprites, event.pos)
                if b:
                    click.play()
                    game_state = b.on_click(game_state)

        # Update.
        all_sprites.update()
        toast_stack.update()

        # Display.
        game_surface.fill((0, 0, 0))
        all_sprites.draw(game_surface)
        toast_stack.draw(game_surface)
        pygame.display.update()

        clock.tick(60)

    return game_state
