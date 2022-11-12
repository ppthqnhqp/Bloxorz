from matplotlib.pyplot import box
import pygame, sys, time, random
import game_utils, solver
from pygame.locals import *
import levels

from copy import deepcopy
from genetic import Population

pygame.init()
pygame.display.set_caption('Bloxorz')
screen = pygame.display.set_mode((840, 600),0,32)
display = pygame.Surface((400, 275), pygame.SRCALPHA, 32)
display = display.convert_alpha()
POKEFONT = pygame.font.Font("assets/PKMN RBYGSC.ttf", 25)


box_component = [pygame.image.load('assets/component_0'+str(x) + '.png').convert() if x < 10 else pygame.image.load('assets/component_'+ str(x) + '.png').convert() for x in range(14) ]

for component in box_component:
    component.set_colorkey((0, 0, 0))

background = pygame.image.load('assets/background.png').convert()
cloud_img = pygame.image.load('assets/clouds.png').convert()
ground_img = pygame.image.load('assets/obj_08.png').convert()
grass_img = pygame.image.load('assets/obj_04.png').convert()
water_img = pygame.image.load('assets/obj_20.png').convert()
bridge_img = pygame.image.load('assets/bridge_0.png').convert()
roundBtn_img = pygame.image.load('assets/button_0.png').convert()
xBtn_img = pygame.image.load('assets/button_2.png').convert()
snow_img = pygame.image.load('assets/snow_0.png').convert()
splitBtn_img = pygame.image.load('assets/button_4.png').convert()

background.set_colorkey((0, 0, 0))
background = pygame.transform.scale(background, (840, 600))
cloud_img.set_colorkey((0, 0, 0))
cloud_img = pygame.transform.scale(cloud_img, (840, 600))
cloud_img.set_alpha(200)
ground_img.set_colorkey((0, 0, 0))
water_img.set_colorkey((0, 0, 0))
grass_img.set_colorkey((0, 0, 0))
bridge_img.set_colorkey((0, 0, 0))
roundBtn_img.set_colorkey((0, 0, 0))
xBtn_img.set_colorkey((0, 0, 0))
snow_img.set_colorkey((0, 0, 0))
splitBtn_img.set_colorkey((0, 0, 0))

#gameObj.boxes = [(0,2),(0,0)]
# gameObj.boxes = [(0,2),(0,1)]
# gameObj.boxes = [(0,1),(0,2)]
# gameObj.boxes = [(0,1),(1,1)]
# gameObj.boxes = [(1,1),(0,1)]
# gameObj.boxes = [(1,1),(2,1)]
# gameObj.boxes = [(0,0)]

level = 1
level, gameObj, map, enumMap, swatches, vitalSwatchesNum = game_utils.gameGenerate(level)
tempGameObj = gameObj
runAlgor = False


currentPop = []
currentGene = ''
runVisual = False

while True:
    # display.fill((0,0,0))
    display = pygame.Surface((400, 275), pygame.SRCALPHA, 32)
    display = display.convert_alpha()
    isProper = True
    isWin = False
    #For change direction in map: for x, row in enumerate(map):
    if runAlgor:
        if i < len(solution):
            isProper, isWin = gameObj.makeMove(map, swatches, solution[i])
            i += 1
            time.sleep(0.3)
        else:
            runAlgor = False
    for y, row in reversed(enumMap):
        for x, tile in reversed(row): 
            if x == 0 or y == 0:
                 display.blit(ground_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 + 10))
            if tile == 'b':
                display.blit(grass_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
                #For change direction in map: display.blit(grass_img, (x * 10 + y * 10, 100 + x * 5 - y * 5))
            elif (tile == 'l' or tile == 'r' or tile == 'k' or tile == 'q'):
                if gameObj.swatchesOn[y][x]:
                    display.blit(bridge_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
                else:
                    display.blit(water_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
            elif tile == 's':
                display.blit(grass_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
                display.blit(roundBtn_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
            elif tile == 'h':
                display.blit(grass_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
                display.blit(xBtn_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
            elif tile == 'f':
                display.blit(snow_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
            elif tile == 'v':
                display.blit(grass_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
                display.blit(splitBtn_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
            elif tile == ' ':
                display.blit(water_img, (144 - x * 16 + y * 16, 220 - x * 8 - y * 8))
            
            if (x == gameObj.boxes[0] and y == gameObj.boxes[1]) or (x == gameObj.boxes[2] and y == gameObj.boxes[3]):
                if gameObj.isStanding:
                    display.blit(box_component[7], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                    display.blit(box_component[6], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                    display.blit(box_component[6], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 24))
                    display.blit(box_component[6], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 32))
                    display.blit(box_component[5], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 40))
                elif gameObj.isConsecutiveBoxes:
                    if gameObj.isAlongYAxis:
                        if gameObj.boxes[0] == x and gameObj.boxes[1] == y:
                            display.blit(box_component[4], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                            display.blit(box_component[3], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                        else:
                            display.blit(box_component[2], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                            display.blit(box_component[1], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                    else:
                        if gameObj.boxes[0] == x and gameObj.boxes[1] == y:
                            display.blit(box_component[11], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                            display.blit(box_component[10], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                            
                        else:
                            display.blit(box_component[9], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                            display.blit(box_component[8], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                            
                elif gameObj.boxes[gameObj.boxChoose*2] == x and gameObj.boxes[gameObj.boxChoose*2+1] == y:
                    display.blit(box_component[7], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                    display.blit(box_component[5], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
                else:
                    display.blit(box_component[13], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 8))
                    display.blit(box_component[12], (144 - x * 16 + y * 16, 220 - x * 8 - y * 8 - 16))
    if not runAlgor and not runVisual:
        for event in pygame.event.get():
            # event = pygame.event.get().pop()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RIGHT:
                    isProper, isWin = gameObj.makeMove(map, swatches, 'R')
                elif event.key == K_LEFT:
                    isProper, isWin = gameObj.makeMove(map, swatches, 'L')
                elif event.key == K_UP: 
                    isProper, isWin = gameObj.makeMove(map, swatches, 'U')
                elif event.key == K_DOWN:
                    isProper, isWin = gameObj.makeMove(map, swatches, 'D')
                elif event.key == K_SPACE:
                    if not gameObj.isConsecutiveBoxes:
                        isProper, isWin = gameObj.makeMove(map, swatches, 'S')
                elif event.key == K_n:
                    level += 1
                    level, gameObj, map, enumMap, swatches, vitalSwatchesNum = game_utils.gameGenerate(level)
                elif event.key == K_b:
                    level -= 1
                    level, gameObj, map, enumMap, swatches, vitalSwatchesNum = game_utils.gameGenerate(level)
                elif event.key == K_a:
                    print('Run Breadth First Search Algorithm level', level)
                    runAlgor = True
                    i = len(gameObj.moves)
                    t = time.time()
                    solution = solver.bfs(map, swatches, gameObj)
                    print(time.time()-t)
                    print(solution)
                    print('-------------------------------------')
                elif event.key == K_g:
                    print('Run Genetic Algorithm level', level)
                    runAlgor = True
                    i = len(gameObj.moves)
                    t = time.time()
                    solution = solver.genetic(map, swatches, gameObj,0,1)
                    print(time.time()-t)
                    print(solution)
                    print('-------------------------------------')
                # for box in gameObj.boxes:
                #     if box[0] > levels.MAX_X or box[0] < 0 or box[1] > levels.MAX_Y or box[1] < 0 or map[box[1]][box[0]] == ' ':
                #         gameObj.boxes = [(levels.levels[level]['start']['x'],levels.levels[level]['start']['y'])]
                if not isProper:
                    level, gameObj, map, enumMap, swatches, vitalSwatchesNum = game_utils.gameGenerate(level)
                elif isWin:
                    level += 1
                    level, gameObj, map, enumMap, swatches, vitalSwatchesNum = game_utils.gameGenerate(level)

    
    screen.blit(background, (0,0))
    screen.blit(cloud_img, (0,0))
    screen.blit(pygame.transform.scale(display, (400*1.8, 275*1.8)), (60, 120))
    text = POKEFONT.render('Level ' + f'{level:02d}', True, (0, 0, 0))
    rect = text.get_rect()
    rect.bottomright = (840, 600) 
    screen.blit(text, rect)
    # screen.blit(display, (0, 100))
    pygame.display.update()
