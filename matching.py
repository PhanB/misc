import csv
from random import randrange
from datetime import datetime

#CONFIGURABLE VARIABLES
POP1_FILE = 'cohort1.rpt'
POP2_FILE = 'cohort3_50.rpt'
RESULTS_FILE = 'COHORT1_COHORT3_ASSIGNMENT.txt' #Primary Output (assignments)
INSUFFICIENT_FILE = 'COHORT1_COHORT3_INSUFFICIENT.txt' #Optional Output (gives ID of those who didnt have enough matches)
DELIMITER = ',' #Delimiter used in files (i.e. ',', '|', '\t')

NUM_MATCHES = 5 #Ratio of matching (e.g. 1:5)
HEADER_LINES = 1 #Number of header lines in file to be removed before parsing (i.e. column headers)
TAIL_LINES = 3 #Same as HEADER_LINES except at end of file


def getTime():
	return '[' + str(datetime.now().time().strftime('%H:%M:%S')) + '] '

def printT(msg):
	print(getTime() + msg)

#Tokenizes a line (used for maps)
def lineToTuple(line):
    tokens = list()
    UID = line[0] #unique idenitifer
    line = line[1:]

    for word in line:
        tokens.append(word)

    return UID, tuple(tokens)

printT("Starting...")

#SORT POP 2 INTO BUCKETS BASED ON ALL VARIABLES (EXCEPT ID)
p2map = {} # (variable1, variable2, ... , variableN) -> list of cohort 3 ID's
data = list(csv.reader(open(POP2_FILE, 'r'), delimiter='DELIMITER'))


insuff = list() # list of those with insufficient matches
assign = {} # pop1.ID -> [pop2.ID, pop2.ID, ... , pop2.ID]

printT("Sorting...")
#GROUP INTO BUCKETS BY ALL AVAILABLE VARIABLES
for line in data[HEADER_LINES:-TAIL_LINES]: #customize splice based on format of data
    if len(line) < 1: #skip blank lines
    	continue
        
    UID, myTuple = lineToTuple(line)

    if myTuple in p2map:
        p2map[myTuple].append(UID)
    else:
        p2map[myTuple] = [UID]

#MATCH EACH ID IN COHORT 1 TO [NUM_MATCHES] RANDOM ID IN COHORT 3 WHERE MATCH
printT("Matching...")
data = list(csv.reader(open(POP1_FILE, 'r'), delimiter=DELIMITER))
for line in data[HEADER_LINES:-TAIL_LINES]: #customize splice based on format of data

    if len(line) < 1: #skip blank lines
        continue


    UID, myTuple = lineToTuple(line)

    if myTuple in p2map:
        poss_part = p2map[myTuple] #list of possible matches

        if len(poss_part) < NUM_MATCHES: #If not enough matches, keep note of this UID (written to INSUFFICIENT_FILE later)
        	insuff.append(UID)

        #select [NUM_MATCHES] (or as many as we can) randomly from list of all possible matches
        assign[UID] = list()
        list_len = len(poss_part)
        for i in range(min(NUM_MATCHES,list_len)):
            random_index = randrange(0,len(poss_part)) #randomly choose index
            assign[UID].append(poss_part[random_index]) #assign
            del poss_part[random_index] #remove from possible matches (each assignment must have a unique cohort3.UID)
printT("Writing results to file...")

f = open(RESULTS_FILE, 'w')
for P1ID in assign.keys(): #P1ID = Population 1 ID
    for P2ID in assign[P1ID]: #P2ID = Population 2 ID
    	f.write(str(P1ID) + '\t' + str(P2ID) + '\n')
f.close()

f = open(INSUFFICIENT_FILE, 'w')
for ID in insuff:
	f.write(str(ID) + '\n')
f.close()

printT("Results written to: " + RESULTS_FILE)

if(len(insuff) > 0):
    printT('Warning: Number of insufficient matches = ' + str(len(insuff)) + ' (see \'' + INSUFFICIENT_FILE + '\' for full list)')

printT("Finished.")

