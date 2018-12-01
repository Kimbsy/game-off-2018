import pygame, os
import math

# Import helper functions.
from helpers import top_draggable_sprite_at_point, aspect_scale, draw_rects

def button_at_point(sprites, pos):
    """Returns a sprite from the sprite group containing the mouse
    position which is of type ButtonSprite.

    Buttons won't overlap so we don't need to reverse the group.
    """
    for sprite in sprites.sprites():
        if (type(sprite) is ButtonSprite) and sprite.rect.collidepoint(pos):
            return sprite
        elif (type(sprite) is ButtonImageSprite) and sprite.rect.collidepoint(pos):
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
    """Sprite which loads an image.

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
        self.selected = False # allows object to be selected even when not hovered over

    def clone(self, offset=(0, 0)):
        x_offset, y_offset = offset
        clone = ImageSprite(self.x + x_offset, self.y + y_offset, self.img_name)
        clone.image = self.image
        clone.rect = self.image.get_rect()
        clone.rect.x = self.rect.x + x_offset
        clone.rect.y = self.rect.y + y_offset
        clone.rotation = self.rotation
        clone.scale = self.scale
        return clone

    def move(self, move):
        """Apply a translation the the position of this sprite's
        rect based on a mousemotion relative movement.
        """
        self.x += move[0]
        self.y += move[1]
        self.rect.x += move[0]
        self.rect.y += move[1]

    def rotate_clockwise(self):
        self.rotation = self.rotation - 30
        if self.rotation == 360:
            self.rotation = 0
        self.update_sprite()

    def rotate_counterclockwise(self):
        self.rotation = self.rotation + 30
        if self.rotation == 360:
            self.rotation = 0
        self.update_sprite()

    def scale_down(self):
        if self.scale - 2 > 0:
            self.scale = self.scale - 2
        self.update_sprite()

    def scale_up(self):
        self.scale += 2
        self.update_sprite()

    def update_sprite(self):

        rotrads = (self.rotation*2*math.pi)/360
        scaled_width = (self.orig_width*self.scale)/100
        scaled_height = (self.orig_height*self.scale)/100
        
        new_width = abs(scaled_height*math.sin(rotrads)) + abs(scaled_width*math.cos(rotrads))

        new_height = abs(scaled_width*math.sin(rotrads)) + abs(scaled_height*math.cos(rotrads))

        loc = self.rect.center

        tempimage = pygame.transform.rotate(self.origimage, self.rotation)
        self.image = aspect_scale( tempimage, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = loc

    def toggle_selected(self):
        if self.selected == False:
            self.selected = True
            return
        if self.selected == True:
            self.selected =  False
            return


class ButtonSprite(BaseSprite):
    """Sprite which displays as a clickable button with text.
    """

    def __init__(self, x, y, text, f, args, w=100, h=20, color=(100,100,100), text_color=(200,200,200)):
        # Need to specify properties before init_img is called.
        self.text = text
        self.f = f
        self.args = args
        self.w = w
        self.h = h
        self.color = color
        self.text_color = text_color

        # Define button text font.
        self.font = pygame.font.SysFont(None, 25)

        # Call the parent constructor.
        super(ButtonSprite, self).__init__(x, y)

    def init_image(self):
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(self.color)
        
        rendered_text = self.font.render(self.text, True, self.text_color)
        text_width, text_height = rendered_text.get_size()
        x_offset = (self.w / 2) - (text_width / 2)
        y_offset = (self.h / 2) - (text_height / 2)
        self.image.blit(rendered_text, (x_offset, y_offset))

    def on_click(self, game_state):
        """Invoke the on_click function.
        """
        return self.f(game_state, *self.args)

class ButtonImageSprite(BaseSprite):
    "clickable image that performs a function"

    def __init__(self,x ,y, img_path, f, args, w=None, h=None):
        self.x = x
        self.y = y
        self.img_path = img_path
        self.f = f
        self.args = args
        self.w = w
        self.h = h
        
        super(ButtonImageSprite, self).__init__(x,y)

    def init_image(self):
        loaded_img = pygame.image.load(self.img_path)
        size = loaded_img.get_size()

        # Create a surface containing the image with a transparent
        # background.

        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.image.blit(loaded_img, (0, 0))
        if self.w:
            self.image = aspect_scale(self.image, (self.w, self.h))


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
        self.font = pygame.font.Font("ARCADECLASSIC.TTF", 40)
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

    def __init__(self, x, y, w, h, font, inactive_colour, active_colour, center_x, text ='', min_width = 300, max_width =550):
        if w < min_width:
            w= min_width

        self.rect = pygame.Rect(x, y, w, h)
        self.center_x = center_x
        self.colour = (0,0,255)
        self.highlight_colour = active_colour
        self.text = text
        self.font = font
        self.txt_surface = self.font.render (self.text, True, self.colour)
        self.min_width = min_width
        self.max_width =max_width
        self.active = False
        self.highlightrect = pygame.Rect(x -2, y-2, w+4, h+4)
        self.framecount = 1

        self.adjust()

    def adjust(self):
        width = max(200, self.txt_surface.get_width()+10)
        if width >= self.min_width:
            pass
        else:
            width = self.min_width
        self.rect.w = width
        self.highlightrect.w = width+4

        if self.center_x:
            self.rect.x = self.center_x - (0.5*self.rect.w)

        self.highlightrect = pygame.Rect(
            self.rect.x -2,
            self.rect.y-2,
            self.rect.w+4,
            self.rect.h+4
        )

    def add_character(self, char):
        if self.rect.w <= self.max_width:
            self.text = self.text + char
            self.txt_surface = self.font.render(self.text, True, self.colour)
            self.adjust()

    def remove_character(self):
        if len(self.text) >= 1:
            self.text = self.text[:-1]
            self.txt_surface = self.font.render (self.text, True, self.colour)
        self.adjust()    

      
    def draw_input_box(self, game_state):
        fps = game_state.get('fps')
        game_surface = game_state.get('game_surface') 
        game_surface.blit(self.txt_surface, (self.center_x+5 - (self.txt_surface.get_width()/2), self.rect.y+5))
        pygame.draw.rect(game_surface, self.colour, self.rect, 2)
        if self.active == True:
            pygame.draw.rect(game_surface, self.highlight_colour, self.highlightrect, 2)
            if self.framecount <= (fps/2):
                self.framecount += 1
            if self.framecount < fps and self.framecount > (fps/2):
                self.framecount += 1
                pygame.draw.line(game_surface,self.highlight_colour, (self.center_x +5 +(self.txt_surface.get_width()/2), self.rect.y +5), (self.center_x +5 +(self.txt_surface.get_width()/2), self.rect.y -5 +self.rect.h))
            if self.framecount >= fps:
                self.framecount =1
        

    def toggle_active(self):
        if self.active == False:
            self.active = True
            return
        if self.active == True:
            self.active =  False
            return

    def event_handle(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            self.remove_character()
            return

        if event.type == pygame.KEYDOWN:
            self.add_character(event.unicode)
            return
class ConfirmBox(object):
    """Input Boxes can be easily generated and managed as a single class.
    """

    def __init__(self, center_x, center_y, message, alt_surface = None, width = 350, height = 190, box_colour = (25,25,220) , message_colour = (230,150,100)):
             
        self.center_x = center_x
        self.center_y = center_y
        self.message = message
        self.rect = pygame.Rect(center_x - (width/2), center_y-(height/2), width, height)
        self.box_colour = box_colour
        self.message_colour = message_colour
        self.font = pygame.font.Font(None, 50)
        self.txt_surface = self.font.render (self.message, True, self.message_colour)
        self.active = False
        self.proceed = None
        self.alt_surface = alt_surface

        self.buttons = pygame.sprite.Group()
        self.yes = ButtonImageSprite(center_x-100, center_y, os.getcwd() + "/data/imgbase/tickbuttonsmall.png", self.confirm, [])
        self.no = ButtonImageSprite(center_x+30, center_y, os.getcwd() + "/data/imgbase/delbuttonsmall.png", self.cancel, [])
        self.buttons.add(self.yes, self.no)
        
       
    def confirm(self, game_state):
        self.proceed = True

    def cancel(self, game_state):
        self.proceed = False

    def toggle_active(self):
        if self.active == False:
            self.active = True
            return
        if self.active == True:
            self.active =  False
            return

    def draw_confirm_box(self, game_state):
        if self.active == True:
            if self.alt_surface:
                game_surface = alt_surface
            else:
                game_surface = game_state.get('game_surface')
            pygame.draw.rect(game_surface, self.box_colour, self.rect)
            game_surface.blit(self.txt_surface, (self.center_x+5 - (self.txt_surface.get_width()/2), self.rect.y+20))
            self.buttons.draw(game_surface)
        
        return game_state        

    def event_handle(self, game_state):
        
        if self.active == True:
            self.draw_confirm_box(game_state)
            pygame.display.update()
            n=0
            while n !=1:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        b = button_at_point(self.buttons, event.pos)
                        if b:
                            if event.button == 1:
                                b.on_click(game_state)
                                n=1
                                return game_state
