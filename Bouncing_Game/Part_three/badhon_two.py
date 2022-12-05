import pygame
from pygame.locals import *


pygame.init()

# arrow speed
clock = pygame.time.Clock()
fps = 60




screen_width = 900
screen_height = 900

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('NSL Game Made by Badhon')

# define game variables
title_size = 45
game_over = 0

# Load Image
background_img = pygame.image.load('img/a.png')
restart_img = pygame.image.load('img/restart_btn.png')

# def draw_grid():
#     for line in range(0,20):
#         pygame.draw.line(screen,(255,255,255),(0,line * title_size),(screen_width,line * title_size))
#         pygame.draw.line(screen,(255,255,255),(line * title_size,0),(line * title_size,screen_height))


class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()

        # chceck mouse over and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                action = True
                print('Clicked')
                self.clicked = True
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked = False

        # draw button
        screen.blit(self.image,self.rect)
        return action

# Players

class Player():
    def __init__(self,x,y):
        self.reset(x,y)



    def update(self,game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over ==0:

            # get pressed 
            key = pygame.key.get_pressed()

            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False :
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


            # check for collision
            self.in_air = True
            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx ,self.rect.y  ,self.width ,self.height):
                    dx  = 0 
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x ,self.rect.y + dy ,self.width ,self.height):
                    #check if blow the ground i.e jumping
                    if self.vel_y <0:
                        dy = tile[1].bottom - self.rect.top
                    if self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom 
                        self.vel_y = 0
                        self.in_air = False

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
            # check for collision with lava   
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1



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

            # if self.rect.bottom > screen_height:
            #     self.rect.bottom = screen_height
            #     dy = 0
        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y >300:
                self.rect.y -= 1.5

        # draw player onto screen
        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen,(255,255,255),self.rect, 2)

        return game_over
    def reset(self,x,y):
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
        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]
        self.image = pygame.transform.scale(img_right,(40,80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True




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
                if tile==3:
                    blob =Enemy(col_count * title_size,row_count* title_size +10)
                    blob_group.add(blob)
                if tile == 6:
                    lava =Lava(col_count * title_size,row_count* title_size + (title_size//2))
                    lava_group.add(lava)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
            pygame.draw.rect(screen,(255,255,255), tile[1],1 )
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.rect =self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter +=1
        if abs(self.move_counter )>50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x,y ):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img,(title_size,title_size //2 ))
        self.rect =self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0




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
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
world = World(world_data)

# create restart buttons
restart_button = Button(screen_width//2 -50,screen_height//2 +100,restart_img)
run = True
while run:
    # control arrow speed
    clock.tick(fps)

    screen.blit(background_img,(0,0))
    # if you want to show the grid line
    # draw_grid()
    world.draw()
    if game_over==0:
        blob_group.update()
    blob_group.draw(screen)
    lava_group.draw(screen)
    
    game_over = player.update(game_over)


    if game_over == -1:
        if restart_button.draw():
            player.reset(100,screen_height -130)
            game_over = 0
            
    
    

    # print(world.tile_list)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()