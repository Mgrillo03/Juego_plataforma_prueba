from distutils.errors import LinkError
from tkinter.tix import Tree
import pygame, sys
from pygame import key
from personaje import Personaje
from villian import Wolf

from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_b, K_n, K_v
pygame.init()

# Useful Function

def in_platform (platforms,pos_x, pos_y):
    '''
        In platform
        this funtion sets if the character is on a platform

        parameters: 
            - **platforms: array** coordinates of every platform on the map
            - **pos_x: float** pos in X axis of the character
            - **pos_y: float** pos in Y axis of the character
        returns: 
            - **True** if the character is on a platform, **False** when its not 
            - **platforms.index(i): int** idex of the platform the character is on
    '''
    for i in platforms:
 
        if pos_x > i[0] and pos_x < i[1] and pos_y <= i[2] and pos_y >= i[2] - 5:
            return True, platforms.index(i)
        
    return False, platforms.index(i)

def in_position (pos1,pos2):
    """
        In position
        this function evaluates the distance between two points of the maps, and determines if the are close enough to make contact

        parameters:
            - **pos1: float** 
            - **pos2: float**
        returns True when they are close, False when they aren't    
    """
    if abs(pos1[0] - pos2[0]) < 20 and abs(pos1[1] - pos2[1]) < 10:
        return True

# Colors
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
GREEN   = (   0, 255,   0)
RED     = ( 255,   0,   0)
BLUE    = (   0,   0, 255)

# Windows size
size  = (800, 500)
# initiate window
screen = pygame.display.set_mode(size)


# Characters init
link = Personaje()
wolf = Wolf()


# keyboard variables init
up      = False
down    = False
left    = False
right   = False

# Platforms variables init
on_platform = False
aux_platform = False

# Platforms coodinates
platforms = [(192,335,340),(367,510,340),(400,543,275),(327,470,210),(530,675,210)]
# set platforms on screen
plat_pos = platforms[0] 
# platforms image load
platform = pygame.transform.scale(pygame.image.load('textures/platforma.png'),(150,100)) #redimensionar el png de la platforma

#Sowrd init
sword_pos = (600,210)
sword_visible = True

### Backgorund image load
background = pygame.image.load(r'textures\background.png')
#sword =  pygame.transform.scale(pygame.image.load(r'sprites\sword.png'),(30,35))
#sword =  pygame.image.load(r'sprites\sword.png')

aux = True
while True:

    ## Keyboard events read
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        keys = pygame.key.get_pressed()       
    
        if keys[K_UP] :
            link.jump = True
        if keys[K_DOWN]:
            
            down = True
        else: 
            down = False

        if keys[K_LEFT]:
            left = True
            link.direction = False
            
        else:
            left = False
        if keys[K_RIGHT]:
            right = True
            link.direction = True
        else:
            right = False
        if keys[K_SPACE] and link.take_sword:
            link.hitting = True
        
        on_sword = in_position((link.pos_x,link.pos_y),sword_pos)
        if keys[K_b] and on_sword:
            link.take_sword = True
            sword_visible = False
            if link.direction :
                link.image_dir = 'rs0'
            else:
                link.image_dir = 'ls0'
        if keys[K_n]:
            link.take_sword = False
            sword_pos = (link.pos_x, link.pos_y)
            sword_visible = True
            if link.direction :
                link.image_dir = 'r0'
            else:
                link.image_dir = 'l0'
        
        if keys[K_v]:
            link.speed = True
            
        else:
            link.speed = False


    ## GRID
    # RENDER GAME GRID
    screen.blit(background,(0,0))

    ## Render platforms    
    for i in platforms:
        screen.blit(platform,(i[0]+42,i[2]+10))

    



## Movement 
    
    if down  and not link.jump and not link.is_jumping: 
        #pos_y += paso
        link.image_dir = 'f0'
        #if cont:
        #    walk = next(walk)
        #cont = true_false(cont)
        #down = False
        
   
# side movements
    if left and link.pos_x > 2 and not link.dead:
        #sprint del personaje
        link.move()
        
    if right and link.pos_x < 770 and not link.dead:
        link.move()
            
# Jump
    # jump init
    if link.jump and not link.is_jumping and not link.dead:
        link.start_jump()    
    
    # continue jumping
    if link.is_jumping :
        link.jumping()
                    
#S determine if the caracter is on a platform
    link.on_platform, plat_index = in_platform(platforms,link.pos_x,link.pos_y)
    plat_pos = platforms[plat_index]
    if link.on_platform:
        link.set_on_platform(plat_pos_y= plat_pos[2])
        
    else:
        link.out_of_platform()
        
    # Link hitting  
    if link.hitting and link.take_sword:
        link.hit()
        if in_position((link.pos_x,link.pos_y),(wolf.posx,wolf.posy)):
            wolf.dead = True

# characters crash
    if in_position((link.pos_x, link.pos_y),(wolf.posx,wolf.posy)):
        if not wolf.dead and not link.hitted:
            #link.hitted = True
            link.dead = True

    if link.dead :
        link.defeated()

    if link.hitted :
        link.injured()
        #link.visible = False
        if link.counter == 100:
            link.counter = 0
            link. visible = True
            link.hitted = False
            sword_pos = (600,210)
            sword_visible = True

    else:
        link.visible = True

    

# Wolf movement
    if wolf.posx < -60:
        wolf.posx = 1000

# wolf dead
    if wolf.dead:
        if aux:
            direction = link.direction
            aux = False
        wolf.defeated(direction)
    else:
        wolf.move()
        aux = True

        
### ---- Render zone  
   
    # character image load
    image = pygame.image.load(r'.\sprites\link\link_'+link.image_dir+'.png')
    # wolf image load
    wolf_image = pygame.image.load('./sprites/wolf/'+wolf.image+'.png')
    # sword image load
    sword_image = pygame.image.load('./sprites/sword.png')
    
    #character render
    if link.visible:
        screen.blit(image,(link.pos_x,link.pos_y))
    # wolf render
    screen.blit(wolf_image,(wolf.posx,wolf.posy))
    # sword rnder
    if sword_visible:
        screen.blit(sword_image,sword_pos)

    #screen.blit(sword,(link.pos_x + 15,link.pos_y))
    #pygame.draw.rect(screen, BLACK, (pos_x, pos_y, 80,80))

    ### ---- Render zone

# Update screen
    pygame.display.flip()

