import cocos
from cocos.director import director

import pyglet

class KeyDisplay(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(KeyDisplay, self).__init__()

        self.text = cocos.text.Label("", x=100, y=280)

        self.keys_pressed = set()
        self.update_text()
        self.add(self.text)

    def update_text(self):
        key_names = [pyglet.window.key.symbol_string (k) for k in self.keys_pressed]
        text = 'Keys: ' + ','.join(key_names)
        self.text.element.text = text

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        self.update_text()

    def on_key_release(self, key, modifiers):
        self.keys_pressed.remove(key)
        self.update_text()

class PicDisplay(cocos.layer.Layer):
    def __init__(self):
        sprite = cocos.sprite.Sprite('Mum.jpg')
        sprite.position = 320,240
        sprite.scale = 1
        self.add(sprite, z=2)

class MouseDisplay(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(MouseDisplay, self).__init__()

        self.posx = 100
        self.posy = 240
        self.text = cocos.text.Label('No mice events yet', x=self.posx, y=self.posy)
        self.add(self.text)

    def update_text(self, x, y):
        text = 'Mouse @ %d, %d' % (x +30, y +30)
        self.text.element.text = text
        self.text.element.x = self.posx
        self.text.element.y = self.posy
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.update_text(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.update_text(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.posx, self.posy = director.get_virtual_coordinates(x, y)
        self.update_text(x, y)







director.init(resizable=True)
director.run(cocos.scene.Scene(KeyDisplay(), MouseDisplay()))
