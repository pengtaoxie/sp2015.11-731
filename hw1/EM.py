#!/usr/bin/env python
import optparse
import sys
import string
from collections import defaultdict

def readFile(filename):
    linecount = 0
    outfile = open('temp.txt', 'w')
    for line in open(filename, "r"):
        line = line.strip()
        line = line.lower()
        linecount += 1
        outfile.write(line + '\n')
        if (linecount >= 100000):
            break
    return linecount

readFile("data/dev-test-train.de-en")
#print readFile("data/dev.align")
#print readFile("dall.al")
gerDic = {}
enDic = {}
tupleList = []

def splitPairs(filename):
    index = 0
    for line in open(filename, "r"):
        sen_list = line.split("|||")
        genS = sen_list[0].strip()
        #genS = genS.lower()
        enS = sen_list[1].strip()
        #enS = enS.lower()
        gerDic[index] = genS
        enDic[index] = enS
        tupleList.append((genS, enS))
        index += 1

#splitPairs("data/dev-test-train.de-en")
splitPairs("temp.txt")
lexGerDic = defaultdict(lambda: defaultdict(float))
lexGerCountDic = defaultdict(int)

def initTransitionP():
    #initialize uniform trans probablities
    #source is german; target is english
    print("initialize uniform t")
    length = len(tupleList)
    for i in xrange(length): #length
        (gS, eS) = tupleList[i] 
        for gword in gS.split():
            for eword in eS.split():
                lexGerDic[gword][eword] += 1
                lexGerCountDic[gword] += 1
    print("calculating the uniform probability")
    for gkey in lexGerDic.keys():
        count = lexGerCountDic[gkey]
        for ekey in lexGerDic[gkey].keys():
            lexGerDic[gkey][ekey] /= count
    print ("done init")

def getCount(gerS, enS, transD, countDic):
    for gw in gerS:
        sum = 0.0
        for ew in enS:
            sum += transD[gw][ew]
        for ew2 in enS:
            if (sum != 0):
                countDic[gw][ew2] += transD[gw][ew2]/sum

def normCount(countDic, transD):
    eCount = defaultdict(float)
    for gkey in countDic.keys():
        for ekey in countDic[gkey].keys():
            eCount[ekey] += countDic[gkey][ekey]
    for gkey in countDic.keys():
        for ekey in countDic[gkey].keys():
            transD[gkey][ekey] = countDic[gkey][ekey] / eCount[ekey]

#pseudocode form www.cs.jhu.edu/~jason/465
#initialize t(e|f) uniformly
#do
#  set count(e|f) to 0 for all e,f
#  set total(f) to 0 for all f
#  for all sentence pairs(e_s, f_s)
#    for all words e in e_s
#      total_s = 0
#      for all words f in f_s
#        totsl_s += t(e|f)
#    for all words e in e_s
#      for all words f in f_s
#        count(e|f) += t(e|f) / total_s
#        total(f) += t(e|f) / total_s
#  for all f in domain(total(.))
#    for all e in domain(count(.|f))
#      t(e|f) = count(e|f) / total(f)
#until convergence

def align(numIts):
    initTransitionP()
    NULL = '_NULL_'
    for i in xrange(numIts):
        print("running %sth iteration of EM'" % i)
        # take a sentence pair
        count = defaultdict(lambda:defaultdict(float))
        for j in xrange(len(tupleList)):
            (gs, es) = tupleList[j]
            gsList = gs.split()
            esList = es.split()
            getCount(gsList, esList, lexGerDic, count)
        normCount(count, lexGerDic)

#used to run 10 times
align(6)


def printable(tList):
    allout = open('output-thresh.txt', 'w')
    for i in xrange(len(tList)): 
        printers=[]
        (gs, es) = tList[i]
        glist = gs.split()
        elist = es.split()
        for gindex in xrange(len(glist)):
            gword = glist[gindex]
            tempEword = elist[0]
            tempMaxIndex = 0
            tempMax = lexGerDic[gword][tempEword]
            for eindex in xrange(1,len(elist)):
                eword = elist[eindex]
                if (lexGerDic[gword][eword] > tempMax):
                    tempMaxIndex = eindex
                    tempMax = lexGerDic[gword][eword]
            if (tempMaxIndex > 0.05):
                printers.append((gindex, tempMaxIndex))
        #sortedP = sorted(printers, key=operator.itemgetter(1))
        prints = ''
        ls = []
        for each in printers:
            ls += [each[1]]
        #print ls
        for eachI in xrange(len(elist)):
            if (eachI not in ls):
                eWord = elist[eachI]
                tempGword = glist[0]
                tempMaxIndex = 0
                tempMax = lexGerDic[tempGword][eWord]
                for gindex in xrange(1,len(glist)):
                    gword = glist[gindex]
                    if (lexGerDic[gword][eWord] > tempMax):
                        tempMaxIndex = gindex
                        tempMax = lexGerDic[gword][eWord]
                if (tempMaxIndex > 0.05):
                    printers.append((tempMaxIndex, eachI))
        for each in printers:
            prints += "%d-%d " % (each[0], each[1])
        allout.write(prints + '\n')     
    return 42

print printable(tupleList)