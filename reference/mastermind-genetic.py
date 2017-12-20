import os, random, sys, time

COLORS = []
slots = 4
guesses = []

def get_result(ai_choice, right_choice):
    assert len(ai_choice) == len(right_choice)

    copy_right_choice = list(right_choice)
    copy_ai_choice = list(ai_choice)

    black = 0
    white = 0

    for i in range(len(right_choice)):
        if right_choice[i] == ai_choice[i]:
            black = black + 1
            copy_right_choice[i] = -1
            copy_ai_choice[i] = -2

    for code in copy_ai_choice:
        if code in copy_right_choice:
            white = white + 1
            for i,c in enumerate(copy_right_choice):
                if c == code:
                    copy_right_choice[i] = -1

    return (black, white)

def cost_fitness(trial):
    WEIGHT_BLACK = 1
    WEIGHT_WHITE = 1

    black_diff = 0
    white_diff = 0

    for guess in guesses:
        guess_code = guess[0]
        guess_result = guess[1]

        trial_result = get_result(trial, guess_code)

        black_diff += abs(trial_result[0] - guess_result[0])
        white_diff += abs(trial_result[1] - guess_result[1])

    return WEIGHT_BLACK*black_diff + WEIGHT_WHITE*white_diff

CROSSOVER_RATIO = 0.5
CROSSOVER_THEN_MUTATION_RATIO = 0.03
PERMUTATION_RATIO = 0.03

def genetic_evolution(popsize, generations):

    def crossover(code1, code2):
        newcode = []
        for i in range(slots):
            if random.random() > CROSSOVER_RATIO:
                newcode.append(code1[i])
            else:
                newcode.append(code2[i])
        return newcode

    def mutate(code):
        i = random.randint(0, slots-1)
        code[i] = random.randint(1, len(COLORS))
        return code

    def permute(code):
        for i in range(slots):
            if random.random() <= PERMUTATION_RATIO:
                a = random.randint(0, slots-1)
                b = random.randint(0, slots-1)
                code[a], code[b] = code[b], code[a] #swap
        return code

    population = [[random.randint(1, len(COLORS)) for i in range(slots)] for j in range(popsize)]
    elites = []
    h = 1
    while len(elites) <= popsize and h <= generations:
        sons = []

        for i in range(len(population)):
            if i == len(population) - 1:
                sons.append(population[i])
                break

            son = crossover(population[i], population[i+1])

            if random.random() <= CROSSOVER_THEN_MUTATION_RATIO:
                son = mutate(son)

            son = permute(son)
            sons.append(son)

        pop_cost = []
        for c in sons: pop_cost.append((cost_fitness(c), c))
        pop_cost = sorted(pop_cost, key=lambda x: x[0])

        elites_temp = [(c) for (score, c) in pop_cost if score == 0]
        if len(elites_temp) == 0:
            h = h + 1
            continue

        for code in elites_temp:
            if code in elites:
                elites.remove(code)
                elites.append([random.randint(1, len(COLORS)) for i in range(slots)])

        for elite_t in elites_temp:
            if len(elites) == popsize: break
            if not elite_t in elites: elites.append(elite_t)

        population=[]
        population.extend(elites_temp)

        j = len(elites_temp)
        while j < popsize:
            population.append([random.randint(1, len(COLORS)) for i in range(slots)])
            j = j + 1

        #if not eliteratio < 0.01:
            #eliteratio -= 0.01
        h = h + 1

    return elites

'''
    if len(sys.argv) != 4:
        print 'Usage:   ./mastermind-genetic+hillclimbing.py colors slots secret_code'
        print 'Example: ./mastermind-genetic+hillclimbing.py 8 4 1234'
        print 'Play with default values.'
        COLORS.extend(range(1, 8 + 1))
        slots = 4
        random.randint(1, len(COLORS))
        secret = []
        for i in range(slots):
            secret.append(random.randint(1,8))
    else:
'''
def main():
    f = open('geneticreport.txt', 'a')
    start = time.time()
    global slots
    COLORS.extend(range(1, int(sys.argv[1]) + 1))
    slots = int(sys.argv[2])
    secret = [random.randint(1, int(sys.argv[1])) for i in range(int(sys.argv[2]))]
    #secret = [int(c) for c in sys.argv[3]]
    #print('Color selections: %s' % COLORS)
    #print('Positions: %s' % slots )
    print('Secret code: %s' % secret)
    print "----------------------------"
    random.seed(os.urandom(32))

    code = []
    code.extend(range(0,slots))
    code[0] = 1

    print('Initial guess: %s' % code)
    result = get_result(code, secret)
    print('Initial feedback: %s \n' % str(result))
    guesses.append((code, result))

    MAX_POP_SIZE = 60
    MAX_GENERATIONS = 100
    turn = 1
    while result != (slots,0):
        elites = genetic_evolution(MAX_POP_SIZE, MAX_GENERATIONS)

        while len(elites) == 0:
            elites = genetic_evolution(MAX_POP_SIZE*2, MAX_GENERATIONS/2)

        code = elites.pop()
        while code in [c for (c, r) in guesses]:
            if len(elites):
                code = elites.pop()
            else:
                code = [random.randint(1, len(COLORS)) for i in range(slots)]
        turn += 1
        result = get_result(code, secret)
        guesses.append((code, result))

        print('Number of turn: %s' % turn)
        print('Next guess: %s' % str(code))
        print('Feedback: %s \n' % str(result))

    end = time.time()
    totalTime = end-start
    print "Secret code solved! Total turn: " + str(turn) + '\t' + "Total Time: ", str(totalTime)
    f.write(repr(turn) + '\t' + repr(totalTime) + '\n')
    f.close()

if __name__ == '__main__':
        main()
