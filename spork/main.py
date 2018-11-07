import pygame

# Importing from sprites/base_sprites.py
from sprites.base_sprites import ImageSprite, ButtonSprite

# Initialise pygame stuff.
pygame.init()
clock = pygame.time.Clock()
game_surface = pygame.display.set_mode((750, 1000))
pygame.display.set_caption('Spork')

# Main group of sprites to display.
all_sprites = pygame.sprite.Group()
all_sprites.add(
    ImageSprite(300, 225, 'w.png'),
    # ImageSprite(490, 363, 'u.png'), # Blue is added by a button click.
    ImageSprite(418, 587, 'b.png'),
    ImageSprite(182, 587, 'r.png'),
    ImageSprite(110, 363, 'g.png'),
)

# Derpy on_click functions for buttons (should live somewhere more
# sensible).
def foo():
    print("foo")
def bar():
    print("bar")
def add_blue():
    all_sprites.add(ImageSprite(490, 363, 'u.png'))

# Add the buttons to the main sprite group.
all_sprites.add(
    ButtonSprite(50, 50, "print foo", foo),
    ButtonSprite(50, 100, "print bar", bar),
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
                    all_sprites.remove(s)
                    all_sprites.add(s)
                
                b = button_at_point(event.pos)
                if b:
                    b.on_click()

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
    

# Run the loop, quit when done.
gameloop()
pygame.quit()
quit()
