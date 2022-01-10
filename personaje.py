#from typing_extensions import Required
#import pygame, sys
#from pygame import key



class Personaje():


    def __init__(self):
        #Posicion inicial
        self.pos_y              = 395 #Posicion en eje Y
        self.pos_x              = 400 #Posicion en eje X
        self.paso               = 3.5 #Velocidad del personaje
        self.paso_jump          = 5.5 #Velocidad del salto
        self.speed              = False #sprint personaje  
        self.jump               = False #activar el salto
        self.is_jumping        = False #Saber si esta saltando
        self.jump_aux           = self.pos_y #lugar donde inicio el salto
        self.jump_max_distance  = 70 #altura maxima del salto
        self.image_dir          = 'f0'#imagen inicial del personaje
        self.jump_max           = self.pos_y - self.jump_max_distance #Altura maxima relativa
        self.cont               = False #variable para frenado de fotogramas corriendo
        self.walk               = 0  #Numero de la foto corriendo que sigue
        self.on_plataform       = False #Define si esta en una plataforma 
        self.aux_plataform      = False 

    def __next(self,pos):
        ''''
        Obtener el siguiente numero en la secuencia de imagenes
        '''
        if pos < 6:
            return pos + 1
        else:
            return 1

    def __true_false(self,aux):
        ''''
        Alterna entre True y False para frenar el cambio de imagenes corriendo y hacerlo mas fluido
        '''
        if aux:
            return False
        else:
            return True

    def move_left(self):
        #sprint del personaje
        if self.speed:
            self.pos_x -=self.paso*2
        else:
            self.pos_x -= self.paso

        #cargar siguiente sprite
        self.image_dir = 'l'+str(self.walk)
        #Frenar la secuencia de sprites para hacerla mas fluida
        #si esta saltando carga el sprite de salto
        if self.cont and not self.is_jumping:
            self.walk = self.__next(self.walk)
        self.cont = self.__true_false(self.cont)
        if self.is_jumping:
            self.image_dir = 'l5'
        #left = False
        #return self.pos_x, self.image_dir

    def move_right(self):
         #sprint del personaje
        if self.speed:
            self.pos_x += self.paso*2
        else:
            self.pos_x +=self. paso
        #cargar siguiente sprite
        self.image_dir = 'r'+str(self.walk)
        #Frenar la secuencia de sprites para hacerla mas fluida
        #si esta saltando carga el sprite de salto
        if self.cont and not self.is_jumping:
            self.walk = self.__next(self.walk)
        self.cont = self.__true_false(self.cont)
        if self.is_jumping:
            self.image_dir = 'r2'
        #right = False

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

    def set_on_plataform(self, plat_pos_y):
        ''''
        define las condiciones si el personaje llega a una plataforma
        '''
        if not self.aux_plataform and not self.going_up:
            print('llegue')
            self.jump_aux = plat_pos_y
            self.is_jumping =False
            self.jump = False
            self.pos_y = plat_pos_y
            self.aux_plataform = True
        #going_up = False

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
                



