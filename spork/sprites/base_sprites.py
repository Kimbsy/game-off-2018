import pygame
import os

class BaseSprite(object):

    def __init__(self, x, y):
        self.pos = (x, y)
        self.is_draggable = False

    def display(self, game_display):
        raise NotImplementedError('Please implement a display method')

    def get_size(self):
        raise NotImplementedError('Please implement a get_size method')

    def get_rect(self):
        size = self.get_size()
        return pygame.Rect(self.pos[0], self.pos[1], size[0], size[1])

class ImageSprite(BaseSprite):

    def __init__(self, x, y, img_name):
        super(ImageSprite, self).__init__(x, y)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.image = pygame.image.load(dir_path + '/../data/' + img_name)
        self.is_draggable = True

    def display(self, game_display):
        pygame.draw.rect(game_display, (0, 0, 255), self.get_rect(), 2)
        game_display.blit(self.image, self.pos)

    def get_size(self):
        return self.image.get_size()
