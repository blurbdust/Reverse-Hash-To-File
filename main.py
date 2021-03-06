#!/usr/bin/python

import sys, getopt, hashlib, thread
#import numpy as np
from timeit import default_timer as timer
from multiprocessing import Process, Lock
#from numbapro import cuda
#from numba import *

block_list = []
byte_list = []
byte = []
blacklisted_index = []
block_size = 4
block_count = 4
thread_count = 1
current_thread = 1
start = 0
end = 0
global_index = 0
string_of_file = ""
actual_hash = ""
found = 0

def main(argv):
#VARIABLES
    help_message = "main.py -i <inputfile or hash> -o <outputfile if hash> -p <progress file>"
    inputhash = "&"
    inputfile = "^"
    output = ""
    output_string = ""
    global start
    start = timer()
    global thread_count
#END OF VARIABLES


    try:
        opts, args = getopt.getopt(argv,"hi:o:p:t:",["ifile=","ofile=","pfile=","tfile="])
    except getopt.GetoptError:
        print help
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print help_message
            sys.exit()
        elif opt in ("-i", "--ifile"):
            if "." in arg:
                inputfile = arg
            else:
                inputhash = arg
        elif opt in ("-o", "--ofile"):
            output = arg
        elif opt in ("-p", "--progress"):
            #with open(arg) as f:
                #progress_lines = f.readlines()
            progress_lines = [line.rstrip('\n') for line in open(arg)]
            continuing_hash_to_file(progress_lines)
        elif opt in ("-t", "--thread", "--threads"):
            thread_count = arg
    if inputfile is not "^":
        try:
            tohash = open(inputfile, "rb")
        except:
            print "Error! Probably file not found... I don't know enough python yet..."
            sys.exit(2)
       
        output_string = file_to_hash(tohash, inputfile)
        print output_string
    elif inputhash is not "&":
        hash_to_file(inputhash)
    else:
        print "Something bad happened."
        sys.exit(2)

    

def file_to_hash(tohash, filename):
    not_hash = ""
    global string_of_file
    string_of_file = tohash.read()
    md5hash = hashlib.md5(string_of_file).hexdigest().upper()
    #For now we are assuming defaults
    
    tmp = filename.encode('hex').upper()
    print tmp
    not_hash += tmp
    not_hash += '-'
    
    hex_of_file = string_of_file.encode('hex').upper()
    
def hash_to_file(inputhash):
    block = []
    maybe_file = ""
    global string_of_file
    global actual_hash
    global found
    global thread_count
    global current_thread
    #inputhash.split(h="-", num=string.count(h))
    total_del = inputhash.count('-')
    hash_list = inputhash.split('-')
    print hash_list
    filename = hash_list[0]
    filename = bytearray.fromhex(filename).decode()
    print filename
    pattern = hash_list[1]
    if "00" in pattern:
        print "No pattern, starting bruteforce from seed. Next few lines are the seed."
    elif "01" in pattern:
        print "Hash came from a zip file. This feature coming soon...ish."
    else:
        print "Something bad happened."
        
    for i in range(2, total_del):
        if i%2 == 0 and i != total_del:
            block_list.append(hash_list[i])
    print block_list
    
    for x in range(0, block_count):
        globals()['block%s' % x] = block_list[x]
    print block0
    
    for i in range(3, total_del):
        if i%2 == 1 and i != total_del:
            byte_list.append(hash_list[i])
    print byte_list

    
    for i in range(0, len(byte_list)):
        for x in range(i, block_count):
            for j in range(0, (int(byte_list[i]) / (2))):
                globals()['block%s' % x] = globals()['block%s' % x] + "**"
            break
   
    print block0
    print block1
    print block2
    print block3

    print "----"
    
    for y in range(0, block_count):
        block.append(globals()['block%s' % y])

    print block
    string_of_file = ''.join(block)
    
    print "----"

    for i in range(1, len(string_of_file) - 1):
        tmp = string_of_file[i] + string_of_file[i - 1]
        byte.append(tmp)

    for j in range(0, len(string_of_file) - 1):
        if (string_of_file[j] != '*'):
            blacklisted_index.append(j)

    print "Blacklisted index", blacklisted_index
    string_of_file = string_of_file.replace('*', '0')
    print string_of_file

    print "----MD5 Hashes Below----"
    
    print hashlib.md5(string_of_file).hexdigest().upper()
    print hash_list[total_del]
    actual_hash = hash_list[total_del]
    
    global global_index
    t = 0
    try:
        for t in range(0, int(thread_count)):
            globals()['Process-%s' % t] = Process(target=compute_file, args=(hashlib.md5(string_of_file).hexdigest().upper(), actual_hash, string_of_file, found, global_index, blacklisted_index, thread_count, current_thread, filename))
            globals()['Process-%s' % t].start()
            print "Working..."
            #thread.start_new_thread( compute_file, (hashlib.md5(string_of_file).hexdigest().upper(), actual_hash, string_of_file, found, global_index, blacklisted_index, thread_count, current_thread))
    except:
        for t in range(0, int(thread_count)):
            globals()['Process-%s' % t].join()
            #Maybe I should put a lock here...
        print "We are at the process spawn exception... Killing myself"
        sys.exit(2)

    while(not found):
        pass

def increment_by_one(string_of_file2, index, thread_count, current_thread, filename):
    global string_of_file
    string_of_file = string_of_file2
    #print string_of_file2
    #The credit goes to Big-E for this function!
    hexval = string_of_file[index]                                                                          # Get the char that needs to be incremented    
    val = int ( hexval, 16 )                                                                                # Convert the char to an int [0-16]

    incremental = int(current_thread) % int(thread_count)
   
    val = (val + (incremental)) % 0x10                                                                      # Increment the int, this will be used to represent the next char
    hexval = "%X" % val                                                                                     # Convert the int back to a hex value
   
    list1 = list(string_of_file)                                                                            # Do stupid python stuff
    list1[index] = hexval                                                                                   # Save new value to array
    string_of_file = ''.join(list1)                                                                         # Do more stupid python stuff
           
    if (thread_count > 1):
           current_thread += 1                                                                              # Increment thread_count
    
    if hexval == '0' and (index + 1) < len(string_of_file):                                                 # Determine if next value to right needs to increment by one
        return increment_by_one(string_of_file, index + 1, thread_count, current_thread, filename)         # Recursivelly call this function for value to right

    #print string_of_file
    return string_of_file                                                                                   # Return from first instance of recursive functions

def continuing_hash_to_file(progress_lines):
    print progress_lines
    global string_of_file
    global global_index
    global blacklisted_index
    string_of_file = progress_lines[0]
    global_index = int(progress_lines[2])
    #blacklisted_index = map(int, progress_lines[3])
    #blacklisted_index = [int(i) for i in progress_lines[3]]
    temp5 = progress_lines[3].replace('[', "").replace(']', "").split(',')
    blacklisted_index = map(int, temp5)

    t = 0
    try:
        for t in range(0, int(thread_count)):
            globals()['Process-%s' % t] = Process(target=compute_file, args=(hashlib.md5(string_of_file).hexdigest().upper(), actual_hash, string_of_file, found, global_index, blacklisted_index, thread_count, current_thread, filename))
            globals()['Process-%s' % t].start()
            print "Working..."
            #globals()['Process-%s' % t].join()
            #thread.start_new_thread( compute_file, (hashlib.md5(string_of_file).hexdigest().upper(), actual_hash, string_of_file, found, global_index, blacklisted_index, thread_count, current_thread))
    except:
        print "We are at the process spawn exception for continuing... Killing myself"
        sys.exit(2)
        
    while(not found):
        pass
    
##    print "Yay!"
##    print "----"
##    print string_of_file
##    print "----"
##    global end
##    end = timer()
##
##    print "It took me ", end-start, " seconds!"
##    I'll come back to making a hex editor for file so it actually outputs the file.
##    f = open(progress_lines[4], 'w+')
##    f.write(string_of_file)
##    f.close()

def compute_file(curent_hash, real_hash, string_of_file2, found, global_index, blacklisted_index, thread_count, current_thread, filename):
    try:
        while(curent_hash != real_hash):
                #Increment and try again
                if global_index not in blacklisted_index:
                    string_of_file2 = increment_by_one(string_of_file2, global_index, thread_count, current_thread, filename)
                else:
                    global_index += 1
    except KeyboardInterrupt:
        print "We are at compute_file exception: ", string_of_file2
        print "Keeping this value"
        dump_current_progress(thread_count, real_hash, string_of_file, global_index, blacklisted_index, filename)


def dump_current_progress(thread_count, real_hash, string_of_file, global_index, blacklisted_index, filename):
    global end
    global start
    #Wow that's a lot of global variables
    print "===============Program Ended because of interrupt==================="
    print string_of_file
    end = timer()
    print "It took me ", end-start, " seconds until you stopped me!"
    progress_filename = "progress_"
    progress_filename += filename
    progress = open(progress_filename, "w+")
    progress.write(string_of_file)
    progress.write("\n")
    progress.write(real_hash)
    progress.write("\n")
    progress.write(str(global_index))
    progress.write("\n")
    progress.write(str(blacklisted_index))
    progress.write("\n")
    progress.write(filename)
    progress.close()
    print "Dumping progress to file..."

def we_got_him(string_of_file):
    print "Yay!"
    found = 1
    print "----"
    print string_of_file
    print "----"
    end = timer()

    print "BROKEN: It took me ", end-start, " seconds!"
    
    f = open(filename, 'w+')
    f.write(string_of_file)
    f.close()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        #dump_current_progress(thread_count, string_of_file)
        sys.exit(0)
