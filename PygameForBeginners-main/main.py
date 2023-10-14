import pygame
import os

pygame.init()
#library for using small 2d games
#Pygame is not a singleton, 
# but it does operate on one primary display surface by default when you create a window using pygame.display.set_mode(). 
# However, Pygame is flexible and allows you to work with multiple display surfaces if needed.
WIDTH,HIGHT = 900 ,500
WIN = pygame.display.set_mode((WIDTH,HIGHT))
pygame.display.set_caption("First Game!") #display on current surface 
WHITE = (255,255,255)
BLACK = (0,0,0)

RED = (255,0,0)
YELLOW = (255,255,0)
#MIDDLE BOARDER
BOARDER = pygame.Rect((WIDTH/2)-5 ,0,10,HIGHT)

HEALTH_FONT = pygame.font.SysFont("comicsans" ,40)

FPS = 60 #how quikly we want it to be updated at
VEL = 5
BULLET_VEL = 20
MAX_BULLETS = 3
SPACESHIP_WIDTH , SPACESHIP_HIGHT = 55 , 40
#custom events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#there are many os so its might be / or \
YELLOW_SPACESHIP_IMAGE = pygame.image.load('.\Assets\spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HIGHT))
YELLOW_SPACESHIP_ROTATED = pygame.transform.rotate(YELLOW_SPACESHIP,90)

RED_SPACESHIP_IMAGE = pygame.image.load('.\Assets\spaceship_red.png')
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HIGHT))
RED_SPACESHIP_ROTATED = pygame.transform.rotate(RED_SPACESHIP,270)

SPACE = pygame.image.load('.\Assets\space.png')
SPACE = pygame.transform.scale(SPACE , (WIDTH,HIGHT))


def draw_window(yellow,red ,red_bullets ,yellow_bullets,red_health,yellow_health):
   #first we filling then updateing
   #the place of functions metter 
   #because of double buffering
   #if wont going to erase anything before it will stay same 
   #WIN.fill(WHITE)
   WIN.blit(SPACE,(0,0))
   pygame.draw.rect(WIN,BLACK,BOARDER)

   red_health_text = HEALTH_FONT.render("Health:" + str(red_health),1,WHITE)
   yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health),1,WHITE)

   WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10,10))
   WIN.blit(yellow_health_text,(10,10))
   #lets draw surface on surface
   WIN.blit(YELLOW_SPACESHIP_ROTATED,(yellow.x,yellow.y))
   WIN.blit(RED_SPACESHIP_ROTATED,(red.x,red.y))
   for bullet in red_bullets:
       pygame.draw.rect(WIN,RED ,bullet)

   for bullet in yellow_bullets:
       pygame.draw.rect(WIN,YELLOW  ,bullet)   

   pygame.display.update()


def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width  < BOARDER.x  : #RIGHT
        yellow.x += VEL   
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0  : #up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height< HIGHT - 15  : #down
        yellow.y += VEL  

def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BOARDER.x + BOARDER.width: #LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH : #RIGHT
        red.x += VEL   
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0  : #up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HIGHT - 15 : #down
        red.y += VEL  

def handle_bullets(yellow_bullets , red_bullets ,yellow ,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): #if yellow bullet got colided whit red character
           pygame.event.post(pygame.event.Event(RED_HIT))
           yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

        

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet): #if red bullet got colided whit red character
           pygame.event.post(pygame.event.Event(YELLOW_HIT))
           red_bullets.remove(bullet) 
        elif bullet.x < 0:
            red_bullets.remove(bullet)     

            

def main():
    #we need keep track of our spaceships
    red = pygame.Rect(700 ,100,SPACESHIP_WIDTH,SPACESHIP_HIGHT)
    yellow = pygame.Rect(300 ,100,SPACESHIP_WIDTH,SPACESHIP_HIGHT)
    clock = pygame.time.Clock()

    red_bullets = []
    yellow_bullets = []
    
    red_health = 10
    yellow_health = 10

    run = True
      
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                     bullet = pygame.Rect(yellow.x + yellow.width ,yellow.y + yellow.height/2 -2 ,10,5)
                     yellow_bullets.append(bullet)

                  if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS :
                      bullet = pygame.Rect(red.x ,red.y + red.height/2 -2 ,10,5)
                      red_bullets.append(bullet)
                      
            if event.type == RED_HIT:
                red_health-=1

            if event.type == YELLOW_HIT:
                yellow_health-=1
        winner_text = ""           
        if red_health <= 0:
            winner_text = "YELLOW WINS!"
        if yellow_health <= 0:
            winner_text = "RED WINS!"

        #we can multyple press key
        #print(red_bullets,yellow_bullets)
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)

 
         
        draw_window(yellow,red,red_bullets,yellow_bullets,red_health,yellow_health)
        clock.tick(FPS) #limiting the speed of while loop 

    pygame.quit()



    

#we wan to run this file directly not if this file was imported from everywhere else
# __name__ is the name of the file
if __name__ == "__main__":
    main()
