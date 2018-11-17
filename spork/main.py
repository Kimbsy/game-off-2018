import pygame, os

# Importing screens
from screens.result_screen import result_loop
from screens.splicer_screen import splicer_loop
from screens.workshop_screen import workshop_loop

# Initialise pygame stuff.
pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit() # Hack to stop sound lagging.
pygame.mixer.init(22050, -16, 2, 1024)
clock = pygame.time.Clock()
built_sprites = pygame.sprite.OrderedUpdates()
display_width = 1200
display_height = 675
game_surface = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Spork')

game_state = {
    'clock': clock,
    'game_surface': game_surface,
    'click_sound': pygame.mixer.Sound(os.getcwd() + '/data/sounds/click.wav'),
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
