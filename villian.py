
from email.mime import image


class Wolf():
    def __init__(self) :
        self.posx    = 780
        self.posy    = 395
        self.walk    = 0
        self.image   = 'wolf_l0'
        self.counter = 0
        self.dead    = False
        self.going_up= True

    def __next(self,pos):
        """
            Next            
            this function alternates between True and False

            Parameters:
            - **pos: bool**

            Returns the opposite of the variable pos
        """
        if pos < 3:
            return pos + 1
        else:
            return 0

    def move(self):
        """
            Move
            this function moves this character one "pos" to the left in the screen

            Parameters:
            None    
            Doesn't return any parameter, just modificate the parameter:
                - self.image : str
                - self.pos : float
        """
        if not self.dead:    
            self.posx -= 0.6
            if self.counter == 8:
                self.image = 'wolf_l'+str(self.walk)
                self.walk = self.__next(self.walk)
                self.counter = 0
            self.counter += 1

    def reset(self):
        """
            Reset
            this funtion reset de initial values of the character when killed

            Parameters: 
                - None      
        
        """
        self.posx    = 780
        self.posy    = 395
        self.walk    = 0
        self.image   = 'wolf_l0'
        self.counter = 0
        self.dead    = False
        self.going_up= True
    

    def defeated(self, direction):
        """
            Defeated
            this function setup the animation when the character is defeated in the same direction that the hero hits it

            Parameters: 
                - **direction: bool** -> the direction of the strike
            Doesn't return any parameter, mudificates the variable os position 
        
        
        
        """
        
        paso = 1.5
        h  = 370    
        self.image = 'wolf_f0'
        if direction:
            self.posx += 1
        else:
            self.posx -= 1
        if self.posy > h and self.going_up:
            self.posy -= paso
        elif self.posy <= h and self.going_up:
            self.going_up = False
            self.posy += paso
        elif self.posy > h and self.posy < 600 and not self.going_up:
            self.posy += paso
        elif self.posy > 600 and not self.going_up:
            self.reset()
        


    

    



