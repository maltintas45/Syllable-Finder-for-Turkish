#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import sys
import copy as cp
from string import maketrans
import re
#import tqdm

reload(sys)
sys.setdefaultencoding('utf-8')

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

def toLower(string):
    upperSpec=["Â","Ç","Ğ","I","İ","Î","Ö","Ş","Ü"]
    lowerSpec=["â","ç","ğ","ı","i","î","ö","ş","ü"]
    for i in range(len(upperSpec)):
        string=string.replace(upperSpec[i],lowerSpec[i])
    return string.lower()

def findSyllables(input,willItReturnOriginal=False):    
    # input : a string that you want to syllable
    # willItReturnOriginal : do it 'True' if you want the syllabeled string with special chars, otherwise it
    # NOTE!this function returns lower case characters
    
    if input=="":
        input="Maharet güzeli görebilmektir, Sevmenin sırrına erebilmektir."
    input=toLower(input)  
    uinput=input.decode("utf-8")
    string=uinput.encode("utf-8","ignore")
    
    
    # convert string VC format
    string=string.lower()
    trantab = maketrans(intab, outtab)
    for i in range(len(speTurkishChars)):
        string=string.replace(speTurkishChars[i],matTurkishChars[i])
    pattern= string.translate(trantab, '')
    
    # find syllables start indexes
    print "finding syllables start indexes.."
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
    print "finding syllables.."
    puncInd=findPuncIndex(pattern)
    syInd=sorted(syInd+puncInd)
    output=[]
    ##print "syInd:",syInd
    for i in range(len(syInd)):
        try:
            output.append(string[syInd[i]:syInd[i+1]])
        except:
            output.append(string[syInd[i]:])
    ##print "output:",output  
    if(willItReturnOriginal==True):
        #convert specific characters to original ones
        print "converting specific characters to original ones.."
        i=0
        k=0
        substring=""
        oriSyll=""
        cand=""
        for o in output:    
            substring=input[i:]        
            ##print o,"  ",input[i:i+len(o)]," ",substring 
            t=0
            x=0        
            if input[i:i+len(o)].lower()!=o:            
                for m in range(len(o)):
                    try:
                        ##print o[-(m+1)], substring[:2*len(o)]
                        x=substring[:2*len(o)].index(o[-(m+1)])+1
                        if x>=len(o)-1:
                            break
                        else:
                            substring=substring[x+1:]
                    except:
                        t+=2
                ##print i,x,t
                oriSyll=input[i:i+x+t]
                ##print oriSyll
                output[k]=oriSyll
                i+=len(o)+findNumberOfSpecChar(oriSyll)
            else:
                i+=len(o)    
            k+=1
    #print(input)    
    #print (output)
    #findSyllableCount(input)
    
    # write the output in file
    out= str("~".join(output))
    ##print out
    with open("syllabelled_data.txt", "w") as text_file:
        text_file.write(out)    
    return output
