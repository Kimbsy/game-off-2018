import pygame, os, random, string

# Import helper functions.
from helpers import *


# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite, InputBox, button_at_point

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
    click = game_state.get('click_sound')
    screen_size = game_state.get('screen_size')
    screen_width = screen_size[0]
    screen_height = screen_size[1]

    toast_stack = game_state.get('toast_stack')
    logo_sprites = pygame.sprite.OrderedUpdates()
    logo_sprites.add(
    	ImageSprite(screen_width*0.31, screen_height*0.2, os.getcwd() +"/data/imgbase/sporklogo1.png"  )
    	)
    company_name = game_state.get('company_name')
    input_font = pygame.font.Font(None, 50)
    input_width, input_height = input_font.render(company_name, True, (0, 0, 0)).get_size()

    company_name_input = InputBox(
        (0.5*screen_width) - (0.5*input_width),
        0.125*screen_height,
        input_width + 10,
        input_height + 10,
        input_font,
        (0, 0, 255),
        (255, 255, 0),
        text=company_name,
        center_x=0.5*screen_width
    )

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

    # Want to refactor this body into seperate functions.
    while not game_state.get('screen_done'):

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and company_name_input.rect.collidepoint(pygame.mouse.get_pos()) == True:
                        company_name_input.toggle_active()
                b = button_at_point(all_sprites, event.pos)
                if b:
                    game_state.update({'company_name': company_name_input.text}) # TODO: this is a little hacky.
                    click.play()
                    game_state = b.on_click(game_state)

            if company_name_input.active == True:      
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
        pygame.display.update()

        clock.tick(60)

    return game_state
