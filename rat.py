import numpy as np
import pygame

NUM_TRAITS = 3

# TODO:
'''
calculate lifespan,
number of offspring,
scale with size, motion,
give rats id
vertical movement
in terms of movement, instead of doing an if still for every potential move, could set direction to 0
you have to call .kill() on the rats' sprites in addition to removing them from rats
'''


class Rat(pygame.sprite.Sprite):
    ###
    # genotype will be an array of 2-tuples, each tuple representing the two alleles for that gene
    # phenotype will be an array, each index representing the expressed gene
    # the order of genes will always be D/d: dark, A/a: agile, R/r: rotund
    ###
    def __init__(self, genotype, ):
        super(Rat, self).__init__()
        self.genotype = genotype
        self.phenotype = self.expressPhenotype()
        self.image = self.selectImage()
        self.surf = self.image
        self.rect = self.randomStartPos()
        self.size = 20
        self.direction = 0
        self.time_till = self.setRandomTime()
        self.speed = self.setSpeed()


    @staticmethod
    def reproduce(male, female):
        global NUM_TRAITS
        child_genotype = []
        for i in range(NUM_TRAITS):
            child_gene = ('', '')
            child_gene[0] = male.genotype[i][np.random.randint(0, 2)]
            child_gene[1] = female.genotype[i][np.random.randint(0, 2)]
            child_genotype.append(child_gene)
        return Rat(child_genotype)


    def expressPhenotype(self):
        global NUM_TRAITS
        phenotype = []
        for i in  range(NUM_TRAITS):
            gene = self.genotype[i]
            if gene[0].isupper() and gene[1].isupper():
                phenotype.append(gene[0])
            elif (gene[0].isupper and gene[1].islower()) or (gene[0].islower() and gene[1].isupper()):
                phenotype.append(gene[0].upper())
            else:
                phenotype.append(gene[0])
        return phenotype

    def selectImage(self):
        if self.phenotype[0] == 'D':
            img = None
            img = pygame.image.load('images/dark_rat.png')
        else:
            img = pygame.image.load('images/light_rat.png')
        return pygame.transform.scale(img, (50, 50))



    def randomStartPos(self):
        x = np.random.randint(30, 1000)
        y = np.random.randint(500, 650)
        return [x, y]


    def setDirection(self):
        if self.rect[1] < 60:
            self.direction = 1
        elif self.rect[1] > 1220:
            self.direction = -1
        else:
            self.direction = np.random.choice([-1, 1])


    def setSpeed(self):
        if self.phenotype[1] == 'A':
            return .3
        else:
            return .05

    # this represents either the time spent moving or the time spent until moving depending of if still or not
    def setRandomTime(self):
        if self.direction == 0:
            return np.random.gamma(1, 2) * 1000
        else:
            return np.random.gamma(1, 2) * 100



    def update(self, time_elapsed):
        pygame.sprite.Sprite.update(self, time_elapsed)
        self.time_till -= time_elapsed
        if self.time_till <= 0 or self.rect[0] < 80 or self.rect[0] > 1200:
            if self.direction == 0:
                self.setDirection()
            else:
                self.direction = 0
            self.setRandomTime()
        self.rect[0] += self.speed * self.direction

    def draw(self, screen):
        screen.blit(self.surf, self.rect.topleft)


