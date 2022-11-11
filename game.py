from copy import deepcopy
from enum import Enum
from queue import Queue

MAX_X = 9
MAX_Y = 14

class Game:
    def __init__(self, level):
        self.start = self.boxes = [level['start']['x'],level['start']['y'],level['start']['x'],level['start']['y']]
        self.boxesPropUtil()
        self.boxChoose = 0
        self.swatchesOn = []
        self.moves = ''
        self.swatchesSwitchNum = 0
        for i in range(MAX_Y+1):
            self.swatchesOn.append([False] * (MAX_X+1))
        geometry = level['geometry']
        for y in range(0, MAX_Y+1):
            for x in range(0, MAX_X+1):
                tile = geometry[y][x]
                if tile == 'k' or tile == 'q':
                    self.swatchesOn[y][x] = True
                if tile == 'e':
                    self.end = [x,y,x,y]
    
    def getTuple(self):
        return (self.boxes[0], self.boxes[1], self.boxes[2], self.boxes[3], self.boxChoose, tuple(tuple(i) for i in self.swatchesOn))

    def __eq__(self, other):
        return self.getTuple() == other.getTuple()

    def __hash__(self):
        return hash(self.getTuple())
        
    def swatchSwitch(self, swatches, x, y):
        xDecoded = f'{x:02d}'
        yDecoded = f'{y:02d}'
        fields = swatches[xDecoded+yDecoded]
        onSwatches = False
        for field in fields:
            xf = field["position"]["x"]
            yf = field["position"]["y"]
            action = field["action"]
            if action == "onoff":
                self.swatchesOn[yf][xf] = not self.swatchesOn[yf][xf]
            elif action == "on":
                self.swatchesOn[yf][xf] = True
            elif action == "off":
                self.swatchesOn[yf][xf] = False
            elif action == "split1":
                self.boxes[0] = xf
                self.boxes[1] = yf
                self.isStanding = False
                self.isConsecutiveBoxes = False
                self.isAlongYAxis = None
            elif action == "split2":
                self.boxes[2] = xf
                self.boxes[3] = yf
                self.isStanding = False
                self.isConsecutiveBoxes = False
                self.isAlongYAxis = None
            
            if action != 'off':
                onSwatches = True
        
        if onSwatches:
            self.swatchesSwitchNum += 1

    def boxesPropUtil(self):
        if self.boxes[0] == self.boxes[2] and self.boxes[1] == self.boxes[3]:
            self.isStanding = True
            self.isConsecutiveBoxes = True
            self.isAlongYAxis = None
        else:
            box1 = [self.boxes[0],self.boxes[1]]
            box2 = [self.boxes[2],self.boxes[3]]
            if box1[0] == box2[0]:
                if box1[1] - box2[1] == 1:
                    self.isStanding = False
                    self.isConsecutiveBoxes = True
                    self.isAlongYAxis = True
                elif box2[1] - box1[1] == 1:
                    self.boxes[3], self.boxes[1] = self.boxes[1], self.boxes[3]
                    self.isStanding = False
                    self.isConsecutiveBoxes = True
                    self.isAlongYAxis = True
            elif box1[1] == box2[1]: 
                if box1[0] - box2[0] == 1:
                    self.isStanding = False
                    self.isConsecutiveBoxes = True
                    self.isAlongYAxis = False
                elif box2[0] - box1[0] == 1:
                    self.boxes[2], self.boxes[0] = self.boxes[0], self.boxes[2]
                    self.isStanding = False
                    self.isConsecutiveBoxes = True
                    self.isAlongYAxis = False
    
            else:
                self.isStanding = False
                self.isConsecutiveBoxes = False
                self.isAlongYAxis = None

    def isProferMove(self, map):
        for i in range(0,2):
            if self.boxes[i*2+1] > MAX_Y or self.boxes[i*2+1] < 0 or self.boxes[i*2] > MAX_X or self.boxes[i*2] < 0 or map[self.boxes[i*2+1]][self.boxes[i*2]] == ' ' or ((map[self.boxes[i*2+1]][self.boxes[i*2]] == 'l' or map[self.boxes[i*2+1]][self.boxes[i*2]] == 'r' or map[self.boxes[i*2+1]][self.boxes[i*2]] == 'k' or map[self.boxes[i*2+1]][self.boxes[i*2]] == 'q') and not self.swatchesOn[self.boxes[i*2+1]][self.boxes[i*2]]):
                return False
        if self.isStanding and map[self.boxes[1]][self.boxes[0]] == 'f':
            return False
        return True

    def makeMove(self, map, swatches, event):
        if event == 'R':
            if self.isStanding:
                x, y = self.boxes[0], self.boxes[1]
                self.boxes = [x,y+2,x,y+1]
            else:
                if self.isConsecutiveBoxes:
                    x0, y0 = self.boxes[0], self.boxes[1]
                    x1, y1 = self.boxes[2], self.boxes[3]
                    if self.isAlongYAxis:
                        self.boxes = [x0,y0+1,x0,y0+1]
                    else:
                        self.boxes = [x0,y0+1,x1,y1+1]
                else:
                    self.boxes[self.boxChoose*2+1] += 1
        elif event == 'L':
            if self.isStanding:
                x, y = self.boxes[0],self.boxes[1]
                self.boxes = [x,y-1,x,y-2]
            else:
                if self.isConsecutiveBoxes:
                    x0, y0 = self.boxes[0],self.boxes[1]
                    x1, y1 = self.boxes[2],self.boxes[3]
                    if self.isAlongYAxis:
                        self.boxes = [x1,y1-1,x1,y1-1]
                    else:
                        self.boxes = [x0,y0-1,x1,y1-1]
                else:
                    self.boxes[self.boxChoose*2+1] -= 1
            
        elif event == 'U':
            if self.isStanding:
                x, y = self.boxes[0], self.boxes[1]
                self.boxes = [x+2,y,x+1,y]
            else:
                if self.isConsecutiveBoxes:
                    x0, y0 = self.boxes[0], self.boxes[1]
                    x1, y1 = self.boxes[2], self.boxes[3]
                    if self.isAlongYAxis:
                        self.boxes = [x0+1,y0,x1+1,y1]
                        
                    else:
                        self.boxes = [x0+1,y0,x0+1,y0]
                else:
                    self.boxes[self.boxChoose*2] += 1
                    
        elif event == 'D':
            if self.isStanding:
                x, y = self.boxes[0], self.boxes[1]
                self.boxes = [x-1,y,x-2,y]
            else:
                if self.isConsecutiveBoxes:
                    x0, y0 = self.boxes[0],self.boxes[1]
                    x1, y1 = self.boxes[2],self.boxes[3]
                    if self.isAlongYAxis:
                        self.boxes = [x0-1,y0,x1-1,y1]
                    else:
                        self.boxes = [x1-1,y1,x1-1,y1]
                else:
                    self.boxes[self.boxChoose*2] -= 1
        elif event == 'S':
            if not self.isConsecutiveBoxes:
                self.boxChoose = 1 - self.boxChoose
    
        self.moves += event

        self.boxesPropUtil()

        if not self.isProferMove(map):
            return (False, False)

        if not self.isConsecutiveBoxes:
            if map[self.boxes[self.boxChoose*2+1]][self.boxes[self.boxChoose*2]] == 's':
                self.swatchSwitch(swatches, self.boxes[self.boxChoose*2], self.boxes[self.boxChoose*2+1])
        else:
            if self.isStanding:
                if map[self.boxes[1]][self.boxes[0]] == 's' or map[self.boxes[1]][self.boxes[0]] == 'h' or map[self.boxes[1]][self.boxes[0]] == 'v':
                    self.swatchSwitch(swatches, self.boxes[0], self.boxes[1])
            else:
                if map[self.boxes[1]][self.boxes[0]] == 's':
                    self.swatchSwitch(swatches, self.boxes[0], self.boxes[1])
                if map[self.boxes[3]][self.boxes[2]] == 's':
                    self.swatchSwitch(swatches, self.boxes[2], self.boxes[3])
        
        return (True, (self.isStanding and self.boxes == self.end))
    
    def isTileAvailable(self, map, x, y):
        if map[y][x] == ' ' or ((map[y][x] == 'l' or map[y][x] == 'r' or map[y][x] == 'k' or map[y][x] == 'q') and not self.swatchesOn[y][x]):
            return False
        return True

    def h1(self):
        xGoal, yGoal = self.end[0], self.end[1]

        x0, y0, x1, y1 = self.boxes

        return ((abs(xGoal - x0) + abs(yGoal - y0)) // 2 + (abs(xGoal - x1) + abs(yGoal - y1)) // 2)


    ## Manhattan distance based heuristic that takes into account tiles not available.
    def h3(self, map):

        [x0, y0, x1, y1] = self.boxes
        x2, y2 = self.end[0], self.end[1]

        heuristic_value = 0
        for x in range(x0, x2 + 1):
            if self.isTileAvailable(map, x, y0):
                heuristic_value += 1
            else:
                heuristic_value += 3
        for y in range(y0, y2 + 1):
            if self.isTileAvailable(map, x0, y):
                heuristic_value += 1
            else:
                heuristic_value += 3
        for x in range(x0, x2 + 1):
            if self.isTileAvailable(map, x, y2):
                heuristic_value += 1
            else:
                heuristic_value += 3
        for y in range(y0, y2 + 1):
            if self.isTileAvailable(map, x2, y):
                heuristic_value += 1
            else:
                heuristic_value += 3

        for x in range(x1, x2 + 1):
            if self.isTileAvailable(map, x, y1):
                heuristic_value += 1
            else:
                heuristic_value += 3
        for y in range(y1, y2 + 1):
            if self.isTileAvailable(map, x1, y):
                heuristic_value += 1
            else:
                heuristic_value += 3

        for x in range(x1, x2 + 1):
            if self.isTileAvailable(map, x, y2):
                heuristic_value += 1
            else:
                heuristic_value += 3
        for y in range(y1, y2 + 1):
            if self.isTileAvailable(map, x2, y):
                heuristic_value += 1
            else:
                heuristic_value += 3

        return heuristic_value
