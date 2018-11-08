import pygame

# Importing from sprites/base_sprites.py
from screens.splicer_screen import splicer_loop
from screens.workshop_screen import workshop_loop

# Initialise pygame stuff.
pygame.init()
clock = pygame.time.Clock()
game_surface = pygame.display.set_mode((750, 1000))
pygame.display.set_caption('Spork')

game_state = {
    'clock': clock,
    'game_surface': game_surface,
    'active_screen': 'workshop_screen',
    'screen_done': False,
    'available_funds': 0.01,
    'quit': False
}

done = False

while not done:
    if game_state.get('quit'):
        done = True
    elif game_state.get('active_screen') == 'workshop_screen':
        game_state.update({'screen_done': False})
        game_state = workshop_loop(game_state)
    elif game_state.get('active_screen') == 'splicer_screen':
        game_state.update({'screen_done': False})
        game_state = splicer_loop(game_state)

pygame.quit()
quit()
