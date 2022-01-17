from distutils.errors import LinkError
from tkinter.tix import Tree
import pygame, sys
from pygame import key
from personaje import Personaje
from villian import Wolf

from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_b, K_n, K_v
pygame.init()

#Funciones utiles

#Saber si el personake se encuentra dentro de de los limites de una plataforma
def in_plataform (plataforms,pos_x, pos_y):
    '''
    Funcion Para determinar si el personaje esta sobre una plataforma
    recibe una lista con las posiciones de cada plataforma en pantalla
    recibe la posicion del personaje y regresa un Bool y una tupla con el resultado
    plataformas : lista de tuplas con las coordenadas de cada plataforma
    pos_x y pos_y es la posicion del personaje
    '''
    for i in plataforms:
 
        if pos_x > i[0] and pos_x < i[1] and pos_y <= i[2] and pos_y >= i[2] - 5:
            return True, plataforms.index(i)
        
    return False, plataforms.index(i)

def in_position (pos1,pos2):
    if abs(pos1[0] - pos2[0]) < 20 and abs(pos1[1] - pos2[1]) < 10:
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


##### PERSONAJE
link = Personaje()
wolf = Wolf()

#Posicion inicial


#inicializacion de movimientos
up      = False
down    = False
left    = False
right   = False

### Dibijo de la primera Plataforma
on_plataform = False
aux_plataform = False

#Existe un desfase entre la posicion ed la imagen y el lugar en el codigo
#Lista de plataformas
plataforms = [(192,335,340),(367,510,340),(400,543,275),(327,470,210),(530,675,210)]
#print(plataforms)
plat_pos = plataforms[0] #Posicion en eje x & y de la plataforma
#print(plat_pos)
plataform = pygame.transform.scale(pygame.image.load('textures/plataforma.png'),(150,100)) #redimensionar el png de la plataforma

#Espada
sword_pos = (600,210)
sword_visible = True

### cargar imagen del fondo
background = pygame.image.load(r'textures\background.png')
#sword =  pygame.transform.scale(pygame.image.load(r'sprites\sword.png'),(30,35))
#sword =  pygame.image.load(r'sprites\sword.png')

aux = True
while True:

    ## Lectura de teclas del usuario
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

    ## Dibujar Plataformas
    
    for i in plataforms:
        screen.blit(plataform,(i[0]+42,i[2]+10))

    



### Calculo de movimiento
    
    if down  and not link.jump and not link.is_jumping: 
        #pos_y += paso
        link.image_dir = 'f0'
        #if cont:
        #    walk = next(walk)
        #cont = true_false(cont)
        #down = False
        
   
#Moviientos laterales
    if left and link.pos_x > 2 and not link.dead:
        #sprint del personaje
        link.move()
        
    if right and link.pos_x < 770 and not link.dead:
        link.move()
            
### SALTO
    #si se oprime la tecla del salto y no esta saltando previamente
    if link.jump and not link.is_jumping and not link.dead:
        link.start_jump()    
    
    ### Funcionn del salto
    if link.is_jumping :
        link.jumping()
                    
#Saber si el personaje esta en una plataforma
    link.on_plataform, plat_index = in_plataform(plataforms,link.pos_x,link.pos_y)
    plat_pos = plataforms[plat_index]
    if link.on_plataform:
        link.set_on_plataform(plat_pos_y= plat_pos[2])
        
    else:
        link.out_of_plataform()

#Movimiento del lobo

### Golpe 
    if link.hitting and link.take_sword:
        link.hit()
        if in_position((link.pos_x,link.pos_y),(wolf.posx,wolf.posy)):
            wolf.dead = True

### Choque d epersonajes
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

    
    if wolf.posx < -60:
        wolf.posx = 1000

#Muerte Lobo
    if wolf.dead:
        if aux:
            direction = link.direction
            aux = False
        wolf.defeated(direction)
    else:
        wolf.move()
        aux = True

        
### ---- ZONA DE DIBUJO    
   
    #Cargar imagen del personaje
    image = pygame.image.load(r'.\sprites\link\link_'+link.image_dir+'.png')
    #Cargar Lobo
    wolf_image = pygame.image.load('./sprites/wolf/'+wolf.image+'.png')
    #Cargar Espada
    sword_image = pygame.image.load('./sprites/sword.png')
    
    #render imagen del personaje   
    if link.visible:
        screen.blit(image,(link.pos_x,link.pos_y))
    #Render imagen lobo
    screen.blit(wolf_image,(wolf.posx,wolf.posy))
    #Render Espada
    if sword_visible:
        screen.blit(sword_image,sword_pos)

    #screen.blit(sword,(link.pos_x + 15,link.pos_y))
    #pygame.draw.rect(screen, BLACK, (pos_x, pos_y, 80,80))

    ### ---- ZONA DE DIBUJO

#Actualizar Pantalla
    pygame.display.flip()

