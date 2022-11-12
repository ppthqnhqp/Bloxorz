from queue import Queue
from game import Game
from genetic import Population
from copy import deepcopy

def bfs(map,swatches,state:Game):
    q = Queue()
    q.put(state)
    visited = {}
    while q.qsize() > 0:
        state = q.get()
        if state in visited:
            continue
        for move in 'RLUD':
            stateDup = deepcopy(state)
            isProper, isWin = stateDup.makeMove(map,swatches,move)
            if isWin:
                return stateDup.moves
            if isProper:
                lenMoves = visited.get(stateDup)
                if not (lenMoves and lenMoves < len(stateDup.moves)):
                    q.put(stateDup)

        if not state.isConsecutiveBoxes:
            stateDup = deepcopy(state)
            isProper, isWin = stateDup.makeMove(map,swatches,'S')
            lenMoves = visited.get(stateDup)
            if not (lenMoves and lenMoves < len(stateDup.moves)):
                q.put(stateDup)
        
        visited[state] = len(state.moves)

def genetic(map,swatches,state:Game,probCross, probMuta):
    popu = Population(map,swatches,state,probCross,probMuta)
    isWin, gene = popu.nextGen()
    gen = 0
    while not isWin and gen <2:
        print(gen)
        isWin, gene = popu.nextGen()
        gen += 1
    return gene
