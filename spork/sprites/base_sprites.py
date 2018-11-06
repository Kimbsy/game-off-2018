import pygame
import os

class BaseSprite(object):
    """Base sprite class.

    Has x and y position, as well as skeleton function
    for getting bounding rectangle.
    """

    def __init__(self, x, y):
        self.pos = (x, y)
        self.is_draggable = False

    def display(self, game_display):
        """Draw the sprite to the game_display.
        """
        raise NotImplementedError('Please implement a display method')

    def get_size(self):
        """Get the width and height of the sprite.
        """
        raise NotImplementedError('Please implement a get_size method')

    def get_rect(self):
        """Get the bounding rectangle for the sprite.
        """
        size = self.get_size()
        return pygame.Rect(self.pos[0], self.pos[1], size[0], size[1])

class ImageSprite(BaseSprite):
    """Sprite which loads an image from ../data/ directory.

    Currently this will load the image each time a sprite
    is made, should cache images somewhere in future.
    """

    def __init__(self, x, y, img_name):
        super(ImageSprite, self).__init__(x, y)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.image = pygame.image.load(dir_path + '/../data/' + img_name)
        self.is_draggable = True

    def display(self, game_display):
        """Draw the bounding rectangle, then blit the
        image to the screen.
        """
        pygame.draw.rect(game_display, (0, 0, 255), self.get_rect(), 2)
        game_display.blit(self.image, self.pos)

    def get_size(self):
        """Sprite size is based on the image.
        """
        return self.image.get_size()
