import pygame, sys
from pygame import key
from personaje import Personaje

from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_b
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
#pos_y = 395
#pos_x = 400

##### PERSONAJE
link = Personaje()

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

### cargar imagen del fondo
background = pygame.image.load(r'textures\background.png')


while True:

    ## Lectura de teclas del usuario
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        keys = pygame.key.get_pressed()
       
        
#lectura de movimientos en eje Y deshabilitados
        if keys[K_UP] :
            link.jump = True
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
        if keys[K_SPACE]:
            link.speed = True
        else:
            link.speed = False

    ## GRID
    # RENDER GAME GRID
    screen.blit(background,(0,0))

    ## Dibujar Plataformas
    
    for i in plataforms:
        screen.blit(plataform,(i[0]+33,i[2]+10))

### Calculo de movimiento
    
    if down  and not link.jump and not link.is_jumping: 
        #pos_y += paso
        link.image_dir = 'f0'
        #if cont:
        #    walk = next(walk)
        #cont = true_false(cont)
        #down = False
        
   
#Moviientos laterales
    if left and link.pos_x > 2:
        #sprint del personaje
        link.move_left()

    if right and link.pos_x < 770:
        link.move_right()

### SALTO
    #si se oprime la tecla del salto y no esta saltando previamente
    if link.jump and not link.is_jumping:
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
        
  ### ---- ZONA DE DIBUJO    
   
    #Cargar imagen del personaje
    image = pygame.image.load(r'.\sprites\link\link_'+link.image_dir+'.png')
    
    #render imagen del personaje
    screen.blit(image,(link.pos_x,link.pos_y))
    
    ### ---- ZONA DE DIBUJO

  #Actualizar Pantalla
    pygame.display.flip()

