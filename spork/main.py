import pygame

# Importing from sprites/base_sprites.py
from sprites.base_sprites import ImageSprite

# Initialise pygame stuff.
pygame.init()
clock = pygame.time.Clock()
game_display = pygame.display.set_mode((750, 1000))
pygame.display.set_caption('foo')

# Global list of sprites to display.
sprites = [
    ImageSprite(300, 225, 'w.png'),
    ImageSprite(490, 363, 'u.png'),
    ImageSprite(418, 587, 'b.png'),
    ImageSprite(182, 587, 'r.png'),
    ImageSprite(110, 363, 'g.png'),
]

def top_draggable_sprite_at_point(pos):
    """Checks if there is a sprite in the global sprite
    list under the mouse position which is draggable.

    Reverses the sprite list so it finds sprites which
    are 'on top' first.
    """
    for sprite in reversed(sprites):
        if sprite.is_draggable and sprite.get_rect().collidepoint(pos):
            return sprite

def gameloop():
    """The main game loop.
    """

    # Want to move these elsewhere/design them away.
    done = False
    dragging = False
    dragged_sprite = None

    # Want to refactor this body into seperate functions.
    while not done:

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                s = top_draggable_sprite_at_point(event.pos)
                if s:
                    dragging = True
                    dragged_sprite = s
                    sprites.remove(s)
                    sprites.append(s)

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                dragged_sprite = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    pos = dragged_sprite.pos
                    rel = event.rel
                    dragged_sprite.pos = (pos[0] + rel[0], pos[1] + rel[1])
        
        # Display.
        game_display.fill((0, 0, 0))

        for sprite in sprites:
            sprite.display(game_display)

        pygame.display.update()
    

# Run the loop, quit when done.
gameloop()
pygame.quit()
quit()
