#Author: Bailey Phan
#Date: October 12, 2017
#Purpose: Print out columns of a csv with matching headers

import subprocess
import sys
import re

def main():

    #get file and headers of columns to print
    filename = sys.argv[1] #file to search
    column_headers = [] #columns to print out
    invalid_headers = [] #headers with invalid characters 

    #check inputted headers
    an = re.compile('^[\w\s\-\/\\!@#$%^&*()_\{\}~\+]+$') #accepts alphanumeric chars, spaces, and symbols
    for arg in sys.argv[2:]:
        if an.match(arg):
            column_headers.append(str(arg).lower())
        else:
            invalid_headers.append(str(arg).lower())

    #if no column headers were accepted don't run program
    if len(column_headers) < 1:
        print_invalid_headers(invalid_headers)
        print("No valid column headers to search for.")
        return 1


    #open file and tokenize first line of it
    try:
        f = open(filename, 'r')
        first_line = f.readline().split(',')
    except IOError:
        print("Unable to open file: " + filename)
        return 1
    
    #create bash command (awk columns which match elements in column_headers)
    bashcommand = ['awk', '-F\',\'']
    awkcmd = '{ print '
    counter = 1

    for word in first_line:
        word = str(word).lower().rstrip()
        #if we find a header that was inputted, awk this column
        if word in column_headers:
            awkcmd = awkcmd + '$' + str(counter) + '"   "'
            #column_headers.remove(word)
        counter+= 1

    awkcmd= awkcmd + '}'
    bashcommand.append(awkcmd)
    bashcommand.append(filename)    

    #print results
    if(awkcmd != '{ print }'):
        #take results of awk and pipe into column -t to format nicely
        #output = subprocess.Popen(bashcommand)
        awk = subprocess.Popen(bashcommand,stdout=subprocess.PIPE)
        output = subprocess.Popen(['column', '-t'], stdin=awk.stdout)
        output.wait()

    #if column headers were inputted that were not found, tell them
    #if(len(column_headers) > 0):
        #print_invalid_headers(invalid_headers)
        #print("Column header(s) not found: " + str(column_headers))

    return 0


def print_invalid_headers(invalid_list):
    if len(invalid_list) > 0:
        print("Invalid headers: " + str(invalid_list))

if __name__ == '__main__':
    main()
