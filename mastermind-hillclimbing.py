# CS 271 - PROGRAMMING ASSIGNMENT
# CREATED BY: KYUNGWOO, YUYA, AND JONATHAN H
# MASTERMIND SOLVER USING HILLCLIMBING MUTATION

import sys, random, numpy, time
from collections import Counter
from itertools import product

if len(sys.argv) < 4:
    print "ERROR: not enough arguments provided"
    print "\tUSAGE: python", sys.argv[0], "<number of colors> <number of positions> <secret code (0 to num_colors-1)>"
    print "\te.g. python 6 4 1 1 2 3"
    exit()

# Input: number of colors and positions
color = int(sys.argv[1])
position = int(sys.argv[2])
secret = [int(i) for i in sys.argv[3:]]

for i in secret:
    if i not in range(color):
        print "ERROR: secret code not in corret format"
        exit()

if len(secret) != position:
    print "ERROR: not enough lengh for secret code"
    exit()

# Function - provides a feedback to codebreaker's answer
def evaluate(guess, sec):
    matches = sum((Counter(sec) & Counter(guess)).values())
    black = sum(c == g for c, g in zip(sec, guess))
    white = matches - black
    return black, white

# Function - generates initial guess values
def generateInitials(position,availColor):
    a = 0
    b = 0
    l = []
    colorLen = len(availColor)
    for i in range(position):
        if b > 1:
            a += 1
            b = 0
            if a==colorLen:
                a=0
        l.append(availColor[a])
        b += 1
    return l

# Function - generates the number of possible responses (heuristic)
def possibleResponse(number):
    return (number * (number + 3)) / 2

# Function - generates a distinctive color through mutation process
def mutation(color, cfg, pgg, availColor):
    fitness = [0] * color
    #print "step1: ", fitness
    for i in range(len(cfg)):
        #print cfg
        idx = cfg[i]
        #print "index:", idx
        fitness[idx] += 100
    #print "step2: ", fitness
    for i in range(len(pgg)):
        if not pgg[i] == -1:
            idx = pgg[i]
            #print idx
            #print fitness[idx]
            fitness[idx] -= 100
    #print "step3: ", fitness
    for i in range(len(cfg)):
        idx = cfg[i]
        if idx in pgg:
            fitness[idx] += 45
    #print "step4: ", fitness
    for i in range(len(fitness)):
        if i not in availColor:
            fitness[i] = 0
            continue
        fitness[i] = 100 - fitness[i]
        if fitness[i] <= 0: fitness[i] = 1
    #print "step5: ", fitness
    roullete = random.randint(1, sum(fitness))
    #print "roulette ", roullete
    roulleteIndex = searchRoulette(fitness, roullete)
    return roulleteIndex

# Function - a support function for mutation()
def searchRoulette(fitness, sumValue):
    for i in range(len(fitness)):
        sumValue = sumValue - fitness[i]
        if sumValue <= 0:
            return  i

# Function - generate a new potential guess to be submitted to codemaker
def potentialCode(cfg, feedback, availColor):
    length = len(cfg)
    pgg = [-1] * len(cfg)
    index = numpy.arange(0,length,1).tolist()
    random.shuffle(index)
    #print "index", index
    for i in range(feedback[0]):
        blackIndex = index.pop()
        #print "black index", blackIndex
        pgg[blackIndex] = cfg[blackIndex]

    if(feedback[1] > 0):
        if feedback[1]==1:
            pgg[index[0]] = cfg[index[1]]
        else:
            index2 = index[:]
            while True:
                random.shuffle(index2)
                if not numpy.array_equal(index,index2):
                    break
            for i in range(feedback[1]):
                pgg[index2[i]] = cfg[index[i]]

    for i in range(len(pgg)):
        if pgg[i] == -1:
            pgg[i] = mutation(color, cfg, pgg, availColor)

    #print "pgg=",pgg
    return pgg

# Function - generates a table that contains heuristic values
# **Note: j is Y-axis, i2 is X-axis
def generateHeuristicTable(position):
    heuristic = numpy.zeros((position+1,position+1))
    count = 0
    countEnd = possibleResponse(position)
    for i in range(position+1):
        i2 = i
        for j in range(i+1):
            if j == (position-1) and i2 == 1:
                i2 -= 1
                continue
            else:
                heuristic[j,i2]=count
                count += 1
                i2 -= 1
                if count == countEnd:
                    return heuristic

def main():
    f = open('hcreport.txt', 'a')
    start = time.time()
    pggHistory = []
    feedbackHistory = []
    availColor = numpy.arange(0,color,1)
    pgg = generateInitials(position,availColor)
    cfg = pgg
    heuristicCfg = -1
    consistencyHistory = set()
    heuristic = generateHeuristicTable(position)
    endNumber = possibleResponse(position)
    print "Secret: ", secret
    print "------------------"
    guessNum = 1
    heuristicCfg = 0;
    feedback = (0, 0)
    while True:
        print "Step", guessNum
        feedbackTemp = evaluate(pgg, secret)
        print "\tSubmitted Guess", pgg, feedbackTemp

        heuristicTemp = heuristic[feedbackTemp[0],feedbackTemp[1]]
        if heuristicTemp == endNumber-1:
            break
        if feedback[0] + feedback[1] == position:
            availColor = numpy.unique(pgg)
        if heuristicTemp == 0:
            availColor = [x for x in availColor if x not in numpy.unique(pgg)]
            pgg = generateInitials(position,availColor)
            guessNum += 1
            continue

        if(heuristicTemp >= heuristicCfg):
            cfg = pgg
            heuristicCfg = heuristicTemp
            feedback = feedbackTemp

        pggHistory.append(pgg)
        feedbackHistory.append(feedbackTemp)

        cnt=1;

        while True:
            cnt += 1
#            if cnt == 10000:
#                print "DEBUG: mutated over 10000 times"
#                break
            pgg = potentialCode(cfg, feedback, availColor)
            if str(pgg) in consistencyHistory:
                continue

            isContinue = False
            for i in range(len(pggHistory)):
                feedback2 = evaluate(pgg, pggHistory[i])
                #print "pggHistory", i, pggHistory[i], feedback2
                if not numpy.array_equal(feedback2, feedbackHistory[i]):
                    isContinue = True
                    break

            if isContinue:
                consistencyHistory.add(str(pgg))
                continue
            else:
                break
        guessNum += 1
    print "final guessNum =", guessNum
    # ----------------------------------------
    end = time.time()
    print "total time = ", end-start
    f.write(repr(guessNum) + '\t' + repr(end-start) + '\n')
    f.close()

if __name__ == '__main__':
    main()
