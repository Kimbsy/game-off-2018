import pygame, sys
from PIL import Image
pygame.init()

def displayImage(screen, px, topleft, prior):
    # ensure that the rect always has positive width, height
    x, y = topleft
    width =  pygame.mouse.get_pos()[0] - topleft[0]
    height = pygame.mouse.get_pos()[1] - topleft[1]
    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)

    # eliminate redundant drawing cycles (when mouse isn't moving)
    current = x, y, width, height
    if not (width and height):
        return current
    if current == prior:
        return current

    # draw transparent box and blit it onto canvas
    screen.blit(px, px.get_rect())
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)
def setup(path, mirror = False):
    px = pygame.image.load(path)
    
    screen = pygame.display.set_mode( px.get_rect()[2:] )
    screen.blit(px, px.get_rect())
    # if mirror == True:
    #     px= pygame.transform.flip(px, True, False),
    
    pygame.display.flip()
    return screen, px

def cropLoop(screen, px):
    topleft = bottomright = prior = None
    obj_rect = px.get_rect()
    n=0
    x=0
    while n!=1:
        # if screen.get_rect().collidepoint(pygame.mouse.get_pos()) == True:
        #     print("TRUE")
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x=1
            if x ==1:
                if event.type == pygame.MOUSEBUTTONUP:
                    if not topleft:
                        topleft = event.pos
                    else:
                        bottomright = event.pos
                        n=1
        if topleft:
            prior = displayImage(screen, px, topleft, prior)
    return ( topleft + bottomright )

if __name__ == "__main__":
    input_loc = 'u.png'
    output_loc = 'out.png'
    screen, px = setup(input_loc)
    left, upper, right, lower = cropLoop(screen, px)

    # ensure output rect always has positive width, height
    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower
    im = Image.open(input_loc)
    im = im.crop(( left, upper, right, lower))
    pygame.display.quit()
    im.save(output_loc)