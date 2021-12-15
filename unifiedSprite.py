import os
import sys, random, pygame
from pygame.locals import *
from abc import ABC, abstractmethod

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
WIDTH = 640 #game window width
HEIGHT = 480 #game window height
FPS = 60 #game's speeds
#Pixsize = 2
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #set the game window
pygame.display.set_caption("Darwin's Game")




white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
brown = (123, 63, 0)
black = (0, 0, 0)

class lifeforms(ABC):
    def __init__(self, hp : int, dead : bool, nrj : int, form : bool, isCaca : bool):
        #variables needed by all lifeforms
        self.hp = hp #"hit points" = life points of a lifeform
        self.dead = dead #defines if a lifeform is dead if dead == true
        self.nrj = nrj #energy points of a lifeforms
        self.form = form #true if plant, false if animal
        self.isCaca = isCaca #defines if lifeform is organic waste

    #defines how a lifeform loses hp, either through damage by another lifeform or when nrj == 0 
    def damage(self):
        pass

    #defines how nrj goes up by eating ==> faut probablement enlever
    def Nrj(self):
        pass

    #changes dead to true and calls devenirCaca() if needed
    def isDead(self):
        pass

    def devenirCaca(self):
        pass


class Animals(lifeforms):
    def __init__(self):
        super().__init__(10, False, 10, True, False)
        self.gender = True
        self.isViande = False
        self.speed = random.randrange(2,5) #animal speed
        self.move = [None, None] #realtive x and y coordinates to move to
        self.direction = None #movement direction


    def bouffe(self):
        pass

    @abstractmethod
    def reproduction(self):
        pass

    def devenirMiams(self):
        pass

    def faireCaca(self):
        pass

    def infligerDegats(self):
        pass


class Carnivore(pygame.sprite.Sprite, Animals):
    def __init__(self, width, height, pos_x, pos_y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.speed = random.randrange(-3, 3)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def chasser(self):
        pass

    def reproduction(self):
        pass 

    def update(self):
        #pass
        self.rect.x += 5
        self.rect.y += 5
        #if self.rect.left < 0:
        #    self.rect.x = 0

        

class Herbivore(Animals):
    def __init__(self):
        super().__init__(True, False)

    def chasserHerbe(self):
        pass

    def reproduction(self):
        pass

    def fuite(self):
        pass

carn_group = pygame.sprite.Group()
carn = Carnivore(5, 5, 100, 100, white)
carn_group.add(carn)

def mainloop():
    while True:
        pygame.time.Clock().tick(FPS) #limit FPS
        for event in pygame.event.get():
            if event.type== QUIT: #if pressing the X, quit the progra
                pygame.quit() #stop pygame
                sys.exit() #stop the program

        #Update
        carn_group.update()

        #Draw/render
        carn_group.draw(screen)
        
        #after drawing everything, flip the display
        pygame.display.flip()
        

            
        

mainloop()