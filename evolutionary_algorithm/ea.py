#!/usr/bin/env python3

class Individual(object):
    def __init__(self, fitnessFunction, mutationFunction, inheritanceFunction, parents, initialGenome=None):
        '''

        :param fitnessFunction: lambda with fitness function f:R^L → R
        :param mutationFunction: lambda with mutation function m:R^L → R^L
        :param parents: list of individuals used as parents
        :param initialGenome: if List of parents is None, this genome is used for initialization
        '''


        self.genome = []
        self.fitnessFunction = fitnessFunction
        self.parents = parents
        self.mutationFunction = mutationFunction
        self.inheritanceFunction = inheritanceFunction


        if parents is None:
            self.genome = initialGenome
        else:
            self.inheritate()

    def inheritate(self):
        '''
        only one parent, just copy genome
        :return: None
        '''

        self.genome = self.parents[0].genome

    def mutate(self):
        '''
        juast apply the given mutation function to out genom
        :return:
        '''
        self.genome = self.mutationFunction(self.genome)

    def evaluateFitness(self):
        '''
        apply fitness function for fintness evaluation
        :return: fitness value
        '''
        return self.fitnessFunction(self.genome)

class EvolutionaryPopulation(object):
    def __init__(self,                                                                                  # dummy default values:
                 L = 3,                                                                                 # genome of length 3
                 offspringSize = 2,                                                                     # offspring's size
                 fitnessFunction=lambda genome: 0,                                                      # dummy fitness function
                 inheritanceFunction=lambda parents: parents[0].genome,                                 # copy genome from first parent
                 mutationFunction=lambda genome: genome,                                                # no mutation
                 externalSelectionFunction=lambda fitness: list(range(len(fitness))),                   # keep whole population
                 parentSelectionFunction=lambda population, fitness: list(range(len(population)))       # all individuals are parents
                 ):
        self.L = 3
        self.fitnessFunction = fitnessFunction
        self.inheritanceFunction = inheritanceFunction
        self.mutationFunction = mutationFunction
        self.externalSelectionFunction = externalSelectionFunction
        self.parentSelectionFunction = parentSelectionFunction
        self.offspringSize = offspringSize

        self.population = []
        self.fitness = []

        self.generation = 0

    def addIndividual(self, genome):
        self.population.append(Individual(self.fitnessFunction, self.mutationFunction, self.inheritanceFunction, None, genome))

    def evaluateFitness(self):
        self.fitness = []
        for individual in self.population:
            self.fitness.append(individual.evaluateFitness())

    def externalSelection(self):

        # externalSelectionFunction returns indices of individuals to keep:
        toKeep = self.externalSelectionFunction(self.fitness)

        oldPopulation = self.population
        self.population = []
        for i in range(len(oldPopulation)):
            if i in toKeep:
                self.population.append(oldPopulation[i])

    def generateOffspring(self):
        self.evaluateFitness()
        for i in range(self.offspringSize):
            parentIndices = self.parentSelectionFunction(self.population, self.fitness)
            parents = []
            for pI in parentIndices:
                parents.append(self.population[pI])
            newIndividual = Individual(self.fitnessFunction, self.mutationFunction, self.inheritanceFunction, parents)
            newIndividual.mutate()
            self.population.append(newIndividual)
            self.fitness.append(newIndividual.evaluateFitness())

    def printPopulation(self):
        # printPopulation sorted by fitness:
        # (use a dictionary for easy sorting)
        print("\nGeneration " + str(self.generation) + ":")
        d = {}
        for i in range(len(self.population)):
            d[self.fitness[i]] = self.population[i].genome
        for key in d.keys():
            print("fitness: " + str(key) + ", \t\tgenome: " + str(d[key]))

    def performCycle(self, numCycles = 1):
        if self.generation == 0:
            self.externalSelection()

        for i in range(numCycles):
            self.generateOffspring()
            self.printPopulation()
            self.externalSelection()
            self.generation += 1



