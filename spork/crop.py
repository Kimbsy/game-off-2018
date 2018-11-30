import pygame, sys, os
from PIL import Image

pygame.init()

def displayImage(screen, px, topleft, prior, image_offset, crop_surface):
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

    #draw other objects on screen
    pygame.draw.rect(screen, (255,255,255) , (0,0 , crop_surface[0], crop_surface[1]))
    instruction_image = pygame.image.load(os.getcwd() + "/data/imgbase/mouseleft.png")
    
    screen.blit(instruction_image, (200 - (instruction_image.get_rect().w/2), 50))
    screen.blit(px, image_offset)

    # draw transparent box and blit it onto canvas
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)
def setup(path, mirror = False):
    crop_surface = (1200, 625)
    image_offset = (500,50)

    px = pygame.image.load(path)
    
    
    screen = pygame.display.set_mode( (crop_surface) )

    
    pygame.draw.rect(screen, (255,255,255) , (0,0 , crop_surface[0], crop_surface[1]))
    instruction_image = pygame.image.load(os.getcwd() + "/data/imgbase/mouseleft.png")
    screen.blit(instruction_image, (200 - (instruction_image.get_rect().w/2), 50))
    screen.blit(px, (image_offset))

   
    pygame.display.flip()
    return screen, px ,crop_surface, image_offset

def cropLoop(screen, px, crop_surface, image_offset, confirm_crop):
    topleft = bottomright = prior = None
    obj_rect = px.get_rect()
    n=0
    x=0
    new_rect = pygame.Rect(0,0, crop_surface[0], crop_surface[1])
    while n!=1:
        if new_rect.collidepoint(pygame.mouse.get_pos()) == True:
              
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
                    prior = displayImage(screen, px, topleft, prior, image_offset, crop_surface)
        if bottomright:
            
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
