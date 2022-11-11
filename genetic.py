from random import randint, random
from queue import Queue
from copy import deepcopy
import math
from functools import reduce 

class Population:
    def __init__(self, map, swatches, state, probCross, probMuta):
        self.map =  map
        self.swatches = swatches
        self.state = state
        self.probCross = probCross
        self.probMuta = probMuta
        self.currentPop = []
        self.generate()
    
    def generate(self):
        q = Queue()
        q.put(self.state)
        visited = {}
        while q.qsize() > 0:
            state = q.get()
            if state in visited:
                continue
            for move in 'RLUD':
                stateDup = deepcopy(state)
                isProper, isWin = stateDup.makeMove(self.map,self.swatches,move)
                if isWin:
                    return
                if isProper:
                    lenMoves = visited.get(stateDup)
                    if not (lenMoves and lenMoves < len(stateDup.moves)):
                        q.put(stateDup)
                        self.currentPop.append(stateDup.moves)

            if not state.isConsecutiveBoxes:
                stateDup = deepcopy(state)
                isProper, isWin = stateDup.makeMove(self.map,self.swatches,'S')
                lenMoves = visited.get(stateDup)
                if not (lenMoves and lenMoves < len(stateDup.moves)):
                    q.put(stateDup)
                    self.currentPop.append(stateDup.moves)
            
            visited[state] = len(state.moves)

    def nextGen(self):
        evolvedPop = []

        while len(self.selection) > 0:
            evolvedPop += self.genTwoChildren()

        self.currentPop = evolvedPop
        isWin, gene = self.getCurrentFitnesses()
        if isWin:
            return True, gene
        else:
            return False, None

    def getCurrentFitnesses(self):
        fitnesses = []
        for i in range(len(self.currentPop)):
            isWin, fitness, newGene = self.getFitness(self.currentPop[i])
            if isWin:
                return True, newGene
            fitnesses.append(fitness)
            self.currentPop[i] = newGene
        self.currentFitnesses = fitnesses
        self.selection = []
        for i in range(len(self.currentFitnesses)):
            if self.currentFitnesses[i] > min(self.currentFitnesses) and self.currentFitnesses[i] <= 1:
                self.selection.append(self.currentPop[i])
                self.selection.append(self.currentPop[i])
        return False, None
    
    def getFitness(self, gene):
        state = deepcopy(self.state)
        newGene = ''
        for move in gene:
            stateDup = deepcopy(state)
            isProper, isWin = stateDup.makeMove(self.map,self.swatches,move)
            if not isProper:
                continue
            newGene += move
            if isWin:
                return True, 0, newGene
            state.makeMove(self.map,self.swatches,move)
        return False, state.h1(), newGene

    def genTwoChildren(self):
        mom = self.select()
        dad = self.select()

        possiblyCrossed = self.crossover(mom, dad) if random() < self.probCross else [mom, dad]
        mutatedChildren = reduce(lambda x, gene: x + self.mutate(gene), possiblyCrossed, [])

        return mutatedChildren

    def select(self):
        return self.selection.pop()

    def crossover(self, mom, dad):
        num1 = math.floor(len(mom) * random())
        num2 = math.floor(len(dad) * random())

        firstOffspring = mom[:num1] + dad[num2:]
        secOffspring = dad[:num2] + mom[num1:]
        return [firstOffspring, secOffspring]

    def mutate(self, gene):
        moves = ['R','L','U','D']
        if (random() < self.probMuta):
            ret = list(map(lambda move: gene + move, moves))
            return ret
        return list(gene)