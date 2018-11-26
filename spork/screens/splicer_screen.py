import pygame, os, random

# Import helper functions.
from helpers import *
from crop import *
# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite, InputBox, button_at_point, ThumbnailSprite, ButtonImage

pygame.init()

white= (255,255,255)
black= (0,0,0)
red = (255,0 ,0, 0)
brown = (139,69,19)
dark_brown= (111,54,10)
splice_sprites = pygame.sprite.OrderedUpdates()
splice_thumbnails = pygame.sprite.Group()


def load_buttons(game_state, splice_canvas):

    x = game_state.get('screen_size')[0]
    y = game_state.get('screen_size')[1]
    
    helpbutton =ButtonImage(0.25*x, 0.8*y, os.getcwd() + "/data/imgbase/" + "helpbuttonsmall.png", dud, [])
    helpbutton.rect.centerx = (0.28 * x) - (((0.07 * x) - 70) / 2)
    workshop=ButtonSprite(0.25*x, 0.92*y, 'WORKSHOP', switch_to_workshop, [])
    workshop.rect.centerx = 0.28*x - ((0.07*x-70)/2)
    quit =ButtonSprite(0.25*x, 0.96*y, 'QUIT', quit_game, [])
    quit.rect.centerx = 0.28*x - ((0.07*x-70)/2)

    splice =ButtonImage(0.05*x, 0.68*y, os.getcwd() + "/data/imgbase/" + "splicebuttonsmall.png", screenshot, [splice_canvas])
    splice.rect.centerx = 0.11*x

    

    splice_sprites.add(
        ButtonImage(0.21*x, 0.18*y, os.getcwd() + "/data/imgbase/addbuttonsmall.png", add_sprite, ["1"]),
        ButtonImage(0.28*x, 0.18*y, os.getcwd() + "/data/imgbase/cropbuttonsmall.png", crop, ["1"]),
        ButtonImage(0.21*x, 0.295*y, os.getcwd() + "/data/imgbase/mirrorbuttonsmall.png", add_sprite, ["1", True]),
        ButtonImage(0.28*x, 0.295*y, os.getcwd() + "/data/imgbase/mirrorcropbuttonsmall.png", crop, ["1", True] ),

        ButtonImage(0.21*x, 0.43*y, os.getcwd() + "/data/imgbase/addbuttonsmall.png", add_sprite, ["2"]),
        ButtonImage(0.28*x, 0.43*y, os.getcwd() + "/data/imgbase/cropbuttonsmall.png", crop, ["2"]),
        ButtonImage(0.21*x, 0.545*y, os.getcwd() + "/data/imgbase/mirrorbuttonsmall.png", add_sprite, ["2", True]),
        ButtonImage(0.28*x, 0.545*y, os.getcwd() + "/data/imgbase/mirrorcropbuttonsmall.png", crop, ["2", True]),

        ButtonImage(0.21*x, 0.675*y, os.getcwd() + "/data/imgbase/copybuttonsmall.png", toggle_copy_mode, []),
        ButtonImage(0.28*x, 0.675*y, os.getcwd() + "/data/imgbase/delbuttonsmall.png", toggle_delete_mode, []),


        splice,
        helpbutton,
        workshop,
        quit,      
    )
    return game_state

def switch_to_workshop(game_state):
    game_state.update({'active_screen': 'workshop_screen'})
    game_state.update({'screen_done': True})
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    return game_state

def quit_game(game_state):
    game_state.update({'quit': True})
    game_state.update({'screen_done': True})
    return game_state

def dud(game_state): #holding function for buttons that don't do anything yet.
    pass
    return game_state

def toggle_delete_mode(game_state):
    delete_mode = game_state.get('delete_mode')
    copy_mode = game_state.get('copy_mode')

    if delete_mode == False:
        game_state.update({'delete_mode': True})
        game_state.update({'copy_mode': False})
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        return game_state
    if delete_mode == True:
        game_state.update({'delete_mode': False})
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        return game_state

    return game_state

def toggle_copy_mode(game_state):
    delete_mode = game_state.get('delete_mode')
    copy_mode = game_state.get('copy_mode')
    if copy_mode == False:
        game_state.update({'copy_mode': True})
        game_state.update({'delete_mode': False})
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        return game_state
    if copy_mode == True:
        game_state.update({'copy_mode': False})
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        return game_state

    return game_state

def add_sprite(game_state, num, mirror = False ):
    x = game_state.get('screen_size')[0]
    y = game_state.get('screen_size')[1]
    locationx =0

    if num == "1":
        locationx = 0.5*x
    elif num == "2":
        locationx = 0.85*x
    else:
        return game_state
    tempsprite = ImageSprite(locationx, 0.5*y, game_state.get('active_sprite' +num))
    
    if mirror == True:
        tempsprite.image = pygame.transform.flip(tempsprite.image, True,False)
        tempsprite.origimage = pygame.transform.flip(tempsprite.origimage, True, False)
    if tempsprite.orig_width >= tempsprite.orig_height:
        factor = 0.25*x/ tempsprite.orig_width
    elif tempsprite.orig_width < tempsprite.orig_height:
        factor = 0.5*y/ tempsprite.orig_height


    tempsprite.scale = 100*factor

    tempsprite.rect.center = (locationx, 0.5*y)
    tempsprite.update_sprite()
       
    splice_sprites.add(tempsprite)
    return game_state

def screenshot(game_state, splice_canvas):
    
    rect = splice_canvas
    new_name = game_state.get('new_sprite_name')
    if not new_name:
        return notify(game_state, 'warn', 'Your invention must have a name.')

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
    

    transparent_surface = pygame.Surface((display_width, display_height), pygame.SRCALPHA, 32)
    splice_sprites.draw(transparent_surface)
    sub = transparent_surface.subsurface(rect)

    pygame.image.save(sub, os.getcwd() + "/data/temp/" + new_name + ".png")
    x = game_state.get('built_sprites')
    x.add(ThumbnailSprite(1,1, os.getcwd() + "/data/temp/" + new_name + ".png", display_width*0.2, display_width*0.2))
    game_state.update({'built_sprites' : x})

    game_state.update({'latest_product': {
        'name': new_name,
        'img': os.getcwd() + "/data/temp/" + new_name + ".png",
        'components': [game_state.get('active_sprite1'), game_state.get('active_sprite2')],
        'total_cost': 4000.3,
    }})

    # Wait for sellotape sound to finish.
    while channel.get_busy():
        pass
    pygame.mouse.set_cursor(*pygame.cursors.arrow)

    return switch_to_screen(game_state, 'result_screen')

def crop(game_state, num, mirror = False):
    screen, px = setup(game_state.get('active_sprite' + num), mirror)
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
    splice_sprites.add(crop_sprite)

    return game_state

def splicer_loop(game_state):
    """The splicer screen loop.
    """
    display_width = game_state.get('screen_size')[0]
    display_height = game_state.get('screen_size')[1]
    game_surface = game_state.get('game_surface')
    click = game_state.get('click_sound')
    clock = game_state.get('clock')
    fps = game_state.get('fps')
    active_sprite1 = game_state.get('active_sprite1')
    active_sprite2 = game_state.get('active_sprite2')
    game_state.update({'crop_sprite' : None})
    thumbnail_size = [0.2*display_width, 0.2*display_height]
    hover_rects1= []
    hover_rects2 = []
    delete_mode = game_state.update({'delete_mode': False })

    splice_canvas = pygame.Rect(0.35*display_width, 0.035*display_height, 0.635* display_width, 0.93*display_height) #set splice canvas area that is captured by screenshot.
    
    active_input = InputBox(
        0.05*display_width,
        0.0625*display_height,
        0.2*display_height,
        0.0625*display_height,
        pygame.font.Font(None, 50),
        (0,0,255),
        (255,255,0),
        0.175*display_width,
        '',
        0.25*display_width,
        0.33*display_width
        )
    # make the input box

    count = 0 # need to design this out. This is to do with making cropped sprites.

    toast_stack = game_state.get('toast_stack')

    splice_sprites.empty()
    splice_thumbnails.empty()
    thumb1 = ThumbnailSprite(0.1*display_width, 0.2*display_height, active_sprite1, thumbnail_size[0], thumbnail_size[1] )
    thumb1.rect.centerx = 0.1*display_width
    thumb2 = ThumbnailSprite(0.1*display_width, 0.45*display_height, active_sprite2,  thumbnail_size[0], thumbnail_size[1])
    thumb2.rect.centerx = 0.1*display_width
    splice_thumbnails.add(thumb1, thumb2)

    #make the thumbnails of your activesprites

    load_buttons(game_state, splice_canvas)
    
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
            if s.deletable == True:
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
                        if game_state.get('delete_mode') == True:
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
                        s.rotate_clockwise() # actually rotates 45 right now.
                
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
                    if s:
                        if event.key == pygame.K_SPACE:
                            s.toggle_deletable()
                        if event.key == pygame.K_LEFT:
                            s.rotate_counterclockwise()
                        if event.key == pygame.K_RIGHT:
                            s.rotate_clockwise()

        keys = pygame.key.get_pressed()
        if s:
            if keys[pygame.K_UP]:
                s.scale_up()
            if keys[pygame.K_DOWN]:
                s.scale_down()

           # Update.
        toast_stack.update()

        # Display.
        game_surface.fill(dark_brown)
        pygame.draw.rect(game_surface, white, splice_canvas)
        
        pygame.draw.rect(game_surface, (51,25, 0), (0.005*display_width, 0.17*display_height, 0.34*display_width, 0.245*display_height))
        pygame.draw.rect(game_surface, (51,25, 0), (0.005*display_width, 0.42*display_height,  0.34*display_width, 0.245*display_height))
        splice_thumbnails.draw(game_surface)

        splice_sprites.draw(game_surface)
        draw_rects(hover_rects1, game_surface, black, 2)
        draw_rects(hover_rects2, game_surface, red, 0)
        active_input.draw_input_box(game_state)

        toast_stack.draw(game_surface)

        pygame.display.update()

        clock.tick(fps)

    return game_state
