from math import factorial
from math import floor
from time import time

rTotal=2
bTotal=2
gTotal=4
sTotal=4
nTotal=4
lTotal=4
pTotal=18

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
    pawnCount=0
    for file in newBoard:
        if file[0]+file[1]>2:
            return
        if file[2]+file[3]>7: #changed to 7
            return
        if file[1]+file[3]>2:
            return
        pawnCount+=file[1]+file[3]
    if pawnCount>pTotal:
        return
    for oldBoard in pawnBoards[emptyPawnBoard]:
        if oldBoard==newBoard:
            return
    pawnBoards[emptyPawnBoard].append(newBoard)

def addLance(newBoard, emptyLanceBoard):
    newBoard=tuple(sorted(newBoard))
    lanceCount=0
    for file in newBoard:
        if file[0]+file[1]>2:
            return
        if file[2]+file[3]>7: #changed to 7
            return
        lanceCount+=file[1]+file[3]
    if lanceCount>lTotal:
        return
    for oldBoard in lanceBoards[emptyLanceBoard]:
        if oldBoard==newBoard:
            return
    lanceBoards[emptyLanceBoard].append(newBoard)

def addKnight(newBoard):
    newBoard=tuple(sorted(newBoard))
    knightCount=0
    for file in newBoard:
        if file[0]>2:
            return
        if file[1]>2:
            return
        if file[2]>5: #added for high nTotal values
            return
        for k in file:
            knightCount+=k
    if knightCount>nTotal:
        return
    for oldBoard in knightBoards:
        if oldBoard==newBoard:
            return
    knightBoards.append(newBoard)

def endgame(n, l, p):
    #n is the number of Knights used already
    #l is the number of Lances used already
    #p is the number of pawns used already
    squares=81-n-l-p
    endgameCombos=0
    #put Kings down
    c=squares*(squares-1)
    squares-=2 #remove the squares taken by the Kings
    for R in range(0, rTotal+1):
        c1=c*(rTotal+1-R)*4**R*factorial(squares)/factorial(squares-R)/factorial(R)
        squares1=squares-R
        for B in [0, 1, 2]:
            c2=c1*(bTotal+1-B)*4**B*factorial(squares1)/factorial(squares1-B)/factorial(B)
            squares2=squares1-B
            for N in range(nTotal+1-n):
                c3=c2*(nTotal+1-n-N)*2**N*factorial(squares2)/factorial(squares2-N)/factorial(N)
                squares3=squares2-N
                for L in range(lTotal+1-l):
                    c4=c3*(lTotal+1-l-L)*2**L*factorial(squares3)/factorial(squares3-L)/factorial(L)
                    squares4=squares3-L
                    for G in range(gTotal+1):
                        c5=c4*(gTotal+1-G)*2**G*factorial(squares4)/factorial(squares4-G)/factorial(G)
                        squares5=squares4-G
                        for S in range(sTotal+1):
                            c6=c5*(sTotal+1-S)*4**S*factorial(squares5)/factorial(squares5-S)/factorial(S)
                            squares6=squares5-S
                            for P in range(pTotal+1-p):
                                c7=c6*(pTotal+1-p-P)*2**P*factorial(squares6)/factorial(squares6-P)/factorial(P)
                                endgameCombos+=c7
    return endgameCombos


startTime=time()

#Phase 1:   The creation of knightBoards, lanceBoards, pawnBoards,
#           knight2lance, lance2pawn,
#           knightCombos, lanceCombos, and pawnCombos
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

knight2lance={}
for knightBoard in knightBoards:
    lanceBoard=()
    for oldFile in knightBoard:
        newFile=(oldFile[0], 0, oldFile[1]+oldFile[2], 0),
        lanceBoard+=newFile
    knight2lance[knightBoard]=lanceBoard
print "knightBoards created: ", len(knightCombos)

lanceBoards={}
for emptyLanceBoard in knight2lance.values():
    lanceBoards[emptyLanceBoard]=[emptyLanceBoard]
print "Compressed into ", len(lanceBoards), " empty lanceBoards"
print ""

print "Creating lanceBoards"
for emptyLanceBoard in lanceBoards:
    i=0
    while i<len(lanceBoards[emptyLanceBoard]):
        lanceBoard=lanceBoards[emptyLanceBoard][i]
        for newFile in [((0, 1, 0, 0),), ((0, 0, 0, 1),)]:
            addLance(lanceBoard+newFile, emptyLanceBoard)
        for j, oldFile in enumerate(lanceBoard):
            for newFile in [((oldFile[0], oldFile[1]+1, oldFile[2], oldFile[3]),), ((oldFile[0], oldFile[1], oldFile[2], oldFile[3]+1),)]:
                addLance(lanceBoard[:j]+newFile+lanceBoard[j+1:], emptyLanceBoard)
        i+=1

lanceCombos={}
for emptyLanceBoard in lanceBoards:
    for lanceBoard in lanceBoards[emptyLanceBoard]:
        combos=[]
        for i in range(9):
            if i<len(lanceBoard):
                file=lanceBoard[i]
                combos.append(comb(2-file[0], file[1])*comb(7-file[2], file[3])*2**file[3])
            else:
                combos.append(1)
        lanceCombos[lanceBoard]=tuple(combos)
print "lanceBoards created: ", len(lanceCombos)

lance2pawn={}
for emptyLanceBoard in lanceBoards:
    for lanceBoard in lanceBoards[emptyLanceBoard]:
        pawnBoard=()
        for oldFile in lanceBoard:
            newFile=(oldFile[0]+oldFile[1], 0, oldFile[2]+oldFile[3], 0),
            pawnBoard+=newFile
        lance2pawn[lanceBoard]=pawnBoard

pawnBoards={}
for emptyPawnBoard in lance2pawn.values():
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
                combos.append(comb(2-file[0], file[1])*comb(7-file[2], file[3])*2**file[3])
            else:
                combos.append(1)
        pawnCombos[pawnBoard]=tuple(combos)
print "Number of pawnBoards created: ", len(pawnCombos)
print "Time elapsed: ", int(time()-startTime), " seconds"
print ""


print "Phase 2: File combinations"

c={}
for n in range(nTotal+1):
    for l in range(lTotal+1):
        for p in range(pTotal+1):
            c[(n,l,p)]=0

for index, knightBoard in enumerate(knightBoards):
    print "Using knightBoard ", index, " of ", len(knightCombos)
    for lanceBoard in lanceBoards[knight2lance[knightBoard]]:
        for pawnBoard in pawnBoards[lance2pawn[lanceBoard]]:
            splitList=list(set(splits(knightBoard)+splits(lanceBoard)+splits(pawnBoard)))
            splitList.sort()
            splitStart=0
            combos=1
            for split in splitList:
                numOfFiles=split-splitStart
                emptyPlaces=9-splitStart
                filePermutations=knightCombos[knightBoard][splitStart]*lanceCombos[lanceBoard][splitStart]*pawnCombos[pawnBoard][splitStart]
                combos*=comb(emptyPlaces, numOfFiles)*filePermutations**numOfFiles
                splitStart=split
            n=0
            for file in knightBoard:
                for num in file:
                    n+=num
            l=0
            for file in lanceBoard:
                l+=file[1]
                l+=file[3]
            p=0
            for file in pawnBoard:
                p+=file[1]
                p+=file[3]
            f=9-splitList[-1] #f is the number of empty files
            for extraP in range(2*f+1):
                if p+extraP<=pTotal:
                    c[(n, l, p+extraP)]+=combos*pawnOnlyBoards[f][extraP]
print "Time elapsed: ", int(time()-startTime), " seconds"
print ""

print "Phase 3: Adding Kings and other pieces"

totalCombos=0
for n in range(nTotal+1):
    for l in range(lTotal+1):
        for p in range(pTotal+1):
            endgameCombos=endgame(n, l, p)
            print "n, l, p is ", n, l, p
            print "endgameCombos is ", endgameCombos
            print "c[(n, l, p)] is ", c[(n, l, p)]
            totalCombos+=endgameCombos*c[(n, l, p)]
            print "total combinations: ", totalCombos
            print ""
print "Finished"
print "Time elapsed: ", int(time()-startTime), " seconds"
