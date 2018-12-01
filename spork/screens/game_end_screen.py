import pygame, os

# Import helper functions.
from helpers import top_draggable_sprite_at_point, aspect_scale, draw_rects
from screen_helpers import quit_game, switch_to_screen, notify

# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite, button_at_point, ThumbnailSprite

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit() # Hack to stop sound lagging.
pygame.mixer.init(22050, -16, 2, 1024)


# Main group of sprites to display.
general_sprites = pygame.sprite.OrderedUpdates()
frame_sprites = pygame.sprite.Group()
background_sprite = pygame.sprite.Group()

def blimp_screen(game_state, sprite):
    sprite.rect.x = 10
    sprite.rect.y = 10
    general_sprites.add(sprite)

    return game_state


def game_end_loop(game_state):
    #The game end screen loop.

    game_surface = game_state.get('game_surface')
    clock = game_state.get('clock')
    click = game_state.get('click_sound')
    size = game_state.get('screen_size')
    screen_width = size[0]
    screen_height = size[1]

    built_sprites = game_state.get('built_sprites')

    toast_stack = game_state.get('toast_stack')
    available_funds = game_state.get('available_funds')

    background_image = ImageSprite(0, 0, os.getcwd() + '/data/workshop.png')
    background_sprite.add(background_image)

    general_sprites.add(ButtonSprite(screen_width*0.5, screen_height*0.05, 'QUIT', quit_game, []))
    
    frame_x = screen_width*0.2
    frame_y = screen_height*0.1
    pic_frame_x = frame_x - screen_width*0.01
    pic_frame_y = frame_y - screen_width*0.01
    i = 0

    # Draw frames on the wall before adding images to them
    while (i < 3):
        general_sprites.add(ThumbnailSprite(pic_frame_x, pic_frame_y, os.getcwd() + '/data/frame.png', screen_width*0.22, screen_width*0.22))
        pic_frame_x += screen_width*0.25
        i += 1

    for keepsake_entry in built_sprites:
        keepsake = keepsake_entry.get('sprite')
        keepsake_name = keepsake_entry.get('name')
        keepsake.rect.x = frame_x
        keepsake.rect.y = frame_y
        frame_sprites.add(keepsake)
        frame_x += screen_width*0.25


    # Want to refactor this body into seperate functions.
    while not game_state.get('screen_done'):

        # Handle events.
        hover_rect = None
        for sprite in frame_sprites:
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                hover_rect = sprite.rect

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if (event.button == 1):
                    for sprite in frame_sprites:
                        if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                            game_state = blimp_screen(game_state, sprite)

                    b = button_at_point(general_sprites, event.pos)
                    if b:
                        click.play()
                        game_state = b.on_click(game_state)

        # Update.
        toast_stack.update()
                
        # Display.
        game_surface.fill((255, 0, 0))
        background_sprite.draw(game_surface)
        general_sprites.draw(game_surface)
        frame_sprites.draw(game_surface)
        
        toast_stack.draw(game_surface)
        
        end_game_text = "Choose an item to take to the worlds fair!"
        
        rendered_text = pygame.font.SysFont(None, 50).render(end_game_text, True, (0,0,0))
        game_surface.blit(rendered_text, (screen_width*0.25, screen_height*0.7))

        if hover_rect:
            pygame.draw.rect(game_surface, (255,0,0), hover_rect, 5)

        pygame.display.update()

        clock.tick(60)

    return game_state
