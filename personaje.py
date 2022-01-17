#from typing_extensions import Required
#import pygame, sys
#from pygame import key



from tokenize import Triple


class Personaje():


    def __init__(self):
        #Posicion inicial
        self.reset()
        
    def reset(self):
    #Condiciones iniciales
        self.pos_y              = 395 #Posicion en eje Y
        self.pos_x              = 400 #Posicion en eje X
        self.paso               = 0.8 #Velocidad del personaje
        self.paso_jump          = 2 #Velocidad del salto
        self.speed              = False #sprint personaje  
        self.jump               = False #activar el salto
        self.is_jumping        = False #Saber si esta saltando
        self.jump_aux           = self.pos_y #lugar donde inicio el salto
        self.jump_max_distance  = 70 #altura maxima del salto
        self.image_dir          = 'f0'#imagen inicial del personaje
        self.jump_max           = self.pos_y - self.jump_max_distance #Altura maxima relativa
        self.cont               = 0 #variable para frenado de fotogramas corriendo
        self.walk               = 0  #Numero de la foto corriendo que sigue
        self.on_plataform       = False #Define si esta en una plataforma 
        self.aux_plataform      = False 
        self.take_sword         = False
        self.visible            = True
        self.counter            = 0
        self.direction          = True #Direcion de moviento True right, False left
        self.counter_hit        = 0
        self.hitting            = False
        self.image_dir_h        = 'rh0'
        self.hitted             = False
        self.going_up           = True
        self.dead               = False

    def __next(self,pos,n):
        ''''
        Obtener el siguiente numero en la secuencia de imagenes
        '''
        if pos < n:
            return pos + 1
        else:
            return 0

    def __true_false(self,aux):
        ''''
        Alterna entre True y False para frenar el cambio de imagenes corriendo y hacerlo mas fluido
        '''
        if aux:
            return False
        else:
            return True

    def move(self):
        #sprint del personaje
        if self.speed:
            paso = self.paso*2
        else:
            paso = self.paso

        if self.direction :
            image_aux = 'r'
            jump = '6'
            self.pos_x += paso
        else:
            image_aux = 'l'
            jump = '5'
            self.pos_x -= paso
        
        
        #cargar siguiente sprite
        if self.take_sword :
            self.image_dir = image_aux+'s'+str(self.walk)
        else:
            self.image_dir = image_aux+str(self.walk)
        
        #Frenar la secuencia de sprites para hacerla mas fluida
        #si esta saltando carga el sprite de salto
        
        if self.cont >= 8 and not self.is_jumping:
            self.walk = self.__next(self.walk,6)
            self.cont = 0
        else:
            self.cont += 1
        
        #self.cont = self.__true_false(self.cont)
        
        if self.is_jumping:
            if self.take_sword:
                self.image_dir = image_aux+'s'+jump
            else:
                self.image_dir = image_aux+jump
        if self.hitting:
            self.image_dir = self.image_dir_h
        
    ''''
    def move_right(self):
        self.direction = True
         #sprint del personaje
        if self.speed:
            self.pos_x += self.paso*2
        else:
            self.pos_x +=self. paso
        #cargar siguiente sprite
        if self.take_sword :
            self.image_dir = 'rs'+str(self.walk)
        else:
            self.image_dir = 'r'+str(self.walk)
        
        #Frenar la secuencia de sprites para hacerla mas fluida
        #si esta saltando carga el sprite de salto
        if self.cont and not self.is_jumping:
            self.walk = self.__next(self.walk,6)
        
        self.cont = self.__true_false(self.cont)
        if self.is_jumping:
            if self.take_sword:
                self.image_dir = 'rs2'
            else:
                self.image_dir = 'r2'
        if self.hitting:
            self.image_dir = self.image_dir_h
        '''

    def start_jump(self):
        ''''
        inicia secuencia de salto
        '''
        self.is_jumping     = True 
        self.jump_aux       = self.pos_y #Define la posicion inicial en el eje Y del salto
        self.going_up       = True #Define si esta subiendo o bajando en el salto
        self.jump_max       = self.pos_y - self.jump_max_distance #La distancia mas alta que puede saltar 
        self.jump           = False #Evita que entre de vuelta en el ciclo
        self.aux_plataform  = False #Indica si esta en una plataforma

    def jumping(self):
        ''''
        Controla el progreso del salto
        '''
        #condicion de subida
        if self.pos_y <= self.jump_aux and self.pos_y > self.jump_max and self.going_up:
            #print('subiendo')
            self.pos_y -= self.paso_jump

        #condicion del punto mas alto
        elif self.pos_y <= self.jump_max and self.going_up:
            #print('arriba')
            self.going_up = False
            self.pos_y += self.paso_jump

        #Condicion de bajada
        elif self.pos_y < self.jump_aux and self.pos_y > self.jump_max and not self.going_up and not self.on_plataform:
            #print('bajando')
            self.pos_y += self.paso_jump
            
        #Condicion de llegada a piso
        elif self.pos_y >= self.jump_aux and not self.going_up:
            #print('abajo')
            self.pos_y = self.jump_aux
            self.is_jumping = False
            self.jump = False
            self.going_up = True

    def set_on_plataform(self, plat_pos_y):
        ''''
        define las condiciones si el personaje llega a una plataforma
        '''
        if not self.aux_plataform and not self.going_up:
            self.jump_aux = plat_pos_y
            self.is_jumping =False
            self.jump = False
            self.pos_y = plat_pos_y
            self.aux_plataform = True

    def out_of_plataform(self):
        ''''
        reset de condiciones cuando no esta en plataforma
        define el salto de una platforma
        '''
        self.jump_aux = 395
        if self.aux_plataform:
            self.jump_aux = 395
            self.jump =False
            self.is_jumping = False
            self.going_up = False
            if self.pos_y < self.jump_aux and self.pos_y > self.jump_max and not self.going_up and not self.on_plataform:
                #Bajada 
                self.pos_y += self.paso_jump
            
        #Condicion de llegada a piso
            elif self.pos_y >= self.jump_aux and not self.going_up :
                #Abajo
                self.pos_y = self.jump_aux
                self.is_jumping = False
                self.jump = False
                self.aux_plataform = False   
                self.going_up = True
                
    def injured(self):
        if self.counter % 5 == 0:
            self.visible = self.__true_false(self.visible)
        self.counter += 1
        
    def hit(self):
  
        if self.counter_hit < 40:
            if self.direction:
                self.image_dir_h = 'rh'+str(self.counter_hit // 10)
                self.counter_hit += 5
            else:
                self.image_dir_h = 'lh'+str(self.counter_hit // 10)
                self.counter_hit += 5
            self.image_dir = self.image_dir_h
        else: 
            #print('no mas golpe')
            self.counter_hit = 0
            self.hitting = False

    def defeated(self):
        paso = 1.5
        h  = 370    
        self.image_dir = 'f0'
        self.dead
            
        if self.pos_y > h and self.going_up:
            self.pos_y -= paso
        elif self.pos_y <= h and self.going_up:
            self.going_up = False
            self.pos_y += paso
        elif self.pos_y > h and self.pos_y < 600 and not self.going_up:
            self.pos_y += paso
        elif self.pos_y > 600 and not self.going_up:
            self.reset()
            self.hitted = True
            
        
