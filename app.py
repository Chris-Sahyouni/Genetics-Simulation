import pygame
import numpy as np
from rat import Rat
from side_panel import *

# this can be used to pass all areas in need of updating to update() at once for efficiency
# UPDATE_REGIONS = []

PREDATION = 6
TEMPERATURE = 65
FOOD_AVAILABILITY = 6

def gameLoop():
    global PREDATION, TEMPERATURE, FOOD_AVAILABILITY

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    RATS = pygame.sprite.Group()
    RATS.add(Rat([('D', 'd'), ('A', 'a'), ('R', 'r')]))
    RATS.add(Rat([('D', 'd'), ('A', 'a'), ('R', 'r')]))
    clock = pygame.time.Clock()
    bg = pygame.image.load('images/forest_bg.jpg')
    running = True


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    checkParamChange(event, button, i)

        screen.blit(bg, [0,0])
        side_panel = pygame.Rect(0, 0, 220, 720)
        screen.fill(pygame.Color('gray50'), side_panel)

        renderSelectivePressures(screen)
        pred_buttons = plusMinusButtons(screen, (118, 26))
        pred_plus = pred_buttons[0]
        pred_minus = pred_buttons[1]
        temp_buttons = plusMinusButtons(screen, (145, 57))
        temp_plus = temp_buttons[0]
        temp_minus = temp_buttons[1]
        fa_buttons = plusMinusButtons(screen, (184, 85))
        fa_plus = fa_buttons[0]
        fa_minus = fa_buttons[1]
        buttons = [pred_plus, pred_minus, temp_plus, temp_minus, fa_plus, fa_minus]

        RATS.draw(screen)
        RATS.update(clock.get_time())

        clock.tick(60)
        pygame.display.update()

    pygame.quit()


def renderSelectivePressures(screen):
    global PREDATION, TEMPERATURE, FOOD_AVAILABILITY
    font = pygame.font.Font('fonts/autumn.ttf', 22)
    color = pygame.Color('black')
    screen.blits([
        (font.render('Predation:', True, color), (15, 20)),
        (font.render('Temperature:', True, color), (15, 50)),
        (font.render('Food Availability:', True, color), (15, 80))
    ])
    screen.blits([
        (font.render(str(PREDATION), True, color), (145, 20)),
        (font.render(str(TEMPERATURE), True, color), (165, 50)),
        (font.render(str(FOOD_AVAILABILITY), True, color), (205, 80))
    ])



def plusMinusButtons(screen, location):
    x = location[0]
    y = location[1]
    font = pygame.font.Font('fonts/autumn.ttf', 20)
    plus_box = pygame.Rect(x, y - 2, 15, 15)
    minus_box = pygame.Rect(x, y + 9, 15, 12)
    gray_plus = pygame.Color('green3')
    gray_minus = pygame.Color('red3')
    black = pygame.Color('black')
    pygame.draw.rect(screen, gray_plus, plus_box)
    pygame.draw.rect(screen, gray_minus, minus_box)
    plus = font.render('+', True, black)
    minus = font.render('-', True, black)
    screen.blit(plus, (x + 2, y - 8))
    screen.blit(minus, (x + 4, y))
    return (plus_box, minus_box)



def checkParamChange(event, button, index):
    global PREDATION, TEMPERATURE, FOOD_AVAILABILITY
    if button.collidepoint(event.pos):
        if index == 0:
            if PREDATION < 12:
                PREDATION += 1
            return
        if index == 1:
            if PREDATION > 1:
                PREDATION -= 1
            return
        if index == 2:
            if TEMPERATURE < 90:
                TEMPERATURE += 5
            return
        if index == 3:
            if TEMPERATURE > 35:
                TEMPERATURE -= 5
            return
        if index == 4:
            if FOOD_AVAILABILITY < 12:
                FOOD_AVAILABILITY += 1
            return
        if index == 5:
            if FOOD_AVAILABILITY > 1:
                FOOD_AVAILABILITY -= 1




gameLoop()

