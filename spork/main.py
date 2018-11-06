import pygame

from sprites.base_sprites import ImageSprite

pygame.init()
clock = pygame.time.Clock()
game_display = pygame.display.set_mode((750, 1000))
pygame.display.set_caption('foo')
pygame.display.update()

sprites = [
    ImageSprite(300, 225, 'w.png'),
    ImageSprite(490, 363, 'u.png'),
    ImageSprite(418, 587, 'b.png'),
    ImageSprite(182, 587, 'r.png'),
    ImageSprite(110, 363, 'g.png'),
]

def top_draggable_sprite_at_point(pos):
    for sprite in reversed(sprites):
        if sprite.is_draggable and sprite.get_rect().collidepoint(pos):
            return sprite

def gameloop():
    done = False
    dragging = False
    dragged_sprite = None

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                s = top_draggable_sprite_at_point(event.pos)
                if s:
                    dragging = True
                    dragged_sprite = s
                    sprites.remove(s)
                    sprites.append(s)

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                dragged_sprite = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    pos = dragged_sprite.pos
                    rel = event.rel
                    dragged_sprite.pos = (pos[0] + rel[0], pos[1] + rel[1])
        
        game_display.fill((0, 0, 0))

        for sprite in sprites:
            sprite.display(game_display)
                
        pygame.display.update()
    

gameloop()
pygame.quit()
quit()
