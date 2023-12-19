import pygame


# once money is added this can return true or false to indicate success/failure
def adjustParameter(param_name, value, sign):
    if sign == 1:
        if param_name == 'temperature':
            if param < 90:
                value += 5
            else:
                if value < 12:
                    value += 1
    if sign == -1:
        if param_name == 'temperature':
            if value > 35:
                value -= 5
            else:
                if value > 1:
                    value -= 1


def plusMinusButtons(screen, location, param_name, param):
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
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if plus_box.collidepoint(event.pos):
                print(param_name)
                gray_plus = pygame.Color('gray30')
            if minus_box.collidepoint(event.pos):
                print(param_name)
                gray_minus = pygame.Color('gray30')
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONUP:
            if plus_box.collidepoint(event.pos):
                gray_plus = pygame.Color('gray60')
                adjustParameter(param_name, param, 1)
            if minus_box.collidepoint(event.pos):
                gray_minus = pygame.Color('gray60')
                adjustParameter(param_name, param, -1)
            pygame.display.update()




def renderSelectivePressures(screen, predation, temperature, foodAv):
    font = pygame.font.Font('fonts/autumn.ttf', 22)
    color = pygame.Color('black')
    screen.blits([
        (font.render('Predation:', True, color), (15, 20)),
        (font.render('Temperature:', True, color), (15, 50)),
        (font.render('Food Availability:', True, color), (15, 80))
    ])
    plusMinusButtons(screen, (118, 30), 'pred', predation)
    plusMinusButtons(screen, (145, 60), 'temp', temperature)
    plusMinusButtons(screen, (184, 90), 'fa', foodAv)