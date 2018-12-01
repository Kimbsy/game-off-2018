import pygame

"""This module contains utility functions used throughout the game.
"""

#from sprites.base_sprites import ButtonSprite

def top_draggable_sprite_at_point(sprites, pos):
    """Returns a sprite from the sprite group containing the mouse
    position which is draggable.

    Reverses the sprite list so it finds sprites which are 'on top'
    first.
    """
    for sprite in reversed(sprites.sprites()):
        if sprite.is_draggable and sprite.rect.collidepoint(pos):
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

def draw_rects(rect_list, game_surface, colour, fill):
    for rect in rect_list:
        pygame.draw.rect(game_surface, colour , rect, fill)
