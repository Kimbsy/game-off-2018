import pygame, os

# Import helper functions.
from helpers import *

# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite, button_at_point, ThumbnailSprite

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit() # Hack to stop sound lagging.
pygame.mixer.init(22050, -16, 2, 1024)

def add_to_workbench(game_state, item_file):
    #Adds items to the workbench, ready to be passed to the splicer through game state, 
    #also adds button to delete choice

    size = game_state.get('screen_size')
    screen_width = size[0]
    screen_height = size[1]

    if not game_state.get('active_sprite1'):
        game_state.update({'active_sprite1': item_file})
        left_sprite.add(ThumbnailSprite(screen_width*0.35, screen_height*0.55, item_file, screen_width*0.2, screen_width*0.2))
        general_sprites.add(left_remove_button)

    elif not game_state.get('active_sprite2'):
        game_state.update({'active_sprite2': item_file})
        right_sprite.add(ThumbnailSprite(screen_width*0.65, screen_height*0.55, item_file, screen_width*0.2, screen_width*0.2))
        general_sprites.add(right_remove_button)

    else:
        print('You can only have 2 items')
        game_state = notify(game_state, 'warn', 'You can only have 2 items')

    return game_state

def remove_workbench_item(game_state, side):
    #empty the gamestate of options to splice and remove images
    if side == 'left':
        game_state.update({'active_sprite1': None})
        left_sprite.empty()
        general_sprites.remove(left_remove_button)
    elif side == 'right':
        game_state.update({'active_sprite2': None})
        right_sprite.empty()
        general_sprites.remove(right_remove_button)

    return game_state

def start_splicer(game_state):
    if game_state.get('active_sprite1') and game_state.get('active_sprite2'):
        return switch_to_screen(game_state, 'splicer_screen')

    print ('You must have two items to splice')
    return game_state

def scroll_up(game_state, surface):
    #scrolls the item list up by moving scrollable_surface and sprites
    for sprite in scrollable_sprites:
        if sprite.y > 2300:
            return game_state

    for sprite in scrollable_sprites:
            sprite.y += 10
            sprite.rect.y +=10

    surface.scroll(0,10)

    return game_state

def scroll_down(game_state, surface):
    for sprite in scrollable_sprites:
        if sprite.y < -1800:
            return game_state

    for sprite in scrollable_sprites:
            sprite.y -= 10
            sprite.rect.y -=10

    surface.scroll(0,-10)

    return game_state

# Main group of sprites to display.
general_sprites = pygame.sprite.OrderedUpdates()
scrollable_sprites = pygame.sprite.Group()
left_sprite = pygame.sprite.OrderedUpdates()
right_sprite = pygame.sprite.OrderedUpdates()

left_remove_button = ButtonSprite(350, 400, 'X', remove_workbench_item, ['left'])
right_remove_button = ButtonSprite(700, 400, 'X', remove_workbench_item, ['right'])


def workshop_loop(game_state):
    """The workshop screen loop.
    """

    # Want to move these elsewhere/design them away.
    dragging = False
    dragged_sprite = None

    game_surface = game_state.get('game_surface')
    clock = game_state.get('clock')
    click = game_state.get('click_sound')
    size = game_state.get('screen_size')
    screen_width = size[0]
    screen_height = size[1]

    toast_stack = game_state.get('toast_stack')

    #scroll_rect = pygame.Rect(0,0,200,500)
    scroll_surface = pygame.surface.Surface((200, 500))
    scroll_rect = scroll_surface.get_rect(x=50, y=50)

    background_image = ImageSprite(0, 0, os.getcwd() + '/data/workshop.png')
    general_sprites.add(background_image)

    general_sprites.add(
        ButtonSprite(400, 50, 'Splice!', start_splicer, []),
        ButtonSprite(400, 100, 'QUIT', quit_game, []),
    )

    items = os.listdir(os.getcwd() + '/data/pixel-components')
   
    x = 50
    y = 10

    general_sprites.add(ButtonSprite(200, 50, 'Up', scroll_up, [scroll_surface]))
    general_sprites.add(ButtonSprite(200, 350, 'Down', scroll_down, [scroll_surface]))

    for item in items:
            item_file = os.getcwd() + '/data/pixel-components/' + item
            scrollable_sprites.add(ThumbnailSprite(x, y, item_file, 50, 50))
            item_text = item[6:-4]
            scrollable_sprites.add(ButtonSprite(x + 50, y, item_text, add_to_workbench, [item_file]))
            y += 75

    keepsakes = os.listdir(os.getcwd() + '/data/temp')
    for keepsake in keepsakes:
        item_file = os.getcwd() + '/data/temp/' + keepsake
        general_sprites.add(ThumbnailSprite(800,100, os.getcwd()+'/data/frame.png', 200, 200))
        general_sprites.add(ThumbnailSprite(815, 120, item_file, 180, 180))

    # Want to refactor this body into seperate functions.
    while not game_state.get('screen_done'):

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if scroll_rect.collidepoint(event.pos) and event.button == 4:
                    scroll_up(game_state, scroll_surface)
                elif scroll_rect.collidepoint(event.pos) and event.button == 5:
                    scroll_down(game_state, scroll_surface)
                else:
                    b = button_at_point(general_sprites, event.pos)
                    c = button_at_point(scrollable_sprites, (event.pos[0]-50,event.pos[1]-50))
                    if b:
                        click.play()
                        game_state = b.on_click(game_state)

                        if c:
                            click.play()
                            game_state = c.on_click(game_state)

        # Update.
        toast_stack.update()
                
        # Display.
        game_surface.fill((255, 0, 0))
        scroll_surface.fill((0,0,0))

        general_sprites.draw(game_surface)
        scrollable_sprites.draw(scroll_surface)
        left_sprite.draw(game_surface)
        right_sprite.draw(game_surface)
        toast_stack.draw(game_surface)
        game_surface.blit(scroll_surface, (50,50))
        pygame.display.update()

        clock.tick(60)

    return game_state
