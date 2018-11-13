import pygame
import os
from helpers import *

# Importing from sprites/base_sprites.py
from sprites.base_sprites import ImageSprite, ButtonSprite, ThumbnailSprite

pygame.init()



def switch_to_splicer(game_state):
    game_state.update({'active_screen': 'splicer_screen'})
    game_state.update({'screen_done': True})
    return game_state
def quit_game(game_state):
    game_state.update({'quit': True})
    game_state.update({'screen_done': True})
    return game_state

def add_to_workbench(game_state, item_file):

    if not game_state.get('left_item'):
        game_state.update({'left_item': item_file})
        all_sprites.add(ImageSprite(200, 300, item_file))

    elif not game_state.get('right_item'):
        game_state.update({'right_item': item_file})
        all_sprites.add(ImageSprite(400, 300, item_file))

    else:
        print('You can only have 2 items')

    return game_state

def remove_workbench_item(game_state):

    game_state.update({'left_item': None})
    #game_state.update({'right_item': None})

    return game_state


# Main group of sprites to display.
all_sprites = pygame.sprite.Group()
all_sprites.add(
    #ImageSprite(300, 225, 'w.png'),
    ThumbnailSprite(50, 200, 'pixel-components/pixel-bike.png'),    
    ButtonSprite(450, 250, 'Splice!', switch_to_splicer, []),
    ButtonSprite(50, 100, 'QUIT', quit_game, []),
    ButtonSprite(200, 300, 'X', remove_workbench_item, []),
    #ButtonSprite(400, 300, 'X', remove_workbench_item, [right_sprite]),
)

items = os.listdir(os.getcwd() + '/data/pixel-components')
x = 50
y = 10

for item in items:

    item_file = 'pixel-components/' + item

    all_sprites.add(ThumbnailSprite(x, y, item_file))

    y += 25
    
    item_text = item[6:-4]

    all_sprites.add(ButtonSprite(x + 50, y, item_text, add_to_workbench, [item_file]))





def top_draggable_sprite_at_point(pos):
    """Returns a sprite from the main sprite group containing the mouse
    position which is draggable.

    Reverses the sprite list so it finds sprites which
    are 'on top' first.
    """
    for sprite in reversed(all_sprites.sprites()):
        if sprite.is_draggable and sprite.rect.collidepoint(pos):
            return sprite

def button_at_point(pos):
    """Returns a sprite from the main sprite group containing the mouse
    position which is of type ButtonSprite.

    Buttons won't overlap so we don't need to reverse the group.
    """
    for sprite in all_sprites.sprites():
        if (type(sprite) is ButtonSprite) and sprite.rect.collidepoint(pos):
            return sprite

def workshop_loop(game_state):
    """The workshop screen loop.
    """

    # Want to move these elsewhere/design them away.
    dragging = False
    dragged_sprite = None

    game_surface = game_state.get('game_surface')
    size = game_state.get('screen_size')
    screen_width = size[0]
    screen_height = size[1]

    # Want to refactor this body into seperate functions.
    while not game_state.get('screen_done'):

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                s = top_draggable_sprite_at_point(event.pos)
                if s:
                    dragging = True
                    dragged_sprite = s
                    all_sprites.remove(s)
                    all_sprites.add(s)
                
                b = button_at_point(event.pos)
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