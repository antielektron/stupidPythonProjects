#!/usr/bin/env python3

import argparse
import sys
import parser
import random
import numpy as np
import ea

def parsingArguments():
    # parsing args:
    parser = argparse.ArgumentParser(description="evolutionary algorithm simulation", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--offspringSize', dest='offspringSize', default = 1 , help='size for new offspring')
    parser.add_argument('--P', dest='P', default = 2, help = 'start population size')
    parser.add_argument('--L', dest='L', default=3, help = 'genome length')
    parser.add_argument('--f', dest='f', default="- (x[0] - 5)**2 + 10", help='fitness function in python syntax. x[0] - x[L] are the arguments')
    parser.add_argument('--epsilon', dest='epsilon', default=0.25, help='epsilon for random mutation')
    parser.add_argument('--cycles', dest='cycles', default=100, help='cycles to calculate')

    if (len(sys.argv) == 1):

        # no parameters given. Print help and ask user at runtime for options:

        settings = {}
        settings["offspringSize"] = 1
        settings["P"] = 2
        settings["L"] = 1
        settings["f"] = "- (x[0] - 5)**2 + 10"
        settings["epsilon"] = 0.25
        settings["cycles"] = 100


        while True:
            parser.print_help()
            print("\ncurrent settings:")
            for key in settings.keys():
                print(str(key) + " = " + str(settings[key]))
            a = input("enter parameter to change. press enter to continue: ")
            if len(a) == 0:
                break
            val = input("enter new value: ")
            settings[a] = val
        # passing settings to parser:
        parser.set_defaults(offspringSize=settings["offspringSize"])
        parser.set_defaults(P=settings["P"])
        parser.set_defaults(L=settings["L"])
        parser.set_defaults(f=settings["f"])
        parser.set_defaults(epsilon=settings["epsilon"])
        parser.set_defaults(cycles=settings["cycles"])
    return parser.parse_args()

# easy adjustable functions for the ea-cycle. Will be packed in lambda objects in main()
def inheritance(parents):
    '''

    :param parents: list of Individuals. Their genome can be accessed by parents[i].genome
    :return: genome for new offspring individual
    '''

    # just copy genome from first parent:
    return parents[0].genome

def mutation(genome, e):
    '''

    :param genome: list of length L of real values: the genome to mutate
    :param e: epsilon value (for random range)
    :return: the mutated genome
    '''

    # mutate new genome by equally distributed random value in range [-e:e]
    newGenome = []

    for i in range(len(genome)):
        newGenome.append(genome[i] + random.random() * 2 * e - e)

    return newGenome

def externalSelection(fitness):
    '''

    :param fitness: list with fitness values
    :return: list of indices of surviving individuals
    '''
    # only keep the fittest
    return [np.argmax(fitness)]

def parentSelection(population, fitness):
    '''
    parent selection method for one individual
    :param population: list of individuals which survived external selection
    :param fitness: list of fitness values for given population
    :return: list of parents for one new offspring individual
    '''

    # only first (and only individual so far) is parent
    return [0]


def main():

    # at first, get arguments
    args = parsingArguments()
    offspringSize = int(args.offspringSize)
    P = int(args.P)
    L = int(args.L)
    f = args.f
    epsilon = float(args.epsilon)
    cycles = int(args.cycles)

    # parse and compile fitness function to evaluateable code
    functionCode = parser.expr(f).compile()

    # build easy adjustable lambda functions for each step of the EA-cycle:

    # fitness function:
    fitnessFunctionLambda = lambda x: eval(functionCode)

    # inheritance function: just copy genome from first parent
    inheritanceFunctionLambda = lambda parents: inheritance(parents)

    # mutation function:
    mutationFunctionLambda = lambda genome: mutation(genome, epsilon)

    # external selection:
    externalSelectionLambda = lambda fitness: externalSelection(fitness)

    # parentSelection:
    parentSelectionLambda = lambda population, fitness: parentSelection(population, fitness)

    ep = ea.EvolutionaryPopulation(L,
                                   offspringSize,
                                   fitnessFunctionLambda,
                                   inheritanceFunctionLambda,
                                   mutationFunctionLambda,
                                   externalSelectionLambda,
                                   parentSelectionLambda)

    #start with random population:
    for i in range(P):
        genome = []
        for i in range(L):
            genome.append(random.random() * 10 - 5) # random value in range [-5:5]. TODO: make adjustable
        ep.addIndividual(genome)

    ep.evaluateFitness() # called manually, because population is modified
    ep.printPopulation()
    ep.performCycle(cycles)

if __name__ == "__main__":
    main()

