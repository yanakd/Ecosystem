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
FPS = 24 #game's speeds
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
        if self.hp == 0:
            self.dead = True

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

    def devenirMiams(self):
        pass

    def faireCaca(self):
        pass

    def infligerDegats(self):
        pass


#-------------------------------------------------Predators-----------------------------------------
class Carnivore(pygame.sprite.Sprite, Animals):
    def __init__(self, width, height, pos_x, pos_y, color):
        Animals.__init__(self)
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

    def contactZoneC(self, i : int):
        if i == 1:
            return self.rect.top
        if i == 2:
            return self.rect.bottom
        if i == 3:
            return self.rect.left
        if i == 4:
            return self.rect.right

    def chasser(self):
        pass

    def reproduction(self):
        pass 

    def get_posX(self):
        return self.rect.x
    
    def get_posY(self):
        return self.rect.y

    def set_x(self, value):
        self.zoneVisionC.x = value

    def set_y(self, value):
        self.zoneVisionC.y = value

    def get_x(self):
        return self.zoneVisionC.x

    def get_y(self):
        return self.zoneVisionC.y

    def set_xC(self, value):
        self.rect.x = value

    def set_yC(self, value):
        self.rect.y = value

    def get_xC(self):
        return self.rect.x

    def get_yC(self):
        return self.rect.y

    def set_color(self):
        self.color = red

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
        

        
#--------------------------------------------Prey--------------------------------------------------
class Herbivore(pygame.sprite.Sprite, Animals):
    def __init__(self, width, height, pos_x, pos_y, color):
        Animals.__init__(self)
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

    def contactZoneH(self, i : int):
        if i == 1:
            return self.rect.top
        if i == 2:
            return self.rect.bottom
        if i == 3:
            return self.rect.left
        if i == 4:
            return self.rect.right
        
    def get_posX(self):
        return self.rect.x
    
    def get_posY(self):
        return self.rect.y

    def set_x(self, value):
        self.zoneVisionH.x = value

    def set_y(self, value):
        self.zoneVisionH.y = value

    def get_x(self):
        return self.zoneVisionH.x

    def get_y(self):
        return self.zoneVisionH.y

    def set_xC(self, value):
        self.rect.x = value

    def set_yC(self, value):
        self.rect.y = value

    def get_xC(self):
        return self.rect.x

    def get_yC(self):
        return self.rect.y

    def set_color(self):
        self.image.fill(red)
    
    def get_color(self):
        return self.color 

    def set_hp(self):
        self.hp = 0
    
    def get_hp(self):
        return self.hp

    
    def update(self):
        if self.hp > 0:    
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
        else: 
            return None 
    
        pygame.draw.rect(screen, (0, 255, 0), self.zoneVisionH)
    


#----------------------------------Groups----------------------------------------------------------
carn_group = pygame.sprite.Group()
herb_group = pygame.sprite.Group()

#-------------------------Creating objetcs automatically------------------------------------------
objC = list()
number_of_Carnivores = range(2)
number_of_Herbivores = range(5)
for i in number_of_Carnivores:
    objC.append(Carnivore(20, 20, random.randrange(10, 630), random.randrange(10, 470), white))
    carn_group.add(objC[i])

objH = list()
for i in number_of_Herbivores:
    objH.append(Herbivore(20, 20, random.randrange(10, 630), random.randrange(10, 470), blue))
    herb_group.add(objH[i])

#----------------------------------Collision--------------------------------------------------------
# 1 == top, 2 == bottom, 3 == left, 4 == right

collision_tolerance = 100
def hunt():
    for i in number_of_Carnivores:
        for j in number_of_Herbivores:
            if objH[j].get_hp() > 0:
                if abs(objH[j].visionZoneH(1) - objC[i].visionZoneC(2)) < collision_tolerance & abs(objC[i].visionZoneC(4) - objH[j].visionZoneH(3)) < collision_tolerance & abs(objC[i].visionZoneC(3) < objH[j].visionZoneH(4)) < collision_tolerance: 
                    objC[i].rect.x = objH[j].rect.x
                    objC[i].rect.y = objH[j].rect.y
                    objC[i].set_x(objH[j].get_x()) 
                    objC[i].set_y(objH[j].get_y()) 

                    objH[j].set_hp()
                    objH[j].set_color()

                if abs(objH[j].visionZoneH(2) - objC[i].visionZoneC(1)) < collision_tolerance & abs(objC[i].visionZoneC(4) - objH[j].visionZoneH(3)) < collision_tolerance & abs(objC[i].visionZoneC(3) < objH[j].visionZoneH(4)) < collision_tolerance:
                    objC[i].rect.x = objH[j].rect.x
                    objC[i].rect.y = objH[j].rect.y
                    objC[i].set_x(objH[j].get_x()) 
                    objC[i].set_y(objH[j].get_y()) 

                    objH[j].set_hp()
                    objH[j].set_color()

                if abs(objH[j].visionZoneH(4) - objC[i].visionZoneC(3)) < collision_tolerance & abs(objC[i].visionZoneC(2) - objH[j].visionZoneH(1)) < collision_tolerance & abs(objC[i].visionZoneC(1) - objH[j].visionZoneH(2)) < collision_tolerance :
                    objC[i].rect.x = objH[j].rect.x
                    objC[i].rect.y = objH[j].rect.y
                    objC[i].set_x(objH[j].get_x()) 
                    objC[i].set_y(objH[j].get_y()) 

                    objH[j].set_hp()
                    objH[j].set_color()

                if abs(objH[j].visionZoneH(3) - objC[i].visionZoneC(4)) < collision_tolerance & abs(objC[i].visionZoneC(2) - objH[j].visionZoneH(1)) < collision_tolerance & abs(objC[i].visionZoneC(1) - objH[j].visionZoneH(2)) < collision_tolerance :
                    objC[i].rect.x = objH[j].rect.x
                    objC[i].rect.y = objH[j].rect.y
                    objC[i].set_x(objH[j].get_x()) 
                    objC[i].set_y(objH[j].get_y()) 

                    objH[j].set_hp()
                    objH[j].set_color()


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
        hunt()
        carn_group.update()
        herb_group.update()

        #Draw/render
        carn_group.draw(screen)
        herb_group.draw(screen)
        
        
        #after drawing everything, flip the display
        pygame.display.flip()
        

mainloop()