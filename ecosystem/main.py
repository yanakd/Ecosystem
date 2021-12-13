import carnivore
import herbivore
import os
import pygame

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Darwin's Game")
screen = pygame.display.set_mode((1080, 720))

clock = pygame.time.Clock()
running = True
while running:
    
    clock.tick(60)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False