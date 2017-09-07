#Author: Bailey Phan
#Date: September 5, 2017
#Purpose: Print out columns of a csv with matching headers

#TODO: take in arguments (first = filename, rest = column headers)

import subprocess

def main():
    filename = 'my_file.csv' #file to search
    column_headers = ['testing', 'one', 'two', 'three', 'sample_id'] #columns to print out

    #open file
    f = open(filename, 'r')
    line = f.readline().split(',')
    
    #create bash command (awk columns which match elements in column_headers)
    bashcommand = ['awk', '-F\',\'']
    awkcmd = '{ print '
    counter = 1

    for word in line:
        #if we find a header that was inputted, awk this column
        if word in column_headers:
            awkcmd = awkcmd + '$' + str(counter) + '"   "'
            column_headers.remove(word)
        counter+= 1

    awkcmd = awkcmd + '}'
    bashcommand.append(awkcmd)
    bashcommand.append(filename)    

    #print results
    if(awkcmd != '{ print }'):
        #take results of awk and pipe into column -t to format nicely
        awk = subprocess.Popen(bashcommand,stdout=subprocess.PIPE)
        output = subprocess.Popen(['column', '-t'], stdin=awk.stdout)
        output.wait()

    #if column headers were inputted that were not found, tell them
    if(len(column_headers) > 0):
        print("Column header(s) not found: " + str(column_headers))

if __name__ == '__main__':
    main()
