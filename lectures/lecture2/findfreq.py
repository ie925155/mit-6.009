#Find Frequencies of elements in a list -- various algorithms

inp = [0, 12, 0, 0, 12, 12, 34, 56, 23, 11, 45, 2, 3, 4, 11, 10, 12]

inps = ["zero", "twelve", "zero", "zero", "twelve", "twelve", "thirty four",
       "fifty six", "twenty three", "eleven", "forty five", "two", "three",
       "four", "eleven", "ten", "twelve" ]


def findFrequencies(input):

    #Freq needs to be as large as the maximum VALUE of the input!
    freq = [0] * (max(input) + 1)
    for i in input:
        freq[i] += 1
    print ("Big List: Maximally occurring element is", freq.index(max(freq)),
          "with frequency", max(freq))
    return

findFrequencies(inp)

inps = ["zero", "twelve", "zero", "zero", "twelve", "twelve", "thirty four",
       "fifty six", "twenty three", "eleven", "forty five", "two", "three",
       "four", "eleven", "ten", "twelve" ]

def findFrequenciesList(input):

    #Each element has frequency 1 to start
    freq = [1] * len(input)
    for i in range(len(input)):
        for j in range(len(input)):
            if input[i] == input[j] and i != j:
                freq[i] += 1

    mfreq = 0
    freqindex = 0
    for i in range(len(freq)):
        if mfreq < freq[i]:
            mfreq = freq[i]
            freqindex = i
            
    print ("List: Maximally occurring element is", input[freqindex],
          "with frequency", mfreq)
    return 

findFrequenciesList(inp)
findFrequenciesList(inps)

def findFrequenciesDict(input):
    
    freqd = {}
    for i in input:
        if i in freqd:
            freqd[i] += 1
        else:
            freqd[i] = 1
    print(freqd)
            
    inpmaxfreq, maxfreq = keywithmaxval(freqd)
    
    print ("Dictionary: Maximally occurring element is", inpmaxfreq,
          "with frequency", maxfreq)
    return

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v = list(d.values())
     k = list(d.keys())
     return k[v.index(max(v))], max(v)


findFrequenciesDict(inp)
findFrequenciesDict(inps)


