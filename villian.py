
from email.mime import image


class Wolf():
    def __init__(self) :
        self.posx    = 780
        self.posy    = 395
        self.walk    = 0
        self.image   = 'wolf_l0'
        self.counter = 0

    def __next(self,pos):
        ''''
        Obtener el siguiente numero en la secuencia de imagenes
        '''
        if pos < 3:
            return pos + 1
        else:
            return 0

    def move(self):
        self.posx -= 1
        if self.counter == 8:
            self.image = 'wolf_l'+str(self.walk)
            self.walk = self.__next(self.walk)
            self.counter = 0
        self.counter += 1



