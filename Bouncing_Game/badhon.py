import pygame
from pygame.locals import *


pygame.init()


screen_width = 750
screen_height = 550

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('NSL Game Store')

# Load Image
# sun_img = pygame.image.load('img/sun.jpg')
bg_img = pygame.image.load('img/a.png')






run = True
while run:
    screen.blit(bg_img,(0,0))
    # screen.blit(sun_img,(0,0))

    pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()