from sprites.base_sprites import ConfirmBox, ButtonImageSprite
import pygame

def quit_game(game_state):
    """Stops the current screen and sets the quit flag so the main loop
    will exit.
    """

     #opens confirmation box allowing user to proceed or cancel
    screen_size = game_state.get('screen_size')
    confirm_quit = ConfirmBox (screen_size[0]/2, screen_size[1]/2 , "Confirm QUIT")
    confirm_quit.active = True
    confirm_quit.event_handle(game_state)
    
    if confirm_quit.proceed != True:
        confirm_quit.proceed == None
        confirm_quit.active = False
        return notify(game_state, 'warn', "You are not a quitter!")
    else:
        confirm_quit.proceed == None
        confirm_quit.active = False

    game_state.update({'quit': True})
    game_state.update({'screen_done': True})
    pygame.mixer.music.stop()
    return game_state

def switch_to_screen(game_state, screen_name):
    """Transition from the current screen to another.
    """
    game_state.update({'active_screen': screen_name})
    game_state.update({'screen_done': True})
    return game_state

def notify(game_state, level, text):
    toast_stack = game_state.get('toast_stack')
    screen_size = game_state.get('screen_size')
    w = screen_size[0] * 0.5
    h = screen_size[1] * 0.1
    toast_stack.push({'level': level, 'text': text})
    return game_state
    