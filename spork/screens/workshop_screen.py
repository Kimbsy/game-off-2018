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

    #remove all sprites from previous time screen was open
    general_sprites.empty()
    scrollable_sprites.empty()
    left_sprite.empty()
    right_sprite.empty()
    game_state.update({'active_sprite1': None, 'active_sprite2': None})

    game_surface = game_state.get('game_surface')
    clock = game_state.get('clock')
    click = game_state.get('click_sound')
    size = game_state.get('screen_size')
    screen_width = size[0]
    screen_height = size[1]

    toast_stack = game_state.get('toast_stack')
    available_funds = game_state.get('available_funds')

    

    #scroll_rect = pygame.Rect(0,0,200,500)
    scroll_surface = pygame.surface.Surface((screen_width*0.25, screen_height*0.8))#200,500
    scroll_rect = scroll_surface.get_rect(x=50, y=50)

    background_image = ImageSprite(0, 0, os.getcwd() + '/data/workshop.png')
    general_sprites.add(background_image)
    

    general_sprites.add(
        ButtonSprite(screen_width*0.3, screen_height*0.1, 'Splice!', start_splicer, []),
        ButtonSprite(screen_width*0.5, screen_height*0.1, 'QUIT', quit_game, []),
    )


    items = os.listdir(os.getcwd() + '/data/pixel-components')
   
    x = 20
    y = 10

    
    general_sprites.add(ButtonSprite(50, 50-20, 'Up', scroll_up, [scroll_surface], w = screen_width*0.25))
    general_sprites.add(ButtonSprite(50, screen_height*0.8 + 50, 'Down', scroll_down, [scroll_surface], screen_width*0.25))


    for item in items:

            item_file = os.getcwd() + '/data/pixel-components/' + item
            scrollable_sprites.add(ThumbnailSprite(x, y, item_file, 50, 50))
            item_text = item[6:-4]
            scrollable_sprites.add(ButtonSprite(x + 50, y, item_text, add_to_workbench, [item_file], w = 150))
            y += 75

    frame_x1 = screen_width*0.3
    frame_x2 = screen_width*0.3
    frame_y = screen_height*0.2
    count = 1

    keepsakes = os.listdir(os.getcwd() + '/data/temp')
    for keepsake in keepsakes:
        item_file = os.getcwd() + '/data/temp/' + keepsake
        if count<=5:
            general_sprites.add(ThumbnailSprite(frame_x1,frame_y, os.getcwd()+'/data/frame.png', 100, 100))
            general_sprites.add(ThumbnailSprite(frame_x1+15, frame_y+20, item_file, 80, 80))
            frame_x1 += 150
            count += 1
        else:
            general_sprites.add(ThumbnailSprite(frame_x2,frame_y + 120, os.getcwd()+'/data/frame.png', 100, 100))
            general_sprites.add(ThumbnailSprite(frame_x2+15, frame_y+140, item_file, 80, 80))
            frame_x2 += 150

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
                elif (event.button == 1):
                    b = button_at_point(general_sprites, event.pos)
                    c = button_at_point(scrollable_sprites, (event.pos[0]-50,event.pos[1]-50))
                    if b:
                        click.play()
                        game_state = b.on_click(game_state)

                    if c and scroll_rect.collidepoint(event.pos):
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
        
        rendered_text = pygame.font.SysFont(None, 25).render(str(available_funds), True, (0,0,0))
        game_surface.blit(rendered_text, (800, 50))

        pygame.display.update()

        clock.tick(60)

    return game_state
