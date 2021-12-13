from abc import ABC, abstractmethod
from lifeforms import lifeforms
import mainn
import sys, random, pygame
from pygame.locals import *
pygame.init()

class Animals(lifeforms):
    def __init__(self, gender : bool, isViande : bool):
        super().__init__(10, False, 10, True, False)
        self.gender = gender
        self.isViande = isViande
        self.x = random.randrange(10, WIDTH-10) #x position
        self.y = random.randrange(10, HEIGHT-10) #y position
        self.z = random.randrange(5, HEIGHT-5) #y position
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
        if self.x < 5 or self.x > WIDTH - 5 or self.y < 5 or self.y > HEIGHT - 5: #if animal is near the border of the screen, change direction
            if self.x < 5:
                self.direction = "E"
            elif self.x > WIDTH - 5:
                self.direction = "W"
            elif self.y < 5:
                self.direction = "S"
            elif self.y > HEIGHT - 5:
                self.direction = "N"
            self.move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
            self.move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative x to a random number between min x and max x
        if self.move[0] != None: #add the relative coordinates to the animal's coordinates
            self.x += self.move[0]
            self.y += self.move[1]


    @abstractmethod
    def reproduction(self):
        pass

    def devenirMiams(self):
        pass

    def faireCaca(self):
        pass

    def infligerDegats(self):
        pass

    def draw():
        pygame.draw.polygon(surface=screen, color=(255, 255, 255), points=[x, y, z])
        