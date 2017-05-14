#!/usr/bin/env python3
import numpy as np
import argparse

# cellular automaton functions:
def generatestart(startcondition,border,size):
    """ 
    :param startcondition: r for random numers zero or one
    :param border: the size of the border one or two
    :param size: size of the whole array
    :return: the initialized array to work with
    """

    #all cells
    cells = np.zeros((size),int)
    #cells without borders
    writableCells = cells[border:size-border]

    #startcondition for seed
    if(startcondition == "s"):
        cells[size // 2] = 1
    #condition for setting random values
    else:
        for i in range(writableCells.shape[0]):
            writableCells[i]=np.round(np.random.rand())
    #print(np.shape(writableCells))
    return cells

def code2FunctionTable(code, r):
    result = {}

    c = code

    if r == 1:
        e = 8
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    if 2**e > c:
                        result[(i,j,k)] = 0
                    else:
                        result[(i,j,k)] = 1
                        c -= 2 ** e
                    e -= 1
    elif r == 2:
        e = 32
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    for l in range(2):
                        for m in range(2):
                            if 2 ** e > c:
                                result[(i, j, k, l, m)] = 0
                            else:
                                result[(i, j, k, l, m)] = 1
                                c -= 2 ** e
                            e -= 1
    return result

def getNextCellValue(functionTable, row, pos, r):
    if r == 1:
        i = row[pos - 1]
        j = row[pos]
        k = row[pos + 1]
        return functionTable[(i,j,k)]
    elif r == 2:
        i = row[pos - 2]
        j = row[pos - 1]
        k = row[pos]
        l = row[pos + 1]
        m = row[pos + 2]
        return functionTable[(i,j,k,l,m)]
    return None

def calculateNextStep(functionTable, size, row, r):
    result = np.zeros((size),int)
    for i in range(r, size - r):
        result[i] = getNextCellValue(functionTable, row, i, r)
    return result

if __name__ == "__main__":
    # parsing args:
    parser = argparse.ArgumentParser(description="one dimensional cellular automaton for k=2")
    #parser.add_argument('--steps', dest='steps', default=20, help='steps per second')
    parser.add_argument('--w', dest='w', default=84, help='field width')
    #parser.add_argument('--h', dest='h', default=livingSpaceHeight, help='field height')
    #parser.add_argument('--fullscreen', dest='fullscreen', action='store_true')
    #parser.add_argument('--window_w', dest='win_w', default=window_w, help='window width')
    #parser.add_argument('--window_h', dest='win_h', default=window_h, help='window height')
    parser.add_argument('--code', dest='code', default='17', help='code for the automaton')
    parser.add_argument('--random', dest='random', action='store_true')
    parser.add_argument('--r', dest='r', default=1, help='radius. can be 1 or 2')
    parser.set_defaults(random=False)

    args = parser.parse_args()

    r = int(args.r)
    c = int(args.code)
    size = int(args.w)
    startcondition = ""

    if args.random:
        startcondition = "r"
    else:
        startcondition = "s"

    functionTable = code2FunctionTable(c, r)
    print(functionTable)
    cells = generatestart(startcondition, r, size)
    print(cells)

    for i in range(20):
        cells = calculateNextStep(functionTable,size,cells, r)
        print(cells)



