
# Sets are dictionaries without values, containing just keys
# that are elements of the set
# A set only contains unique elements and is unordered
mylist = ['nowplaying', 'PBS', 'PBS', 'nowplaying', 'job',\
          'debate', 'thenandnow']
myset = set(mylist)
print (myset)
mynewlist = list(myset)
print (mynewlist)

output = set()
for x in mylist:
    output.add(x)
print (output)

#Timing dictionaries/sets and list membership checks

def timingCheck(n):
    
    L = list(range(n))
    S = set(L)
        
    found = 0
    print ('Start list membership check')
    for i in range(len(L)):
        #We need to sequentially traverse list L on the next line
        if i in L:
            found += 1
            if found % 10000 == 0:
                print('.', end='')
    print('\nEnd list membership check')

    found = 0
    print ('Start set membership check')
    for i in range(len(S)):
        #We do a fast lookup in the set S on the next line
        if i in S:
            found += 1
            if found % 10000 == 0:
                print ('.', end='')
    print('\nEnd set membership check')


#Pair sum problem using sets
A = [42, 35, 9, 45, 88, 80, 167, 78]

def pairSum(L, k):
    S = set()
    for num in L:
        if k - num in S:
            print('Found a pair', num, ',', k - num, 'that sums to', k)
            return
        else:
            S.add(num)
    print('Could not find a pair that sums to', k)
    

##pairSum(A, 80)
##pairSum(A, 81)


#Pair of Sum of Pairs Using Dictionaries
A = [42, 35, 9, 45, 88, 80, 167, 78]

def pairSumofPairs(L):
    H = {}
    for i in range(len(A)):
        for j in range(i+1, len(A)):
            d = A[i] + A[j]
            if d in H:
                #A pair (or more) sum to the same quantity
                H[d].append((A[i], A[j]))
            else:
                #First time for this sum
                H[d] = [(A[i], A[j])]

    for p in H.values():
        if len(p) > 1:
            print (p)
            

##pairSumofPairs(A)


#Given the latest triple (in order of announcement) and the maintained
#data structure, we want to determine if we can yell Bingo and
#also update the data structure appropriately.
def permutationBingoCheck(permT, Bins):

    #Want all permutations to map to the same tuple/triple
    permTstandard = tuple(sorted(permT))
    bingo = False

    #Lookup permTstandard in Bins
    if permTstandard in Bins:
        Bins[permTstandard].add(permT)
        if len(Bins[permTstandard]) == 6:
            bingo = True
    else:
        Bins[permTstandard] = set()
        #The set doesn't store duplicate permutations!
        Bins[permTstandard].add(permT)

    return bingo, permTstandard


#Given a sequence L read out number by number, determine when
#to yell Bingo.
def playBingo():

    B = {}
    L = []
    while True:
        num = int(input('Give a number:'))
        L.append(num)
        if num == -1:
            print ('Game ended with no Bingo!')
            return
        elif len(L) > 2:
            bingo, triple = permutationBingoCheck(tuple(L[-3:]), B)
            if bingo:
                print ('Bingo!', triple)
                return


##A = [2, 19, 4, 1, 100, 1, 4, 19, 1, 4, 1,
##     19, 100, 192, 100, 4, 19, 2, 1, 19, 4]
##playBingo(A[:-1])
##playBingo(A)

