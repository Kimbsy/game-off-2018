import pygame

# Importing from sprites/base_sprites.py
from sprites.base_sprites import ImageSprite, ButtonSprite

# Initialise pygame stuff.
pygame.init()
clock = pygame.time.Clock()
display_width = 1000
display_height = 700
game_surface = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Spork')

# Main group of sprites to display.
workshop_sprites = pygame.sprite.Group()
splice_sprites = pygame.sprite.Group()
splice_sprites.add(
    ImageSprite(300, 225, 'w.png'),
    # ImageSprite(490, 363, 'u.png'), # Blue is added by a button click.
    #ImageSprite(418, 587, 'b.png'),   
)

# Derpy on_click functions for buttons (should live somewhere more
# sensible).
def addspoon():
    workshop_sprites.add(ImageSprite(100, 100, 'spoon.jpeg'))
def startsplice():
    splice()
    workshopdone = True
def add_blue():
    workshop_sprites.add(ImageSprite(490, 363, 'u.png'))

# Add the buttons to the main sprite group.
workshop_sprites.add(
    ButtonSprite(50, 50, "Add spoon", addspoon),
    ButtonSprite(50, 100, "Start splice", startsplice),
    ButtonSprite(50, 150, "add blue", add_blue),
)

def top_draggable_sprite_at_point(pos):
    """Returns a sprite from the main sprite group containing the mouse
    position which is draggable.

    Reverses the sprite list so it finds sprites which
    are 'on top' first.
    """
    for sprite in reversed(workshop_sprites.sprites()):
        if sprite.is_draggable and sprite.rect.collidepoint(pos):
            return sprite

def button_at_point(pos):
    """Returns a sprite from the main sprite group containing the mouse
    position which is of type ButtonSprite.

    Buttons won't overlap so we don't need to reverse the group.
    """
    for sprite in workshop_sprites.sprites():
        if (type(sprite) is ButtonSprite) and sprite.rect.collidepoint(pos):
            return sprite

def workshop():
    """TThe loop for the workshop screen.
    """

    # Want to move these elsewhere/design them away.
    workshopdone = False
    dragging = False
    dragged_sprite = None
    game_surface.fill((255, 0, 0))

    # Want to refactor this body into seperate functions.
    while not workshopdone:
        #print(pygame.mouse.get_pressed())

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                workshopdone = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                              
                b = button_at_point(event.pos)
                if b:
                    b.on_click()

        

        # Display.
        game_surface.fill((255, 0, 0))
        workshop_sprites.draw(game_surface)
        pygame.display.update()


def splice():
    """The main game loop.
    """

    # Want to move these elsewhere/design them away.
    splicedone = False
    dragging = False
    dragged_sprite = None

    # Want to refactor this body into seperate functions.
    while not splicedone:
        #print(pygame.mouse.get_pressed())

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                splicedone = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                               
                b = button_at_point(event.pos)
                if b:
                    b.on_click()

        # Display.
        game_surface.fill((0, 0, 0))
        splice_sprites.draw(game_surface)
        pygame.display.update()
    

# Run the loop, quit when done.



workshop()
pygame.quit()
quit()
