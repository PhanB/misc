import csv
from random import randrange
from datetime import datetime


RESULTS_FILE = 'COHORT1_COHORT3_ASSIGNMENT.txt'
INSUFFICIENT_FILE = 'COHORT1_COHORT3_INSUFFICIENT.txt'

def getTime():
	return '[' + str(datetime.now().time().strftime('%H:%M')) + ']\t'

def printT(msg):
	print(getTime() + msg)

printT("Starting...")

#SORT COHORT 3 BY DOB & YEAR
c3map = {} # (dob,year) -> list of cohort 3 enrolids
data = list(csv.reader(open('cohort3_pop.rpt', 'r'), delimiter='\t'))

ip = list() # list of those with insufficient partners
assign = {} # cohort1.enrolid -> list of cohort3.enrolid's

printT("Sorting...")
#group into buckets by dob and sex
for line in data[2:-4]: #customize splice based on format of data
        if len(line) < 1: #skip blank lines
                continue
        line = line[0].split()
        enrolid = line[0]
        dob = line[1]
        sex = line[2]


        if (dob,sex) in c3map:
                c3map[(dob,sex)].append(enrolid)
        else:
                c3map[(dob,sex)] = [enrolid]

#MATCH EACH ENROLID IN COHORT 1 TO 5 RANDOM ENROLIDS IN COHORT 3 WHERE DOB/SEX MATCH
printT("Matching...")
data = list(csv.reader(open('cohort1.rpt', 'r'), delimiter='\t'))
for line in data[1:-4]: #customize splice based on format of data

        if len(line) < 1: #skip blank lines
                continue

        line = line[0].split(',')
        #print(line)
        enrolid = line[0]
        dob = line[1]
        sex = line[2]

        if (dob,sex) in c3map:
                poss_part = c3map[(dob,sex)] #list of possible partners
                if len(poss_part) < 5:
                	ip.append(enrolid)
                #select 5 (or as many as we can) randomly
                assign[enrolid] = list()
                list_len = len(poss_part)
                for i in range(min(5,list_len)):
                        random_index = randrange(0,len(poss_part)) #randomly choose index
                        assign[enrolid].append(poss_part[random_index]) #assign
                        del poss_part[random_index] #remove from possible partners (each assignment must have a unique cohort3.enrolid)
printT("Writing results to file...")

f = open(RESULTS_FILE.txt, 'w')
for C1EID in assign.keys(): #C1EID = Cohort 1 Enroll ID
        for C3EID in assign[C1EID]: #C3EID = Cohort 3 Enroll ID
                #print('C1: ' , C1EID , '\tC3: ' , C3EID)
                f.write(str(C1EID) + '\t' + str(C3EID) + '\n')
f.close()

f = open(INSUFFICIENT_FILE, 'w')
for eid in ip:
	f.write(str(eid) + '\n')
f.close()

printT("Results written to: " + RESULTS_FILE)

printT("Finished.")

