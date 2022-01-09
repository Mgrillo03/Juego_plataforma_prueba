import pygame, sys
from pygame import key

from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_b
pygame.init()

#Funciones utiles
#Cambia alterna entre true y false
def true_false(aux):
    if aux:
        return False
    else:
        return True
#Obetener el siguiente numero del 1 al 6--- se utiliza para cambiar de imagen mientras camina 
def next(pos):
    if pos < 6:
        return pos + 1
    else:
        return 1
#Saber si el personake se encuentra dentro de de los limites de una plataforma
def in_plataform (x,y,pos_x, pos_y):
    if pos_x > x[0] and pos_x < x[1] and pos_y <= y and pos_y >= y - 5:
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

#inicializacion de variables
cont    = False
#Velocidad del personaje
paso    = 1
#Velocidad del salto
paso_jump = 4
#inicializacion de movimientos
up      = False
down    = False
left    = False
right   = False
#Variable numero de imagen de caminata
walk = 0

#Limite superior para efecto de profundidad
#limit_y = 410
#Variable para activar el sprint
speed = False
#Variable de salto
jump = False #activar el salto
is_jumping = False #Saber si esta saltando
jump_aux = pos_y #lugar donde inicio el salto
jump_max_distance = 70 #altura maxima del salto
suma = 0 #variable de control para edicion
image_dir = 'f1'#imagen inicial del personaje
jump_max = pos_y - jump_max_distance #Altura maxima relativa

### Dibijo de la primera Plataforma
on_plataform = False
aux_plataform = False
plat_pos_x = (358, 505) #Posicion en eje x de la plataforma
plat_pos_y = 340  #posision en eje Y de la plataforma

plataform = pygame.transform.scale(pygame.image.load('textures/plataforma.png'),(150,100)) #redimensionar el png de la plataforma

### cargar imagen del fondo
background = pygame.image.load(r'textures\background.png')


while True:

    ## Lectura de teclas del usuario
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        keys = pygame.key.get_pressed()
       
        '''
        lectura de movimientos en eje Y deshabilitados
        if keys[K_UP] :
            #Por ahora deshabilitado
            up = True
        else :
            up = False
        if keys[K_DOWN]:
            #Por ahora deshabilitado
            down = True
        else: 
            down = False
        '''
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

    ## Dibujar Plataforma
    screen.blit(plataform,(400,350))
    
    


    ### Calculo de movimiento
    ''''
    Efecto de profundidad, eliminado momentaneamente 


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
   
   #Moviientos laterales
    if left and pos_x > 2:
        #sprint del personaje
        if speed:
            pos_x -= paso*4
        else:
            pos_x -= paso
        #cargar siguiente sprite
        image_dir = 'l'+str(walk)
        #Frenar la secuencia de sprites para hacerla mas fluida
        #si esta saltando carga el sprite de salto
        if cont and not is_jumping:
            walk = next(walk)
        cont = true_false(cont)
        if is_jumping:
            image_dir = 'l5'
        #left = False
    if right and pos_x < 790:
        #sprint del personaje
        if speed:
            pos_x += paso*4
        else:
            pos_x += paso
        #cargar siguiente sprite
        image_dir = 'r'+str(walk)
        #Frenar la secuencia de sprites para hacerla mas fluida
        #si esta saltando carga el sprite de salto
        if cont and not is_jumping:
            walk = next(walk)
        cont = true_false(cont)
        if is_jumping:
            image_dir = 'r2'
        #right = False
    
    ### Activar Salto
    #si se oprime la tecla del salto y no esta saltando previamente
    if jump and not is_jumping:
        is_jumping = True
        jump_aux = pos_y
        going_up = True
        jump_max = pos_y - jump_max_distance
        jump = False
        aux_plataform = False
    
    ### Funcionn del salto
    if is_jumping :
        
        #condicion de subida
        if pos_y <= jump_aux and pos_y > jump_max and going_up:
            #print('subiendo')
            pos_y -= paso_jump

        #condicion del punto mas alto
        elif pos_y <= jump_max and going_up:
            #print('arriba')
            going_up = False
            pos_y += paso_jump

        #Condicion de bajada
        elif pos_y < jump_aux and pos_y > jump_max and not going_up and not on_plataform:
            #print('bajando')
            pos_y += paso_jump

        #Condicion de llegada a piso
        elif pos_y >= jump_aux and not going_up:
            #print('abajo')
            pos_y = jump_aux
            is_jumping = False
            jump = False
        
    #Saber si el personaje esta en una plataforma
    on_plataform = in_plataform(plat_pos_x,plat_pos_y,pos_x,pos_y)
    if on_plataform:
        suma += 1        
        #   print('estoy aqui'+str(suma))
        if not aux_plataform and not going_up:
            #print('llegue')
            jump_aux = plat_pos_y
            is_jumping =False
            jump = False
            pos_y = plat_pos_y
            aux_plataform = True
        #going_up = False
    elif not on_plataform:
        jump_aux = 395
        suma = 0
        if aux_plataform:
            jump =False
            is_jumping = False
            going_up = False
            if pos_y < jump_aux and pos_y > jump_max and not going_up and not on_plataform:
                #print('bajando2')
                pos_y += paso_jump

        #Condicion de llegada a piso
            elif pos_y >= jump_aux and not going_up :
                #print('abajo2')
                pos_y = jump_aux
                is_jumping = False
                jump = False
                aux_plataform = False   
        
    ### ---- ZONA DE DIBUJO    
   
    #Cargar imagen del personaje
    image = pygame.image.load(r'.\sprites\link\link_'+image_dir+'.png')
    
    #render imagen del personaje
    screen.blit(image,(pos_x,pos_y))
    #pygame.draw.rect(screen, BLACK, (pos_x, pos_y, 80,80))
    

    


    ### ---- ZONA DE DIBUJO

    #Actualizar Pantalla
    pygame.display.flip()
