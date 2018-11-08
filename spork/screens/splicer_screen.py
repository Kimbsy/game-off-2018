import pygame

# Importing from sprites/base_sprites.py
from sprites.base_sprites import ImageSprite, ButtonSprite

pygame.init()

def switch_to_workshop(game_state):
    game_state.update({'active_screen': 'workshop_screen'})
    game_state.update({'screen_done': True})
    return game_state
def quit_game(game_state):
    game_state.update({'quit': True})
    game_state.update({'screen_done': True})
    return game_state
def add_blue(game_state):
    all_sprites.add(ImageSprite(490, 363, 'u.png'))
    return game_state

# Main group of sprites to display.
all_sprites = pygame.sprite.Group()
all_sprites.add(
    ImageSprite(490, 363, 'u.png'),
    ButtonSprite(50, 50, 'Workshop!', switch_to_workshop),
    ButtonSprite(50, 100, 'QUIT', quit_game),
    ButtonSprite(50, 150, "add blue", add_blue),
)

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

def splicer_loop(game_state):
    """The splicer screen loop.
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