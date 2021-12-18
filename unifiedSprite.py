import os
import sys, random, pygame
from pygame.locals import *
from abc import ABC, abstractmethod

#------------------------------------------Initialise pygame----------------------------
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

#------------------------------------------Set up the display---------------------------
WIDTH = 640 #game window width
HEIGHT = 480 #game window height
FPS = 60 #game's speeds
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #set the game window
pygame.display.set_caption("Darwin's Game")


#-----------------------------------------Declaring colours------------------------------
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
brown = (123, 63, 0)
black = (0, 0, 0)

#------------------------------Lifeforms is the bas class from which every living being devolves from--------------
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


#--------------------------------Animals (along with Plants are the 2 main )
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


#-------------------------------------------------Predators-----------------------------------------
class Carnivore(pygame.sprite.Sprite, Animals):
    def __init__(self, width, height, pos_x, pos_y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.speed = 5 #random.randrange(1, 5)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.move = [None, None]
        self.direction = None
        self.zoneVisionC = pygame.Rect(self.rect.x-10, self.rect.y-10, width+20, height+20)

    def visionZoneC(self, i : int):
        if i == 1:
            return self.zoneVisionC.top
        if i == 2:
            return self.zoneVisionC.bottom
        if i == 3:
            return self.zoneVisionC.left
        if i == 4:
            return self.zoneVisionC.right

    def chasser(self):
        pass

    def reproduction(self):
        pass 

    def getSpeed(self):
        return self.rect.x, self.rect.y

    def update(self):
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
        if self.rect.x < 5 or self.rect.x > WIDTH - 5 or self.rect.y < 5 or self.rect.y > HEIGHT - 5: #if cell is near the border of the screen, change direction
            if self.rect.x < 5:
                self.direction = "E"
            elif self.rect.x > WIDTH - 5:
                self.direction = "W"
            elif self.rect.y < 5:
                self.direction = "S"
            elif self.rect.y > HEIGHT - 5:
                self.direction = "N"
            self.move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
            self.move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative x to a random number between min x and max x
        if self.move[0] != None: #add the relative coordinates to the cells coordinates
            self.rect.x += self.move[0]
            self.zoneVisionC.x += self.move[0]
            self.rect.y += self.move[1]
            self.zoneVisionC.y += self.move[1]
 
        pygame.draw.rect(screen, (0, 255, 0), self.zoneVisionC)
        self.chasser()

        
#--------------------------------------------Prey--------------------------------------------------
class Herbivore(pygame.sprite.Sprite, Animals):
    def __init__(self, width, height, pos_x, pos_y, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.speed = random.randrange(1, 5)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.move = [None, None]
        self.direction = None
        self.width = width
        self.height = height
        self.zoneVisionH = pygame.Rect(self.rect.x-10, self.rect.y-10, self.width+20, self.height+20)
        
    def visionZoneH(self, i : int):
        if i == 1:
            return self.zoneVisionH.top
        if i == 2:
            return self.zoneVisionH.bottom
        if i == 3:
            return self.zoneVisionH.left
        if i == 4:
            return self.zoneVisionH.right
        
    def getSpeed(self):
        return self.rect.x, self.rect.y
    
    def chasserHerbe(self):
        pass

    def reproduction(self):
        pass

    def fuite(self):
        pass
    
    def update(self):
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
        if self.rect.x < 5 or self.rect.x > WIDTH - 5 or self.rect.y < 5 or self.rect.y > HEIGHT - 5: #if cell is near the border of the screen, change direction
            if self.rect.x < 5:
                self.direction = "E"
            elif self.rect.x > WIDTH - 5:
                self.direction = "W"
            elif self.rect.y < 5:
                self.direction = "S"
            elif self.rect.y > HEIGHT - 5:
                self.direction = "N"
            self.move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
            self.move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative x to a random number between min x and max x
        if self.move[0] != None: #add the relative coordinates to the cells coordinates
            self.rect.x += self.move[0]
            self.zoneVisionH.x += self.move[0]
            self.rect.y += self.move[1]
            self.zoneVisionH.y += self.move[1]
 
        pygame.draw.rect(screen, (0, 255, 0), self.zoneVisionH)
    


#----------------------------------Groups----------------------------------------------------------
carn_group = pygame.sprite.Group()
herb_group = pygame.sprite.Group()

#-------------------------Creating objetcs automatically------------------------------------------
objC = list()
for i in range(5):
    objC.append(Carnivore(20, 20, random.randrange(10, 630), random.randrange(10, 470), white))
    carn_group.add(objC[i])

objH = list()
for i in range(5):
    objH.append(Herbivore(20, 20, random.randrange(10, 630), random.randrange(10, 470), blue))
    herb_group.add(objH[i])
 
#----------------------------------Collision--------------------------------------------------------
collision_tolerance = 10
#Repeat this for every animal
def hunt():
    max_len = len(objH) + len(objC)
    for i in range(max_len):  #how to access object attribute of object inside list
        if abs(dir(objH[1::].visionZoneH(1)) - dir(objC[::-1].visionZoneC(2))) < collision_tolerance:  #1:: => from 1 to end of list, ::-1 from end to start of list
            setattr(dir(objC[::-1]), dir(objC[::-1].getSpeed()), dir(objH[::-1].getSpeed()))   #setattr(object, attribute to be changed, new attribute value)
        if abs(objH[1::].visionZoneH(2) - objC[::-1].visionZoneC(1)) < collision_tolerance:
            print('bottom top')
        if abs(objH[1::].visionZoneH(4) - objC[::-1].visionZoneC(3)) < collision_tolerance:
            print('left right')
        if abs(objH[1::].visionZoneH(3) - objC[::-1].visionZoneC(4)) < collision_tolerance:
            print('right left')

#----------------------------------Mainloop----------------------------------------------------------
def mainloop():
    while True:
        pygame.time.Clock().tick(FPS) #limit FPS
        for event in pygame.event.get():
            if event.type == QUIT: #if pressing the X, quit the program
                pygame.quit() #stop pygame
                sys.exit() #stop the program

        #Update
        screen.fill(0)
        carn_group.update()
        herb_group.update()
        hunt()

        #Draw/render
        carn_group.draw(screen)
        herb_group.draw(screen)
        
        
        #after drawing everything, flip the display
        pygame.display.flip()
        

mainloop()