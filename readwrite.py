import xml.etree.cElementTree as ET
import os
import re
from os import listdir
from os.path import isfile, join
import glob, os
import time

def cleanHtml(raw_string):
    cleaner=re.compile('<.*?>')
    clean_text=re.sub(cleaner,"",raw_string)
    return clean_text

def readFromFile(file_name,path=os.path.dirname(__file__)):  
    os.chdir(path)
    clean_text=""
    for file in glob.glob("*"+file_name+"*"):
        #print(file)
        f = open(file, "r") 
        raw_string=f.read()    
        clean_text+=cleanHtml(raw_string)+" "
    return clean_text

def combineFiles(file_name,path=os.path.dirname(__file__)):        
    os.chdir(path)
    syl_string=""
    for file in sorted(glob.glob("*"+file_name+"*")):
        print(file)
        f = open(file, "r")
        syl_string+=f.read()+"~ ~"
        f.close()
        os.remove(file)
    syl_string=syl_string[:-3]
    with open("syllabelled_data.txt", "w") as text_file:
        text_file.write(syl_string)
        
def reportData(input):
    numberOfTokens=len(input.split(" "))
    numberOfChars=len(input)
    print "numberOfTokens :",numberOfTokens
    print "numberOfChars :",numberOfChars

