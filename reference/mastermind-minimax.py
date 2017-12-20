import sys, time
from collections import Counter
from itertools import product
from random import randint

color = int(sys.argv[1])
position = int(sys.argv[2])
secret = [randint(0, color-1) for i in range(position)]

color_str = ''.join(str(i)for i in range(color))
secret_str = ''.join(str(j) for j in secret)

ALL_CODES = [''.join(c) for c in product(color_str, repeat=position)]
gsbc_mp = {}  # mapping of (guess, secret) and (bulls, cows)

def genRandGuess(position):
    a = 0
    b = 0
    l = []
    for i in range(position):
        if b > 1:
            a += 1
            b = 0
        l.append(a)
        b += 1
    return l

def evaluate(guess, secret):
    if (guess, secret) in gsbc_mp:
        return gsbc_mp[(guess, secret)]
    if (secret, guess) in gsbc_mp:
        return gsbc_mp[(secret, guess)]
    matches = sum((Counter(secret) & Counter(guess)).values())
    bulls = sum(c == g for c, g in zip(secret, guess))
    cows = matches - bulls
    gsbc_mp[(guess, secret)] = (bulls, cows)
    return bulls, cows

def alpha_beta(guess_codes, secret_codes):
    min_count = float("inf")
    final_guess = ""
    for guess in guess_codes:
        bulls_cows_counter = {}
        max_count = -float("inf")
        for secret in secret_codes:
            bulls, cows = evaluate(guess, secret)
            if (bulls, cows) in bulls_cows_counter:
                bulls_cows_counter[(bulls, cows)] += 1
                if bulls_cows_counter[(bulls, cows)] > max_count:
                    max_count = bulls_cows_counter[(bulls, cows)]
                    if max_count >= min_count:
                        break
            else:
                bulls_cows_counter[(bulls, cows)] = 1
        if max_count < min_count:
            final_guess = guess
            min_count = max_count
    return final_guess

def knuth(secret, guessNum):
    """Run Knuth's 5-guess algorithm on the given secret."""
    print(secret)
    codes = ALL_CODES
    guess = ''.join(str(k) for k in genRandGuess(position))
#    key = lambda g: max(Counter(evaluate(g, c) for c in codes).values())
    while True:
        feedback = evaluate(guess, secret)
        guessNum += 1
        print("Guess {}: feedback {}".format(guess, feedback))
        if guess == secret:
            return guessNum
            #break
        codes = [c for c in codes if evaluate(guess, c) == feedback]
        if len(codes) == 1:
            guess = codes[0]
        else:
#            guess = min(ALL_CODES, key=key)
            guess = alpha_beta(ALL_CODES, codes)

def main():
    guessNum = 0
    f = open("alphabeta.txt", 'a')
    start = time.time()
    guessNum = knuth(secret_str, guessNum)
    end = time.time()
    totalTime = end - start
    print guessNum
    print totalTime
    f.write(repr(guessNum) + '\t' + repr(end-start) + '\n')
    f.close()

if __name__ == '__main__':
    main()
