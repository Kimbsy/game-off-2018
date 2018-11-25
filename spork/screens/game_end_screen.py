import pygame, os

# Import helper functions.
from helpers import *

# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite, button_at_point, ThumbnailSprite

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit() # Hack to stop sound lagging.
pygame.mixer.init(22050, -16, 2, 1024)




def start_splicer(game_state):
    if game_state.get('active_sprite1') and game_state.get('active_sprite2'):
        return switch_to_screen(game_state, 'splicer_screen')

    print ('You must have two items to splice')
    return game_state



# Main group of sprites to display.
general_sprites = pygame.sprite.OrderedUpdates()




def game_end_loop(game_state):
    #The game end screen loop.

    game_surface = game_state.get('game_surface')
    clock = game_state.get('clock')
    click = game_state.get('click_sound')
    size = game_state.get('screen_size')
    screen_width = size[0]
    screen_height = size[1]

    toast_stack = game_state.get('toast_stack')
    available_funds = game_state.get('available_funds')


    #background_image = ImageSprite(0, 0, os.getcwd() + '/data/workshop.png')
    #general_sprites.add(background_image)
    

    # general_sprites.add(
    #     ButtonSprite(screen_width*0.3, screen_height*0.1, 'Splice!', start_splicer, []),
    #     ButtonSprite(screen_width*0.5, screen_height*0.1, 'QUIT', quit_game, []),
    # )



    frame_x1 = screen_width*0.3
    frame_x2 = screen_width*0.3
    frame_y = screen_height*0.2
    count = 0

    keepsakes = os.listdir(os.getcwd() + '/data/temp')
    for keepsake in keepsakes:
        item_file = os.getcwd() + '/data/temp/' + keepsake
        if count<5:
            general_sprites.add(ThumbnailSprite(frame_x1,frame_y, os.getcwd()+'/data/frame.png', 100, 100))
            general_sprites.add(ThumbnailSprite(frame_x1+15, frame_y+20, item_file, 80, 80))
            frame_x1 += 150
            count += 1
        else:
            general_sprites.add(ThumbnailSprite(frame_x2,frame_y + 120, os.getcwd()+'/data/frame.png', 100, 100))
            general_sprites.add(ThumbnailSprite(frame_x2+15, frame_y+140, item_file, 80, 80))
            frame_x2 += 150

    # if count = 10:
    #     end_game()

    # Want to refactor this body into seperate functions.
    while not game_state.get('screen_done'):

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if (event.button == 1):
                    b = button_at_point(general_sprites, event.pos)
                    if b:
                        click.play()
                        game_state = b.on_click(game_state)

        # Update.
        toast_stack.update()
                
        # Display.
        game_surface.fill((255, 0, 0))

        general_sprites.draw(game_surface)
        
        toast_stack.draw(game_surface)
        
        
        # rendered_text = pygame.font.SysFont(None, 25).render(str(available_funds), True, (0,0,0))
        # game_surface.blit(rendered_text, (800, 50))

        pygame.display.update()

        clock.tick(60)

    return game_state
