import os
import sys, random, pygame
from pygame.locals import *
from abc import ABC, abstractmethod


#------------------------------------------Initialise pygame----------------------------
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

#------------------------------------------Set up the display---------------------------
WIDTH = 1080 #game window width
HEIGHT = 720 #game window height
FPS = 30 #game's speeds
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #set the game window
pygame.display.set_caption("Darwin's Game")


#-----------------------------------------Declaring variables------------------------------
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
brown = (123, 63, 0)
black = (0, 0, 0)
gender = ["male", "female"]

#------------------------------Lifeforms is the bas class from which every living being devolves from--------------
class lifeforms(pygame.sprite.Sprite, ABC):
    def __init__(self, width, height, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        #variables needed by all lifeforms
        self.hp = 10 #"hit points" = life points of a lifeform
        self.dead = False #defines if a lifeform is dead if dead == true
        self.nrj = 10 #energy points of a lifeforms
        self.isCaca = False #defines if lifeform is organic waste

        self.image = pygame.Surface([width, height]).convert_alpha()
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]



    #defines how a lifeform loses hp, either through damage by another lifeform or when nrj == 0 
    def damage(self):
        pass

    #defines how nrj goes up by eating ==> faut probablement enlever
    def Nrj(self):
        pass

    #changes dead to true and calls devenirCaca() if needed
    def isDead(self):
        if self.hp >= 0:
           return True
        else:
            return False

    def get_posX(self):
        return self.rect.x
    
    def get_posY(self):
        return self.rect.y

    def set_xC(self, value):
        self.rect.x = value

    def set_yC(self, value):
        self.rect.y = value

    def set_color(self, value):
        self.color = value
    
    def set_meat(self):
        self.image.fill(red)
        self.color = red

    def set_foul(self):
        self.image.fill(brown)
        self.color = brown

    def set_black(self):
        self.image.fill(black)
        self.color = black

    def get_color(self):
        return self.color 

    def set_hp(self, value): 
        i = value
        self.hp += i

    def set_nrj(self, value):
        i = value
        self.nrj += i
    
    def get_nrj(self):
        return self.nrj
    
    def get_hp(self):
        return self.hp

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_X(self, value):
        self.rect.x = value


#--------------------------------Animals (along with Plants are the 2 main )
class Animals(lifeforms):
    def __init__(self, width, height, pos_x, pos_y):
        lifeforms.__init__(self, width, height, pos_x, pos_y)
        self.my_gender = random.choice(gender)
        self.isViande = False
        self.speed = random.choice([1, 2, 3, 4, 5]) #animal speed
        self.move = [None, None] #realtive x and y coordinates to move to
        self.direction = None #movement direction
        self.isMiams = False
        self.speed = random.randrange(1, 5)
        self.move = [None, None]
        self.direction = None
        self.preg = False
        
    def set_direction(self):
        self.direction *= -1

    def get_direction(self):
        return self.direction

    def get_gender(self):
        return self.my_gender
    
    def pregnant(self):
        self.preg = True

    def not_pregnant(self):
        self.preg = False
        
    def get_pregnant(self):
        return self.preg

    def get_isMiams(self):
        return self.isMiams

    def set_isMiams(self, value):
        self.isMiams = value

    def update(self):
        #-----------------------------------------------------------------HP and NRJ management--------------------------------------------------------------------------------------------
        if self.hp > 0:   
            self.nrj -= 0.05  
            if self.nrj <= 0 :
                self.nrj = 0
                if self.hp > 0:
                    self.hp -= 0.5 
        #---------------------------------------------------------------------Random mvmt-----------------------------------------------------------------------------------------------------------------------------
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
                self.move[0] = random.randint(directions[self.direction][0][0],directions[self.direction][0][1])  #change relative x to a random number between min x and max x
                self.move[1] = random.randint(directions[self.direction][1][0],directions[self.direction][1][1])  #change relative x to a random number between min x and max x
            if self.rect.x < 5 or self.rect.x > WIDTH - 5 or self.rect.y < 5 or self.rect.y > HEIGHT - 5: #if cell is near the border of the screen, change direction
                if self.rect.x < 5:
                    self.direction = "E"
                elif self.rect.x > WIDTH - 5:
                    self.direction = "W"
                elif self.rect.y < 5:
                    self.direction = "S"
                elif self.rect.y > HEIGHT - 5:
                    self.direction = "N"
                self.move[0] = random.randint(directions[self.direction][0][0],directions[self.direction][0][1])  #change relative x to a random number between min x and max x
                self.move[1] = random.randint(directions[self.direction][1][0],directions[self.direction][1][1])  #change relative x to a random number between min x and max x
            if self.move[0] != None: #add the relative coordinates to the cells coordinates
                self.rect.x += self.move[0]
                self.zoneVisionH.x += self.move[0]
                self.rect.y += self.move[1]
                self.zoneVisionH.y += self.move[1]
        #-----------------------------------------------------------When dead => become meat--------------------------------------------------------------------------------------
        elif self.hp <= 0 and self.isMiams == False:
            self.hp = 0
            self.image.fill(red)
            self.color = red

#-------------------------------------------------Predators-----------------------------------------
class Carnivore(Animals):
    def __init__(self, width, height, pos_x, pos_y):
        lifeforms.__init__(self, width, height, pos_x, pos_y)
        Animals.__init__(self, width, height, pos_x, pos_y)
        pygame.sprite.Sprite.__init__(self)
        
        self.color = white
        self.image.fill(self.color)
        self.zoneVisionC = pygame.Rect(self.rect.x-10, self.rect.y-10, width+20, height+20)
    #-----------------------------Getters/setters
    def set_x(self, value):
        self.zoneVisionC.x = value

    def set_y(self, value):
        self.zoneVisionC.y = value

    def get_x(self):
        return self.zoneVisionC.x

    def get_y(self):
        return self.zoneVisionC.y

    def update(self):
        #-----------------------------------------------------------------HP and NRJ management--------------------------------------------------------------------------------------------

        if self.hp > 0:
            self.nrj -= 0.05  
            if self.nrj <= 0 :
                self.nrj = 0
                if self.hp > 0:
                    self.hp -= 0.5 
        #-------------------------------------------------------------------------Random mvmt------------------------------------------------------------------------------

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
                    self.move[0] = random.randint(directions[self.direction][0][0],directions[self.direction][0][1])  #change relative x to a random number between min x and max x
                    self.move[1] = random.randint(directions[self.direction][1][0],directions[self.direction][1][1])  #change relative x to a random number between min x and max x
            if self.rect.x < 5 or self.rect.x > WIDTH - 5 or self.rect.y < 5 or self.rect.y > HEIGHT - 5: #if cell is near the border of the screen, change direction
                if self.rect.x < 5:
                    self.direction = "E"
                elif self.rect.x > WIDTH - 5:
                    self.direction = "W"
                elif self.rect.y < 5:
                    self.direction = "S"
                elif self.rect.y > HEIGHT - 5:
                    self.direction = "N"
                self.move[0] = random.randint(directions[self.direction][0][0],directions[self.direction][0][1])  #change relative x to a random number between min x and max x
                self.move[1] = random.randint(directions[self.direction][1][0],directions[self.direction][1][1])  #change relative x to a random number between min x and max x
            if self.move[0] != None: #add the relative coordinates to the cells coordinates
                self.rect.x += self.move[0]
                self.zoneVisionC.x += self.move[0]
                self.rect.y += self.move[1]
                self.zoneVisionC.y += self.move[1] 
        #-----------------------------------------------------------When dead => become meat--------------------------------------------------------------------------------------

        elif self.hp <= 0 and self.isMiams == False:
            self.hp = 0
            self.image.fill(red)
            self.color = red 
            
#--------------------------------------------Prey--------------------------------------------------
class Herbivore(Animals):
    def __init__(self, width, height, pos_x, pos_y):
        Animals.__init__(self, width, height, pos_x, pos_y)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height]).convert_alpha()
        
        self.color = blue
        self.image.fill(self.color)
        self.zoneVisionH = pygame.Rect(self.rect.x-10, self.rect.y-10, self.width+20, self.height+20)
        
    #-------------------------------Getters/setters---------------------    
    def set_x(self, value):
        self.zoneVisionH.x = value

    def set_y(self, value):
        self.zoneVisionH.y = value

    def get_x(self):
        return self.zoneVisionH.x

    def get_y(self):
        return self.zoneVisionH.y
           
#-----------------------------Plants--------------------------------------------------
class Plants(lifeforms):
    def __init__(self, width, height, pos_x, pos_y):
        lifeforms.__init__(self, width, height, pos_x, pos_y)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height]).convert_alpha()

        self.color = green
        self.image.fill(self.color)
        self.zoneSemis = pygame.Rect(self.rect.x-50, self.rect.y-50, self.width+100, self.height+100)
        self.zoneRacine = pygame.Rect(self.rect.x-50, self.rect.y-50, self.width+100, self.height+100)


    #-----------------------------------------------------------------HP and NRJ management--------------------------------------------------------------------------------------------
    def update(self):
        if self.isDead() == False and self.nrj > 0 :
            self.nrj -= 0.05  
        elif self.nrj <= 0 :
            self.nrj = 0
            if self.hp > 0:
                self.hp -= 0.05
        elif self.hp <= 0 :
            self.hp = 0
            self.image.fill(brown)
            self.color = brown
        
        
            
#----------------------------------Groups----------------------------------------------------------
carn_group = pygame.sprite.Group()
herb_group = pygame.sprite.Group()
plant_group = pygame.sprite.Group()
child_group = pygame.sprite.Group()

#-------------------------Instanciating initial objects------------------------------------------
    #Range determines the amount of creatures present at the start of the sim
number_of_Carnivores = range(10)
number_of_Herbivores = range(30)
number_of_Plants = range(30)

objC = list()
for i in number_of_Carnivores:
    objC.append(Carnivore(20, 20, random.randrange(10, WIDTH-10), random.randrange(10, HEIGHT-10)))
    carn_group.add(objC[i])

objH = list()
for i in number_of_Herbivores:
    objH.append(Herbivore(20, 20, random.randrange(10, WIDTH-10), random.randrange(10, HEIGHT-10)))
    herb_group.add(objH[i])

objP = list()
for i in number_of_Plants:
    objP.append(Plants(20, 20, random.randrange(10, WIDTH-10), random.randrange(10, HEIGHT-10)))
    plant_group.add(objP[i])

#----------------------------------Killing/Eating--------------------------------------------------------
# 1 == top, 2 == bottom, 3 == left, 4 == right
def hunt():
    global number_of_Herbivores_alive
    for i in range(0,len(objC)):
         for j in range(0,len(objH)):
             if objH[j].get_hp() > 0:
                collide = pygame.Rect.colliderect(objC[i].rect, objH[j].rect)
                if collide and objH[j].get_color != brown :
                    objH[j].set_hp(-5)
                    if objH[j].isDead() == True:
                        if objC[i].get_nrj() <= 5:
                            objC[i].set_nrj(5)

                        elif objC[i].get_nrj() == 6:
                            objC[i].set_nrj(4)
                            if objC[i].get_hp() <= 9:
                                objC[i].set_hp(1)

                        elif objC[i].get_nrj() == 7:
                            objC[i].set_nrj(3)
                            if objC[i].get_hp() <= 8:
                                objC[i].set_hp(2)
                            elif objC[i].get_hp() == 9:
                                objC[i].set_hp(1)
                            else:
                                objC[i].set_hp(0)

                        elif objC[i].get_nrj() == 8:
                            objC[i].set_nrj(2)
                            if objC[i].get_hp() <= 7:
                                objC[i].set_hp(3)
                            elif objC[i].get_hp() == 8:
                                objC[i].set_hp(2)
                            elif objH[i].get_hp() == 9:
                                objC[i].set_hp(1)
                            else:
                                objC[i].set_hp(0)

                        elif objC[i].get_nrj() == 9:
                            objC[i].set_nrj(1)
                            if objC[i].get_hp() <= 6:
                                objC[i].set_hp(4)
                            elif objC[i].get_hp() == 7:
                                objC[i].set_hp(3)
                            elif objC[i].get_hp() == 8:
                                objC[i].set_hp(2)
                            elif objC[i].get_hp() == 9:
                                objC[i].set_hp(1)
                            else:
                                objC[i].set_hp(0)

                        elif objC[i].get_nrj() == 10:
                            objC[i].set_nrj(0)
                            if objC[i].get_hp() <= 5:
                                objC[i].set_hp(5)
                            elif objC[i].get_hp() == 6:
                                objC[i].set_hp(4)
                            elif objC[i].get_hp() == 7:
                                objC[i].set_hp(3)
                            elif objC[i].get_hp() == 8:
                                objC[i].set_hp(2)
                            elif objC[i].get_hp() == 9:
                                objC[i].set_hp(1)
                            else:
                                objC[i].set_hp(0)

def brouter():
    global number_of_Plants_alive
    for i in range(0,len(objH)):
         for j in range(0,len(objP)):
             if objP[j].get_hp() > 0:
                collide = pygame.Rect.colliderect(objH[i].rect, objP[j].rect)
                if collide:
                    objP[j].set_hp(-10)
                    if objP[j].isDead() == True:
                        objP[j].set_X(WIDTH+50)
                    if objH[i].get_nrj() <= 5:
                        objH[i].set_nrj(5)
                        number_of_Plants_alive -= 1

                    elif objH[i].get_nrj() == 6:
                        objH[i].set_nrj(4)
                        if objH[i].get_hp() <= 9:
                            objH[i].set_hp(1)
                            number_of_Plants_alive -= 1

                    elif objH[i].get_nrj() == 7:
                        objH[i].set_nrj(3)
                        if objH[i].get_hp() <= 8:
                            objH[i].set_hp(2)
                        elif objH[i].get_hp() == 9:
                            objH[i].set_hp(1)
                        else:
                             objH[i].set_hp(0)
                             number_of_Plants_alive -= 1

                    elif objH[i].get_nrj() == 8:
                        objH[i].set_nrj(2)
                        if objH[i].get_hp() <= 7:
                            objH[i].set_hp(3)
                        elif objH[i].get_hp() == 8:
                            objH[i].set_hp(2)
                        elif objH[i].get_hp() == 9:
                            objH[i].set_hp(1)
                        else:
                             objH[i].set_hp(0)
                             number_of_Plants_alive -= 1

                    elif objH[i].get_nrj() == 9:
                        objH[i].set_nrj(1)
                        if objH[i].get_hp() <= 6:
                            objH[i].set_hp(4)
                        elif objH[i].get_hp() == 7:
                            objH[i].set_hp(3)
                        elif objH[i].get_hp() == 8:
                            objH[i].set_hp(2)
                        elif objH[i].get_hp() == 9:
                            objH[i].set_hp(1)
                        else:
                             objH[i].set_hp(0)
                             number_of_Plants_alive -= 1

                    elif objH[i].get_nrj() == 10:
                        objH[i].set_nrj(0)
                        if objH[i].get_hp() <= 5:
                            objH[i].set_hp(5)
                        elif objH[i].get_hp() == 6:
                            objH[i].set_hp(4)
                        elif objH[i].get_hp() == 7:
                            objH[i].set_hp(3)
                        elif objH[i].get_hp() == 8:
                            objH[i].set_hp(2)
                        elif objH[i].get_hp() == 9:
                            objH[i].set_hp(1)
                        else:
                             objH[i].set_hp(0)
                             number_of_Plants_alive -= 1

def absorbHerb():
    global number_of_Herbivores_alive
    for i in range(0,len(objH)):
        for j in range(0,len(objP)):
            if objH[i].get_color() == brown:
                collide = pygame.Rect.colliderect(objH[i].rect, objP[j].zoneRacine)
                if collide: 
                    objH[i].set_X(WIDTH+50)
                    number_of_Herbivores_alive -= 1

def absorbCarn():
    global number_of_Carnivores_alive
    for i in range(0,len(objC)):
        for j in range(0,len(objP)):
            if objC[i].get_color() == brown:
                collide = pygame.Rect.colliderect(objC[i].rect, objP[j].zoneRacine)
                if collide: 
                    objC[i].set_X(WIDTH+50)
                    number_of_Carnivores_alive -= 1



#---------------------------------Create offspring--------------------------------------------------
def create_herb():
    global number_of_Herbivores_alive
    objH.append(Herbivore(20, 20, random.randrange(10, WIDTH-10), random.randrange(10, HEIGHT-10)))
    herb_group.add(objH)
    number_of_Herbivores_alive += 1
    
def create_carn():
    global number_of_Carnivores_alive
    objC.append(Carnivore(20, 20, random.randrange(10, WIDTH-10), random.randrange(10, HEIGHT-10), white))
    carn_group.add(objC)
    number_of_Carnivores_alive += 1

def create_plant():
    global number_of_Plants_alive
    objP.append(Plants(20, 20, random.randrange(10, WIDTH-10), random.randrange(10, HEIGHT-10), green))
    plant_group.add(objP)
    number_of_Plants_alive += 1


    
#---------------------------------Reproduction---------------------------------------------------
def reproduction_Herbivores():
    for i in range(0,len(objH)):
        for j in range(0,len(objH)):
            collide = pygame.Rect.colliderect(objH[i].zoneVisionH, objH[j].zoneVisionH)
            if objH[j].get_nrj() >= 8 and objH[i].get_nrj() >= 8:
                if collide and objH[j].get_gender() == "male" and objH[i].get_gender() == "female" and objH[j].isDead() == False and objH[i].isDead() == False and objH[i].get_pregnant() == False:
                    objH[i].pregnant()
                if random.randrange(0,1500) == 2 and objH[i].get_pregnant() == True and number_of_Herbivores_alive < 20:
                    create_herb()
                    objH[i].not_pregnant()

def reproduction_Carnivores():
    for i in range(0,len(objC)):
        for j in range(0,len(objC)):
            collide = pygame.Rect.colliderect(objC[i].zoneVisionC, objC[j].zoneVisionC)
            if objC[j].get_nrj() >= 8 and objC[i].get_nrj() >= 8:
                if collide and objC[j].get_gender() == "male" and objC[i].get_gender() == "female" and objC[j].isDead() == False and objC[i].isDead() == False and objC[i].get_pregnant() == False:
                    objC[i].pregnant()
                if random.randrange(0,1500) == 2 and objC[i].get_pregnant() == True and number_of_Carnivores_alive < 20:
                    create_carn()
                    objC[i].not_pregnant()

def reproduction_Plants():
    if random.randrange(0,2000) == 2:
        for i in range(0,len(objP)):
            if objP[i].get_nrj() >= 5 and objP[i].get_hp() != 0 and random.randrange(0,150) == 2:
                    create_plant()
            else:
                return None



#---------------------------------------Highlights the males-----------------------------------------
def malesHerb():
    for i in number_of_Herbivores:
        for j in number_of_Herbivores:
            if objH[j].get_gender() == "male":
                male = pygame.Rect(objH[j].get_xC()-10, objH[j].get_yC()-10, objH[j].get_width()+20, objH[j].get_height()+20)
                pygame.draw.rect(screen, (0, 255, 0), male)
            if objH[i].get_gender() == "male":               
                male = pygame.Rect(objH[i].get_xC()-10, objH[i].get_yC()-10, objH[i].get_width()+20, objH[i].get_height()+20)
                pygame.draw.rect(screen, (0, 255, 255), male)

def malesCarn():
    for i in number_of_Carnivores:
        for j in number_of_Carnivores:
            if objC[j].get_gender() == "male":
                male = pygame.Rect(objC[j].get_xC()-10, objC[j].get_yC()-10, objC[j].get_width()+20, objC[j].get_height()+20)
                pygame.draw.rect(screen, (0, 255, 0), male)
            if objC[i].get_gender() == "male":               
                male = pygame.Rect(objC[i].get_xC()-10, objC[i].get_yC()-10, objC[i].get_width()+20, objC[i].get_height()+20)
                pygame.draw.rect(screen, (0, 255, 255), male) 

#---------------------------------------Highlight Zone Racine--------------------------------------- 
def zoneRacine():
    for i in number_of_Plants: 
        pygame.draw.rect(screen, (255, 255, 0), objP[i].zoneRacine )

#-----------------------------------------------Caca------------------------------------------------

def become_caca():
    for j in range(0,len(objH)):
        for i in range(0,len(objC)):
            if objH[j].get_color() == red and random.randrange(0,100) == 2:
                objH[j].set_isMiams(True)
                objH[j].set_foul()

def become_caca2():
    for i in range(0,len(objC)):
        if objC[i].get_color() == red and random.randrange(0,100) == 2:
            objC[i].set_isMiams(True)
            objC[i].set_foul()

def become_caca3():
    for i in range(0,len(objP)):
        if objP[i].get_hp() == 0 and random.randrange(0,100) == 2:
            objP[i].set_X(WIDTH+50)

                


#------------------------------------------------UI----------------------------------------------------
    #Herb
number_of_Herbivores_alive = 0
initial_Herbivores = len(objH)
    #Carn
number_of_Carnivores_alive = 0
initial_Carnivores = len(objC)
    #Plant
number_of_Plants_alive = 0
initial_Plants = len(objP)

def texts(): 
    font = pygame.font.Font(None,30)
    NbrOfHerb = font.render("Herbivores are the blue ones", 1,(0,0,255))
    NbrOfCarn = font.render("Carnivores are the white ones", 1,(255,255,255))
    NbrOfPlant = font.render("Plants are the green ones", 1,(0,255,0))
    screen.blit(NbrOfHerb, (WIDTH-(WIDTH-10), HEIGHT-(HEIGHT-10)))
    screen.blit(NbrOfCarn, (WIDTH-(WIDTH-10)+350, HEIGHT-(HEIGHT-10)))
    screen.blit(NbrOfPlant, (WIDTH-(WIDTH-10)+350+350, HEIGHT-(HEIGHT-10)))
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
        #print("HP:  " + str(objC[0].get_hp()) + "," + " " + "NRJ: " + str(objC[0].get_nrj()) + ", " + "X: " + str(objC[0].rect.x))
        
        hunt()
        brouter()    
        absorbHerb()
        absorbCarn()
        reproduction_Carnivores()
        reproduction_Herbivores()
        reproduction_Plants()
        carn_group.update()
        herb_group.update()
        plant_group.update()
        become_caca()
        become_caca2()
        become_caca3()

        #Draw/render
        carn_group.draw(screen)
        herb_group.draw(screen)
        plant_group.draw(screen)
        texts()
        
        
        #after drawing everything, flip the display
        pygame.display.flip()
        

mainloop()