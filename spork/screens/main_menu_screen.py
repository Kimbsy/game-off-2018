import pygame, os, random, string

# Import helper functions.
from helpers import *


# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite, InputBox, button_at_point, TextSprite

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit() # Hack to stop sound lagging.
pygame.mixer.init(22050, -16, 2, 1024)

def start_game(game_state):
    game_state.update({
        'active_music': 'Komiku_School.mp3',
        'music_done': True,
    })
    return switch_to_screen(game_state, 'workshop_screen')

def main_menu_loop(game_state):
    """The main menu screen loop.
    """

    game_surface = game_state.get('game_surface')
    clock = game_state.get('clock')
    fps = game_state.get('fps')
    click = game_state.get('click_sound')
    screen_size = game_state.get('screen_size')
    screen_width = screen_size[0]
    screen_height = screen_size[1]
    framecount = 1

    toast_stack = game_state.get('toast_stack')
    logo_sprites = pygame.sprite.OrderedUpdates()
    logo_sprites.add(
    	ImageSprite(
            screen_width*0.315,
            screen_height*0.15,
            os.getcwd() +"/data/imgbase/sporklogo1.png"
        )
    )
    company_name = game_state.get('company_name')
    input_font = pygame.font.Font(None, 50)
    input_width, input_height = 0.1* screen_width, 0.0625*screen_height

    company_name_input = InputBox(
        (0.5*screen_width) - (0.5*input_width),
        0.68*screen_height,
        input_width + 10,
        input_height + 10,
        input_font,
        (0, 0, 255),
        (255, 255, 0),
        center_x=0.5*screen_width,
        text=company_name
    )
    company_name_input.active = True

    # Main group of sprites to display.
    all_sprites = pygame.sprite.OrderedUpdates()
    all_sprites.add(
        ButtonSprite(
            (screen_width * 0.455),
            (screen_height * 0.8),
            'Play!',
            start_game,
            [],
        ),
        ButtonSprite(
            (screen_width * 0.455),
            (screen_height * 0.9),
            'Quit',
            quit_game,
            [],
        ),
        

    )
    name_prompt = pygame.sprite.Group(
        TextSprite( (0.43*screen_width) , 0.65 *screen_height, 400, 30, "Enter Company Name", (255,255,255))
        )

    # Want to refactor this body into seperate functions.
    while not game_state.get('screen_done'):

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                b = button_at_point(all_sprites, event.pos)
                if b:
                    game_state.update({'company_name': company_name_input.text}) # TODO: this is a little hacky.
                    click.play()
                    game_state = b.on_click(game_state)
    
            company_name_input.event_handle(event) #Input Box Class has inbuilt event handling function for key down events.

        # Update.
        all_sprites.update()
        toast_stack.update()

        # Display.
        game_surface.fill((0, 0, 0))
        all_sprites.draw(game_surface)
        logo_sprites.draw(game_surface)
       
        company_name_input.draw_input_box(game_state)
        toast_stack.draw(game_surface)

        

        if framecount <= (fps/2):
            framecount += 1
        elif framecount < fps and framecount > (fps/2):
            framecount += 1
            name_prompt.draw(game_surface)
        elif framecount >= fps:
            framecount =1

        pygame.display.update()

        clock.tick(fps)

    return game_state
