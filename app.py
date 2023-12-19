import pygame
import numpy as np
from rat import Rat
from selective_pressures import renderSelectivePressures


PREDATION = 6
TEMPERATURE = 65
FOOD_AVAILABILITY = 6


# this can be used to pass all areas in need of updating to update() at once for efficiency
# UPDATE_REGIONS = []

pygame.init()
screen = pygame.display.set_mode((1280, 720))
RATS = pygame.sprite.Group()
RATS.add(Rat([('D', 'd'), ('A', 'a'), ('R', 'r')]))
RATS.add(Rat([('D', 'd'), ('A', 'a'), ('R', 'r')]))
clock = pygame.time.Clock()
bg = pygame.image.load('images/forest_bg.jpg')
running = True


# --------------------------------- Game Loop -------------------------------- #

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
        

    screen.blit(bg, [0,0])
    side_panel = pygame.Rect(0, 0, 220, 720)
    screen.fill(pygame.Color('gray50'), side_panel)
    renderSelectivePressures(screen, PREDATION, TEMPERATURE, FOOD_AVAILABILITY)
    RATS.draw(screen)
    RATS.update(clock.get_time())

    clock.tick(60)
    pygame.display.update()

pygame.quit()



