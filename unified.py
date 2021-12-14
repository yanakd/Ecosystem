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
    def __init__(self, gender : bool, isViande : bool):
        super().__init__(10, False, 10, True, False)
        self.gender = gender
        self.isViande = isViande
        self.x = [WIDTH+20, HEIGHT/2] #misleading, not the x of the object but rather one point of the triangle which itself has an x and y coordinates
        self.y = [WIDTH+25, HEIGHT/2] #same 
        self.z = [(self.y[0]-self.x[0])/2, self.x[1]+5] #same
        self.speed = random.randrange(2,5) #animal speed
        self.move = [None, None] #realtive x and y coordinates to move to
        self.direction = None #movement direction

    def bouffe(self):
        pass

    def roam(self):
        directions = {"S":((-1,2),(1,self.speed)),"SW":((-self.speed,-1),(1,self.speed)),"W":((-self.speed,-1),(-1,2)),"NW":((-self.speed,-1),(-self.speed,-1)),"N":((-1,2),(-self.speed,-1)),"NE":((1,self.speed),(-self.speed,-1)),"E":((1,self.speed),(-1,2)),"SE":((1,self.speed),(1,self.speed))} #((min x, max x)(min y, max y))
        directionsName = ("S","SW","W","NW","N","NE","E","SE") #possible directions
        if random.randrange(0,5) == 2: #move about once every 5 frames
            if self.direction == None: #if no direction is set, set a random one
                self.direction = random.choice(directionsName)
            else:
                a = directionsName.index(self.direction) #get the index of direction in directions list
                b = random.randrange(a-1,a+2) #set the direction to be the same, or one next to the current direction
                if b > len(directionsName)-1: #if direction index is outside the list, move back to the start
                    b = 0
                self.direction = directionsName[b]
            self.move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
            self.move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative y to a random number between min y and max y
        if (self.x[0] < 5) or (self.x[0] > WIDTH - 5) or (self.y[1] < 5) or (self.y[1] > HEIGHT - 5): #if animal is near the border of the screen, change direction
            if (self.x[0] < 5):
                self.direction = "E"
            elif (self.x[0] > WIDTH - 5):
                self.direction = "W"
            elif (self.y[1] < 5):
                self.direction = "S"
            elif (self.y[1] > HEIGHT - 5):
                self.direction = "N"
            self.move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
            self.move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative x to a random number between min x and max x
        if self.move[0] != None: #add the relative coordinates to the animal's coordinates
            self.x[0] += self.move[0]
            self.x[1] += self.move[0]
            self.y[0] += self.move[1]
            self.y[1] += self.move[1]


    @abstractmethod
    def reproduction(self):
        pass

    def devenirMiams(self):
        pass

    def faireCaca(self):
        pass

    def infligerDegats(self):
        pass


class Carnivore(Animals):
    def __init__(self):
        super().__init__(True, False)

    def chasser(self):
        pass

    def reproduction(self):
        pass

    def drawCarn(self):
        pygame.draw.polygon(surface=screen, color=(255, 255, 255), points=[self.x, self.z, self.y])  #(50,100), (53,105), (56,100) 



class Herbivore(Animals):
    def __init__(self):
        super().__init__(True, False)

    def chasserHerbe(self):
        pass

    def reproduction(self):
        pass

    def fuite(self):
        pass

carn = Carnivore()
animals = []
animals.append(carn)
#for i in range(10):
    #animals.append(carn)

def mainloop():
    while True:
        for event in pygame.event.get():
            if event.type== QUIT: #if pressing the X, quit the progra
                pygame.quit() #stop pygame
                sys.exit() #stop the program
        for i in animals:
            i.drawCarn()
            i.roam()
        pygame.display.update() #update display
        pygame.time.Clock().tick(FPS) #limit FPS

            
        

mainloop()