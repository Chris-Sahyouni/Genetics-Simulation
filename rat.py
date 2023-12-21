import numpy as np
import pygame
import math

NUM_TRAITS = 3
REPRODUCTION_RATE = 3
MAX_LIFESPAN = 10

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
        global MAX_LIFESPAN
        super(Rat, self).__init__()
        self.genotype = genotype
        self.phenotype = self.expressPhenotype()
        self.size = self.determineSize()
        self.image = self.selectImage()
        self.surf = self.image
        self.rect = self.randomStartPos()
        self.direction = np.random.choice([-1, 1])
        self.time_till = self.setRandomTime()
        self.speed = self.setSpeed()
        self.max_offspring = 6
        self.num_offspring = 0
        self.time_alive = 0
        self.reproduction_ready = False
        self.score = self.calculateScore(params)
        self.lifespan = self.calculateLifespan()
        self.isalive = True


    @staticmethod
    def reproduce(male, female, params, env_health):
        global NUM_TRAITS
        child_genotype = []
        mutations = [['M'], ['p', 's'], ['w']]
        mutation_probs = [None, .0042, .0031, .0025, .0021, .0018]
        mut_prob = mutation_probs[env_health]
        for i in range(NUM_TRAITS):
            child_gene = ['', '']
            child_gene[0] = male.genotype[i][np.random.randint(0, 2)]
            child_gene[1] = female.genotype[i][np.random.randint(0, 2)]

            for j in range(2):
                mutate = np.random.choice([True, False], p=[mut_prob, 1-mut_prob])
                if mutate:
                    child_gene[j] = np.random.choice(mutations[i])

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


    def calculateScore(self, params):
        p = params[0]
        t = params[1] // 5 - 6
        fs = params[2]
        # note that these each start with a None value so that the indices line up the with the levels of the environmental parameters
        temp_table = {
            'R': [None, 0.6, 0.7, 0.8, 0.9, 0.95, 1, 1, 0.9, 0.7, 0.5, 0.35, 0.2],
            'r': [None, 0.2, 0.35, 0.5, 0.7, 0.9, 1, 1, 0.95, 0.9, 0.8, 0.7, 0.6],
            'M': [None, 0.8, 0.9, 0.9, 0.9, 1, 1, 1, 1, 0.9, 0.9, 0.8, 0.8]
        }
        fs_table = {
            'A': [None, 0.4, 0.45, 0.55, 0.65, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 1, 1],
            'a': [None, 0.1, 0.15, 0.2, 0.3, 0.4, 0.45, 0.55, 0.6, 0.75, 0.9, 0.95, 1],
            'p': [None, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4],
            's': [None, 0.7, 0.8, 0.8, 0.8, 0.9, 0.9, 0.9, 0.9, 1, 1, 1, 1]
        }
        pred_on_speed = {
            'A': [None, 0.4, 0.45, 0.55, 0.65, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 1, 1],
            'a': [None, 0.1, 0.15, 0.2, 0.3, 0.4, 0.45, 0.55, 0.6, 0.75, 0.9, 0.95, 1],
            'p': [None, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4],
            's': [None, 0.7, 0.8, 0.8, 0.8, 0.9, 0.9, 0.9, 0.9, 1, 1, 1, 1]
        }
        pred_on_color = {
            'D': [None, 0.4, 0.45, 0.55, 0.65, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 1, 1],
            'd': [None, 0.1, 0.15, 0.2, 0.3, 0.4, 0.45, 0.55, 0.6, 0.75, 0.9, 0.95, 1],
            'w': [None, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4]
        }
        score = 0
        color = self.phenotype[0]
        agility = self.phenotype[1]
        rotundity = self.phenotype[2]
        score += temp_table[rotundity][t]
        score += fs_table[agility][fs]
        score += pred_on_speed[agility][p]
        score += pred_on_color[color][p]
        score /= 4
        return score



    def calculateLifespan(self):
        global MAX_LIFESPAN
        lifespan = (self.score * MAX_LIFESPAN) + 4
        prob = self.score / 2.5
        lifespan = np.random.choice([lifespan, 3], p=[1-prob, prob])
        return lifespan




    # def lifespan(self):
    #     lifespan = (self.score / 3) + 10
    #     mortality_rate = 1 - ((self.score / 32) + .5)
    #     mortality_rate /= 2.5
    #     mortality_rate += .05
    #     sterile = np.random.choice((True, False), p=[mortality_rate, 1 - mortality_rate])
    #     # print('Rat mortality rate:', mortality_rate * 100)
    #     if sterile:
    #         lifespan = 3
    #     # print('Rat will live for:', lifespan)
    #     return lifespan



    # def calculateScore(self, params):
    #     pvector = list(params)
    #     pvector[1] /= 5
    #     pvector[1] -= 6
    #     dval, aval, rval = 0, 0, 0
    #     if self.phenotype[0] == 'D':
    #         dval = 1
    #     else:
    #         dval = -1
    #     if self. phenotype[1] == 'A':
    #         aval = 1
    #     else:
    #         aval = -1
    #     if self.phenotype[2] == 'R':
    #         rval = 1
    #     else:
    #         rval = -1
    #     M = np.array([[dval, 0, 0],
    #                   [aval, 0, aval],
    #                   [0, -1*rval, 0]])
    #     score_vector = M @ pvector
    #     # print(score_vector)
    #     return score_vector.mean()



    def determineSize(self):
        if self.phenotype[2] == 'R':
            return 50
        return 50


    def selectImage(self):
        img = None
        if self.phenotype[0] == 'D':
            if self.phenotype[2] == 'M':
                img = pygame.load('images/dark_metabolic.png')
            else:
                img = pygame.image.load('images/dark_rat.png')
        elif self.phenotype[0] == 'd':
            if self.phenotype[2] == 'M':
                img = pygame.image.load('images/light_metabolic.png')
            else:
                img = pygame.image.load('images/light_rat.png')
        else:
            if self.phenotype[2] == 'M':
                img = pygame.load('images/albino_metabolic.png')
            else:
                img = pygame.load('images/albinor_rat.png')
        if self.phenotype[2] == 'R' or self.phenotype[2] == 'M':
            return pygame.transform.scale(img, (self.size, self.size))
        else:
            return pygame.transform.scale(img, (self.size / 2, self.size))


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
        if self.phenotype[1] == 's':
            return 10
        elif self.phenotype[1] == 'p':
            return 0
        elif self.phenotype[1] == 'A':
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


        if self.time_alive >= self.lifespan * 1000:
            # rat dies
            self.reproduction_ready = False
            self.isalive = False

        elif self.num_offspring < self.max_offspring and self.time_alive >= 4000:
            time_mature = self.time_alive - 4000
            if time_mature >= self.num_offspring * REPRODUCTION_RATE * 1000:
                self.reproduction_ready = True


    def draw(self, screen):
        screen.blit(self.surf, self.rect.topleft)



