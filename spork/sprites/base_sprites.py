import pygame, os

from helpers import *

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

    def move(self, move):
        """Apply a translation the the position of this sprite's
        rect based on a mousemotion relative movement.
        """
        self.x += move[0]
        self.y += move[1]
        self.rect.x += move[0]
        self.rect.y += move[1]

    def rotate90(self):
        self.image = pygame.transform.rotate(self.image,90)

    def scale(self):
        self.image = pygame.transform.scale(self.image, (50,50))

class ThumbnailSprite(ImageSprite):
    #Make thumbnails not draggable and small
    def __init__(self, x, y, img_name):
        super(ThumbnailSprite, self).__init__(x, y, img_name)

        self.is_draggable = False

    def init_image(self):
        # Load the image from file and scale it to thumbnail size.
        dir_path = os.path.dirname(os.path.realpath(__file__))
        loaded_img = pygame.image.load(dir_path + '/../data/' + self.img_name)
        size = loaded_img.get_size()

        # Create a surface containing the image with a transparent
        # background.
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)

        self.image.blit(loaded_img, (0, 0))

        self.image = aspect_scale(self.image, 50, 50)

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

class InputBox:
    """Input Boxes can be easily generated and managed as a single class.
    """

    def __init__(self, x, y, w, h, text =''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (0,0,255)
        self.text = text
        self.txt_surface = FONT.render (text, True, self.color)
        self.active = False

