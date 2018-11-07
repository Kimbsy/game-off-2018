import pygame
import os

class BaseSprite(pygame.sprite.Sprite):
    """The base sprite class contains useful common functionality.
    """

    def __init__(self, x, y):
        super(BaseSprite, self).__init__()

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
        dir_path = os.path.dirname(os.path.realpath(__file__))
        loaded_img = pygame.image.load(dir_path + '/../data/' + self.img_name)
        size = loaded_img.get_size()

        # Create a surface containing the image with a transparent
        # background.
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.image.blit(loaded_img, (0, 0))

    def move(self, move):
        """Apply a translation the the position of this sprite's
        rect based on a mousemotion relative movement.
        """
        self.rect.x += move[0]
        self.rect.y += move[1]

class ButtonSprite(BaseSprite):
    """Sprite which displays as a clickable button with text.
    """

    def __init__(self, x, y, text, f):
        # Need to specify properties before init_img is called.
        self.font = pygame.font.SysFont(None, 25)
        self.text = text
        self.text_color = (200, 200, 200)
        self.f = f

        # Call the parent constructor.
        super(ButtonSprite, self).__init__(x, y)

    def init_image(self):
        self.image = pygame.Surface([100, 20])
        self.image.fill((100, 100, 100))
        
        rendered_text = self.font.render(self.text, True, self.text_color)
        self.image.blit(rendered_text, (15, 0))

    def on_click(self):
        """Invoke the on_click function.
        """
        self.f()
