import numpy as np
import pygame
import math

NUM_TRAITS = 3

# TODO:
'''
calculate lifespan,
number of offspring,
give rats id
vertical movement
fullscreen mode
mutations
'''


class Rat(pygame.sprite.Sprite):
    ###
    # genotype will be an array of lists of size 2, each list representing the two alleles for that gene
    # phenotype will be an array, each index representing the expressed gene
    # the order of genes will always be D/d: dark, A/a: agile, R/r: rotund
    ###
    def __init__(self, genotype, params):
        super(Rat, self).__init__()
        self.genotype = genotype
        self.phenotype = self.expressPhenotype()
        self.image = self.selectImage()
        self.surf = self.image
        self.rect = self.randomStartPos()
        self.size = self.determineSize()
        self.direction = np.random.choice([-1, 1])
        self.time_till = self.setRandomTime()
        self.speed = self.setSpeed()
        self.max_offspring = 2
        self.num_offspring = 0
        self.time_alive = 0
        self.reproduction_ready = False
        self.lifespan = self.calculateLifespan(params)
        self.isalive = True


    @staticmethod
    def reproduce(male, female, params):
        global NUM_TRAITS
        child_genotype = []
        for i in range(NUM_TRAITS):
            child_gene = ['', '']
            child_gene[0] = male.genotype[i][np.random.randint(0, 2)]
            child_gene[1] = female.genotype[i][np.random.randint(0, 2)]
            child_genotype.append(child_gene)
        male.num_offspring += 1
        female.num_offspring += 1
        male.reproduction_ready = False
        female.reproduction_ready = False
        return Rat(child_genotype, params)



    def expressPhenotype(self):
        global NUM_TRAITS
        phenotype = []
        for i in range(NUM_TRAITS):
            gene = self.genotype[i]
            if gene[0].isupper() and gene[1].isupper():
                phenotype.append(gene[0])
            elif (gene[0].isupper() and gene[1].islower()) or (gene[0].islower() and gene[1].isupper()):
                phenotype.append(gene[0].upper())
            else:
                phenotype.append(gene[0])
        return phenotype


    def calculateLifespan(self, params):
        pvector = list(params)
        pvector[1] /= 5
        pvector[1] -= 6
        dval, aval, rval = 0, 0, 0
        if self.phenotype[0] == 'D':
            dval = 1
        else:
            dval = -1
        if self. phenotype[1] == 'A':
            aval = 1
        else:
            aval = -1
        if self.phenotype[2] == 'R':
            rval = 1
        else:
            rval = -1
        M = np.array([[dval, 0, 0],
                      [aval, 0, aval],
                      [0, -1*rval, 0]])
        score_vector = M @ pvector
        mean = score_vector.mean()
        return (mean / 2) + 8



    # this difference is not noticeable
    def determineSize(self):
        if self.phenotype[2] == 'R':
            return 25
        return 15


    def selectImage(self):
        if self.phenotype[0] == 'D':
            img = None
            img = pygame.image.load('images/dark_rat.png')
        else:
            img = pygame.image.load('images/light_rat.png')
        return pygame.transform.scale(img, (50, 50))



    def randomStartPos(self):
        x = np.random.randint(300, 1000)
        y = np.random.randint(500, 650)
        return [x, y]


    def setDirection(self):
        if self.rect[1] < 235 + self.size:
            self.direction = 1
        elif self.rect[1] > 1220 - self.size:
            self.direction = -1
        else:
            self.direction = np.random.choice([-1, 1])


    def setSpeed(self):
        if self.phenotype[1] == 'A':
            return 3
        else:
            return 1

    # this represents either the time spent moving or the time spent until moving depending of if still or not
    def setRandomTime(self):
        if self.direction == 0:
            return np.random.gamma(5, 20) * 100
        else:
            return np.random.gamma(5, 20) * 100



    def update(self, time_elapsed):
        pygame.sprite.Sprite.update(self, time_elapsed)
        self.time_till -= time_elapsed
        self.time_alive += time_elapsed
        if self.time_till <= 0 or self.rect[0] < 235 + self.size or self.rect[0] > 1200 - self.size:
            if self.direction == 0:
                self.setDirection()
            else:
                self.direction = 0
            self.setRandomTime()
        self.rect[0] += self.speed * self.direction

        if self.num_offspring < self.max_offspring and self.time_alive >= (self.num_offspring + 2) * 2000:
            self.reproduction_ready = True

        if self.time_alive >= self.lifespan * 1000:
            self.reproduction_ready = False
            self.isalive = False



    def draw(self, screen):
        screen.blit(self.surf, self.rect.topleft)


