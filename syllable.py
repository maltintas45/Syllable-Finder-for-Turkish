#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import sys
import copy as cp
from string import maketrans
import time

# to close printing to console
# if you would like to see print outputs on console please do these;
#       * make the following two lines as comments
#       * restart kernel 
#reload(sys)
#sys.setdefaultencoding('utf-8')

# define vowel characters
vowels=["a","e","ı","i","o","ö","u","ü","â","Â","î","Î"]

# define special characters and global equivalent characters of them
speTurkishChars=["â","ç","ğ","ı","î","ö","ş","ü","Â","Ç","Ğ","İ","Î","Ö","Ş","Ü"]
matTurkishChars=["a","c","g","i","i","o","s","u","a","c","g","i","i","o","s","u"]

# map global characters  as V (Vowel) or  C(Consonant)
intab="bcdfghjklmnprstuvwyxzaeiou"
outtab="CCCCCCCCCCCCCCCCCCCCCVVVVV"

def findAllIndex(pattern):
    allIndex=[]
    ind=pattern.rindex("V")
    while ind!=-1:
        allIndex.append(ind)
        pattern=pattern[:ind]
        ##print ind
        try:
            ind=pattern.rindex("V")
        except:
            break            
    return allIndex
def findPuncIndex(string):
    puncInd=[]
    punc=["!",",",".","-","(",")","?",";",":"," ","[","]","\"","'","&","\n"]
    numbers=[str(i) for i in range(10)]
    punc+=numbers
    for c in punc:
        puncInd+=[pos for pos, char in enumerate(string) if char ==c]
    #print puncInd
    return puncInd

def findNumberOfSpecChar(string):
    syCount=0
    for v in speTurkishChars:
        c=string.count(v)
        #print v, c
        syCount+=c
    return syCount

def findSyllableCount(string):    
    syCount=0
    for v in vowels:
        c=string.count(v)
        print v, c
        syCount+=c
    print("The word '%s' contains %d syllables"%(string,syCount))
    return syCount

def isTheyEqual(a,b):
    return a.lower()==b.lower()

def prepareString(binput):
    uinput=binput.decode("utf-8").lower()    
    upperSpec=["Â","Ç","Ğ","I","İ","Î","Ö","Ş","Ü","’"]
    lowerSpec=["â","ç","ğ","ı","i","î","ö","ş","ü","'"]    
    binput=uinput.encode("utf-8","ignore")
    for i in range(len(upperSpec)):
        binput=binput.replace(upperSpec[i],lowerSpec[i])   
   
    for i in range(len(speTurkishChars)):
        binput=binput.replace(speTurkishChars[i],matTurkishChars[i])
    
    return binput;

def findSyllables(string="Maharet güzeli görebilmektir, Sevmenin sırrına erebilmektir.",willItReturnOriginal=True,output_name="syllabelled_data"):    
    # input : a string that you want to syllable
    # willItReturnOriginal : do it 'True' if you want the syllabeled string with special chars, otherwise it
    tic=time.clock()
    print "finding syllables is started"
    original_input=cp.copy(string).decode("utf-8")
    string=prepareString(string)   
    
    # convert string VC format
    trantab = maketrans(intab, outtab)
    pattern= string.translate(trantab)
    
    # find syllables start indexes
    print "\tfinding syllables start indexes.."
    voInd=findAllIndex(pattern)
    ##print voInd, pattern, string
    syInd=[]
    for i in voInd:
        if i==0:
            syInd.append(i)
        elif pattern[i-1]=="C":
            if i-1==0:
                syInd.append(i-1)
            elif pattern[i-2]=="C":
                if i-2==0:
                    syInd.append(i-2)
                elif pattern[i-3]=="V":
                    syInd.append(i-1)
                elif pattern[i-3]!="C":
                    syInd.append(i-2)                
                else:
                    syInd.append(i-1)                
            else:
                syInd.append(i-1)
        else:
            syInd.append(i)
    ##print pattern, syInd
    
    # find syllables
    print "\tfinding syllables.."
    puncInd=findPuncIndex(pattern)
    syInd=sorted(syInd+puncInd)
    output=[]
    ##print "syInd:",syInd
    for i in range(len(syInd)):
        try:
            output.append(string[syInd[i]:syInd[i+1]])
        except:
            output.append(string[syInd[i]:])
    #print "output:",output  
    if(willItReturnOriginal==True):
        #convert specific characters to original ones
        print "\tconverting specific characters to original ones.."
        i=0
        k=0
        for o in output:
            #print o,":",o.decode("utf-8"),"-->",i,"-",i+len(o.decode("utf-8")), original_input[i:i+len(o.decode("utf-8"))]
            output[k]=original_input[i:i+len(o.decode("utf-8"))].encode("utf-8","ignore")
            i+=len(o.decode("utf-8"))
            k+=1
            
    # write the output in file
    out= str("~".join(output))
    ##print out
    with open(output_name+".txt", "w") as text_file:
        text_file.write(out)
    toc=time.clock()
    print "finding syllables is finished and saved '",output_name,"' file in ",toc-tic
    return output
