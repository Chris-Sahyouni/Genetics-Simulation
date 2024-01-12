import numpy as np
import pygame

NUM_TRAITS = 3
REPRODUCTION_RATE = 3
MAX_LIFESPAN = 10
MAX_OFFSPRING = 6

# TODO:
'''
 - the metabolic rats chefs hats are invisible
 - add a reset game button
 - there should probably not be any random events for the first 15 seconds or so
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
        self._size = self.determineSize()
        self.image = self.selectImage()
        self.surf = self.image
        self.rect = self.randomStartPos()
        self._direction = 0
        self._time_till_move = self.setRandomTime()
        self._time_till_angle = self.setRandomTime()
        self._angle = 1
        self._speed = self.setSpeed()
        self._orientation = 1
        self._num_offspring = 0
        self._time_alive = 0
        self.reproduction_ready = False
        self._score = self.calculateScore(params)
        self._lifespan = self.calculateLifespan()
        self.isalive = True

    @staticmethod
    def reproduce(male, female, params, env_health):
        global NUM_TRAITS
        child_genotype = []
        mutations = [["w"], ["p", "s"], ["M"]]
        mutation_probs = [None, 0.0042, 0.0031, 0.0025, 0.0021, 0.0018]
        mut_prob = mutation_probs[env_health]
        for i in range(NUM_TRAITS):
            child_gene = ["", ""]
            child_gene[0] = male.genotype[i][np.random.randint(0, 2)]
            child_gene[1] = female.genotype[i][np.random.randint(0, 2)]

            for j in range(2):
                mutate = np.random.choice([True, False], p=[mut_prob, 1 - mut_prob])
                if mutate:
                    child_gene[j] = np.random.choice(mutations[i])

            child_genotype.append(child_gene)
        male._num_offspring += 1
        female._num_offspring += 1
        male.reproduction_ready = False
        female.reproduction_ready = False
        return Rat(child_genotype, params)

    def expressPhenotype(self):
        global NUM_TRAITS
        phenotype = []
        for i in range(NUM_TRAITS):
            gene = self.genotype[i]
            if gene[0].isupper() and gene[1].isupper():
                if gene[0] == "M" or gene[1] == "M":
                    phenotype.append("M")
                else:
                    phenotype.append(gene[0])
            elif (gene[0].isupper() and gene[1].islower()) or (
                gene[0].islower() and gene[1].isupper()
            ):
                if gene[0].isupper():
                    phenotype.append(gene[0])
                else:
                    phenotype.append(gene[1])
            else:
                if gene[0] == "a" or gene[1] == "a":
                    phenotype.append("a")
                elif gene[0] == 'd' or gene[1] == 'd':
                    phenotype.append('d')
                elif (gene[0] == "p" and gene[1] == "s") or (gene[1] == "p" and gene[0] == "s"):
                    phenotype.append("p")
                else:
                    phenotype.append(gene[0])
        return phenotype

    def calculateScore(self, params):
        p = params[0]
        t = params[1] // 5 - 6
        fs = params[2]
        # note that these each start with a None value so that the indices line up the with the levels of the environmental parameters
        temp_table = {
            "R": [None, 0.6, 0.7, 0.8, 0.9, 0.95, 1, 1, 0.9, 0.7, 0.5, 0.35, 0.2],
            "r": [None, 0.2, 0.35, 0.5, 0.7, 0.9, 1, 1, 0.95, 0.9, 0.8, 0.7, 0.6],
            "M": [None, 0.8, 0.9, 0.9, 0.9, 1, 1, 1, 1, 0.9, 0.9, 0.8, 0.8],
        }
        fs_table = {
            "A": [None, 1, 1, 1, 0.95, 0.9, 0.85, 0.8, 0.75, 0.65, 0.55, 0.45, 0.4],
            "a": [None, 1, 0.95, 0.9, 0.75, 0.6, 0.55, 0.45, 0.4, 0.3, 0.2, 0.15, 0.1],
            "p": [None, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1],
            "s": [None, 1, 1, 1, 1, 0.9, 0.9, 0.9, 0.9, 0.8, 0.8, 0.8, 0.7],
        }
        pred_on_speed = {
            "A": [None, 1, 1, 1, 0.95, 0.9, 0.85, 0.8, 0.75, 0.65, 0.55, 0.45, 0.4],
            "a": [None, 1, 0.95, 0.9, 0.75, 0.6, 0.55, 0.45, 0.4, 0.3, 0.2, 0.15, 0.1],
            "p": [None, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1],
            "s": [None, 1, 1, 1, 1, 0.9, 0.9, 0.9, 0.9, 0.8, 0.8, 0.8, 0.7],
        }
        pred_on_color = {
            "D": [None, 1, 1, 1, 0.95, 0.9, 0.85, 0.8, 0.75, 0.65, 0.55, 0.45, 0.4],
            "d": [None, 1, 0.95, 0.9, 0.75, 0.6, 0.55, 0.45, 0.4, 0.3, 0.2, 0.15, 0.1],
            "w": [None, 0.4, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1],
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
        lifespan = (self._score * MAX_LIFESPAN) + 4
        prob = self._score / 3
        lifespan = np.random.choice([lifespan, 3], p=[1 - prob, prob])
        return lifespan

    def determineSize(self):
        if self.phenotype[2] == "R":
            return 50
        return 50

    def selectImage(self):
        img = None
        if self.phenotype[0] == "D":
            if self.phenotype[2] == "M":
                img = pygame.image.load("images/dark_metabolic.png")
            else:
                img = pygame.image.load("images/dark_rat.png")
        elif self.phenotype[0] == "d":
            if self.phenotype[2] == "M":
                img = pygame.image.load("images/light_metabolic.png")
            else:
                img = pygame.image.load("images/light_rat.png")
        else:
            if self.phenotype[2] == "M":
                img = pygame.image.load("images/albino_metabolic.png")
            else:
                img = pygame.image.load("images/albino_rat.png")

        if self.phenotype[2] == "R":
            return pygame.transform.scale(img, (self._size, self._size))
        elif self.phenotype[2] == 'M':
            return pygame.transform.scale(img, (self._size * 2, self._size * 2))
        else:
            return pygame.transform.scale(img, (self._size / 2, self._size))

    def randomStartPos(self):
        x = np.random.randint(300, 1000)
        y = np.random.randint(500, 650)
        return [x, y]

    def setOrientation(self):
        if self._orientation != self._direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self._orientation = self._direction

    def setDirection(self):
        if self.rect[0] < 300 + self._size:
            self._direction = 1
        elif self.rect[0] > 1150 - self._size:
            self._direction = -1
        else:
            self._direction = np.random.choice([-1, 1])
        self.setOrientation()

    def setSpeed(self):
        if self.phenotype[1] == "s":
            return 10
        elif self.phenotype[1] == "p":
            return 0
        elif self.phenotype[1] == "A":
            return 3
        else:
            return 1

    def setRandomTime(self):
        return ((np.random.rand() * 3) + 0.5) * 1000

    def _updateMovement(self, time_elapsed):
        pygame.sprite.Sprite.update(self, time_elapsed)
        self._time_till_move -= time_elapsed
        if self._time_till_move <= 0:
            if self._direction == 0:
                self.setDirection()
            else:
                self._direction = 0
            self._time_till_move = self.setRandomTime()

        if self.rect[0] < 250:
            self._direction = 0
            self.rect[0] += 1
            self._time_till_move = self.setRandomTime()

        if self.rect[0] > 1150:
            self._direction = 0
            self.rect[0] -= 1
            self._time_till_move = self.setRandomTime()

        self.rect[0] += self._speed * self._direction

    def _updateAngle(self, time_elapsed):
        self._time_till_angle -= time_elapsed
        if self._time_till_angle <= 0:
            self._rotateImage()
            self._time_till_angle = self.setRandomTime()

    def update(self, time_elapsed):
        global MAX_OFFSPRING
        self._time_alive += time_elapsed
        self._updateMovement(time_elapsed)
        self._updateAngle(time_elapsed)

        if self._time_alive >= self._lifespan * 1000:
            self.reproduction_ready = False
            self.isalive = False

        elif self._num_offspring < MAX_OFFSPRING and self._time_alive >= 4000:
            time_mature = self._time_alive - 4000
            if time_mature >= self._num_offspring * REPRODUCTION_RATE * 1000:
                self.reproduction_ready = True

    def _rotateImage(self):
        new_img = pygame.transform.rotate(
            self.image, -self._angle * 45 * self._orientation
        )
        buffered_rect = self.rect
        self.image = new_img
        self.rect = buffered_rect
        self.rect[1] -= 20
        self._angle = -self._angle

    def draw(self, screen):
        screen.blit(self.surf, self.rect.topleft)
