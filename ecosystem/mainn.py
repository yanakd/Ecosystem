import os
import sys, random, pygame
from pygame.locals import *

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

def mainloop():
    while True:
        for event in pygame.event.get():
            if event.type== QUIT: #if pressing the X, quit the progra
                pygame.quit() #stop pygame
                sys.exit() #stop the program
        pygame.draw.polygon(surface=screen, color=(255, 255, 255), points=[(50,100), (56,100), (53,103)])
        pygame.display.update() #update display
        pygame.time.Clock().tick(FPS) #limit FPS

            
        

mainloop()