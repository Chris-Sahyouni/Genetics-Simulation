import pygame
import numpy as np
from rat import Rat
from predator import Predator
from enum import IntEnum

# this can be used to pass all areas in need of updating to update() at once for efficiency
# UPDATE_REGIONS = []

class RandEvent(IntEnum):
    NO_EVENT = 0
    VOLCANO = 1
    DISEASE = 2
    HUNTERS = 3
    GARBAGE = 4
    RADIATION = 5
    AIR_QUALITY = 6
    GREEN_BILL = 7
    ELECTRIC_CAR = 8
    OZONE = 9


PREDATION = 1
TEMPERATURE = 65
FOOD_SCARCITY = 1
ENVIRONMENTAL_HEALTH = 5
RATS = pygame.sprite.Group()
PREDATORS = pygame.sprite.Group()
REPRODUCE_QUEUE = []
FOOD = []
STARTING_RATS = 6
RAT_STATS = {
    'A': STARTING_RATS,
    'a': 0,
    'R': STARTING_RATS,
    'r': 0,
    'D': STARTING_RATS,
    'd': 0,
    'M': 0,
    'p': 0,
    's': 0,
    'w': 0
}

GENE_TO_WORD = {
    'A': 'Agile',
    'a': 'Slow',
    'R': 'Rotund',
    'r': 'Skinny',
    'D': 'Dark',
    'd': 'Light',
    'M': 'Metabolic',
    'p': 'Paralyzed',
    's': 'Sprint',
    'w': 'Albino'
}

MESSAGES = []

TIME_TILL_EVENT = 0

img = pygame.image.load('images/food.png')
FOOD_IMG = pygame.transform.scale(img, (12, 12))


def gameLoop():
    global PREDATION, TEMPERATURE, FOOD_SCARCITY, RATS, PREDATORS
    pygame.init()
    print('-------------- New Game ----------------')

    screen = pygame.display.set_mode((1280, 720))

    env_params = (PREDATION, TEMPERATURE, FOOD_SCARCITY)

    for i in range(STARTING_RATS):
        RATS.add(Rat([['D', 'd'], ['A', 'a'], ['R', 'r']], env_params))

    PREDATORS.add(Predator())

    # make sure initial rats dont die instantly
    for rat in RATS:
        rat.lifespan = np.random.randint(10, 15)

    clock = pygame.time.Clock()

    bg = pygame.image.load('images/forest_bg.jpg')

    for i in range(13 - FOOD_SCARCITY):
        addFood()

    running = True
    paused = False
    rand_event = RandEvent(0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    checkParamChange(event, button, i)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = True

        while paused:
            clock = None
            screen.fill(pygame.Color('white'), (1220, 70, 12, 50))
            screen.fill(pygame.Color('white'), (1240, 70, 12, 50))
            if rand_event != RandEvent.NO_EVENT:
                rand_event_message = displayRandomEvent(screen, rand_event)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    paused = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(buttons):
                        checkParamChange(event, button, i)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    clock = pygame.time.Clock()
                    paused = False
                    if rand_event != RandEvent.NO_EVENT:
                        addMessage(rand_event_message)
                        executeRandEvent(rand_event)


        screen.blit(bg, [0,0])
        side_panel = pygame.Rect(0, 0, 235, 720)
        screen.fill(pygame.Color('gray50'), side_panel)
        screen.fill(pygame.Color('gray50'), (1050, 0, 230, 90))

        screen.fill(pygame.Color('black'), (15, 120, 200, 1))
        screen.fill(pygame.Color('black'), (15, 455, 200, 1))

        displaySelectivePressures(screen)
        pred_buttons = plusMinusButtons(screen, (118, 26))
        pred_plus = pred_buttons[0]
        pred_minus = pred_buttons[1]
        temp_buttons = plusMinusButtons(screen, (145, 57))
        temp_plus = temp_buttons[0]
        temp_minus = temp_buttons[1]
        fa_buttons = plusMinusButtons(screen, (158, 85))
        fa_plus = fa_buttons[0]
        fa_minus = fa_buttons[1]
        buttons = [pred_plus, pred_minus, temp_plus, temp_minus, fa_plus, fa_minus]

        displayRatStats(screen)
        displayMessages(screen)
        displayEnvHealth(screen)
        displayFood(screen)

        RATS.update(clock.get_time())
        RATS.draw(screen)

        PREDATORS.update(clock.get_time())
        PREDATORS.draw(screen)

        newGeneration()
        killRats()

        rand_event = generateRandomEvent(clock.get_time())
        if rand_event != 0:
            paused = True

        clock.tick(60)
        pygame.display.update()

    pygame.quit()


# ---------------------------------------------------------------------------- #


def generateRandomEvent(time_elapsed):
    global TIME_TILL_EVENT
    TIME_TILL_EVENT += time_elapsed
    if TIME_TILL_EVENT >= 5000:
        TIME_TILL_EVENT = 0
        re = np.random.choice(list(range(10)), p=[.94, .01, .01, .01, .005, .005, .005, .005, .005, .005])
        return RandEvent(re)
    return 0


def displayRandomEvent(screen, rand_event):
    text = ""
    img = pygame.surface.Surface((0,0))
    if rand_event == RandEvent.VOLCANO:
        text = ['A nearby volcano has erupted killing', f'90% of the rat population!']
        img = pygame.image.load('images/volcano.png')
    elif rand_event == RandEvent.DISEASE:
        text = ['An infectious disease called the Modelovirus', f'has killed 60% of the rat population!']
        img = pygame.image.load('images/virus.png')
    elif rand_event == RandEvent.HUNTERS:
        text = ['Hunters have begun hunting the rat population for', 'their nutritious meat increasing the predation level by 4']
        img = pygame.image.load('images/hunters.png')
    elif rand_event == RandEvent.GARBAGE:
        text = ['Garbage from a nearby town is being dumped', 'in the forest decreasing environmental health by 1']
        # img = pygame.image.load('images/.png'), need a picture for garbage
    elif rand_event == RandEvent.RADIATION:
        text = ['A nearby nuclear blast has caused radiation', 'to decrease environmental health by 3']
        img = pygame.image.load('images/nuclear_waste.png')
    elif rand_event == RandEvent.AIR_QUALITY:
        text = ['Poor air quality has decreased environmental', 'health by 1']
        img = pygame.image.load('images/air_quality.png')
    elif rand_event == RandEvent.GREEN_BILL:
        text = ['Congress has passed a wildlife protection', 'bill increasing environmental health by 1']
        img = pygame.image.load('images/congress.png')
    elif rand_event == RandEvent.ELECTRIC_CAR:
        text = ['Electric cars have been invented', 'increasing environmental health by 1']
        img = pygame.image.load('images/electric_car.png')
    elif rand_event == RandEvent.OZONE:
        text = ['A new hole has appeared in the ozone', 'layer decreasing environmental health by 2']
        img = pygame.image.load('images/ozone.png')

    img = pygame.transform.scale(img, (140, 140))
    font = pygame.font.Font('fonts/autumn.ttf', 20)
    screen.fill(pygame.Color('gray50'), (500, 200, 400, 300))
    for i, m in enumerate(text):
        message = font.render(m, True, pygame.Color('white'))
        screen.blit(message, (510, 210 + (i * 20)))
    screen.blit(img, (635, 285))
    return text



def executeRandEvent(rand_event):
    global RATS, RandEvent, PREDATION, ENVIRONMENTAL_HEALTH
    if rand_event == RandEvent.NO_EVENT:
        return
    if rand_event == RandEvent.VOLCANO:
        i = 0
        n = len(RATS)
        for rat in RATS:
            kill(rat)
            i += 1
            if i == int(.9 * n):
                break
        return
    if rand_event == RandEvent.DISEASE:
        i = 0
        n = len(RATS)
        for rat in RATS:
            kill(rat)
            i += 1
            if i == int(.6 * n):
                break
        return
    if rand_event == RandEvent.HUNTERS:
        PREDATION = min(12, PREDATION + 4)
        return
    if rand_event == RandEvent.GARBAGE or rand_event == RandEvent.AIR_QUALITY:
        ENVIRONMENTAL_HEALTH = max(ENVIRONMENTAL_HEALTH - 1, 1)
        return
    if rand_event == RandEvent.GREEN_BILL or rand_event == RandEvent.ELECTRIC_CAR:
        ENVIRONMENTAL_HEALTH = min(ENVIRONMENTAL_HEALTH + 1, 5)
        return
    if rand_event == RandEvent.RADIATION:
        ENVIRONMENTAL_HEALTH = max(ENVIRONMENTAL_HEALTH - 3, 1)
        return
    if rand_event == RandEvent.OZONE:
        ENVIRONMENTAL_HEALTH = max(ENVIRONMENTAL_HEALTH - 2, 1)


def newGeneration():
    global RATS, REPRODUCE_QUEUE, RAT_STATS, PREDATION, TEMPERATURE, FOOD_SCARCITY, ENVIRONMENTAL_HEALTH
    for rat in RATS:
        if rat.reproduction_ready and rat.isalive:
            REPRODUCE_QUEUE.append(rat)
    while len(REPRODUCE_QUEUE) > 1:
        male = np.random.choice(REPRODUCE_QUEUE)
        REPRODUCE_QUEUE.remove(male)
        female = np.random.choice(REPRODUCE_QUEUE)
        REPRODUCE_QUEUE.remove(female)
        new_rat = Rat.reproduce(male, female, (PREDATION, TEMPERATURE, FOOD_SCARCITY), ENVIRONMENTAL_HEALTH)
        for gene in new_rat.phenotype:
            RAT_STATS[gene] += 1
        RATS.add(new_rat)
        checkForMutations(new_rat)
    REPRODUCE_QUEUE.clear()


def checkForMutations(rat):
    global GENE_TO_WORD
    mutations = 'Mspw'
    for gene in rat.phenotype:
        if gene in mutations:
            addMessage(f'A mutant {GENE_TO_WORD[gene].lower()} rat was born')


def killRats():
    global RATS, RAT_STATS
    for rat in RATS:
        if not rat.isalive:
            kill(rat)
        if len(RATS) == 0:
            addMessage('The Rat population has gone extinct')


def kill(rat):
    global RATS, RAT_STATS
    rat.kill()
    RATS.remove(rat)
    for gene in rat.phenotype:
        RAT_STATS[gene] -= 1


def addFood():
    global FOOD
    x = np.random.randint(250, 1125)
    y = np.random.randint(550, 650)
    FOOD.append((x, y))


def displayRatStats(screen):
    global RAT_STATS, RATS, GENE_TO_WORD
    geneToWord = {
        'A': 'Agile',
        'a': 'Slow',
        'R': 'Rotund',
        'r': 'Skinny',
        'D': 'Dark',
        'd': 'Light',
        'M': 'Metabolic',
        'p': 'Paralyzed',
        's': 'Sprint',
        'w': 'Albino'
    }
    y = 150
    n = len(RATS) or 1
    color = pygame.Color('black')
    font = pygame.font.Font('fonts/autumn.ttf', 16)
    screen.blit(font.render('#', True, color), (95, 130))
    screen.blit(font.render('%', True, color), (125, 130))
    for gene in RAT_STATS:
        screen.blit(font.render(geneToWord[gene], True, color), (15, y))
        screen.blit(font.render(str(RAT_STATS[gene]), True, color), (95, y))
        percent = "{:.1f}".format((RAT_STATS[gene] / n) * 100)
        screen.blit(font.render(percent, True, color), (125, y))
        y += 30


def displayEnvHealth(screen):
    global ENVIRONMENTAL_HEALTH
    font = pygame.font.Font('fonts/autumn.ttf', 20)
    surf = font.render(f"Environmental Heath: {ENVIRONMENTAL_HEALTH}", True, pygame.Color('white'))
    screen.blit(surf, (1065, 10))


def displayMessages(screen):
    global MESSAGES
    y = 465
    font = pygame.font.Font('fonts/autumn.ttf', 14)
    sm = pygame.font.Font('fonts/autumn.ttf', 11)
    color = pygame.Color('white')
    for message in MESSAGES:
        i = 0
        if isinstance(message, list):
            for m in message:
                screen.blit(sm.render(m, True, color), (15, y + i*10))
                i += 1
        else:
            screen.blit(font.render(message, True, color), (15, y))
        y += 25 + i*10

def displayFood(screen):
    global FOOD, FOOD_IMG
    for f in FOOD:
        screen.blit(FOOD_IMG, (f[0], f[1], 12, 12))


def displaySelectivePressures(screen):
    global PREDATION, TEMPERATURE, FOOD_SCARCITY
    font = pygame.font.Font('fonts/autumn.ttf', 22)
    color = pygame.Color('black')
    screen.blits([
        (font.render('Predation:', True, color), (15, 20)),
        (font.render('Temperature:', True, color), (15, 50)),
        (font.render('Food Scarcity:', True, color), (15, 80))
    ])
    screen.blits([
        (font.render(str(PREDATION), True, color), (142, 20)),
        (font.render(str(TEMPERATURE), True, color), (165, 50)),
        (font.render(str(FOOD_SCARCITY), True, color), (180, 80))
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
    global PREDATION, TEMPERATURE, FOOD_SCARCITY, FOOD, PREDATORS
    if button.collidepoint(event.pos):
        if index == 0:
            if PREDATION < 12:
                PREDATION += 1
                PREDATORS.add(Predator())
            return
        if index == 1:
            if PREDATION > 1:
                PREDATION -= 1
                pred = PREDATORS.sprites().pop()
                pred.kill()
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
            if FOOD_SCARCITY < 12:
                FOOD_SCARCITY += 1
                FOOD.pop()
            return
        if index == 5:
            if FOOD_SCARCITY > 1:
                FOOD_SCARCITY -= 1
                addFood()


def addMessage(message):
    global MESSAGES
    MESSAGES.insert(0, message)
    if len(MESSAGES) > 20:
        MESSAGES.pop()


gameLoop()

