import sys, subprocess

for i in range(100):
    subprocess.call([sys.executable, 'mastermind-hillclimbing.py', '12', '8'])
    #subprocess.call([sys.executable, 'mastermind-genetic-refactored.py', '9', '6'])
    #subprocess.call([sys.executable, 'mastermind-minimax2.py', '8', '5'])

steps = []
time = []

my_report = open('hcreport.txt','r')
#my_report = open('geneticreport.txt', 'r')
#my_report = open('alphabeta.txt', 'r')

data = [n for n in my_report.read().split()]

for i in range(len(data)):
    if isinstance(i, int) and i%2 == 0:
        steps.append(data[i])
    else:
        time.append(data[i])

print "=================================================="
print "Average Steps: ", sum(map(float,steps))/len(steps)
print "Average Time: ", sum(map(float,time))/len(time)
