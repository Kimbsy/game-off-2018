import pygame

from sprites.base_sprites import ImageSprite, CompoundSprite

pygame.init()
game_display = pygame.display.set_mode((750, 1000))
pygame.display.set_caption('foo')

red_sprite = ImageSprite(100, 100, 'r.png')
blue_sprite = ImageSprite(400, 500, 'u.png')

trip_green_sprite = CompoundSprite(600, 100, [])
trip_green_sprite.add(ImageSprite(0, 0, 'g.png'))
trip_green_sprite.add(ImageSprite(0, 150, 'g.png'))
trip_green_sprite.add(ImageSprite(0, 300, 'g.png'))

sprites = [red_sprite, blue_sprite, trip_green_sprite]

def get_nested_sprites():
    all_sprites = []
    for sprite in sprites:
        if type(sprite) is CompoundSprite:
            all_sprites.extend(sprite.children)
        all_sprites.append(sprite)

    return all_sprites

def draggable_sprite_at_point(pos):
    for sprite in reversed(get_nested_sprites()):
        if sprite.is_draggable and sprite.get_rect().collidepoint(pos):
            return sprite

def gameloop():
    done = False
    dragging = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                s = draggable_sprite_at_point(event.pos)
                if s:
                    print('start dragging')
                    dragging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                print('end dragging')
                dragging = False

        for sprite in sprites:
            sprite.display(game_display)
            
        pygame.display.flip()


    

gameloop()
pygame.quit()
quit()
