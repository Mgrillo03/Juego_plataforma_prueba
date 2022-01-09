import pygame, sys
from pygame import key

from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_b
pygame.init()

def true_false(aux):
    if aux:
        return False
    else:
        return True

def next(pos):
    if pos < 6:
        return pos + 1
    else:
        return 1
    
def in_plataform (x,y,pos_x, pos_y):
    if pos_x > x[0] and pos_x < x[1] and pos_y <= y:
        return True

    

#Definir Colores
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
GREEN   = (   0, 255,   0)
RED     = ( 255,   0,   0)
BLUE    = (   0,   0, 255)

#Crear ventana
size  = (800, 500)

screen = pygame.display.set_mode(size)
#Posicion inicial
pos_y = 395
pos_x = 100

#inicializacion
cont    = False
paso    = 1
paso_jump = 4
up      = False
down    = False
left    = False
right   = False
walk = 0
limit_y = 410
speed = False
jump = False
is_jumping = False
jump_aux = pos_y
jump_max_distance = 70

###Plataforma
on_plataform = False
plat_pos_x = (400, 550)
plat_pos_y = 345

plataform = pygame.transform.scale(pygame.image.load('textures/plataforma.png'),(150,100))

### Fondo
background = pygame.image.load(r'textures\background.png')

###Plataforma

suma = 0

image_dir = 'f1'
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_UP] :
            up = True
        else :
            up = False
        if keys[K_DOWN]:
            down = True
        else: 
            down = False
        if keys[K_LEFT]:
            left = True
        else:
            left = False
        if keys[K_RIGHT]:
            right = True
        else:
            right = False
        if keys[K_b]:
            speed = True
        else:
            speed = False
        if keys [K_SPACE]:
            jump = True

    ## GRID
    # RENDER GAME GRID
    screen.blit(background,(0,0))

    ## Plataforma
    screen.blit(plataform,(400,350))
    
    
    ### ---- ZONA DE DIBUJO

    ###Movimiento
    ''''
    if up and pos_y > limit_y and not jump and not is_jumping:
        pos_y -= paso
        image_dir = 'b'+str(walk)
        if cont:
            walk = next(walk)
        cont = true_false(cont)
        #up = False
    if down and pos_y < 450 and not jump and not is_jumping: 
        pos_y += paso
        image_dir = 'f'+str(walk)
        if cont:
            walk = next(walk)
        cont = true_false(cont)
        #down = False
        '''
    if left and pos_x > 2:
        if speed:
            pos_x -= paso*4
        else:
            pos_x -= paso
        
        image_dir = 'l'+str(walk)
        if cont and not is_jumping:
            walk = next(walk)
        cont = true_false(cont)
        if is_jumping:
            image_dir = 'l5'
        #left = False
    if right and pos_x < 790:
        if speed:
            pos_x += paso*4
        else:
            pos_x += paso
        image_dir = 'r'+str(walk)
        if cont and not is_jumping:
            walk = next(walk)
        cont = true_false(cont)
        if is_jumping:
            image_dir = 'r2'
        #right = False
    ### Salto
    if jump and not is_jumping:
        is_jumping = True
        jump_aux = pos_y
        going_up = True
        jump_max = pos_y - jump_max_distance
        jump = False
    

    if is_jumping :
        
        if pos_y <= jump_aux and pos_y > jump_max and going_up:
            print('subiendo')
            pos_y -= paso_jump
        elif pos_y <= jump_max and going_up:
            print('arriba')
            going_up = False
            pos_y += paso_jump
        elif pos_y < jump_aux and pos_y > jump_max and not going_up and not on_plataform:
            print('bajando')
            pos_y += paso_jump
        elif pos_y >= jump_aux and not going_up :
            print('abajo')
            pos_y = jump_aux
            is_jumping = False
            jump = False
        
    on_plataform = in_plataform(plat_pos_x,plat_pos_y,pos_x,pos_y)
    if on_plataform:
        suma += 1
        jump_aux = plat_pos_y
        print('estoy aqui'+str(suma))
        #going_up = False
    else:
        jump_aux = 395
        suma = 0
        
    
   
   
    image = pygame.image.load(r'.\sprites\link\link_'+image_dir+'.png')
    
    screen.blit(image,(pos_x,pos_y))
    #pygame.draw.rect(screen, BLACK, (pos_x, pos_y, 80,80))
    

    


    ### ---- ZONA DE DIBUJO

    #Actualizar Pantalla
    pygame.display.flip()
