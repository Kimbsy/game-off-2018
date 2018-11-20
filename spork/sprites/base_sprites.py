import pygame, os

# Import helper functions.
from helpers import *

def button_at_point(sprites, pos):
    """Returns a sprite from the sprite group containing the mouse
    position which is of type ButtonSprite.

    Buttons won't overlap so we don't need to reverse the group.
    """
    for sprite in sprites.sprites():
        if (type(sprite) is ButtonSprite) and sprite.rect.collidepoint(pos):
            return sprite

class BaseSprite(pygame.sprite.Sprite):
    """The base sprite class contains useful common functionality.
    """

    def __init__(self, x, y):
        super(BaseSprite, self).__init__()

        self.x = x
        self.y = y

        # Sprites are not draggable by default.
        self.is_draggable = False

        # Initialise the image surface.
        self.init_image()

        # We base the size of the sprite on its image surface.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def init_image(self):
        """Create the image surface that represents this sprite.

        Should be implemented by child classes.
        """
        raise NotImplementedError('Please implement an init_image method')

class ImageSprite(BaseSprite):
    """Sprite which loads an image from ../data/ directory.

    Currently this will load the image each time a sprite is made,
    should cache images somewhere in future.
    """

    def __init__(self, x, y, img_name):
        # Need the image name before init_image is called
        self.img_name = img_name

        # Call the parent constructor.
        super(ImageSprite, self).__init__(x, y)

        # These image sprites should be draggable.
        self.is_draggable = True

    def init_image(self):
        # Load the image from file and get its size.
        loaded_img = pygame.image.load(self.img_name)
        size = loaded_img.get_size()

        # Create a surface containing the image with a transparent
        # background.
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.image.blit(loaded_img, (0, 0))
        self.origimage = self.image
        self.rotation = 0
        # self.center_point = self.rect.center()
        self.orig_width = size[0]
        self.orig_height = size[1]
        self.aspect_scale= self.orig_width / self.orig_height
        self.scale = 100
        self.cropping = False # object cannot initially be deleted

    def move(self, move):
        """Apply a translation the the position of this sprite's
        rect based on a mousemotion relative movement.
        """
        self.x += move[0]
        self.y += move[1]
        self.rect.x += move[0]
        self.rect.y += move[1]

    def rotate45(self):
        self.rotation = self.rotation + 90
        #self.update_sprite()

        orig_rect = self.image.get_rect()

        print(orig_rect.center)
        print(pygame.mouse.get_pos())

        self.image = pygame.transform.rotate(self.origimage, self.rotation)
        self.rect = self.image.get_rect(center = (orig_rect.center[1],orig_rect.center[0]))
        # self.rect = orig_rect.copy()
        # self.center = self.image.get_rect().center
        # self.image = self.image.subsurface(self.rect).copy

        # orig_rect = image.get_rect()
        # rot_image = pygame.transform.rotate(image, angle)
        # rot_rect = orig_rect.copy()
        # rot_rect.center = rot_image.get_rect().center
        # rot_image = rot_image.subsurface(rot_rect).copy


    def scale_down(self):
        if self.scale - 2 > 0:
            self.scale = self.scale - 2

        self.update_sprite()

    def scale_up(self):
        self.scale += 2

        self.update_sprite()

    def update_sprite(self):

        new_width = int((self.orig_width*self.scale) /100)
        new_height =int((self.orig_height*self.scale)/100)


        loc = self.image.get_rect().center
        

        tempimage = pygame.transform.rotate(self.origimage, self.rotation)
        tempimage.get_rect().center = loc
        self.image = aspect_scale( tempimage, (new_width, new_height))
        self.image.get_rect().center = loc
        self.rect = self.image.get_rect()

    def toggle_cropping(self):
        if self.cropping == False:
            self.cropping = True
            return
        if self.cropping == True:
            self.cropping =  False
            return



class ButtonSprite(BaseSprite):
    """Sprite which displays as a clickable button with text.
    """

    def __init__(self, x, y, text, f, args):
        # Need to specify properties before init_img is called.
        self.text = text
        self.f = f
        self.args = args

        # Define button text font.
        self.font = pygame.font.SysFont(None, 25)
        self.text_color = (200, 200, 200)

        # Call the parent constructor.
        super(ButtonSprite, self).__init__(x, y)

    def init_image(self):
        self.image = pygame.Surface((100, 20))
        self.image.fill((100, 100, 100))
        
        rendered_text = self.font.render(self.text, True, self.text_color)
        self.image.blit(rendered_text, (15, 0))

    def on_click(self, game_state):
        """Invoke the on_click function.
        """
        return self.f(game_state, *self.args)

class TextSprite(BaseSprite):
    """Displays text wrapping lines within the bounding rectangle.
    """

    def __init__(self, x, y, w, h, text):
        self.w = w
        self.h = h
        self.text = text

        # Define button text font.
        self.font = pygame.font.SysFont(None, 25)
        self.text_color = (0, 0, 0)
        
        # Call the parent constructor.
        super(TextSprite, self).__init__(x, y)

    def init_image(self):
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        
        split_text = [line.split(' ') for line in self.text.splitlines()]

        x, y = (0, 0)
        space = self.font.size(' ')[0]

        for line in split_text:
            for word in line:
                word_surface = self.font.render(word, True, self.text_color)
                word_width, word_height = word_surface.get_size()
                if x + word_width > self.w:
                    x = 0
                    y += word_height
                self.image.blit(word_surface, (x, y))
                x += word_width + space
            x = 0
            y += word_height

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

class InputBox(object):
    """Input Boxes can be easily generated and managed as a single class.
    """

    def __init__(self, x, y, w, h, font, inactive_colour, active_colour, text =''):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = (0,0,255)
        self.highlight_colour = active_colour
        self.text = text
        self.font = font
        self.txt_surface = self.font.render (self.text, True, self.colour)
        self.active = False
        self.highlightrect = pygame.Rect(x -2, y-2, w+4, h+4)

    def add_character(self, char):
        self.text = self.text + char
        self.txt_surface = self.font.render (self.text, True, self.colour)
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        self.highlightrect.w = width +4


    def remove_character(self):
        if len(self.text) >= 1:
            self.text = self.text[:-1]
            self.txt_surface = self.font.render (self.text, True, self.colour)

      
    def draw_input_box(self, game_state):
        game_surface = game_state.get('game_surface') 
        game_surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(game_surface, self.colour, self.rect, 2)
        if self.active == True:
            pygame.draw.rect(game_surface, self.highlight_colour, self.highlightrect, 2)
        

    def toggle_active(self):
        if self.active == False:
            self.active = True
            return
        if self.active == True:
            self.active =  False
            return

    def event_handle(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.remove_character()

            else:
                self.add_character(event.unicode)

