from copy import deepcopy
import levels
import game

def swatchesDecode(swatches):
    vitalSwatchesNum = 0
    swatchesDict = dict()
    for swatch in swatches:
        x = swatch["position"]["x"]
        y = swatch["position"]["y"]
        xDecoded = f'{x:02d}'
        yDecoded = f'{y:02d}'
        swatchesDict[xDecoded+yDecoded] =swatch['fields']
        for field in swatch['fields']:
            if field['action'] != 'off':
                vitalSwatchesNum += 1
            break
    return swatchesDict, vitalSwatchesNum


def gameGenerate(levelNo):
    level = levels.levels[levelNo-1]
    gameObj = game.Game(level)
    map = level['geometry']
    enumMap = [list(enumerate(row)) for row in map]
    enumMap = list(enumerate(enumMap))
    swatches, vitalSwatchesNum = swatchesDecode(level['swatches'])
    return gameObj, map, enumMap, swatches, vitalSwatchesNum