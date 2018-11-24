import pygame, os, random

# Import helper functions.
from helpers import *
from crop import *
# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite, InputBox, button_at_point, ThumbnailSprite

pygame.init()

white= (255,255,255)
black= (0,0,0)
red = (255,0 ,0, 0)
brown = (139,69,19)
dark_brown= (111,54,10)
splice_sprites = pygame.sprite.OrderedUpdates()
splice_thumbnails = pygame.sprite.Group()

def load_buttons(game_state):

    x = game_state.get('screen_size')[0]
    y = game_state.get('screen_size')[1]
    splice_sprites.add(
        ButtonSprite(0.05*x, 0.25*y, "add 1", add_1, []),
        ButtonSprite(0.15*x, 0.25*y, "crop 1", crop, ["1"]),
        ButtonSprite(0.05*x, 0.5*y, "add 2", add_2, []),
        ButtonSprite(0.15*x, 0.5*y, "crop 2", crop, ["2"]),
        ButtonSprite(0.1*x, 0.8*y, "SPLICE", screenshot, []),
        ButtonSprite(0.1*x, 0.85*y, 'Workshop!', switch_to_workshop, []),
        ButtonSprite(0.1*x, 0.9*y, 'QUIT', quit_game, []),
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

def add_1(game_state):
    splice_sprites.add(ImageSprite(490, 363, game_state.get('active_sprite1')))
    return game_state

def add_2(game_state):
    splice_sprites.add(ImageSprite(390, 363, game_state.get('active_sprite2')))
    return game_state

def screenshot(game_state):
    new_name = game_state.get('new_sprite_name')
    if not new_name:
        return notify(game_state, 'warn', 'Your sprite must have a name.')
    print(new_name)

    # Choose a sellotape sound and begin playing it.
    sound_file = random.choice([
        'sellotape_001.wav',
        'sellotape_002.wav',
    ])
    sellotape_sound = pygame.mixer.Sound(os.getcwd() + '/data/sounds/sellotape/' + sound_file)
    channel = pygame.mixer.Channel(0)
    channel.play(sellotape_sound)
    
    display_width = game_state.get('screen_size')[0]
    display_height = game_state.get('screen_size')[1]
    rect = pygame.Rect(10*display_width/28,display_height/28, 16*display_width/28, 26*display_height/28)

    transparent_surface = pygame.Surface((display_width, display_height), pygame.SRCALPHA, 32)
    splice_sprites.draw(transparent_surface)
    sub = transparent_surface.subsurface(rect)

    pygame.image.save(sub, os.getcwd() + "/data/temp/" + new_name + ".png")
    x = game_state.get('built_sprites')
    x.add(ImageSprite(1,1, os.getcwd() + "/data/temp/" + new_name + ".png"))
    game_state.update({'built_sprites' : x})

    for i in game_state.get('built_sprites'):
        print(i.img_name)

    game_state.update({'latest_product': {
        'name': new_name,
        'img': os.getcwd() + "/data/temp/" + new_name + ".png",
        'components': [game_state.get('active_sprite1'), game_state.get('active_sprite2')],
        'total_cost': 4000.3,
    }})

    # Wait for sellotape sound to finish.
    while channel.get_busy():
        pass

    return switch_to_screen(game_state, 'result_screen')

def crop(game_state, num):
    screen, px = setup(game_state.get('active_sprite' + num))
    left, upper, right, lower = cropLoop(screen, px)

    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower

    im = Image.open(game_state.get('active_sprite'+ num))
    im = im.crop(( left, upper, right, lower))
    im.save('outie.png')
    display_width = 1200
    display_height = 675
    game_state.update({'game_surface': pygame.display.set_mode((display_width, display_height))})
    crop_sprite = (ImageSprite(490, 263, os.getcwd()+ '/outie.png'))
    game_state.update({'crop_sprite' : crop_sprite})

    return game_state

def splicer_loop(game_state):
    """The splicer screen loop.
    """
    display_width = game_state.get('screen_size')[0]
    display_height = game_state.get('screen_size')[1]
    game_surface = game_state.get('game_surface')
    click = game_state.get('click_sound')
    clock = game_state.get('clock')
    active_sprite1 = game_state.get('active_sprite1')
    active_sprite2 = game_state.get('active_sprite2')
    game_state.update({'crop_sprite' : None})
    hover_rects1= []
    hover_rects2 = []
    
    active_input = InputBox(0.05*display_width, 0.125*display_height, 200, 0.1*display_height ,pygame.font.Font(None, 50) , (0,0,255), (255,255,0))
    # make the input box

    count = 0 # need to design this out. This is to do with making cropped sprites.

    toast_stack = game_state.get('toast_stack')

    splice_sprites.empty()
    splice_thumbnails.empty()
    splice_thumbnails.add(ThumbnailSprite(0.1*display_width, 0.3*display_height, active_sprite1, 0.2*display_width, 0.2*display_height))
    splice_thumbnails.add(ThumbnailSprite(0.1*display_width, 0.55*display_height, active_sprite2, 0.2*display_width, 0.2*display_height))

    #make the thumbnails of your activesprites

    load_buttons(game_state)
    
    # Want to move these elsewhere/design them away.
    dragging = False
    dragged_sprite = None

    while not game_state.get('screen_done'):
        if pygame.mouse.get_pos():
            s = top_draggable_sprite_at_point(splice_sprites, pygame.mouse.get_pos())
        else:
            s = None

        if s:
            hover_rects1 = [s.rect]
            if s.cropping == True:
                hover_rects2 = [pygame.Rect(s.rect.x -2, s.rect.y-2 , 10, 10 ),
                                pygame.Rect(s.rect.x + s.rect.w -8 , s.rect.y -2, 10, 10 ), 
                                pygame.Rect(s.rect.x + s.rect.w -8, s.rect.y + s.rect.h -8, 10, 10 ),
                                pygame.Rect(s.rect.x -2, s.rect.y + s.rect.h -8, 10, 10 )
                                ]

            else:
                hover_rects2 = []


        else:
            hover_rects1 = []
            hover_rects2 = []
        # Handle events.
        for event in pygame.event.get():
           
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:    
                    if s:
                        if s.cropping == True:
                            splice_sprites.remove(s)
                        else:
                            dragging = True
                            dragged_sprite = s
                            splice_sprites.remove(s)
                            splice_sprites.add(s)
                    if active_input.rect.collidepoint(pygame.mouse.get_pos()) == True:
                        active_input.toggle_active()
                        

                if event.button == 3:
                    if s:
                        s.rotate45() # actually rotates 90 right now.
                
                
                b = button_at_point(splice_sprites, event.pos)
                if b:
                    game_state.update({'new_sprite_name': active_input.text}) # TODO: this is a little hacky.
                    game_state = b.on_click(game_state)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    dragged_sprite = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dragged_sprite.move(event.rel)
                
            
            if active_input.active == True:      
                active_input.event_handle(event) #Input Box Class has inbuilt event handling function for key down events.
            elif active_input.active == False:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if s:
                            s.toggle_cropping()

        keys = pygame.key.get_pressed()
        if s:
            if keys[pygame.K_UP]:
                s.scale_up()
            if keys[pygame.K_DOWN]:
                s.scale_down()


        if game_state.get('crop_sprite') != None and count ==0:
            splice_sprites.add(game_state.get('crop_sprite'))

        # Update.
        toast_stack.update()

        # Display.
        game_surface.fill(dark_brown)
        pygame.draw.rect(game_surface, white, (10*display_width/28,display_height/28, 16*display_width/28, 26*display_height/28))
        splice_thumbnails.draw(game_surface)
        splice_sprites.draw(game_surface)
        draw_rects(hover_rects1, game_surface, black, 2)
        draw_rects(hover_rects2, game_surface, red, 0)
        active_input.draw_input_box(game_state)

        toast_stack.draw(game_surface)

        pygame.display.update()

        clock.tick(60)

    return game_state
