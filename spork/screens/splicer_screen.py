import pygame, os, random

# Import helper functions.
from helpers import top_draggable_sprite_at_point, aspect_scale, draw_rects
from screen_helpers import quit_game, switch_to_screen, notify

#import crop module
from crop import *
# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite, InputBox, button_at_point, ThumbnailSprite, ButtonImageSprite, ConfirmBox, TextSprite

pygame.init()

white= (255,255,255)
black= (0,0,0)
red = (255,0 ,0, 0)
brown = (139,69,19)
dark_brown= (111,54,10)
splice_sprites = pygame.sprite.OrderedUpdates()
control_sprites = pygame.sprite.OrderedUpdates()
splice_thumb1 = pygame.sprite.Group()
splice_thumb2 = pygame.sprite.Group()


def load_buttons(game_state, splice_canvas, confirm_splice, confirm_crop):
    x = game_state.get('screen_size')[0]
    y = game_state.get('screen_size')[1]
    
    helpbutton =ButtonImageSprite(0.25*x, 0.8*y, os.getcwd() + "/data/imgbase/helpbuttonsmall.png", toggle_help, [])
    helpbutton.rect.centerx = (0.28 * x) - (((0.07 * x) - 70) / 2)
    workshop=ButtonSprite(0.25*x, 0.92*y, 'WORKSHOP', switch_to_workshop, [])
    workshop.rect.centerx = 0.28*x - ((0.07*x-70)/2)
    quit =ButtonSprite(0.25*x, 0.96*y, 'QUIT', quit_game, [])
    quit.rect.centerx = 0.28*x - ((0.07*x-70)/2)

    splice =ButtonImageSprite(0.05*x, 0.68*y, os.getcwd() + "/data/imgbase/" + "splicebuttonsmall.png", screenshot, [splice_canvas, confirm_splice])
    splice.rect.centerx = 0.11*x

    control_sprites.add(
        ButtonImageSprite(0.21*x, 0.18*y, os.getcwd() + "/data/imgbase/addbuttonsmall.png", add_sprite, ["1"]),
        ButtonImageSprite(0.28*x, 0.18*y, os.getcwd() + "/data/imgbase/cropbuttonsmall.png", crop, ["1", confirm_crop]),
        ButtonImageSprite(0.21*x, 0.295*y, os.getcwd() + "/data/imgbase/mirrorbuttonsmall.png", add_sprite, ["1", True]),
        ButtonImageSprite(0.28*x, 0.295*y, os.getcwd() + "/data/imgbase/mirrorcropbuttonsmall.png", crop, ["1", confirm_crop, True] ),

        ButtonImageSprite(0.21*x, 0.43*y, os.getcwd() + "/data/imgbase/addbuttonsmall.png", add_sprite, ["2"]),
        ButtonImageSprite(0.28*x, 0.43*y, os.getcwd() + "/data/imgbase/cropbuttonsmall.png", crop, ["2", confirm_crop]),
        ButtonImageSprite(0.21*x, 0.545*y, os.getcwd() + "/data/imgbase/mirrorbuttonsmall.png", add_sprite, ["2", True]),
        ButtonImageSprite(0.28*x, 0.545*y, os.getcwd() + "/data/imgbase/mirrorcropbuttonsmall.png", crop, ["2", confirm_crop, True]),

        ButtonImageSprite(0.21*x, 0.675*y, os.getcwd() + "/data/imgbase/copybuttonsmall.png", toggle_copy_mode, []),
        ButtonImageSprite(0.28*x, 0.675*y, os.getcwd() + "/data/imgbase/delbuttonsmall.png", toggle_delete_mode, []),

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

def load_help_sprites(game_state):
    thumbsize = 80
    display_width = game_state.get('screen_size')[0]
    display_height = game_state.get('screen_size')[1]
    help_sprites = pygame.sprite.Group()

    mleft = ThumbnailSprite(0.38*display_width, 0.08*display_height, os.getcwd() + "/data/imgbase/mouseleft.png", thumbsize, thumbsize)
    mlefttxt = TextSprite(0.47*display_width, 0.12* display_height, 0.18*display_width, thumbsize, "Drag Object (Default) /n Delete / Copy")

    mright = ThumbnailSprite(0.38*display_width, 0.22*display_height, os.getcwd() + "/data/imgbase/mouseright.png", thumbsize, thumbsize)
    mrighttxt =TextSprite(0.47*display_width, 0.26* display_height, 0.18*display_width, thumbsize, "Lock Selected Object")

    addthumb = ThumbnailSprite(0.38*display_width, 0.36*display_height, os.getcwd() + "/data/imgbase/addbuttonsmall.png", thumbsize, thumbsize)
    addthumbtxt = TextSprite(0.47*display_width, 0.40*display_height, 0.18*display_width, thumbsize, "Add Object")

    mirrorthumb = ThumbnailSprite(0.38*display_width, 0.50*display_height, os.getcwd() + "/data/imgbase/mirrorbuttonsmall.png", thumbsize, thumbsize)
    mirrorthumbtxt = TextSprite(0.47*display_width, 0.54*display_height, 0.18*display_width, thumbsize, "Add Mirror Image Object")

    cropthumb = ThumbnailSprite(0.38*display_width, 0.64*display_height, os.getcwd() + "/data/imgbase/cropbuttonsmall.png", thumbsize, thumbsize)
    cropthumbtxt = TextSprite(0.47*display_width, 0.68*display_height, 0.18*display_width, thumbsize, "Add Cropped Object")

    mirrorcropthumb = ThumbnailSprite(0.38*display_width, 0.78*display_height, os.getcwd() + "/data/imgbase/mirrorcropbuttonsmall.png", thumbsize, thumbsize)
    mirrorcropthumbtxt = TextSprite(0.47*display_width, 0.82*display_height, 0.18*display_width, thumbsize, "Add Mirror Image Cropped Object")

    copythumb = ThumbnailSprite(0.69*display_width, 0.08*display_height, os.getcwd() + "/data/imgbase/copybuttonsmall.png", thumbsize, thumbsize)
    copythumbtxt = TextSprite(0.78*display_width, 0.12*display_height, 0.18*display_width, thumbsize, "Toggle Copy Mode")

    delthumb = ThumbnailSprite(0.69*display_width, 0.22*display_height, os.getcwd() + "/data/imgbase/delbuttonsmall.png", thumbsize, thumbsize)
    delthumbtxt = TextSprite(0.78*display_width, 0.26*display_height, 0.18*display_width, thumbsize, "Toggle Delete Mode")

    arrowup = ThumbnailSprite(0.69*display_width, 0.36*display_height, os.getcwd() + "/data/imgbase/arrow-up.png", thumbsize, thumbsize)
    arrowuptxt = TextSprite(0.78*display_width, 0.40*display_height, 0.18*display_width, thumbsize, "Scale Up")

    arrowdown = ThumbnailSprite(0.69*display_width, 0.5*display_height, os.getcwd() + "/data/imgbase/arrow-down.png", thumbsize, thumbsize)
    arrowdowntxt = TextSprite(0.78*display_width, 0.54*display_height, 0.18*display_width, thumbsize, "Scale Down")

    arrowleft = ThumbnailSprite(0.69*display_width, 0.64*display_height, os.getcwd() + "/data/imgbase/arrow-left.png", thumbsize, thumbsize)
    arrowlefttxt = TextSprite(0.78*display_width, 0.68*display_height, 0.18*display_width, thumbsize, "Rotate AntiClockwise")

    arrowright = ThumbnailSprite(0.69*display_width, 0.78*display_height, os.getcwd() + "/data/imgbase/arrow-right.png", thumbsize, thumbsize)
    arrowrighttxt = TextSprite(0.78*display_width, 0.82*display_height, 0.18*display_width, thumbsize, "Rotate Clockwise")

    help_sprites.add(mleft, mlefttxt,
        mright, mrighttxt,
        addthumb, addthumbtxt,
        mirrorthumb, mirrorthumbtxt,
        cropthumb, cropthumbtxt,
        mirrorcropthumb, mirrorcropthumbtxt,
        copythumb, copythumbtxt,
        delthumb, delthumbtxt,
        arrowup, arrowuptxt,
        arrowdown, arrowdowntxt,
        arrowleft, arrowlefttxt,
        arrowright, arrowrighttxt
        )

    return help_sprites

def open_help(game_state, help_sprites):
    display_width = game_state.get('screen_size')[0]
    display_height = game_state.get('screen_size')[1]
    game_surface = game_state.get('game_surface')
    pygame.draw.rect(game_surface, (200,100, 200), (0.365*display_width, 0.06*display_height, 0.605*display_width, 0.88*display_height))

    help_sprites.draw(game_surface)
    return game_state

def toggle_help(game_state):
    tutorial = game_state.get('tutorial')
    game_state.update({'tutorial': not tutorial})
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

def add_sprite(game_state, num, mirror = False):
    splice_canvas = game_state.get('splice_canvas')
    screen_size = game_state.get('screen_size')
    location_x = 0

    if num == "1":
        location_x = 0.4 * splice_canvas.w
    elif num == "2":
        location_x = 0.8 * splice_canvas.w
    else:
        return game_state
    tempsprite = ImageSprite(location_x, (0.5 * splice_canvas.h), game_state.get('active_sprite' + num))
    
    if mirror == True:
        tempsprite.image = pygame.transform.flip(tempsprite.image, True, False)
        tempsprite.origimage = pygame.transform.flip(tempsprite.origimage, True, False)

    factor = 0.8 * splice_canvas.y / tempsprite.orig_height

    tempsprite.scale = 1000 * factor

    tempsprite.rect.center = (location_x, (0.5 * splice_canvas.h))
    tempsprite.update_sprite()
       
    splice_sprites.add(tempsprite)
    return game_state

def screenshot(game_state, splice_canvas, confirm_splice):

    new_name = game_state.get('new_sprite_name')
    if not new_name:
        return notify(game_state, 'warn', 'Your invention must have a name.')

    #opens confirmation box allowing user to proceed or cancel
    confirm_splice.active = True
    confirm_splice.event_handle(game_state)
    
    if confirm_splice.proceed != True:
        confirm_splice.proceed == None
        confirm_splice.active = False
        return notify(game_state, 'warn', 'You cancelled this splice.')
    else:
        confirm_splice.proceed == None
        confirm_splice.active = False 

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
    splice_canvas_surface = pygame.Surface((splice_canvas.w, splice_canvas.h), pygame.SRCALPHA, 32)
    splice_sprites.draw(splice_canvas_surface)
    transparent_surface.blit(splice_canvas_surface, (splice_canvas.x, splice_canvas.y))
    sub = transparent_surface.subsurface(splice_canvas)

    pygame.image.save(sub, os.getcwd() + "/data/temp/" + new_name + ".png")
    x = game_state.get('built_sprites')
    x.add(ThumbnailSprite(1, 1, os.getcwd() + "/data/temp/" + new_name + ".png", display_width * 0.2, display_width * 0.2))
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

def crop(game_state, num, confirm_crop, mirror = False):
    screen, px, crop_surface, image_offset = setup(game_state.get('active_sprite' + num), mirror)


    left, upper, right, lower = cropLoop(screen, px, crop_surface, image_offset, confirm_crop)

    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower

    confirm_crop.active = True
    confirm_crop.event_handle(game_state)
    
    if confirm_crop.proceed != True:
        confirm_crop.proceed == None
        confirm_crop.active = False
        return notify(game_state, 'warn', 'You cancelled this crop operation.')
    else:
        confirm_crop.proceed == None
        confirm_crop.active = False

    im = Image.open(game_state.get('active_sprite'+ num))
    im = im.crop(( left-int(image_offset[0]), upper-int(image_offset[1]), right-int(image_offset[0]), lower-int(image_offset[1])))
    im.save('outie.png')
    display_width = 1200
    display_height = 675
    game_state.update({'game_surface': pygame.display.set_mode((display_width, display_height))})
    crop_sprite = (ImageSprite(490, 263, os.getcwd()+ '/outie.png'))
    splice_sprites.add(crop_sprite)

    return game_state

def get_relative_mouse_pos(pos):
    x, y = pygame.mouse.get_pos()
    return (x - pos[0], y - pos[1])

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
    game_state.update({'delete_mode': False })
    game_state.update({'copy_mode': False})

    splice_canvas = pygame.Rect(0.35*display_width, 0.035*display_height, 0.635* display_width, 0.93*display_height) #set splice canvas area that is captured by screenshot.
    splice_canvas_surface = pygame.Surface((splice_canvas.w, splice_canvas.h), pygame.SRCALPHA, 32)
    game_state.update({'splice_canvas': splice_canvas})
    
    # make the input box
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

    confirm_splice = ConfirmBox( display_width/2, display_height/2 , "Confirm Splice")
    confirm_crop = ConfirmBox( display_width/6, (display_height*3)/4 , "Confirm Crop")
    
    #generate all confirmation boxes that could be spawned by this screen

    toast_stack = game_state.get('toast_stack')

    splice_sprites.empty()
    splice_thumb1.empty()
    splice_thumb2.empty()
    thumb1 = ThumbnailSprite(0.1*display_width, 0.2*display_height, active_sprite1, thumbnail_size[0], thumbnail_size[1] )
    thumb1.rect.centerx = 0.1*display_width
    thumb2 = ThumbnailSprite(0.1*display_width, 0.45*display_height, active_sprite2,  thumbnail_size[0], thumbnail_size[1])
    thumb2.rect.centerx = 0.1*display_width
    splice_thumb1.add(thumb1)
    splice_thumb2.add(thumb2)

    #make the thumbnails of your activesprites

    help_sprites = load_help_sprites(game_state)
    
    #make sprites for the help pop-up

    load_buttons(game_state, splice_canvas, confirm_splice, confirm_crop)
    
    # Want to move these elsewhere/design them away.
    dragging = False
    dragged_sprite = None
    selected = None

    while not game_state.get('screen_done'):
        if pygame.mouse.get_pos():
            s = top_draggable_sprite_at_point(splice_sprites, get_relative_mouse_pos((splice_canvas.x, splice_canvas.y)))
        else:
            s = None
        if selected:
            s= selected

        if s:
            hover_rects1 = [s.rect]
            if s.selected == True:
                r = s.rect
                hover_rects2 = [
                    pygame.Rect((r.x - 2), (r.y - 2), 10, 10),
                    pygame.Rect((r.x + r.w - 8), (r.y - 2), 10, 10), 
                    pygame.Rect((r.x + r.w - 8), (r.y + r.h - 8), 10, 10),
                    pygame.Rect((r.x - 2), (r.y + r.h - 8), 10, 10)
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

                    # Hacky, but the expectation here is real
                    if splice_thumb1.sprites()[0].rect.collidepoint(pygame.mouse.get_pos()):
                            game_state = add_sprite(game_state, "1")
                    elif splice_thumb2.sprites()[0].rect.collidepoint(pygame.mouse.get_pos()):
                            game_state = add_sprite(game_state, "2")

                    else:
                        s = top_draggable_sprite_at_point(splice_sprites, get_relative_mouse_pos((splice_canvas.x, splice_canvas.y)))
                        if s:
                            if game_state.get('delete_mode') == True:
                                splice_sprites.remove(s)

                            elif game_state.get('copy_mode') == True:
                                copied_image = s.clone(offset=(20, 20))

                                splice_sprites.add(copied_image)

                                #s.update_sprite()

                            else:
                                dragging = True
                                dragged_sprite = s
                                splice_sprites.remove(s)
                                splice_sprites.add(s)
                        if active_input.rect.collidepoint(pygame.mouse.get_pos()) == True:
                            active_input.toggle_active()
                
                    b = button_at_point(control_sprites, pygame.mouse.get_pos())
                    if b:
                        game_state.update({'new_sprite_name': active_input.text}) # TODO: this is a little hacky.
                        game_state = b.on_click(game_state)
                    if event.button == 3: #right click to select lock a sprite you are hovering on
                        if s:
                            if s.selected == False:
                                s.toggle_selected()
                                selected = s
                            elif s.selected == True:
                                s.toggle_selected()
                                selected = None

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
                        if event.key == pygame.K_LEFT:
                            s.rotate_counterclockwise()
                        if event.key == pygame.K_RIGHT:
                            s.rotate_clockwise()
                        if event.key == pygame.K_DELETE:
                            splice_sprites.remove(s)


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
        splice_thumb1.draw(game_surface)
        splice_thumb2.draw(game_surface)
        control_sprites.draw(game_surface)
        
        # Only draw the splice sprites inside the splice canvas
        splice_canvas_surface.fill(white)
        splice_sprites.draw(splice_canvas_surface)
        draw_rects(hover_rects1, splice_canvas_surface, black, 2)
        draw_rects(hover_rects2, splice_canvas_surface, red, 0)
        game_surface.blit(splice_canvas_surface, (splice_canvas.x, splice_canvas.y))

        active_input.draw_input_box(game_state)

        #confirm_splice.draw_confirm_box(game_state)

        if game_state.get('tutorial') == True:
            open_help(game_state, help_sprites)
            
        toast_stack.draw(game_surface)

        pygame.display.update()

        clock.tick(fps)

    return game_state
