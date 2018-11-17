import pygame, os

# Import helper functions.
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
        self.image = pygame.transform.rotate(self.image,45)
        self.rect = self.image.get_rect()

    def scale(self):
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()


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

    def __init__(self, x, y, w, h, text, text_color=(0, 0, 0)):
        self.w = w
        self.h = h
        self.text = text

        # Define button text font.
        self.font = pygame.font.SysFont(None, 25)
        self.text_color = text_color
        
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
                self.max_x = x
            x = 0
            y += word_height

        self.max_y = y
        if y > word_height:
            self.max_x = self.w

class ToastSprite(BaseSprite):
    """Displays a notification at the bottom of the screen.
    """

    def __init__(self, screen_size, index, message):
        self.level = message.get('level')
        self.text = message.get('text')
        self.screen_size = screen_size
        self.w = screen_size[0] * 0.5
        self.h = screen_size[1] * 0.1
        self.index = index
        self.age = 0
        self.done = False
        self.to_remove = False
        self.target_h = self.h

        if self.level == 'error':
            self.background_color = (244, 66, 66)
            self.text_color = (0, 0, 0)
        elif self.level == 'warn':
            self.background_color = (244, 190, 65)
            self.text_color = (0, 0, 0)
        elif self.level == 'ok':
            self.background_color = (65, 244, 110)
            self.text_color = (0, 0, 0)

        super(ToastSprite, self).__init__(
            self.screen_size[0] * 0.25,
            self.h * (9 - self.index)
        )
        self.target_y = self.rect.y

    def init_image(self):
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(self.background_color)
        text = TextSprite(
            0,
            0,
            self.w * 0.8,
            self.h,
            self.text,
            text_color=self.text_color
        )
        x_offset = (self.w * 0.5) - (text.max_x * 0.5)
        y_offset = (self.h * 0.5) - (text.max_y * 0.5)
        self.image.blit(text.image, (x_offset, y_offset))

    def slide_down_by_one(self, new_index):
        self.index = new_index
        self.target_y += self.h

    def update(self, i):
        self.rect.x = self.screen_size[0] * 0.25
        self.rect.y = self.h * (9 - self.index)

        if not self.done:
            self.age += 1
        elif self.target_h > 0:
            self.target_h = max(self.target_h - 6, 0)
            self.image = pygame.transform.scale(
                self.image,
                (int(self.w), int(self.target_h))
            )
        else:
            self.to_remove = True

        if self.target_y > self.y:
            self.y = max(self.y + 1, self.target_y)
            self.rect.y = self.y

class ToastStack(pygame.sprite.Group):
    """Displays messages the bottom of the screen for a few seconds to
    notify the player of something.
    """

    def __init__(self):
        super(ToastStack, self).__init__()

    def init_size(self, screen_size):
        self.screen_size = screen_size

    def push(self, message):
        index = len(self.sprites())
        self.add(ToastSprite(self.screen_size, index, message))

    def pop(self, toast):
        self.remove(toast)
        self.slide_down()

    def slide_down(self):
        for i, toast in enumerate(self.sprites()):
            toast.slide_down_by_one(i)

    def update(self):
        for i, toast in enumerate(self.sprites()):
            toast.update(i)
            if toast.to_remove:
                self.pop(toast)
            elif toast.age > 180:
                toast.done = True

class InputBox:
    """Input Boxes can be easily generated and managed as a single class.
    """

    def __init__(self, x, y, w, h, text =''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (0,0,255)
        self.text = text
        self.txt_surface = FONT.render (text, True, self.color)
        self.active = False
