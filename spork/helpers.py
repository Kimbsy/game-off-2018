import pygame

"""This module contains utility functions used throughout the game.
"""

from sprites.base_sprites import ButtonSprite

def quit_game(game_state):
    """Stops the current screen and sets the quit flag so the main loop
    will exit.
    """
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

def top_draggable_sprite_at_point(sprites, pos):
    """Returns a sprite from the sprite gruop containing the mouse
    position which is draggable.

    Reverses the sprite list so it finds sprites which are 'on top'
    first.
    """
    for sprite in reversed(sprites.sprites()):
        if sprite.is_draggable and sprite.rect.collidepoint(pos):
            return sprite

def button_at_point(sprites, pos):
    """Returns a sprite from the sprite group containing the mouse
    position which is of type ButtonSprite.

    Buttons won't overlap so we don't need to reverse the group.
    """
    for sprite in sprites.sprites():
        if (type(sprite) is ButtonSprite) and sprite.rect.collidepoint(pos):
            return sprite

def aspect_scale(img, target):
    """Scales 'img' to fit into box bx/by.  This method will retain the
     original image's aspect ratio
    """
    bx, by = target
    ix, iy = img.get_size()
    if ix > iy:
        # Fit to width.
        scale_factor = bx / float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # Fit to height.
        scale_factor = by / float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx / float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (int(sx), int(sy)))
