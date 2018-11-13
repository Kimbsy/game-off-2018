import pygame, os

# Importing from sprites/base_sprites.py
from sprites.base_sprites import ImageSprite, ButtonSprite

pygame.init()

white= (255,255,255)
black= (0,0,0)
red = (255,0 ,0, 0)
brown = (139,69,19)
dark_brown= (111,54,10)
splice_sprites = pygame.sprite.Group()

def load_buttons(game_state):
    splice_sprites.add(
    ButtonSprite((4000/28), 600, 'Workshop!', switch_to_workshop, []),
    ButtonSprite(4000/28, 500, 'QUIT', quit_game, []),
    ButtonSprite(4000/28, 150, "add pot", add_pot, []),
    ButtonSprite(4000/28, 250, "add flower", add_flower, []),
    ButtonSprite(4000/28, 350, "screenshot", screenshot, []),
    )
    return game_state

def switch_to_workshop(game_state):
    game_state.update({'active_screen': 'workshop_screen'})
    game_state.update({'screen_done': True})
    return game_state
def quit_game(game_state):
    game_state.update({'quit': True})
    game_state.update({'screen_done': True})
    return game_state
def add_pot(game_state):
    splice_sprites.add(ImageSprite(490, 363, os.getcwd() + "/data/pixel-components/" + "pixel-pot.png"))
    return game_state
def add_flower(game_state):
    splice_sprites.add(ImageSprite(390, 263, os.getcwd() + "/data/pixel-components/" + "pixel-flower.png"))
    return game_state
def screenshot(game_state, text):
    display_width = game_state.get('screen_size')[0]
    display_height = game_state.get('screen_size')[1]
    rect = pygame.Rect(10*display_width/28,display_height/28, 16*display_width/28, 26*display_height/28)
    sub = game_state.get('game_surface').subsurface(rect)
    pygame.image.save(sub, os.getcwd() + "/data/temp/" + text + ".png")
    x= game_state.get('built_sprites')
    x.add(ImageSprite(1,1, os.getcwd() + "/data/temp/" + text + ".png"))
    game_state.update({'built_sprites' : x})
    for i in game_state.get('built_sprites'):
        print(i.img_name)

    switch_to_workshop(game_state)

    return game_state


def top_draggable_sprite_at_point(pos):
    """Returns a sprite from the main sprite group containing the mouse
    position which is draggable.

    Reverses the sprite list so it finds sprites which
    are 'on top' first.
    """
    for sprite in reversed(splice_sprites.sprites()):
        if sprite.is_draggable and sprite.rect.collidepoint(pos):
            return sprite

def button_at_point(pos):
    """Returns a sprite from the main sprite group containing the mouse
    position which is of type ButtonSprite.

    Buttons won't overlap so we don't need to reverse the group.
    """
    for sprite in splice_sprites.sprites():
        if (type(sprite) is ButtonSprite) and sprite.rect.collidepoint(pos):
            return sprite

def splicer_loop(game_state):
    """The splicer screen loop.
    """
    display_width = game_state.get('screen_size')[0]
    display_height = game_state.get('screen_size')[1]
    game_surface = game_state.get('game_surface')
    active_sprite1 = game_state.get('active_sprite1')
    active_sprite2 = game_state.get('active_sprite2')

    splice_sprites.empty()

    load_buttons(game_state)
    
    # Want to move these elsewhere/design them away.
    dragging = False
    dragged_sprite = None

    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = (255,0,0)
    color_active = (255,0,255)
    font = pygame.font.Font(None, 32)
    color = color_active
    text = ''
    
    # Want to refactor this body into seperate functions.
    while not game_state.get('screen_done'):

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                s = top_draggable_sprite_at_point(event.pos)
                if event.button == 1:    
                    if s:
                        dragging = True
                        dragged_sprite = s
                        splice_sprites.remove(s)
                        splice_sprites.add(s)

                if event.button ==2:
                    if s:
                        s.rotate90()
                if event.button ==3:
                    if s:
                        s.scale()
                
                b = button_at_point(event.pos)
                if b:
                    if b.text == "screenshot":
                        game_state = b.on_click(game_state, text)
                    else:
                        game_state = b.on_click(game_state)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    dragged_sprite = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dragged_sprite.move(event.rel)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                game_state

        # Display.
        game_surface.fill(white)
        pygame.draw.rect(game_surface, red, (10*display_width/28,display_height/28, 16*display_width/28, 26*display_height/28))
        splice_sprites.draw(game_surface)

        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        game_surface.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(game_surface, color, input_box, 2)

        #print(os.getcwd())

        pygame.display.update()

    return game_state
