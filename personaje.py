#from typing_extensions import Required
#import pygame, sys
#from pygame import key



from tokenize import Triple


class Personaje():


    def __init__(self):
        # Set initial position
        self.reset()
        
    def reset(self):
        #  Initial Positions
        self.pos_y              = 395 ## initial position in axis Y
        self.pos_x              = 400 ## initial position in axis X
        self.paso               = 0.8 ## character speed
        self.paso_jump          = 2 ## jump speed
        self.speed              = False ## sprint   
        self.jump               = False ## activate jump
        self.is_jumping        = False ## True when is jumping
        self.jump_aux           = self.pos_y ## value of pos Y when started jumping
        self.jump_max_distance  = 70 ## max jumping distance
        self.image_dir          = 'f0'## directory of the character image
        self.jump_max           = self.pos_y - self.jump_max_distance ## jump max pos Y
        self.cont               = 0 ## stop of fps
        self.walk               = 0  ## next character image
        self.on_platform       = False ## true if character is on platform
        self.aux_platform      = False ## aux when is on platform
        self.take_sword         = False ## True if sword is taken
        self.visible            = True ## True if character is visible
        self.counter            = 0 ## Counter of the character twinkling
        self.direction          = True ## movement direction True  = right, false = left
        self.counter_hit        = 0 ## regulate the fps of the hit movement
        self.hitting            = False ## true when character is hitting
        self.image_dir_h        = 'rh0' ## first image when hitting
        self.hitted             = False ## True when character get hitted
        self.going_up           = True ## True when character is going up
        self.dead               = False ## True when character is dead

    def __next(self,pos,n):
        """
            Next            
            this funtion get the next number to load the movement image

            Parameters:
            - **pos: int**

            Returns: 
            - ** pos: int **
        """
        if pos < n:
            return pos + 1
        else:
            return 0

    def __true_false(self,aux):
        """
            True False           
            this function alternates between True and False

            Parameters:
            - **pos: bool**

            Returns the opposite of the variable pos        
        
        """
        if aux:
            return False
        else:
            return True

    def move(self):
        """
            Move
            this function moves this character one "pos"  in X to the left or right in the screen
                it considers when the sword is taken, the character is jumping or its running

            Parameters:
            None    
            Doesn't return any parameter, just modificate the parameter:
                - self.image : str
                - self.pos : float
        """
        # character sprint
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
        
        
        # load nect sprite
        if self.take_sword :
            self.image_dir = image_aux+'s'+str(self.walk)
        else:
            self.image_dir = image_aux+str(self.walk)
        
        # Slow down the sprotes load frecuency to make it more fluid
        # if jumping it loads the jumping sprite
        
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
        

    def start_jump(self):
        """
            start jump
            this function initiate the variables to start the jump

            parameters: 
                - None
            doesn't return any value, it modificates the intern variables
        
        """
        self.is_jumping     = True 
        self.jump_aux       = self.pos_y ## initial pos y when jumping
        self.going_up       = True ## define if the character is going up or down
        self.jump_max       = self.pos_y - self.jump_max_distance ## set the hieghst point of the jump 
        self.jump           = False ## avoid to set initial values in the midddle of the jump
        self.aux_platform  = False ##  True when player is on a platform 

    def jumping(self):
        """
            Jumping
            this function controlates the secuence of a jump

            parameters: 
                - None
            doesn't return any value, it modificates the intern variables
                
        """
        # up condition
        if self.pos_y <= self.jump_aux and self.pos_y > self.jump_max and self.going_up:
            #print('subiendo')
            self.pos_y -= self.paso_jump

        # heighest  condition
        elif self.pos_y <= self.jump_max and self.going_up:
            #print('arriba')
            self.going_up = False
            self.pos_y += self.paso_jump

        # down condition
        elif self.pos_y < self.jump_aux and self.pos_y > self.jump_max and not self.going_up and not self.on_platform:
            #print('bajando')
            self.pos_y += self.paso_jump
            
        # floor condition
        elif self.pos_y >= self.jump_aux and not self.going_up:
            #print('abajo')
            self.pos_y = self.jump_aux
            self.is_jumping = False
            self.jump = False
            self.going_up = True

    def set_on_platform(self, plat_pos_y):
        """
            Set on platform
            this funtion set the initial values when the character is on a platform

            parameters: 
                - **plat_pos_y: float** the pos in the axis Y of the platform that the character is on
            doesn't return any value, it modificates the intern variables
        """
        if not self.aux_platform and not self.going_up:
            self.jump_aux = plat_pos_y
            self.is_jumping =False
            self.jump = False
            self.pos_y = plat_pos_y
            self.aux_platform = True

    def out_of_platform(self):
        """
            Out of platform
            this funtion determines when the character is out of a platform and control the fall from it

            parameters: 
                - None
            doesn't return any value, it modificates the intern variables        
        """
        self.jump_aux = 395
        if self.aux_platform:
            self.jump_aux = 395
            self.jump =False
            self.is_jumping = False
            self.going_up = False
            if self.pos_y < self.jump_aux and self.pos_y > self.jump_max and not self.going_up and not self.on_platform:
                #Bajada 
                self.pos_y += self.paso_jump
            
        # floor condition
            elif self.pos_y >= self.jump_aux and not self.going_up :
                #Abajo
                self.pos_y = self.jump_aux
                self.is_jumping = False
                self.jump = False
                self.aux_platform = False   
                self.going_up = True
                
    def injured(self):
        """
            Injured
            this funtion set the twinkling of the character when is hitted
        """
        if self.counter % 5 == 0:
            self.visible = self.__true_false(self.visible)
        self.counter += 1
        
    def hit(self):
        """
            hit
            this funtion controls the movement of the character when hitting
            parameters: 
                - None
            doesn't return any value, it modificates the intern variables
        """  
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
        """
            Defeated
            this funtion controls the animation when the character is defeated

            parameters: 
                - None
            doesn't return any value, it modificates the intern variables
        """
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
            
        
