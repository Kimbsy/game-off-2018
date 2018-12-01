import pygame, os

# Import helper functions.
from helpers import top_draggable_sprite_at_point, aspect_scale, draw_rects
from screen_helpers import quit_game, switch_to_screen, notify

# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite, button_at_point, ThumbnailSprite, TextSprite, ButtonImageSprite

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
        left = ThumbnailSprite(screen_width*0.275, screen_height*0.55, item_file, screen_width*0.2, screen_width*0.2)
        left.rect.centerx = screen_width*0.275 + (left.w / 2)
        left_sprite.add(left)
        general_sprites.add(left_remove_button)

    elif not game_state.get('active_sprite2'):
        game_state.update({'active_sprite2': item_file})
        right = ThumbnailSprite(screen_width*0.5, screen_height*0.55, item_file, screen_width*0.2, screen_width*0.2)
        right.rect.centerx = screen_width*0.5 + (right.w / 2)
        right_sprite.add(right)
        general_sprites.add(right_remove_button)

    else:
        print('You can only have 2 items')
        game_state = notify(game_state, 'warn', 'You can only have 2 items')

    return game_state

def remove_workbench_item(game_state, side):
    #empty the game_state of options to splice and remove images
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
    game_state = notify(game_state, 'warn', 'You must have two items to splice')
    return game_state

def scroll_up(game_state, surface):
    #scrolls the item list up by moving scrollable_surface and sprites
    for sprite in scrollable_sprites:
        if sprite.y > 3800:
            return game_state

    for sprite in scrollable_sprites:
            sprite.y += 10
            sprite.rect.y +=10

    surface.scroll(0,10)

    return game_state

def scroll_down(game_state, surface):
    for sprite in scrollable_sprites:
        if sprite.y < -3200:
            return game_state

    for sprite in scrollable_sprites:
            sprite.y -= 10
            sprite.rect.y -=10

    surface.scroll(0,-10)

    return game_state

def end_game(game_state):
    return switch_to_screen(game_state, 'game_end_screen')


# Main group of sprites to display.
general_sprites = pygame.sprite.OrderedUpdates()
splice_button = pygame.sprite.OrderedUpdates()
scrollable_sprites = pygame.sprite.Group()
left_sprite = pygame.sprite.OrderedUpdates()
right_sprite = pygame.sprite.OrderedUpdates()

left_remove_button = ButtonSprite(300, 375, 'X', remove_workbench_item, ['left'], w=50) #350, 400
right_remove_button = ButtonSprite(600, 375, 'X', remove_workbench_item, ['right'], w=50)


def workshop_loop(game_state):
    """The workshop screen loop.
    """
    built_sprites = game_state.get('built_sprites')
    if len(built_sprites) > 2: # should be > 2
        #add a button to the workbench that says go to the world fair! which calls the function below
        game_state = end_game(game_state)
        return game_state

    #remove all sprites from previous time screen was open
    general_sprites.empty()
    scrollable_sprites.empty()
    left_sprite.empty()
    right_sprite.empty()
    game_state.update({'active_sprite1': None, 'active_sprite2': None})

    game_surface = game_state.get('game_surface')
    clock = game_state.get('clock')
    fps = game_state.get('fps')
    click = game_state.get('click_sound')
    size = game_state.get('screen_size')
    screen_width = size[0]
    screen_height = size[1]

    toast_stack = game_state.get('toast_stack')
    available_funds = game_state.get('available_funds')
    company = game_state.get('company_name')

    held_down = False

    scroll_surface = pygame.surface.Surface((screen_width*0.2, screen_height*0.8))#200,500
    scroll_rect = scroll_surface.get_rect(x=50, y=50)

    background_image = ImageSprite(0, 0, os.getcwd() + '/data/imgbase/workshop.png')
    general_sprites.add(background_image)

    general_sprites.add(TextSprite(screen_width*0.35, screen_height*0.3, screen_width*0.25, screen_height*0.2, company))

    general_sprites.add(
        ButtonSprite(screen_width * 0.8, screen_height * 0.05, 'QUIT', quit_game, []),
    )
    splice_button.add(ButtonSprite(screen_width * 0.4, screen_height * 0.5, 'Splice!', start_splicer, [], color=(0,255,0), text_color=(0,0,0)))

    items = os.listdir(os.getcwd() + '/data/pixel-components')
   
    x = 20
    y = 10

    general_sprites.add(ButtonSprite(50, 50-20, 'Up', scroll_up, [scroll_surface], w = screen_width*0.2))
    general_sprites.add(ButtonSprite(50, screen_height*0.8 + 50, 'Down', scroll_down, [scroll_surface], screen_width*0.2))

    for item in items:
        item_file = os.getcwd() + '/data/pixel-components/' + item
        temp_item = ButtonImageSprite(x, y, item_file, add_to_workbench, [item_file], w=100, h=100)
        temp_item.rect.centerx = x + (temp_item.w / 2)
        scrollable_sprites.add(temp_item)
        item_text = item[6:-4]
        scrollable_sprites.add(ButtonSprite(x + 100, y, item_text, add_to_workbench, [item_file], w = 100))
        y += 125

    frame_x = screen_width*0.7
    frame_y = screen_height*0.6

    for keepsake_entry in built_sprites:
        keepsake = keepsake_entry.get('sprite')
        keepsake.rect.x = frame_x
        keepsake.rect.y = frame_y
        general_sprites.add(keepsake)

        keepsake_name = keepsake_entry.get('name')
        general_sprites.add(TextSprite(frame_x, frame_y, screen_width*0.1, screen_height*0.05, keepsake_name))

        frame_x += screen_width*0.1
        frame_y += screen_height*0.05



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
                    held_down = True
                    b = button_at_point(general_sprites, event.pos)
                    c = button_at_point(scrollable_sprites, (event.pos[0]-50,event.pos[1]-50))
                    if b:
                        click.play()
                        game_state = b.on_click(game_state)

                    if c and scroll_rect.collidepoint(event.pos):
                        click.play()
                        game_state = c.on_click(game_state)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    held_down = False

        # Needed to hold down up and down scroll buttons
        if held_down:
            b = button_at_point(general_sprites, pygame.mouse.get_pos())
            b2 = button_at_point(splice_button, pygame.mouse.get_pos())
            if b:
                game_state = b.on_click(game_state)
            elif b2:
                game_state = b2.on_click(game_state)


        # Update.
        toast_stack.update()
                
        # Display.
        game_surface.fill((255, 0, 0))
        scroll_surface.fill((200,200,200))

        general_sprites.draw(game_surface)

        # only draw splice button if both sprites present
        if len(left_sprite.sprites()) and len(right_sprite.sprites()):
            splice_button.draw(game_surface)
        
        scrollable_sprites.draw(scroll_surface)
        left_sprite.draw(game_surface)
        right_sprite.draw(game_surface)
        toast_stack.draw(game_surface)
        game_surface.blit(scroll_surface, (50,50))
        
        funds_string = "Lifetime earnings: £{0:.2f}".format(available_funds)
        rendered_text = pygame.font.SysFont(None, 25).render(funds_string, True, (0,0,0))
        game_surface.blit(rendered_text, (screen_width * 0.7, screen_height * 0.1))

        pygame.display.update()

        clock.tick(fps)

    return game_state
