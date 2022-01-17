
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
        ''''
        Obtener el siguiente numero en la secuencia de imagenes
        '''
        if pos < 3:
            return pos + 1
        else:
            return 0

    def move(self):
        if not self.dead:    
            self.posx -= 0.6
            if self.counter == 8:
                self.image = 'wolf_l'+str(self.walk)
                self.walk = self.__next(self.walk)
                self.counter = 0
            self.counter += 1

    def reset(self):
        self.posx    = 780
        self.posy    = 395
        self.walk    = 0
        self.image   = 'wolf_l0'
        self.counter = 0
        self.dead    = False
        self.going_up= True
    

    def defeated(self, direction):
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
        


    

    



