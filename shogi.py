from math import factorial
from math import floor
from time import time

def comb(n, k):
    return factorial(n)/factorial(k)/factorial(n-k)

def splits(board):
    splitList=[]
    for i in range(len(board)-1):
        if board[i]!=board[i+1]:
            splitList.append(i+1)
    splitList.append(len(board))
    return tuple(splitList)

def addPawn(newBoard, emptyPawnBoard):
    newBoard=tuple(sorted(newBoard))
    for file in newBoard:
        if file[0]+file[1]>2:
            return
        if file[2]+file[3]>5:
            return
        if file[1]+file[3]>2:
            return
    for oldBoard in pawnBoards[emptyPawnBoard]:
        if oldBoard==newBoard:
            return
    pawnBoards[emptyPawnBoard].append(newBoard)

def addLancer(newBoard, emptyLancerBoard):
    newBoard=tuple(sorted(newBoard))
    totalLancers=0
    for file in newBoard:
        if file[0]+file[1]>2:
            return
        if file[2]+file[3]>5:
            return
        totalLancers+=file[1]+file[3]
    if totalLancers>4:
        return
    for oldBoard in lancerBoards[emptyLancerBoard]:
        if oldBoard==newBoard:
            return
    lancerBoards[emptyLancerBoard].append(newBoard)

def addKnight(newBoard):
    newBoard=tuple(sorted(newBoard))
    totalKnights=0
    for file in newBoard:
        if file[0]>2:
            return
        if file[1]>2:
            return
        for k in file:
            totalKnights+=k
    if totalKnights>4:
        return
    for oldBoard in knightBoards:
        if oldBoard==newBoard:
            return
    knightBoards.append(newBoard)

def endgame(n, l, p):
    #n is the number of Knights used already
    #l is the number of Lancers used already
    #p is the number of pawns used already
    s=81-n-l-p
    endgameCombos=0
    #put Kings down
    c=s*(s-1)
    s-=2 #remove the squares taken by the Kings
    for R in [0, 1, 2]:
        c1=c*(3-R)*4**R*factorial(s)/factorial(s-R)/factorial(R)
        s1=s-R
        for B in [0, 1, 2]:
            c2=c1*(3-B)*4**B*factorial(s1)/factorial(s1-B)/factorial(B)
            s2=s1-B
            for N in range(5-n):
                c3=c2*(5-n-N)*2**N*factorial(s2)/factorial(s2-N)/factorial(N)
                s3=s2-N
                for L in range(5-l):
                    c4=c3*(5-l-L)*2**L*factorial(s3)/factorial(s3-L)/factorial(L)
                    s4=s3-L
                    for G in range(5):
                        c5=c4*(5-G)*2**G*factorial(s4)/factorial(s4-G)/factorial(G)
                        s5=s4-G
                        for S in range(5):
                            c6=c5*(5-S)*4**S*factorial(s5)/factorial(s5-S)/factorial(S)
                            s6=s5-S
                            for P in range(19-p):
                                c7=c6*(19-p-P)*2**P*factorial(s6)/factorial(s6-P)/factorial(P)
                                endgameCombos+=c7
    return endgameCombos


startTime=time()

#Phase 1:   The creation of knightBoards, lancerBoards, pawnBoards,
#           knight2lancer, lancer2pawn,
#           knightCombos, lancerCombos, and pawnCombos
print "Phase 1: Creating Boards"
print ""

print "Creating pawnOnlyBoards"
pawnOnlyBoards=[]
for f in range(10):
    fCombos=[]
    for p in range(2*f+1):
        fpCombos=0
        minTwos=p-f if p>f else 0
        maxTwos=int(floor(p/2))
        for twos in range(minTwos, maxTwos+1):
            ones=p-2*twos
            zeroes=f-p+twos
            fpCombos+=57**twos*16**ones*comb(f, twos)*comb(f-twos, ones)
        fCombos.append(fpCombos)
    pawnOnlyBoards.append(fCombos)

print "Creating knightBoards"
knightBoards=[()]
i=0
while i<len(knightBoards):
    knightBoard=knightBoards[i]
    for newFile in [((1, 0, 0),), ((0, 1, 0),), ((0, 0, 1),)]:
        addKnight(knightBoard+newFile)
    for j, oldFile in enumerate(knightBoard):
        for newFile in [((oldFile[0]+1, oldFile[1], oldFile[2]),), ((oldFile[0], oldFile[1]+1, oldFile[2]),), ((oldFile[0], oldFile[1], oldFile[2]+1),)]:
            addKnight(knightBoard[:j]+newFile+knightBoard[j+1:])
    i+=1

knightCombos={}
for knightBoard in knightBoards:
    combos=[]
    for i in range(9):
        if i<len(knightBoard):
            file=knightBoard[i]
            combos.append(comb(2, file[0])*comb(2, file[1])*comb(5, file[2])*2**file[2])
        else:
            combos.append(1)
    knightCombos[knightBoard]=tuple(combos)

knight2lancer={}
for knightBoard in knightBoards:
    lancerBoard=()
    for oldFile in knightBoard:
        newFile=(oldFile[0], 0, oldFile[1]+oldFile[2], 0),
        lancerBoard+=newFile
    knight2lancer[knightBoard]=lancerBoard
print "knightBoards created: ", len(knightCombos)

lancerBoards={}
for emptyLancerBoard in knight2lancer.values():
    lancerBoards[emptyLancerBoard]=[emptyLancerBoard]
print "Compressed into ", len(lancerBoards), " empty lancerBoards"
print ""

print "Creating lancerBoards"
for emptyLancerBoard in lancerBoards:
    i=0
    while i<len(lancerBoards[emptyLancerBoard]):
        lancerBoard=lancerBoards[emptyLancerBoard][i]
        for newFile in [((0, 1, 0, 0),), ((0, 0, 0, 1),)]:
            addLancer(lancerBoard+newFile, emptyLancerBoard)
        for j, oldFile in enumerate(lancerBoard):
            for newFile in [((oldFile[0], oldFile[1]+1, oldFile[2], oldFile[3]),), ((oldFile[0], oldFile[1], oldFile[2], oldFile[3]+1),)]:
                addLancer(lancerBoard[:j]+newFile+lancerBoard[j+1:], emptyLancerBoard)
        i+=1

lancerCombos={}
for emptyLancerBoard in lancerBoards:
    for lancerBoard in lancerBoards[emptyLancerBoard]:
        combos=[]
        for i in range(9):
            if i<len(lancerBoard):
                file=lancerBoard[i]
                combos.append(comb(2-file[0], file[1])*comb(5-file[2], file[3])*2**file[3])
            else:
                combos.append(1)
        lancerCombos[lancerBoard]=tuple(combos)
print "lancerBoards created: ", len(lancerCombos)

lancer2pawn={}
for emptyLancerBoard in lancerBoards:
    for lancerBoard in lancerBoards[emptyLancerBoard]:
        pawnBoard=()
        for oldFile in lancerBoard:
            newFile=(oldFile[0]+oldFile[1], 0, oldFile[2]+oldFile[3], 0),
            pawnBoard+=newFile
        lancer2pawn[lancerBoard]=pawnBoard

pawnBoards={}
for emptyPawnBoard in lancer2pawn.values():
    pawnBoards[emptyPawnBoard]=[emptyPawnBoard]
print "Compressed into ", len(pawnBoards), " empty pawnBoards"
print "Time elapsed: ", int(time()-startTime), " seconds"
print ""

print "Creating pawnBoards"
for index, emptyPawnBoard in enumerate(pawnBoards):
    i=0
    if index%25==0:
        print "Filling emptyPawnBoard ", index, " of ", len(pawnBoards)
    while i<len(pawnBoards[emptyPawnBoard]):
        pawnBoard=pawnBoards[emptyPawnBoard][i]
        for j, oldFile in enumerate(pawnBoard):
            for newFile in [((oldFile[0], oldFile[1]+1, oldFile[2], oldFile[3]),), ((oldFile[0], oldFile[1], oldFile[2], oldFile[3]+1),)]:
                addPawn(pawnBoard[:j]+newFile+pawnBoard[j+1:], emptyPawnBoard)
        i+=1


print "Finished pawnBoard creation. Calculating combinations for pawnboards."
pawnCombos={}
for emptyPawnBoard in pawnBoards:
    for pawnBoard in pawnBoards[emptyPawnBoard]:
        combos=[]
        for i in range(9):
            if i<len(pawnBoard):
                file=pawnBoard[i]
                combos.append(comb(2-file[0], file[1])*comb(5-file[2], file[3])*2**file[3])
            else:
                combos.append(1)
        pawnCombos[pawnBoard]=tuple(combos)
print "Number of pawnBoards created: ", len(pawnCombos)
print "Time elapsed: ", int(time()-startTime), " seconds"
print ""


print "Phase 2: File combinations"

c={}
for n in range(5):
    for l in range(5):
        for p in range(19):
            c[(n,l,p)]=0

for index, knightBoard in enumerate(knightBoards):
    print "Using knightBoard ", index, " of ", len(knightCombos)
    for lancerBoard in lancerBoards[knight2lancer[knightBoard]]:
        for pawnBoard in pawnBoards[lancer2pawn[lancerBoard]]:
            splitList=list(set(splits(knightBoard)+splits(lancerBoard)+splits(pawnBoard)))
            splitList.sort()
            splitStart=0
            combos=1
            for split in splitList:
                numOfFiles=split-splitStart
                emptyPlaces=9-splitStart
                filePermutations=knightCombos[knightBoard][splitStart]*lancerCombos[lancerBoard][splitStart]*pawnCombos[pawnBoard][splitStart]
                combos*=comb(emptyPlaces, numOfFiles)*filePermutations**numOfFiles
                splitStart=split
            n=0
            for file in knightBoard:
                for num in file:
                    n+=num
            l=0
            for file in lancerBoard:
                l+=file[1]
                l+=file[3]
            p=0
            for file in pawnBoard:
                p+=file[1]
                p+=file[3]
            f=9-splitList[-1] #f is the number of empty files
            for extraP in range(2*f+1):
                c[(n, l, p+extraP)]+=combos*pawnOnlyBoards[f][extraP]
print "Time elapsed: ", int(time()-startTime), " seconds"
print ""

print "Phase 3: Adding Kings and other pieces"

totalCombos=0
for n in range(5):
    for l in range(5):
        for p in range(19):
            endgameCombos=endgame(n, l, p)
            print "n, l, p is ", n, l, p
            print "endgameCombos is ", endgameCombos
            print "c[(n, l, p)] is ", c[(n, l, p)]
            totalCombos+=endgameCombos*c[(n, l, p)]
            print "total combinations: ", totalCombos
            print ""
print "Finished"
print "Time elapsed: ", int(time()-startTime), " seconds"
