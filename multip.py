import multiprocessing
import numpy as np
import time as t
from syllable import findSyllables
from readwrite import readFromFile, combineFiles

def worker(num,halm):
    """thread worker function"""
    #print 'Worker:', num
    findSyllables(halm,True,"syllabelled_part_"+str(num))
    return

if __name__ == '__main__':
    jobs = []
    cpu_count=multiprocessing.cpu_count()
    print "This script will run on ",str(cpu_count)," processor"
    
    #prepare to all their halm 
    start_time=t.time()
    raw=readFromFile("sometxt")
    pieces=raw.split(" ")
    portion = len(pieces)/cpu_count
    syl_string=range(cpu_count)
    #print portion
    #print raw[portion*7:]

    for i in range(cpu_count):
        try:
            p = multiprocessing.Process(target=worker, args=(i," ".join(pieces[portion*i:portion*(i+1)])))
        except:
            p = multiprocessing.Process(target=worker, args=(i," ".join(pieces[portion*i:])))
        jobs.append(p)
        p.start()
        
    # Wait for all threads to complete
    for j in jobs:
        j.join()
    print "Combination started.."    
    combineFiles("syllabelled_part")
    print "Syllabification is finished with run time :",t.time()-start_time
