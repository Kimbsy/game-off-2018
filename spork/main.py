import pygame

# Importing screens
from screens.result_screen import result_loop
from screens.splicer_screen import splicer_loop
from screens.workshop_screen import workshop_loop

# Initialise pygame stuff.
pygame.init()
clock = pygame.time.Clock()
built_sprites = pygame.sprite.Group()
display_width = 1000
display_height = 700
game_surface = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Spork')

game_state = {
    'clock': clock,
    'game_surface': game_surface,
    'active_screen': 'workshop_screen', # TODO: eventually will start at 'main_menu_screen'
    'company_name': 'KimbCass Inc.',
    'screen_done': False,
    'available_funds': 0.01,
    'quit': False,
    'screen_size': (display_width, display_height),
    'active_sprite1': None,
    'active_sprite2': None,
    'built_sprites': built_sprites,
}

done = False

while not done:
    active_screen = game_state.get('active_screen')
    if game_state.get('quit'):
        done = True

    elif active_screen == 'maim_menu_screen':
        pass                # TODO

    elif active_screen == 'workshop_screen':
        game_state.update({'screen_done': False})
        game_state = workshop_loop(game_state)

    elif active_screen == 'splicer_screen':
        game_state.update({'screen_done': False})
        game_state = splicer_loop(game_state)

    elif active_screen == 'packaging_screen':
        pass                # TODO

    elif active_screen == 'result_screen':
        game_state.update({'screen_done': False})
        game_state = result_loop(game_state)

pygame.quit()
quit()
