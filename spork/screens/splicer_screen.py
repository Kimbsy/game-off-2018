import pygame, os

# Import helper functions.
from helpers import *

# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite, InputBox, button_at_point

pygame.init()

white= (255,255,255)
black= (0,0,0)
red = (255,0 ,0, 0)
brown = (139,69,19)
dark_brown= (111,54,10)
splice_sprites = pygame.sprite.OrderedUpdates()

def load_buttons(game_state):
    splice_sprites.add(
    ButtonSprite((4000/28), 600, 'Workshop!', switch_to_workshop, []),
    ButtonSprite(4000/28, 500, 'QUIT', quit_game, []),
    ButtonSprite(4000/28, 150, "add 1", add_1, []),
    ButtonSprite(4000/28, 250, "add 2", add_2, []),
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
def add_1(game_state):
    splice_sprites.add(ImageSprite(490, 363, game_state.get('active_sprite1')))
    return game_state
def add_2(game_state):
    splice_sprites.add(ImageSprite(390, 363, game_state.get('active_sprite2')))
    return game_state
def screenshot(game_state):
    new_name = game_state.get('new_sprite_name')
    print(new_name)
    display_width = game_state.get('screen_size')[0]
    display_height = game_state.get('screen_size')[1]
    rect = pygame.Rect(10*display_width/28,display_height/28, 16*display_width/28, 26*display_height/28)
    sub = game_state.get('game_surface').subsurface(rect)
    pygame.image.save(sub, os.getcwd() + "/data/temp/" + new_name + ".png")
    x= game_state.get('built_sprites')
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

    return switch_to_screen(game_state, 'result_screen')


def splicer_loop(game_state):
    """The splicer screen loop.
    """
    display_width = game_state.get('screen_size')[0]
    display_height = game_state.get('screen_size')[1]
    game_surface = game_state.get('game_surface')
    active_sprite1 = game_state.get('active_sprite1')
    active_sprite2 = game_state.get('active_sprite2')
    hover_rects1= []
    hover_rects2 = []
    active_input = InputBox(100, 100, 140,32 ,pygame.font.Font(None, 32) , (0,0,255), (255,255,0))


    splice_sprites.empty()

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
            hover_rects2 = [pygame.Rect(s.rect.x -2, s.rect.y-2 , 10, 10 ),
                            pygame.Rect(s.rect.x + s.rect.w -8 , s.rect.y -2, 10, 10 ), 
                            pygame.Rect(s.rect.x + s.rect.w -8, s.rect.y + s.rect.h -8, 10, 10 ),
                            pygame.Rect(s.rect.x -2, s.rect.y + s.rect.h -8, 10, 10 )
                            ]


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
                        dragging = True
                        dragged_sprite = s
                        splice_sprites.remove(s)
                        splice_sprites.add(s)
                    if active_input.rect.collidepoint(pygame.mouse.get_pos()) == True:
                        active_input.toggle_active()
                        

                if event.button == 3:
                    if s:
                        s.rotate45()
                
                
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
                        if event.key == pygame.K_UP:
                            s.scale_up()
                        if event.key == pygame.K_DOWN:
                            s.scale_down()

                
        # Display.
        game_surface.fill(dark_brown)
        pygame.draw.rect(game_surface, white, (10*display_width/28,display_height/28, 16*display_width/28, 26*display_height/28))
        splice_sprites.draw(game_surface)
        draw_rects(hover_rects1, game_surface, black, 2)
        draw_rects(hover_rects2, game_surface, red, 0)
        active_input.draw_input_box(game_state)

        pygame.display.update()

    return game_state
