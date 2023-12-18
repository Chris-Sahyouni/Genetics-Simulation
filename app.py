import pygame
from rat import Rat



def eventHandler():
    global running, RATS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False






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
    eventHandler()
    screen.blit(bg, [0,0])
    RATS.draw(screen)
    RATS.update(clock.get_time())
    clock.tick()
    pygame.display.update()

pygame.quit()