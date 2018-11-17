import pygame, os

# Import helper functions.
from helpers import *

# Import sprites.
from sprites.base_sprites import ImageSprite, ButtonSprite

class ThumbnailSprite(ImageSprite):
    """Make thumbnails not draggable and small.
    """

    def __init__(self, x, y, img_name, w, h):

        self.w = w
        self.h = h

        super(ThumbnailSprite, self).__init__(x, y, img_name)

        self.is_draggable = False


    def init_image(self):
        # Load the image from file and scale it to thumbnail size.
        loaded_img = pygame.image.load(self.img_name)
        size = loaded_img.get_size()

        # Create a surface containing the image with a transparent
        # background.
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

        self.image.blit(loaded_img, (0, 0))

        self.image = aspect_scale(self.image, (self.w, self.h))

pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
pygame.mixer.quit() # Hack to stop sound lagging.
pygame.mixer.init(22050, -16, 2, 1024)

def add_to_workbench(game_state, item_file):

    if not game_state.get('active_sprite1'):
        game_state.update({'active_sprite1': item_file})
        left_sprite.add(ThumbnailSprite(300, 300, item_file, 200, 200))
        all_sprites.add(ButtonSprite(300, 250, 'X', remove_workbench_item, ['left']))

    elif not game_state.get('active_sprite2'):
        game_state.update({'active_sprite2': item_file})
        right_sprite.add(ThumbnailSprite(600, 300, item_file, 200, 200))
        all_sprites.add(ButtonSprite(600, 250, 'X', remove_workbench_item, ['right']))

    else:
        print('You can only have 2 items')
        game_state = notify(game_state, 'warn', 'You can only have 2 items')

    return game_state

def remove_workbench_item(game_state, side):

    if side == 'left':
        game_state.update({'active_sprite1': None})
        left_sprite.empty()
    elif side == 'right':
        game_state.update({'active_sprite2': None})
        right_sprite.empty()

    return game_state

def start_splicer(game_state):
    if game_state.get('active_sprite1') and game_state.get('active_sprite2'):
        return switch_to_screen(game_state, 'splicer_screen')

    print ('You must have two items to splice')
    return game_state

# Main group of sprites to display.
all_sprites = pygame.sprite.OrderedUpdates()
left_sprite = pygame.sprite.OrderedUpdates()
right_sprite = pygame.sprite.OrderedUpdates()
all_sprites.add(
    ButtonSprite(300, 50, 'Splice!', start_splicer, []),
    ButtonSprite(300, 100, 'QUIT', quit_game, []),
    #ButtonSprite(200, 300, 'X', remove_workbench_item, []),
    #ButtonSprite(400, 300, 'X', remove_workbench_item, [right_sprite]),
)


items = os.listdir(os.getcwd() + '/data/pixel-components')
x = 50
y = 10

for item in items:

    item_file = os.getcwd() + '/data/pixel-components/' + item

    all_sprites.add(ThumbnailSprite(x, y, item_file, 50, 50))

    y += 25
    
    item_text = item[6:-4]

    all_sprites.add(ButtonSprite(x + 50, y, item_text, add_to_workbench, [item_file]))

def workshop_loop(game_state):
    """The workshop screen loop.
    """

    # Want to move these elsewhere/design them away.
    dragging = False
    dragged_sprite = None

    game_surface = game_state.get('game_surface')
    clock = game_state.get('clock')
    click = game_state.get('click_sound')
    size = game_state.get('screen_size')
    screen_width = size[0]
    screen_height = size[1]

    toast_stack = game_state.get('toast_stack')

    # Want to refactor this body into seperate functions.
    while not game_state.get('screen_done'):

        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(game_state)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # s = top_draggable_sprite_at_point(all_sprites, event.pos)
                # if s:
                #     dragging = True
                #     dragged_sprite = s
                #     all_sprites.remove(s)
                #     all_sprites.add(s)
                
                b = button_at_point(all_sprites, event.pos)
                if b:
                    click.play()
                    game_state = b.on_click(game_state)

            # elif event.type == pygame.MOUSEBUTTONUP:
            #     if event.button == 1:
            #         dragging = False
            #         dragged_sprite = None

            # elif event.type == pygame.MOUSEMOTION:
            #     if dragging:
            #         dragged_sprite.move(event.rel)

        # Update.
        toast_stack.update()

        # Display.
        game_surface.fill((0, 0, 0))

        #rect = pygame.Rect(100, 100, 100, 100)
        #pygame.draw.rect(game_surface, (255, 0, 0), (50,20,200,500), 10)

        all_sprites.draw(game_surface)
        left_sprite.draw(game_surface)
        right_sprite.draw(game_surface)
        toast_stack.draw(game_surface)
        pygame.display.update()

        clock.tick(60)

    return game_state
