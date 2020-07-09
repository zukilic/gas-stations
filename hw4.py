"""
Zeynep Ülkü Kılıç
18120205011

PROJE ÖDEVİ
"""

import math
import itertools
import time

infi = math.inf

Limit = 100     #k yani minimum durma uzaklığı
F = 300         #bir depo ile gidilebilecek maksimum uzaklık
D = 1300        #toplam gidilecek mesafe

#istasyonların başlangıç noktasına uzaklıklarını içeren array
mList = [150, 150, 150, 350, 500, 550, 600, 600, 700, 750, 800, 900, 1000, 1100]
 #istasyonların bir depo benzin maliyeti
pList = [77, 51, 67, 73, 81, 72, 86, 87, 94, 88, 85, 72, 81, 52]

N = len(mList)  #toplam istasyon sayısı

print("distance from the starting point of the gas stations:\n", mList)
print("filling costs of gas staitons:\n", pList)

###############################################################################

def greedy():
    #choosing where to start
    i = 0
    idxmin = 0
    cost = pList[idxmin]
    while(i < N):
        if(mList[i] >= Limit and mList[i] <= F):
            if(pList[i] < cost):
                cost = pList[i]
                idxmin = i
        i += 1
    #choosing the rest
    i = idxmin
    while i < N:
        min = infi
        j = idxmin + 1
        while j < N:
            if(mList[j] - mList[i] >= Limit and mList[j] - mList[i] <= F):
                if(pList[j] < min):
                    min = pList[j]
                    idxmin = j
            j += 1
        if(min != infi):
            cost += min
            i = idxmin
        else:
            i += 1
    #checking the last statiton is true or not
    if(D - mList[idxmin] > F):
        return 0
    return cost

start = time.time()
print("minimum cost with greedy algortihm is:", greedy())
stop = time.time()
print("time: {:.10f} seconds".format(stop - start))


###############################################################################

minCost = []    #for dynamic programming
#making the list 2d
for i in range(N+1):
    minCost.append([])

#initializing the list with infinitive
for i in range(N+1):
    for j in range(N+2):
        minCost[i].append(infi)
        #rows of minCost means starting points,
        #first row means the 0.km, second row means first station..
        #columns of minCost means destinations
        #one before the last column means minimum cost from that point to the end
        #last column means that rows minimums index

#cost of the gas from starting point to D
def dynamic(start):
    if(start > N):
        print("WRONG ENTRY")
        return 0
    if(minCost[start][N] != infi):
        return minCost[start][N]
    if(minCost[start][N+1] != infi):
        minCost[start][N] = dynamic(minCost[start][N+1] + 1) + minCost[start][minCost[start][N+1]]
        return minCost[start][N]
    else:
        i = start
        while (i < N):
            if(start == 0):
                if(mList[i] >= Limit and mList[i] <= F):
                    minCost[start][i] = pList[i]
            elif(mList[i] - mList[start-1] >= Limit and mList[i]-mList[start-1] <= F):
                minCost[start][i] = pList[i]
            i += 1
    minCost[start][N+1] = minCost[start].index(min(minCost[start]))
    if(start != N):
        minCost[start][N] = dynamic(minCost[start][N+1] + 1) + minCost[start][minCost[start][N+1]]
    else: 
        minCost[start][N] = 0
    return minCost[start][N]


#if 0 is entered to the function it means starting point is 0.km
#if 1 is entered to the function it means starting point is first station
#if 2 is entered to the function it means starting point is second station...
start = time.time()
print("minimum cost with dynamic programming is:", dynamic(0))
stop = time.time()
print("time: {:.10f} seconds".format(stop - start))
i = 0
for row in minCost:
    print(i, row)
    i +=1
print("if we start from the first station, minimum cost with dynamic programming is:", dynamic(1))


###############################################################################

def unique():
    a = mList[0]
    idx = 0
    min = infi
    for i in range(len(mList)):
        if mList[i] == a and i != 0:
            idx += 1
    for i in range(idx+1):
        if min > pList[i]:
            min = pList[i]
    return min

#calculates the minimum cost between two stations
count = 0
def div_con(start, end):
    global count
    if count == 0:
        if end >= N:
            return 0
        if(mList[start] < Limit or mList[start] > F):
            return 0
        if(D - mList[end] > F):
            return 0
        count = 1
        
    if(mList[end] - mList[start] >= Limit and mList[end] - mList[start] <= F):
        return pList[end]

    cost = infi
    
    i = start + 1
    while (i < end):
        min = div_con(start, i) + div_con(i, end)
        if(min < cost): 
            cost = min
        i += 1
        
    return cost            

start = time.time()
print("minimum cost with divide&conquer is:", div_con(0, N-1) + unique())
stop = time.time()
print("time: {:.10f} seconds".format(stop - start))

print("if we start from the first station, minimum cost with divide&conquer is:", div_con(0, N-1))

###############################################################################

def brute_force():
    all_combinations = []
    paths = []
    costs = []
    for r in range(len(mList) + 1):
        combinations_object = itertools.combinations(mList, r)
        combinations_list = list(combinations_object)
        all_combinations += combinations_list
    all_combinations.pop(0)
    for i in range(len(all_combinations)):
        a = 0
        for j in range(len(all_combinations[i])):
            if(len(all_combinations[i]) > 1):
                if(j == 0 and (all_combinations[i][j] <= F and all_combinations[i][j] >= Limit)):
                    a += 1
                if(j > 0 and (all_combinations[i][j]-all_combinations[i][j-1] >= Limit and all_combinations[i][j]-all_combinations[i][j-1] <= F)):
                    a += 1
                if(j == len(all_combinations[i])-1 and D-all_combinations[i][j] <= F):
                    a += 1
        if(len(all_combinations[i]) > 1):
            if a == len(all_combinations[i])+1:
                paths.append(all_combinations[i])
    
    paths = list(set(paths))    #making paths unique
    for i in range(len(paths)):
        cost = 0
        for j in range(len(paths[i])):
            idx = mList.index(paths[i][j])
            idx2 = idx + 1
            r = 2
            while(idx2 < len(mList) and mList[idx2] == mList[idx]):
                if(pList[idx2] < pList[idx]):
                    idx = idx2
                idx2 = mList.index(paths[i][j]) + r
                r += 1
            cost += pList[idx]
        costs.append(cost)
    x = min(costs)
    y = costs.index(x)
    print("path will be: ", paths[y])
    return min(costs)

start = time.time()
print("minimum cost with brute-force is:", brute_force())
stop = time.time()
print("time: {:.10f} seconds".format(stop - start))
