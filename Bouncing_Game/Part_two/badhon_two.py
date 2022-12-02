import pygame
from pygame.locals import *


pygame.init()

# arrow speed
clock = pygame.time.Clock()
fps = 60




screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('NSL Game Made by Badhon')

# define game variables
title_size = 50


# Load Image
background_img = pygame.image.load('img/a.png')


# def draw_grid():
#     for line in range(0,20):
#         pygame.draw.line(screen,(255,255,255),(0,line * title_size),(screen_width,line * title_size))
#         pygame.draw.line(screen,(255,255,255),(line * title_size,0),(line * title_size,screen_height))



# Players

class Player():
    def __init__(self,x,y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right,(40,80))
            img_left = pygame.transform.flip(img_right,True,False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.image = self.images_right[self.index]
        self.image = pygame.transform.scale(img_right,(40,80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0


    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 5
        # get pressed 
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter +=1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter +=1
            self.direction = 1
        if key[pygame.K_LEFT]== False and key[pygame.K_RIGHT]== False:
            self.counter = 0
            self.index =0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        # add Gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
 
        # Handle animation
        
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

# calculate new playrt position
        #check collision at new position
# adjust player position
        # update player co-ordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0


        # draw player onto screen
        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen,(255,255,255),self.rect, 2)




class World():
    def __init__(self,data):
        self.tile_list = []

        # Load images
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')

        row_count= 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1 :
                    img = pygame.transform.scale(dirt_img, (title_size,title_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count *title_size
                    img_rect.y = row_count *title_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2 :
                    img = pygame.transform.scale(grass_img, (title_size,title_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count *title_size
                    img_rect.y = row_count *title_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
            pygame.draw.rect(screen,(255,255,255), tile[1],1 )
            

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]




player = Player(100,screen_height -130)
world = World(world_data)

run = True
while run:
    # control arrow speed
    clock.tick(fps)

    screen.blit(background_img,(0,0))
    # if you want to show the grid line
    # draw_grid()
    world.draw()
    player.update()
    
    

    # print(world.tile_list)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()